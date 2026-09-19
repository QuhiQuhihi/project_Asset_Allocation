import numpy as np
import pytest

from research.factors_liabilities import (
    cashflow_measures,
    exposure_target_allocation,
    factor_decomposition,
    match_liability_zeros,
)


def test_factor_variance_reconstructs_assets_and_retains_negative_contributions():
    b = np.array([[1, 0.2], [0.5, 1], [0.2, 0.8]])
    f = np.array([[0.04, -0.018], [-0.018, 0.01]])
    d = np.diag([0.001, 0.002, 0.003])
    w = np.array([0.7, 0.2, 0.1])
    result = factor_decomposition(w, b, f, d)
    np.testing.assert_allclose(result["variance"], w @ (b @ f @ b.T + d) @ w, atol=1e-15)
    assert result["factor_variance"][1] < 0
    np.testing.assert_allclose(
        result["factor_variance"].sum() + result["residual_variance"], result["variance"]
    )


def test_target_allocation_known_inverse_variance_split_and_infeasibility():
    # The growth target fixes asset 3 at 40%. Identical exposures on assets 1/2
    # leave 60% split inversely to their residual variances 1:4 => 48% and 12%.
    b = np.array([[1.0, 0], [1.0, 0], [0, 1.0]])
    d = np.diag([1.0, 4.0, 2.0])
    np.testing.assert_allclose(
        exposure_target_allocation(b, d, [0.6, 0.4]), [0.48, 0.12, 0.40], atol=1e-7
    )
    np.testing.assert_allclose(
        exposure_target_allocation(b, d, [0.6, 0.4], cap=0.4), [0.4, 0.2, 0.4], atol=1e-7
    )
    with pytest.raises(ValueError, match="infeasible"):
        exposure_target_allocation(b, d, [0.8, 0.8])
    for scale in [1e-14, 1.0, 1e14]:
        with pytest.raises(ValueError, match="positive semidefinite"):
            factor_decomposition([1, 0], np.eye(2), scale * np.array([[1, 2], [2, 1]]), np.eye(2))


def test_zero_hedge_matches_direct_cashflows_and_independent_linear_system():
    lt, cf, at, rate = np.array([4.0, 7.0]), np.array([60.0, 70.0]), np.array([2.0, 10.0]), 0.04
    pv = float(np.sum(cf * np.exp(-rate * lt)))
    dd = float(np.sum(lt * cf * np.exp(-rate * lt)))
    hedge = match_liability_zeros(lt, cf, at, rate, pv + 3)
    reference = np.linalg.solve(np.vstack([np.ones(2), at]), [pv, dd])
    np.testing.assert_allclose(hedge["market_values"], reference, atol=1e-12)
    assert hedge["cash"] == pytest.approx(3.0)
    asset = cashflow_measures(at, hedge["face_values"], rate)
    assert asset["pv"] == pytest.approx(pv)
    assert asset["dollar_duration"] == pytest.approx(dd)


def test_duration_finite_difference_and_parallel_vs_shape_residual():
    lt, cf, at, rate = np.array([4.0, 7.0]), np.array([60.0, 70.0]), np.array([2.0, 10.0]), 0.04
    liability = cashflow_measures(lt, cf, rate)
    h = match_liability_zeros(lt, cf, at, rate, liability["pv"])
    face = h["face_values"]

    def surplus(shift):
        return sum(face * np.exp(-(rate + shift) * at)) - sum(cf * np.exp(-(rate + shift) * lt))

    bump = 1e-5
    slope = (surplus(bump) - surplus(-bump)) / (2 * bump)
    assert abs(slope) < 1e-5
    second = (surplus(bump) + surplus(-bump) - 2 * surplus(0)) / bump**2
    exact_second = sum(at**2 * face * np.exp(-rate * at)) - sum(lt**2 * cf * np.exp(-rate * lt))
    assert second == pytest.approx(exact_second, rel=1e-5)
    # A linear tilt shocks long maturities more than short maturities.
    shaped = sum(face * np.exp(-(rate + 0.002 * (at - 6)) * at))
    shaped -= sum(cf * np.exp(-(rate + 0.002 * (lt - 6)) * lt))
    assert abs(shaped) > 1.0


def test_liability_hedge_rejects_unfunded_unspanned_or_invalid_inputs():
    with pytest.raises(ValueError, match="Insufficient capital"):
        match_liability_zeros([5], [100], [2, 10], 0.04, 50)
    with pytest.raises(ValueError, match="outside"):
        match_liability_zeros([12], [100], [2, 10], 0.04, 100)
    for times, amounts, rates in [
        ([0], [100], 0.04),
        ([2], [-1], 0.04),
        ([2], [100], [0.03, 0.04]),
    ]:
        with pytest.raises(ValueError):
            cashflow_measures(times, amounts, rates)
