"""Independent identities and discrete-tail edge cases for allocation tutorials."""

import numpy as np
import pytest
from numpy.testing import assert_allclose

from research.views_tailrisk import (
    black_litterman,
    empirical_expected_shortfall,
    expected_shortfall_allocation,
    minimum_variance_allocation,
    quadratic_allocation,
)


def test_black_litterman_scalar_update_and_covariance_semantics():
    result = black_litterman([[0.04]], [1], 2, [[1]], [0.12], [[0.003]], tau=0.1)
    prior_mean, prior_variance = 0.08, 0.004
    scalar_mean = (prior_mean / prior_variance + 0.12 / 0.003) / (1 / prior_variance + 1 / 0.003)
    scalar_variance = 1 / (1 / prior_variance + 1 / 0.003)
    assert_allclose(result.posterior_mean, [scalar_mean])
    assert_allclose(result.mean_covariance, [[scalar_variance]])
    assert_allclose(result.predictive_covariance, [[0.04 + scalar_variance]])


def test_black_litterman_no_views_no_innovation_and_reference_recovery():
    covariance = np.array([[0.04, 0.008], [0.008, 0.01]])
    reference = np.array([0.6, 0.4])
    prior = black_litterman(covariance, reference, 3, np.empty((0, 2)), [], np.empty((0, 0)))
    assert_allclose(prior.posterior_mean, 3 * covariance @ reference)
    assert_allclose(prior.mean_covariance, 0.05 * covariance)
    assert_allclose(prior.predictive_covariance, 1.05 * covariance)
    posterior = black_litterman(
        covariance,
        reference,
        3,
        [[1, -1]],
        [prior.implied_mean[0] - prior.implied_mean[1]],
        [[0.001]],
    )
    assert_allclose(posterior.posterior_mean, prior.implied_mean)
    assert np.trace(posterior.mean_covariance) < np.trace(prior.mean_covariance)
    assert_allclose(quadratic_allocation(prior.implied_mean, covariance, 3), reference, atol=1e-7)


def test_black_litterman_independent_precision_solution_and_tau_cancellation():
    covariance = np.array([[0.04, 0.01], [0.01, 0.0225]])
    picks, views = np.array([[1, -1], [0, 1]]), np.array([0.03, 0.02])
    tau = 0.05
    omega = np.diag(np.diag(picks @ (tau * covariance) @ picks.T))
    result = black_litterman(covariance, [0.5, 0.5], 2, picks, views, omega, tau)
    precision = np.linalg.inv(tau * covariance) + picks.T @ np.linalg.solve(omega, picks)
    rhs = np.linalg.solve(tau * covariance, result.implied_mean) + picks.T @ np.linalg.solve(
        omega, views
    )
    assert_allclose(result.posterior_mean, np.linalg.solve(precision, rhs))
    assert_allclose(result.mean_covariance, np.linalg.inv(precision))
    scaled = black_litterman(covariance, [0.5, 0.5], 2, picks, views, omega * 10, tau * 10)
    assert_allclose(scaled.posterior_mean, result.posterior_mean)
    assert_allclose(scaled.mean_covariance, 10 * result.mean_covariance)


def test_expected_shortfall_fractional_tail_ties_and_signed_losses():
    # Exactly 50% mass: all 40% at loss=5 and another 10% at loss=1.
    assert_allclose(empirical_expected_shortfall([5, 5, 1, 0], 0.5, [0.2, 0.2, 0.3, 0.3]), 4.2)
    # Top 1.5 equally weighted observations: (8 + 0.5 * 4) / 1.5.
    assert_allclose(empirical_expected_shortfall([0, 1, 4, 8], 0.625), 20 / 3)
    assert_allclose(empirical_expected_shortfall([-3, -2, -1], 0), -2)
    assert_allclose(empirical_expected_shortfall([-3, -2, -1], 0.9), -1)


def test_es_lp_known_two_asset_hedge_and_negative_objective():
    result = expected_shortfall_allocation([[-0.1, 0.1], [0.1, -0.1]], alpha=0.5)
    assert_allclose(result.weights, [0.5, 0.5])
    assert_allclose(result.expected_shortfall, 0, atol=1e-12)
    profitable = expected_shortfall_allocation([[0.01, 0.02], [0.01, 0.03]], alpha=0.5)
    assert_allclose(profitable.weights, [0, 1])
    assert_allclose(profitable.expected_shortfall, -0.02)


def test_es_lp_probability_mass_matches_exhaustive_weight_grid():
    scenarios = np.array([[-0.12, 0.01], [0.02, -0.04], [0.05, 0.03], [0.1, 0.0]])
    probabilities = np.array([0.08, 0.22, 0.4, 0.3])
    result = expected_shortfall_allocation(scenarios, 0.8, probabilities, max_weight=0.8)
    grid = np.linspace(0.2, 0.8, 12001)
    objective = np.array(
        [
            empirical_expected_shortfall(-scenarios @ np.array([w, 1 - w]), 0.8, probabilities)
            for w in grid
        ]
    )
    assert result.expected_shortfall <= objective.min() + 1e-10
    assert objective.min() - result.expected_shortfall < 1e-5
    # Reordering scenarios cannot alter the unique optimum.
    permuted = expected_shortfall_allocation(
        scenarios[::-1], 0.8, probabilities[::-1], max_weight=0.8
    )
    assert_allclose(result.weights, permuted.weights)


def test_shared_return_floor_and_analytic_minimum_variance():
    scenarios = np.array([[-0.1, 0.01], [0.14, 0.01]])
    es = expected_shortfall_allocation(scenarios, 0.5, min_return=0.015, max_weight=0.8)
    assert_allclose(es.weights, [0.5, 0.5])
    covariance = np.diag([0.04, 0.01])
    assert_allclose(minimum_variance_allocation(covariance, [0.08, 0.02]), [0.2, 0.8], atol=1e-7)
    constrained = minimum_variance_allocation(covariance, [0.08, 0.02], min_return=0.05)
    assert_allclose(constrained, [0.5, 0.5], atol=1e-7)
    with pytest.raises(ValueError, match="infeasible"):
        minimum_variance_allocation(covariance, [0.08, 0.02], min_return=0.09)


def test_invalid_probability_and_covariance_inputs_fail_explicitly():
    with pytest.raises(ValueError, match="sum to one"):
        empirical_expected_shortfall([1, 2], probabilities=[0.2, 0.2])
    with pytest.raises(ValueError, match="eigenvalues"):
        black_litterman([[1, 2], [2, 1]], [0.5, 0.5], 2, [[1, 0]], [0], [[1]])
    with pytest.raises(ValueError, match="cap"):
        expected_shortfall_allocation([[0.1, 0.2]], max_weight=0.4)
    with pytest.raises(ValueError, match="failed"):
        expected_shortfall_allocation([[0.1, 0.2]], min_return=0.3)


def test_covariance_validation_and_optimization_are_scale_invariant():
    for scale in [1e-18, 1.0, 1e18]:
        with pytest.raises(ValueError, match="eigenvalues"):
            minimum_variance_allocation(scale * np.array([[1.0, 2.0], [2.0, 1.0]]), [0, 0])
        with pytest.raises(ValueError, match="symmetric"):
            minimum_variance_allocation(scale * np.array([[1.0, 0.2], [0.1, 1.0]]), [0, 0])
        covariance = scale * np.diag([0.04, 0.01])
        assert_allclose(minimum_variance_allocation(covariance, [0, 0]), [0.2, 0.8], atol=1e-7)
        mean = scale * np.array([0.024, 0.014])
        result = quadratic_allocation(mean, covariance, 3)
        reference = quadratic_allocation(mean / scale, covariance / scale, 3)
        assert_allclose(result, reference, atol=1e-7)
