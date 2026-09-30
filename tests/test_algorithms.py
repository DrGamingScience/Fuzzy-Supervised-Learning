"""Equation-level and end-to-end tests for the three estimators."""

from __future__ import annotations

import unittest

import numpy as np
from numpy.testing import assert_allclose

from fuzzy_supervised_learning import FCM, SSFCM, SSMCFCM
from fuzzy_supervised_learning.dashboard_support import (
    build_ssfcm_supervision,
    fit_dashboard_models,
    generate_demo_data,
    project_to_2d,
)
from fuzzy_supervised_learning.fcm import update_membership as fcm_membership
from fuzzy_supervised_learning.ssfcm import update_membership as ssfcm_membership
from fuzzy_supervised_learning.ssmc_fcm import (
    build_exponents,
    solve_target_mu,
    update_membership as ssmc_membership,
)


class MembershipKernelTests(unittest.TestCase):
    def test_fcm_membership_matches_closed_form_for_m_two(self) -> None:
        # For m=2, weights are inverse squared distances: [1/4, 1].
        actual = fcm_membership(np.array([[4.0, 1.0]]), 2.0)
        assert_allclose(actual, [[0.2, 0.8]], atol=1e-14)

    def test_fcm_zero_distance_is_shared_between_coincident_centers(self) -> None:
        actual = fcm_membership(np.array([[0.0, 0.0, 2.0]]), 2.0)
        assert_allclose(actual, [[0.5, 0.5, 0.0]], atol=0.0)

    def test_ssfcm_respects_supervised_lower_bound(self) -> None:
        supervision = np.array([[0.3, 0.0]])
        actual = ssfcm_membership(
            np.array([[4.0, 1.0]]), supervision, fuzzifier=2.0
        )
        assert_allclose(actual, [[0.44, 0.56]], atol=1e-14)
        self.assertTrue(np.all(actual >= supervision))
        assert_allclose(actual.sum(axis=1), 1.0)

    def test_eq19_solver_reports_small_residual(self) -> None:
        result = solve_target_mu(
            A=0.5,
            d_target=2.0,
            fuzzifier=2.0,
            supervised_fuzzifier=4.0,
        )
        self.assertLessEqual(abs(result.residual), 1e-12)
        self.assertGreater(result.value, 0.0)

    def test_ssmc_supervised_fuzzifier_increases_target_membership(self) -> None:
        Q = np.array([[4.0, 1.0]])
        almost_fcm = ssmc_membership(Q, [0], 2.0, 2.0001)
        supervised = ssmc_membership(Q, [0], 2.0, 4.0)
        strongly_supervised = ssmc_membership(Q, [0], 2.0, 8.0)
        self.assertLess(almost_fcm[0, 0], supervised[0, 0])
        self.assertLess(supervised[0, 0], strongly_supervised[0, 0])
        assert_allclose(strongly_supervised.sum(axis=1), 1.0)

        # Eq. (16): all Lagrange-stationarity terms are equal in the row.
        target_term = 4.0 * supervised[0, 0] ** 3.0 * Q[0, 0]
        other_term = 2.0 * supervised[0, 1] * Q[0, 1]
        assert_allclose(target_term, other_term, atol=1e-11)

    def test_exponent_matrix_changes_only_supervised_pairs(self) -> None:
        actual = build_exponents([-1, 1, 0], 3, 2, 2.0, 4.0)
        assert_allclose(actual, [[2.0, 2.0], [2.0, 4.0], [4.0, 2.0]])


class EstimatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.X = np.array(
            [
                [0.0, 0.0],
                [0.1, 0.0],
                [0.0, 0.1],
                [10.0, 10.0],
                [10.1, 10.0],
                [10.0, 10.1],
            ]
        )
        self.initial_centers = np.array([[0.0, 0.0], [10.0, 10.0]])

    def test_all_three_estimators_fit_and_preserve_simplex(self) -> None:
        models = [
            FCM(2, random_state=7),
            SSFCM(2, random_state=7),
            SSMCFCM(2, random_state=7),
        ]
        for model in models:
            if isinstance(model, SSFCM):
                model.fit(
                    self.X,
                    np.zeros((len(self.X), 2)),
                    initial_centers=self.initial_centers,
                )
            elif isinstance(model, SSMCFCM):
                model.fit(
                    self.X,
                    np.full(len(self.X), -1),
                    initial_centers=self.initial_centers,
                )
            else:
                model.fit(self.X, initial_centers=self.initial_centers)
            self.assertTrue(model.converged_)
            self.assertEqual(model.cluster_centers_.shape, (2, 2))
            self.assertEqual(model.membership_.shape, (6, 2))
            assert_allclose(model.membership_.sum(axis=1), 1.0, atol=1e-12)
            self.assertTrue(np.all(np.isfinite(model.membership_)))

    def test_unsupervised_paths_of_all_algorithms_match(self) -> None:
        fcm = FCM(2).fit(self.X, initial_centers=self.initial_centers)
        ssfcm = SSFCM(2).fit(
            self.X,
            np.zeros((len(self.X), 2)),
            initial_centers=self.initial_centers,
        )
        ssmc = SSMCFCM(2).fit(
            self.X,
            np.full(len(self.X), -1),
            initial_centers=self.initial_centers,
        )
        assert_allclose(fcm.cluster_centers_, ssfcm.cluster_centers_, atol=1e-12)
        assert_allclose(fcm.cluster_centers_, ssmc.cluster_centers_, atol=1e-12)
        assert_allclose(fcm.membership_, ssfcm.membership_, atol=1e-12)
        assert_allclose(fcm.membership_, ssmc.membership_, atol=1e-12)

    def test_random_state_is_deterministic(self) -> None:
        first = SSMCFCM(2, random_state=11).fit(self.X)
        second = SSMCFCM(2, random_state=11).fit(self.X)
        assert_allclose(first.cluster_centers_, second.cluster_centers_)
        assert_allclose(first.objective_history_, second.objective_history_)

    def test_ssmc_supervised_fit_records_solver_diagnostics(self) -> None:
        targets = np.array([-1, 0, -1, -1, 1, -1])
        model = SSMCFCM(2, random_state=3).fit(
            self.X,
            targets,
            initial_centers=self.initial_centers,
        )
        self.assertTrue(model.converged_)
        self.assertEqual(len(model.solver_diagnostics_history_), model.n_iter_)
        for iteration_diagnostics in model.solver_diagnostics_history_:
            self.assertEqual(len(iteration_diagnostics), 2)
            for diagnostic in iteration_diagnostics:
                self.assertLessEqual(abs(diagnostic.solver.residual), model.solver_tol)

    def test_invalid_supervision_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "row sums exceed one"):
            SSFCM(2).fit(self.X, np.full((len(self.X), 2), 0.6))
        with self.assertRaisesRegex(ValueError, "valid cluster index"):
            SSMCFCM(2).fit(self.X, [2, -1, -1, -1, -1, -1])


class DashboardSupportTests(unittest.TestCase):
    def test_demo_data_is_deterministic_and_balanced(self) -> None:
        first_X, first_y = generate_demo_data(31, 3, 0.5, 9)
        second_X, second_y = generate_demo_data(31, 3, 0.5, 9)
        assert_allclose(first_X, second_X)
        assert_allclose(first_y, second_y)
        self.assertEqual(first_X.shape, (31, 2))
        self.assertLessEqual(np.bincount(first_y).max() - np.bincount(first_y).min(), 1)

    def test_dashboard_can_fit_and_compare_all_algorithms(self) -> None:
        X, truth = generate_demo_data(45, 3, 0.35, 4)
        targets = np.full(len(X), -1)
        for cluster in range(3):
            targets[np.flatnonzero(truth == cluster)[0]] = cluster
        models = fit_dashboard_models(
            "So sánh cả ba",
            X,
            targets,
            n_clusters=3,
            fuzzifier=2.0,
            supervised_fuzzifier=4.0,
            supervision_strength=0.6,
            tol=1e-5,
            max_iter=300,
            random_state=4,
        )
        self.assertEqual(tuple(models), ("FCM", "sSFCM", "sSMC-FCM"))
        for model in models.values():
            self.assertEqual(model.membership_.shape, (45, 3))
            assert_allclose(model.membership_.sum(axis=1), 1.0, atol=1e-12)

    def test_dashboard_supervision_and_projection(self) -> None:
        supervision = build_ssfcm_supervision([0, -1, 1], 3, 2, 0.7)
        assert_allclose(supervision, [[0.7, 0.0], [0.0, 0.0], [0.0, 0.7]])
        X = np.array([[1.0, 2.0, 3.0], [2.0, 1.0, 4.0], [3.0, 0.0, 2.0]])
        centers = X[:2]
        projected, projected_centers, axes = project_to_2d(X, centers)
        self.assertEqual(projected.shape, (3, 2))
        self.assertEqual(projected_centers.shape, (2, 2))
        self.assertEqual(axes, ("PC1", "PC2"))


if __name__ == "__main__":
    unittest.main()
