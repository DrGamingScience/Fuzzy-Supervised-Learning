"""Semi-Supervised Fuzzy C-Means (sSFCM), Endo et al. (2009)."""

from __future__ import annotations

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
    weighted_centers,
)


def validate_supervision(
    supervision: ArrayLike | None,
    n_samples: int,
    n_clusters: int,
) -> FloatArray:
    if supervision is None:
        return np.zeros((n_samples, n_clusters), dtype=np.float64)
    U_bar = as_float_matrix(supervision, "supervision")
    expected = (n_samples, n_clusters)
    if U_bar.shape != expected:
        raise ValueError(f"supervision must have shape {expected}; got {U_bar.shape}")
    if np.any(U_bar < 0.0) or np.any(U_bar > 1.0):
        raise ValueError("supervision values must lie in [0, 1]")
    row_sums = U_bar.sum(axis=1)
    if np.any(row_sums > 1.0 + 1e-12):
        bad = np.flatnonzero(row_sums > 1.0 + 1e-12)
        raise ValueError(f"supervision row sums exceed one at rows {bad.tolist()}")
    return U_bar.copy()


def update_membership(
    dist_sq: ArrayLike,
    supervision: ArrayLike,
    fuzzifier: float,
) -> FloatArray:
    """Apply sSFCM Eq. (6), or Eq. (8) when ``fuzzifier == 1``."""
    Q = as_float_matrix(dist_sq, "dist_sq")
    U_bar = as_float_matrix(supervision, "supervision")
    if Q.shape != U_bar.shape:
        raise ValueError("dist_sq and supervision must have the same shape")
    if np.any(Q < 0.0):
        raise ValueError("dist_sq must be non-negative")
    U_bar = validate_supervision(U_bar, Q.shape[0], Q.shape[1])
    remaining = 1.0 - U_bar.sum(axis=1)

    if fuzzifier == 1.0:
        allocation = np.zeros_like(Q)
        allocation[np.arange(Q.shape[0]), np.argmin(Q, axis=1)] = 1.0
    elif np.isfinite(fuzzifier) and fuzzifier > 1.0:
        allocation = inverse_distance_membership(Q, fuzzifier)
    else:
        raise ValueError("fuzzifier must be finite and at least 1 for sSFCM")

    membership = U_bar + remaining[:, None] * allocation
    check_membership(membership)
    return membership


def update_centers(
    X: ArrayLike,
    membership: ArrayLike,
    supervision: ArrayLike,
    fuzzifier: float,
) -> FloatArray:
    data = as_float_matrix(X, "X")
    U = as_float_matrix(membership, "membership")
    U_bar = validate_supervision(supervision, data.shape[0], U.shape[1])
    if U.shape != U_bar.shape:
        raise ValueError("membership and supervision must have the same shape")
    differences = np.abs(U - U_bar)
    return weighted_centers(data, differences**fuzzifier, context="sSFCM")


def objective(
    membership: ArrayLike,
    supervision: ArrayLike,
    dist_sq: ArrayLike,
    fuzzifier: float,
) -> float:
    U = as_float_matrix(membership, "membership")
    U_bar = as_float_matrix(supervision, "supervision")
    Q = as_float_matrix(dist_sq, "dist_sq")
    if U.shape != U_bar.shape or U.shape != Q.shape:
        raise ValueError("membership, supervision, and dist_sq must have the same shape")
    value = float(np.sum((np.abs(U - U_bar) ** fuzzifier) * Q))
    if not np.isfinite(value) or value < 0.0:
        raise FloatingPointError("sSFCM objective is not a finite non-negative number")
    return value


class SSFCM:
    """sSFCM estimator using a supervised lower-bound membership matrix."""

    def __init__(
        self,
        n_clusters: int,
        *,
        fuzzifier: float = 2.0,
        tol: float = 1e-5,
        max_iter: int = 300,
        random_state: int | None = None,
    ) -> None:
        if isinstance(n_clusters, bool) or not isinstance(n_clusters, (int, np.integer)):
            raise TypeError("n_clusters must be an integer")
        if n_clusters < 2:
            raise ValueError("n_clusters must be at least 2")
        if not np.isfinite(fuzzifier) or fuzzifier < 1.0:
            raise ValueError("fuzzifier must be finite and at least 1")
        if not np.isfinite(tol) or tol <= 0.0:
            raise ValueError("tol must be finite and positive")
        if isinstance(max_iter, bool) or not isinstance(max_iter, (int, np.integer)) or max_iter < 1:
            raise ValueError("max_iter must be a positive integer")
        self.n_clusters = int(n_clusters)
        self.fuzzifier = float(fuzzifier)
        self.tol = float(tol)
        self.max_iter = int(max_iter)
        self.random_state = random_state

    def fit(
        self,
        X: ArrayLike,
        supervision: ArrayLike | None = None,
        *,
        initial_centers: ArrayLike | None = None,
    ) -> "SSFCM":
        data = as_float_matrix(X, "X")
        U_bar = validate_supervision(
            supervision, data.shape[0], self.n_clusters
        )
        centers = initialize_centers(
            data, self.n_clusters, self.random_state, initial_centers
        )
        self.objective_history_: list[float] = []
        self.center_shift_history_: list[float] = []
        self.converged_ = False

        for iteration in range(1, self.max_iter + 1):
            dist_sq = squared_euclidean_distances(data, centers)
            membership = update_membership(dist_sq, U_bar, self.fuzzifier)
            new_centers = update_centers(data, membership, U_bar, self.fuzzifier)
            shift = float(np.linalg.norm(new_centers - centers))
            new_dist_sq = squared_euclidean_distances(data, new_centers)
            self.objective_history_.append(
                objective(membership, U_bar, new_dist_sq, self.fuzzifier)
            )
            self.center_shift_history_.append(shift)
            centers = new_centers
            if shift < self.tol:
                self.converged_ = True
                break

        self.cluster_centers_ = centers
        self.membership_ = membership
        self.supervision_ = U_bar
        self.labels_ = np.argmax(membership, axis=1)
        self.n_iter_ = iteration
        self.objective_ = self.objective_history_[-1]
        self.n_features_in_ = data.shape[1]
        return self

    def predict_membership(self, X: ArrayLike) -> FloatArray:
        """Predict new, unsupervised samples (Eq. (6) with U_bar = 0)."""
        require_fitted(self)
        data = as_float_matrix(X, "X")
        Q = squared_euclidean_distances(data, self.cluster_centers_)
        zeros = np.zeros((data.shape[0], self.n_clusters), dtype=np.float64)
        return update_membership(Q, zeros, self.fuzzifier)

    def predict(self, X: ArrayLike) -> np.ndarray:
        return np.argmax(self.predict_membership(X), axis=1)

    def fit_predict(
        self,
        X: ArrayLike,
        supervision: ArrayLike | None = None,
        *,
        initial_centers: ArrayLike | None = None,
    ) -> np.ndarray:
        return self.fit(
            X, supervision=supervision, initial_centers=initial_centers
        ).labels_

