"""Pure-Python helpers used by the Streamlit dashboard."""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np
from numpy.typing import ArrayLike, NDArray

from ._common import FloatArray, as_float_matrix
from .fcm import FCM
from .ssfcm import SSFCM
from .ssmc_fcm import SSMCFCM, validate_supervised_targets

IntArray = NDArray[np.int64]


def generate_demo_data(
    n_samples: int,
    n_clusters: int,
    cluster_std: float,
    random_state: int,
) -> tuple[FloatArray, IntArray]:
    """Generate deterministic two-dimensional Gaussian clusters without sklearn."""
    if n_samples < n_clusters:
        raise ValueError("n_samples must be at least n_clusters")
    if n_clusters < 2:
        raise ValueError("n_clusters must be at least 2")
    if not np.isfinite(cluster_std) or cluster_std <= 0.0:
        raise ValueError("cluster_std must be finite and positive")

    rng = np.random.default_rng(random_state)
    angles = np.linspace(0.0, 2.0 * np.pi, n_clusters, endpoint=False)
    centers = np.column_stack((np.cos(angles), np.sin(angles))) * 5.0
    counts = np.full(n_clusters, n_samples // n_clusters, dtype=np.int64)
    counts[: n_samples % n_clusters] += 1

    chunks = [
        rng.normal(loc=centers[index], scale=cluster_std, size=(count, 2))
        for index, count in enumerate(counts)
    ]
    X = np.vstack(chunks)
    labels = np.repeat(np.arange(n_clusters, dtype=np.int64), counts)
    order = rng.permutation(n_samples)
    return X[order], labels[order]


def build_ssfcm_supervision(
    supervised_targets: ArrayLike | None,
    n_samples: int,
    n_clusters: int,
    strength: float,
) -> FloatArray:
    """Convert target indices to the lower-bound matrix required by sSFCM."""
    if not np.isfinite(strength) or strength < 0.0 or strength > 1.0:
        raise ValueError("supervision strength must lie in [0, 1]")
    targets = validate_supervised_targets(
        supervised_targets, n_samples, n_clusters
    )
    supervision = np.zeros((n_samples, n_clusters), dtype=np.float64)
    rows = np.flatnonzero(targets >= 0)
    supervision[rows, targets[rows]] = strength
    return supervision


def fit_dashboard_models(
    algorithm: str,
    X: ArrayLike,
    supervised_targets: ArrayLike | None,
    *,
    n_clusters: int,
    fuzzifier: float,
    supervised_fuzzifier: float,
    supervision_strength: float,
    tol: float,
    max_iter: int,
    random_state: int,
) -> Mapping[str, FCM | SSFCM | SSMCFCM]:
    """Fit one dashboard selection or all three algorithms with aligned settings."""
    data = as_float_matrix(X, "X")
    targets = validate_supervised_targets(
        supervised_targets, data.shape[0], n_clusters
    )
    common = dict(
        n_clusters=n_clusters,
        fuzzifier=fuzzifier,
        tol=tol,
        max_iter=max_iter,
        random_state=random_state,
    )
    available = {"FCM", "sSFCM", "sSMC-FCM", "So sánh cả ba"}
    if algorithm not in available:
        raise ValueError(f"unknown dashboard algorithm: {algorithm}")

    requested = (
        ("FCM", "sSFCM", "sSMC-FCM")
        if algorithm == "So sánh cả ba"
        else (algorithm,)
    )
    models: dict[str, FCM | SSFCM | SSMCFCM] = {}
    for name in requested:
        if name == "FCM":
            models[name] = FCM(**common).fit(data)
        elif name == "sSFCM":
            supervision = build_ssfcm_supervision(
                targets,
                data.shape[0],
                n_clusters,
                supervision_strength,
            )
            models[name] = SSFCM(**common).fit(data, supervision)
        else:
            models[name] = SSMCFCM(
                **common,
                supervised_fuzzifier=supervised_fuzzifier,
            ).fit(data, targets)
    return models


def project_to_2d(
    X: ArrayLike,
    centers: ArrayLike,
) -> tuple[FloatArray, FloatArray, tuple[str, str]]:
    """Project data and centers together for a consistent dashboard plot."""
    data = as_float_matrix(X, "X")
    cluster_centers = as_float_matrix(centers, "centers")
    if data.shape[1] != cluster_centers.shape[1]:
        raise ValueError("X and centers must have the same feature count")
    if data.shape[1] == 1:
        return (
            np.column_stack((data[:, 0], np.zeros(data.shape[0]))),
            np.column_stack(
                (cluster_centers[:, 0], np.zeros(cluster_centers.shape[0]))
            ),
            ("Feature 1", "Baseline"),
        )
    if data.shape[1] == 2:
        return data.copy(), cluster_centers.copy(), ("Feature 1", "Feature 2")

    mean = data.mean(axis=0)
    _, _, right_vectors = np.linalg.svd(data - mean, full_matrices=False)
    components = right_vectors[:2].T
    return (
        (data - mean) @ components,
        (cluster_centers - mean) @ components,
        ("PC1", "PC2"),
    )


def maximum_solver_residual(model: object) -> float | None:
    """Return the largest Eq. (19) residual recorded by an sSMC-FCM fit."""
    history = getattr(model, "solver_diagnostics_history_", None)
    if history is None:
        return None
    values = [
        abs(diagnostic.solver.residual)
        for iteration in history
        for diagnostic in iteration
    ]
    return max(values, default=0.0)

