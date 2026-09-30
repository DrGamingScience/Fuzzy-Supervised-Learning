"""Semi-supervised FCM with multiple fuzzification coefficients.

This module follows Khang, Tran, and Fowler (2021), Eqs. (7)-(20).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from ._common import (
    FloatArray,
    as_float_matrix,
    check_membership,
    initialize_centers,
    inverse_distance_membership,
    require_fitted,
    squared_euclidean_distances,
    validate_model_parameters,
    weighted_centers,
)


@dataclass(frozen=True)
class SolverResult:
    """Diagnostic result for the scalar root in Eq. (19)."""

    value: float
    residual: float
    n_iter: int


@dataclass(frozen=True)
class SupervisedRowDiagnostic:
    """Diagnostic information for one supervised membership row."""

    sample_index: int
    target_cluster: int
    solver: SolverResult
    used_zero_distance_rule: bool = False


def validate_supervised_targets(
    supervised_targets: ArrayLike | None,
    n_samples: int,
    n_clusters: int,
) -> np.ndarray:
    """Validate the one-target-per-sample representation; -1 means unlabeled."""
    if supervised_targets is None:
        return np.full(n_samples, -1, dtype=np.int64)
    raw = np.asarray(supervised_targets)
    if raw.ndim != 1 or raw.shape[0] != n_samples:
        raise ValueError(
            f"supervised_targets must have shape ({n_samples},); got {raw.shape}"
        )
    if np.issubdtype(raw.dtype, np.bool_):
        raise TypeError("supervised_targets must contain integer cluster indices")
    try:
        numeric = raw.astype(np.float64)
    except (TypeError, ValueError) as error:
        raise TypeError(
            "supervised_targets must contain integer cluster indices"
        ) from error
    if not np.all(np.isfinite(numeric)) or not np.all(numeric == np.floor(numeric)):
        raise ValueError("supervised_targets must contain finite integers")
    targets = numeric.astype(np.int64)
    invalid = (targets < -1) | (targets >= n_clusters)
    if np.any(invalid):
        bad = np.flatnonzero(invalid)
        raise ValueError(
            "supervised_targets values must be -1 or a valid cluster index; "
            f"invalid rows: {bad.tolist()}"
        )
    return targets


def build_exponents(
    supervised_targets: ArrayLike | None,
    n_samples: int,
    n_clusters: int,
    fuzzifier: float,
    supervised_fuzzifier: float,
) -> FloatArray:
    """Build the pair-specific exponent matrix from Eq. (8)."""
    if not np.isfinite(fuzzifier) or fuzzifier <= 1.0:
        raise ValueError("fuzzifier must be finite and greater than 1")
    if not np.isfinite(supervised_fuzzifier) or supervised_fuzzifier <= fuzzifier:
        raise ValueError("supervised_fuzzifier must be finite and greater than fuzzifier")
    targets = validate_supervised_targets(
        supervised_targets, n_samples, n_clusters
    )
    exponents = np.full((n_samples, n_clusters), fuzzifier, dtype=np.float64)
    rows = np.flatnonzero(targets >= 0)
    exponents[rows, targets[rows]] = supervised_fuzzifier
    return exponents


def solve_target_mu(
    A: float,
    d_target: float,
    fuzzifier: float,
    supervised_fuzzifier: float,
    *,
    tol: float = 1e-12,
    max_iter: int = 200,
) -> SolverResult:
    """Solve sSMC-FCM Eq. (19) by bracket expansion and bisection."""
    values = (A, d_target, fuzzifier, supervised_fuzzifier, tol)
    if not all(np.isfinite(value) for value in values):
        raise ValueError("Eq. (19) parameters must be finite")
    if A < 0.0:
        raise ValueError("A must be non-negative")
    if d_target <= 0.0:
        raise ValueError("d_target must be positive")
    if fuzzifier <= 1.0:
        raise ValueError("fuzzifier must be greater than 1")
    if supervised_fuzzifier <= fuzzifier:
        raise ValueError("supervised_fuzzifier must be greater than fuzzifier")
    if tol <= 0.0:
        raise ValueError("tol must be positive")
    if isinstance(max_iter, bool) or not isinstance(max_iter, (int, np.integer)) or max_iter < 1:
        raise ValueError("max_iter must be a positive integer")

    b = (supervised_fuzzifier - fuzzifier) / (supervised_fuzzifier - 1.0)
    log_rhs = -(
        np.log(supervised_fuzzifier) + 2.0 * np.log(d_target)
    ) / (supervised_fuzzifier - 1.0)
    rhs = float(np.exp(log_rhs))

    def log_left(mu: float) -> float:
        return float(np.log(mu) - b * np.log(mu + A))

    low = 0.0
    high = 1.0
    expansion_count = 0
    while log_left(high) < log_rhs:
        high *= 2.0
        expansion_count += 1
        if expansion_count > 1024 or not np.isfinite(high):
            raise RuntimeError("could not bracket the positive root of Eq. (19)")

    residual = float("inf")
    value = high
    for iteration in range(1, max_iter + 1):
        value = (low + high) / 2.0
        log_value = log_left(value)
        left = float(np.exp(log_value))
        residual = left - rhs
        if abs(residual) <= tol * max(1.0, rhs):
            return SolverResult(value=value, residual=residual, n_iter=iteration)
        if log_value < log_rhs:
            low = value
        else:
            high = value

    raise RuntimeError(
        "Eq. (19) solver did not reach tolerance: "
        f"residual={residual:.3e}, tol={tol:.3e}, iterations={max_iter}"
    )


def update_membership(
    dist_sq: ArrayLike,
    supervised_targets: ArrayLike | None,
    fuzzifier: float,
    supervised_fuzzifier: float,
    *,
    solver_tol: float = 1e-12,
    solver_max_iter: int = 200,
    return_diagnostics: bool = False,
) -> FloatArray | tuple[FloatArray, list[SupervisedRowDiagnostic]]:
    """Update mixed unlabeled/labeled memberships with Eqs. (15), (17)-(20)."""
    Q = as_float_matrix(dist_sq, "dist_sq")
    if np.any(Q < 0.0):
        raise ValueError("dist_sq must be non-negative")
    if not np.isfinite(fuzzifier) or fuzzifier <= 1.0:
        raise ValueError("fuzzifier must be finite and greater than 1")
    if not np.isfinite(supervised_fuzzifier) or supervised_fuzzifier <= fuzzifier:
        raise ValueError("supervised_fuzzifier must be finite and greater than fuzzifier")

    n_samples, n_clusters = Q.shape
    targets = validate_supervised_targets(
        supervised_targets, n_samples, n_clusters
    )
    membership = np.zeros_like(Q)
    diagnostics: list[SupervisedRowDiagnostic] = []

    unlabeled = targets < 0
    if np.any(unlabeled):
        membership[unlabeled] = inverse_distance_membership(
            Q[unlabeled], fuzzifier
        )

    for row in np.flatnonzero(~unlabeled):
        target = int(targets[row])
        zero_clusters = np.flatnonzero(Q[row] == 0.0)
        if zero_clusters.size:
            # Eqs. (17)-(19) are undefined for d_min=0.  The objective is
            # minimized on zero-distance clusters.  Prefer the supervised
            # target when it is one of them; otherwise split deterministically.
            if target in zero_clusters:
                membership[row, target] = 1.0
            else:
                membership[row, zero_clusters] = 1.0 / zero_clusters.size
            diagnostics.append(
                SupervisedRowDiagnostic(
                    sample_index=int(row),
                    target_cluster=target,
                    solver=SolverResult(value=float("nan"), residual=0.0, n_iter=0),
                    used_zero_distance_rule=True,
                )
            )
            continue

        # Eq. (17), calculated through logs to avoid overflowing Q / min(Q).
        log_normalized_q = np.log(Q[row]) - np.min(np.log(Q[row]))
        mu = np.zeros(n_clusters, dtype=np.float64)
        non_target = np.arange(n_clusters) != target

        # Eq. (18): d_ij^2 equals the normalized squared distance.
        log_mu = -(
            np.log(fuzzifier) + log_normalized_q[non_target]
        ) / (fuzzifier - 1.0)
        mu[non_target] = np.exp(log_mu)
        A = float(mu[non_target].sum())
        d_target = float(np.exp(0.5 * log_normalized_q[target]))
        solver = solve_target_mu(
            A,
            d_target,
            fuzzifier,
            supervised_fuzzifier,
            tol=solver_tol,
            max_iter=solver_max_iter,
        )
        mu[target] = solver.value
        total = float(mu.sum())
        if not np.isfinite(total) or total <= 0.0:
            raise FloatingPointError(f"Eq. (20) failed at sample {row}")
        membership[row] = mu / total
        diagnostics.append(
            SupervisedRowDiagnostic(
                sample_index=int(row),
                target_cluster=target,
                solver=solver,
            )
        )

    check_membership(membership)
    if return_diagnostics:
        return membership, diagnostics
    return membership


def update_centers(
    X: ArrayLike,
    membership: ArrayLike,
    exponents: ArrayLike,
) -> FloatArray:
    """Update centers using Eq. (10)."""
    data = as_float_matrix(X, "X")
    U = as_float_matrix(membership, "membership")
    M = as_float_matrix(exponents, "exponents")
    if U.shape != M.shape:
        raise ValueError("membership and exponents must have the same shape")
    if U.shape[0] != data.shape[0]:
        raise ValueError("membership and X must have the same number of samples")
    if np.any(M <= 1.0):
        raise ValueError("all exponents must be greater than 1")
    check_membership(U)
    return weighted_centers(data, U**M, context="sSMC-FCM")


def objective(
    membership: ArrayLike,
    dist_sq: ArrayLike,
    exponents: ArrayLike,
) -> float:
    """Evaluate Eq. (7)."""
    U = as_float_matrix(membership, "membership")
    Q = as_float_matrix(dist_sq, "dist_sq")
    M = as_float_matrix(exponents, "exponents")
    if U.shape != Q.shape or U.shape != M.shape:
        raise ValueError("membership, dist_sq, and exponents must have the same shape")
    value = float(np.sum((U**M) * Q))
    if not np.isfinite(value) or value < 0.0:
        raise FloatingPointError("sSMC-FCM objective is not a finite non-negative number")
    return value


class SSMCFCM:
    """sSMC-FCM estimator with one optional supervised target per sample."""

    def __init__(
        self,
        n_clusters: int,
        *,
        fuzzifier: float = 2.0,
        supervised_fuzzifier: float = 4.0,
        tol: float = 1e-5,
        max_iter: int = 300,
        solver_tol: float = 1e-12,
        solver_max_iter: int = 200,
        random_state: int | None = None,
    ) -> None:
        validate_model_parameters(n_clusters, fuzzifier, tol, max_iter)
        if not np.isfinite(supervised_fuzzifier) or supervised_fuzzifier <= fuzzifier:
            raise ValueError("supervised_fuzzifier must be finite and greater than fuzzifier")
        if not np.isfinite(solver_tol) or solver_tol <= 0.0:
            raise ValueError("solver_tol must be finite and positive")
        if (
            isinstance(solver_max_iter, bool)
            or not isinstance(solver_max_iter, (int, np.integer))
            or solver_max_iter < 1
        ):
            raise ValueError("solver_max_iter must be a positive integer")
        self.n_clusters = int(n_clusters)
        self.fuzzifier = float(fuzzifier)
        self.supervised_fuzzifier = float(supervised_fuzzifier)
        self.tol = float(tol)
        self.max_iter = int(max_iter)
        self.solver_tol = float(solver_tol)
        self.solver_max_iter = int(solver_max_iter)
        self.random_state = random_state

    def fit(
        self,
        X: ArrayLike,
        supervised_targets: ArrayLike | None = None,
        *,
        initial_centers: ArrayLike | None = None,
    ) -> "SSMCFCM":
        data = as_float_matrix(X, "X")
        targets = validate_supervised_targets(
            supervised_targets, data.shape[0], self.n_clusters
        )
        exponents = build_exponents(
            targets,
            data.shape[0],
            self.n_clusters,
            self.fuzzifier,
            self.supervised_fuzzifier,
        )
        centers = initialize_centers(
            data, self.n_clusters, self.random_state, initial_centers
        )
        self.objective_history_: list[float] = []
        self.center_shift_history_: list[float] = []
        self.solver_diagnostics_history_: list[list[SupervisedRowDiagnostic]] = []
        self.converged_ = False

        for iteration in range(1, self.max_iter + 1):
            dist_sq = squared_euclidean_distances(data, centers)
            membership, diagnostics = update_membership(
                dist_sq,
                targets,
                self.fuzzifier,
                self.supervised_fuzzifier,
                solver_tol=self.solver_tol,
                solver_max_iter=self.solver_max_iter,
                return_diagnostics=True,
            )
            new_centers = update_centers(data, membership, exponents)
            shift = float(np.linalg.norm(new_centers - centers))
            new_dist_sq = squared_euclidean_distances(data, new_centers)
            self.objective_history_.append(
                objective(membership, new_dist_sq, exponents)
            )
            self.center_shift_history_.append(shift)
            self.solver_diagnostics_history_.append(diagnostics)
            centers = new_centers
            if shift < self.tol:
                self.converged_ = True
                break

        self.cluster_centers_ = centers
        self.membership_ = membership
        self.labels_ = np.argmax(membership, axis=1)
        self.supervised_targets_ = targets
        self.exponents_ = exponents
        self.n_iter_ = iteration
        self.objective_ = self.objective_history_[-1]
        self.n_features_in_ = data.shape[1]
        return self

    def predict_membership(self, X: ArrayLike) -> FloatArray:
        """Predict new samples without supervision, using Eq. (15)."""
        require_fitted(self)
        data = as_float_matrix(X, "X")
        Q = squared_euclidean_distances(data, self.cluster_centers_)
        return inverse_distance_membership(Q, self.fuzzifier)

    def predict(self, X: ArrayLike) -> np.ndarray:
        return np.argmax(self.predict_membership(X), axis=1)

    def fit_predict(
        self,
        X: ArrayLike,
        supervised_targets: ArrayLike | None = None,
        *,
        initial_centers: ArrayLike | None = None,
    ) -> np.ndarray:
        return self.fit(
            X,
            supervised_targets=supervised_targets,
            initial_centers=initial_centers,
        ).labels_

