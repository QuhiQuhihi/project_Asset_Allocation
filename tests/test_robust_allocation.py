import numpy as np
import pytest

from research.robust_allocation import allocation_candidates, minimum_worst_variance


def test_diagonal_reference_and_binding_cap():
    cov = np.diag([1.0, 4.0, 9.0])
    exact = (1 / np.diag(cov)) / (1 / np.diag(cov)).sum()
    np.testing.assert_allclose(minimum_worst_variance([cov]), exact, atol=1e-6)
    # Once the first asset binds at 50%, the remainder has inverse-variance weights.
    np.testing.assert_allclose(minimum_worst_variance([cov], 0.5), [0.5, 9 / 26, 4 / 26], atol=1e-6)


def test_two_scenario_minimax_matches_exhaustive_grid():
    covs = np.array([[[1, 0], [0, 4]], [[9, 0], [0, 1]]], dtype=float)
    w = minimum_worst_variance(covs)
    grid = np.linspace(0, 1, 100001)
    losses = np.maximum(grid**2 + 4 * (1 - grid) ** 2, 9 * grid**2 + (1 - grid) ** 2)
    np.testing.assert_allclose(w[0], grid[losses.argmin()], atol=1e-5)
    np.testing.assert_allclose(minimum_worst_variance(covs * 1e-4), w, atol=1e-7)


def test_invalid_uncertainty_set_is_rejected():
    for covs, cap in [
        ([np.eye(3)], 0.2),
        ([np.array([[1, 2], [2, 1]])], 1),
        ([np.zeros((3, 3))], 1),
    ]:
        with pytest.raises(ValueError):
            minimum_worst_variance(covs, cap)
    for scale in [1e-14, 1.0, 1e14]:
        for invalid in [np.array([[1, 2], [2, 1]]), np.array([[1, 0.2], [0.1, 1]])]:
            with pytest.raises(ValueError):
                minimum_worst_variance([scale * invalid])


def test_future_returns_cannot_change_frozen_allocations():
    rng = np.random.default_rng(730)
    returns = rng.normal(size=(200, 6)) * 0.01
    first = allocation_candidates(returns[:126])
    returns[126:] += 10
    second = allocation_candidates(returns[:126])
    for name, weights in first.items():
        np.testing.assert_array_equal(weights, second[name])
        assert weights.min() >= -1e-10
        assert abs(weights.sum() - 1) < 1e-8
        if "capped" in name:
            assert weights.max() <= 0.35 + 1e-8
