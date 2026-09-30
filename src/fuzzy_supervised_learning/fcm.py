"""Fuzzy C-Means (FCM)."""

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
    validate_model_parameters,
    weighted_centers,
)


def update_membership(dist_sq: ArrayLike, fuzzifier: float) -> FloatArray:
    """Update FCM memberships from squared distances."""
    return inverse_distance_membership(dist_sq, fuzzifier)


def update_centers(X: ArrayLike, membership: ArrayLike, fuzzifier: float) -> FloatArray:
    data = as_float_matrix(X, "X")
    U = as_float_matrix(membership, "membership")
    if U.shape[0] != data.shape[0]:
        raise ValueError("membership and X must have the same number of samples")
    check_membership(U)
    return weighted_centers(data, U**fuzzifier, context="FCM")


def objective(membership: ArrayLike, dist_sq: ArrayLike, fuzzifier: float) -> float:
    U = as_float_matrix(membership, "membership")
    Q = as_float_matrix(dist_sq, "dist_sq")
    if U.shape != Q.shape:
        raise ValueError("membership and dist_sq must have the same shape")
    value = float(np.sum((U**fuzzifier) * Q))
    if not np.isfinite(value) or value < 0.0:
        raise FloatingPointError("FCM objective is not a finite non-negative number")
    return value


class FCM:
    """Fuzzy C-Means estimator using alternating optimization."""

    def __init__(
        self,
        n_clusters: int,
        *,
        fuzzifier: float = 2.0,
        tol: float = 1e-5,
        max_iter: int = 300,
        random_state: int | None = None,
    ) -> None:
        validate_model_parameters(n_clusters, fuzzifier, tol, max_iter)
        self.n_clusters = int(n_clusters)
        self.fuzzifier = float(fuzzifier)
        self.tol = float(tol)
        self.max_iter = int(max_iter)
        self.random_state = random_state

    def fit(self, X: ArrayLike, *, initial_centers: ArrayLike | None = None) -> "FCM":
        data = as_float_matrix(X, "X")
        centers = initialize_centers(
            data, self.n_clusters, self.random_state, initial_centers
        )
        self.objective_history_: list[float] = []
        self.center_shift_history_: list[float] = []
        self.converged_ = False

        for iteration in range(1, self.max_iter + 1):
            dist_sq = squared_euclidean_distances(data, centers)
            membership = update_membership(dist_sq, self.fuzzifier)
            new_centers = update_centers(data, membership, self.fuzzifier)
            shift = float(np.linalg.norm(new_centers - centers))
            new_dist_sq = squared_euclidean_distances(data, new_centers)
            self.objective_history_.append(
                objective(membership, new_dist_sq, self.fuzzifier)
            )
            self.center_shift_history_.append(shift)
            centers = new_centers
            if shift < self.tol:
                self.converged_ = True
                break

        self.cluster_centers_ = centers
        self.membership_ = membership
        self.labels_ = np.argmax(membership, axis=1)
        self.n_iter_ = iteration
        self.objective_ = self.objective_history_[-1]
        self.n_features_in_ = data.shape[1]
        return self

    def predict_membership(self, X: ArrayLike) -> FloatArray:
        require_fitted(self)
        data = as_float_matrix(X, "X")
        dist_sq = squared_euclidean_distances(data, self.cluster_centers_)
        return update_membership(dist_sq, self.fuzzifier)

    def predict(self, X: ArrayLike) -> np.ndarray:
        return np.argmax(self.predict_membership(X), axis=1)

    def fit_predict(self, X: ArrayLike, *, initial_centers: ArrayLike | None = None) -> np.ndarray:
        return self.fit(X, initial_centers=initial_centers).labels_

