"""Shared validation and numerical kernels."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatArray = NDArray[np.float64]


def as_float_matrix(value: ArrayLike, name: str, *, allow_empty: bool = False) -> FloatArray:
    array = np.asarray(value, dtype=np.float64)
    if array.ndim != 2:
        raise ValueError(f"{name} must be a 2-D array; got shape {array.shape}")
    if not allow_empty and (array.shape[0] == 0 or array.shape[1] == 0):
        raise ValueError(f"{name} must not be empty")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite values")
    return array


def validate_model_parameters(
    n_clusters: int,
    fuzzifier: float,
    tol: float,
    max_iter: int,
) -> None:
    if isinstance(n_clusters, bool) or not isinstance(n_clusters, (int, np.integer)):
        raise TypeError("n_clusters must be an integer")
    if n_clusters < 2:
        raise ValueError("n_clusters must be at least 2")
    if not np.isfinite(fuzzifier) or fuzzifier <= 1.0:
        raise ValueError("fuzzifier must be finite and greater than 1")
    if not np.isfinite(tol) or tol <= 0.0:
        raise ValueError("tol must be finite and positive")
    if isinstance(max_iter, bool) or not isinstance(max_iter, (int, np.integer)):
        raise TypeError("max_iter must be an integer")
    if max_iter < 1:
        raise ValueError("max_iter must be at least 1")


def squared_euclidean_distances(X: FloatArray, centers: FloatArray) -> FloatArray:
    """Return pairwise squared Euclidean distances with round-off clipped to zero."""
    if X.shape[1] != centers.shape[1]:
        raise ValueError(
            "X and centers must have the same feature count; "
            f"got {X.shape[1]} and {centers.shape[1]}"
        )
    distances = (
        np.einsum("ij,ij->i", X, X)[:, None]
        + np.einsum("ij,ij->i", centers, centers)[None, :]
        - 2.0 * X @ centers.T
    )
    np.maximum(distances, 0.0, out=distances)
    if not np.all(np.isfinite(distances)):
        raise FloatingPointError("distance computation produced NaN or infinity")
    return distances


def initialize_centers(
    X: FloatArray,
    n_clusters: int,
    random_state: int | None,
    initial_centers: ArrayLike | None,
) -> FloatArray:
    if X.shape[0] < n_clusters:
        raise ValueError("n_samples must be greater than or equal to n_clusters")
    if initial_centers is not None:
        centers = as_float_matrix(initial_centers, "initial_centers")
        expected = (n_clusters, X.shape[1])
        if centers.shape != expected:
            raise ValueError(f"initial_centers must have shape {expected}; got {centers.shape}")
        return centers.copy()

    rng = np.random.default_rng(random_state)
    indices = rng.choice(X.shape[0], size=n_clusters, replace=False)
    return X[indices].copy()


def inverse_distance_membership(dist_sq: ArrayLike, fuzzifier: float) -> FloatArray:
    """FCM membership update, including the conventional exact-zero rule."""
    distances = as_float_matrix(dist_sq, "dist_sq")
    if np.any(distances < 0.0):
        raise ValueError("dist_sq must be non-negative")
    if not np.isfinite(fuzzifier) or fuzzifier <= 1.0:
        raise ValueError("fuzzifier must be finite and greater than 1")

    membership = np.zeros_like(distances)
    zero_mask = distances == 0.0
    zero_rows = np.any(zero_mask, axis=1)
    if np.any(zero_rows):
        counts = zero_mask[zero_rows].sum(axis=1, keepdims=True)
        membership[zero_rows] = zero_mask[zero_rows] / counts

    regular_rows = ~zero_rows
    if np.any(regular_rows):
        log_weights = -np.log(distances[regular_rows]) / (fuzzifier - 1.0)
        log_weights -= np.max(log_weights, axis=1, keepdims=True)
        weights = np.exp(log_weights)
        membership[regular_rows] = weights / weights.sum(axis=1, keepdims=True)

    return membership


def weighted_centers(
    X: FloatArray,
    weights: FloatArray,
    *,
    context: str,
) -> FloatArray:
    if weights.shape[0] != X.shape[0]:
        raise ValueError("weights and X must have the same number of samples")
    denominators = weights.sum(axis=0)
    empty = np.flatnonzero(denominators <= np.finfo(np.float64).tiny)
    if empty.size:
        raise FloatingPointError(
            f"{context}: clusters {empty.tolist()} have zero total weight; "
            "choose different initial centers or supervision"
        )
    centers = weights.T @ X / denominators[:, None]
    if not np.all(np.isfinite(centers)):
        raise FloatingPointError(f"{context}: center update produced NaN or infinity")
    return centers


def check_membership(membership: FloatArray, *, atol: float = 1e-10) -> None:
    if not np.all(np.isfinite(membership)):
        raise FloatingPointError("membership contains NaN or infinity")
    if np.any(membership < -atol):
        raise FloatingPointError("membership contains negative values")
    if not np.allclose(membership.sum(axis=1), 1.0, atol=atol, rtol=0.0):
        raise FloatingPointError("membership rows do not sum to one")


def require_fitted(model: object) -> None:
    if not hasattr(model, "cluster_centers_"):
        raise RuntimeError("this estimator is not fitted yet")

