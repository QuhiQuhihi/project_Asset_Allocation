"""Independent identities and boundary cases for allocation validation tools."""

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.stats import norm

from research.validation import (
    cscv_diagnostics,
    deflated_sharpe_ratio,
    expected_maximum_sharpe,
    probabilistic_sharpe_ratio,
    purged_train_indices,
    sharpe_ratio,
)


def test_purging_matches_independent_discrete_information_sets():
    starts = np.arange(36)
    ends = starts + 5
    test = np.arange(14, 20)
    for embargo in (0, 3):
        held_out_information = set()
        for row in test:
            held_out_information.update(range(starts[row], ends[row] + embargo + 1))
        oracle = [
            i for i in range(36) if not (set(range(starts[i], ends[i] + 1)) & held_out_information)
        ]
        np.testing.assert_array_equal(purged_train_indices(starts, ends, test, embargo), oracle)
    np.testing.assert_array_equal(purged_train_indices(starts, ends, test, 3), np.r_[0:9, 28:36])


def test_purging_disjoint_test_intervals_does_not_discard_unrelated_gap():
    starts = np.arange(20)
    ends = starts + 1
    train = purged_train_indices(starts, ends, np.array([3, 14]), embargo=1)
    np.testing.assert_array_equal(train, [0, 1, 6, 7, 8, 9, 10, 11, 12, 17, 18, 19])
    assert 2 not in train  # [2,3] shares the closed test endpoint.


@pytest.mark.parametrize(
    "kwargs",
    [
        {"starts": [0, 0], "ends": [1, 2], "test_indices": [0]},
        {"starts": [0, 1], "ends": [1, 0], "test_indices": [0]},
        {"starts": [0, 1], "ends": [1, 2], "test_indices": [2]},
        {"starts": [0, 1], "ends": [1, 2], "test_indices": [0, 0]},
        {"starts": [0, 1], "ends": [1, 2], "test_indices": [0], "embargo": -1},
        {"starts": [0, 1], "ends": [1, 2], "test_indices": [0], "embargo": 0.5},
    ],
)
def test_invalid_information_intervals_are_rejected(kwargs):
    with pytest.raises(ValueError):
        purged_train_indices(**kwargs)


def test_cscv_detects_complete_rank_reversal():
    noise = np.array([-0.003, -0.001, 0.001, 0.003])[:, None]
    first = noise + [0.03, 0.01, -0.01]
    second = noise + [-0.03, 0.01, 0.03]
    result = cscv_diagnostics(np.vstack([first, second]), n_blocks=2)
    np.testing.assert_array_equal(result.selected, [0, 2])
    np.testing.assert_allclose(result.relative_rank, 0.25)
    np.testing.assert_allclose(result.logit, -np.log(3))
    assert (result.logit <= 0).mean() == 1


def test_cscv_persistent_winner_and_tie_conventions():
    base = np.tile([-0.003, -0.001, 0.001, 0.003], 4)[:, None]
    stable = cscv_diagnostics(base + [0.0, 0.01, 0.02, 0.03], n_blocks=4)
    assert len(stable) == 6
    np.testing.assert_array_equal(stable.selected, 3)
    np.testing.assert_allclose(stable.relative_rank, 0.8)
    np.testing.assert_allclose(stable.logit, np.log(4))
    tied = cscv_diagnostics(np.repeat(base, 3, axis=1), n_blocks=4)
    np.testing.assert_array_equal(tied.selected, 0)
    np.testing.assert_array_equal(tied.relative_rank, 0.5)
    np.testing.assert_array_equal(tied.logit, 0)


def test_psr_normal_identity_and_one_trial_dsr():
    observed, count = 0.1, 101
    # Under Gaussian observations, asymptotic variance is (1+SR^2/2)/(T-1).
    expected = norm.cdf(observed / np.sqrt((1 + observed**2 / 2) / (count - 1)))
    actual = probabilistic_sharpe_ratio(observed, count)
    assert actual == pytest.approx(expected)
    assert probabilistic_sharpe_ratio(observed, count, observed) == 0.5
    assert expected_maximum_sharpe(0.3, 1) == 0
    assert deflated_sharpe_ratio(observed, count, 0.3, 1) == actual


def test_expected_maximum_against_independent_order_statistic_integral():
    # Independent Normal maximum density: n*phi(z)*Phi(z)^(n-1).
    n_trials = 100
    exact, _ = quad(lambda z: z * n_trials * norm.pdf(z) * norm.cdf(z) ** (n_trials - 1), -10, 10)
    approximation = expected_maximum_sharpe(1.0, n_trials)
    assert abs(approximation - exact) / exact < 0.02
    scores = [deflated_sharpe_ratio(0.1, 504, 0.04, n) for n in [1, 16, 64, 256]]
    assert all(a > b for a, b in zip(scores, scores[1:]))


def test_sharpe_scale_invariance_and_invalid_inputs():
    values = np.array([-0.02, 0.01, -0.01, 0.03])
    assert sharpe_ratio(values) == pytest.approx(sharpe_ratio(7 * values))
    with pytest.raises(ValueError):
        sharpe_ratio(np.ones(8))
    with pytest.raises(ValueError):
        cscv_diagnostics(np.ones((8, 3)), n_blocks=4)
    with pytest.raises(ValueError):
        cscv_diagnostics(np.ones((9, 3)), n_blocks=4)
    with pytest.raises(ValueError):
        cscv_diagnostics(np.array([[0.1, 0.2], [np.nan, 0.3], [0.3, 0.1]]), n_blocks=2)
    with pytest.raises(ValueError):
        probabilistic_sharpe_ratio(0.1, 20, kurtosis=0)  # Excess kurtosis is not accepted.
    with pytest.raises(ValueError):
        probabilistic_sharpe_ratio(0.1, 20, skewness=100, kurtosis=3)
    with pytest.raises(ValueError):
        expected_maximum_sharpe(0.1, 0)
    with pytest.raises(ValueError):
        expected_maximum_sharpe(-0.1, 8)
