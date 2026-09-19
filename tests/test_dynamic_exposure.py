"""Independent arithmetic and information-boundary checks for exposure rules."""

import numpy as np
import pytest

from research.dynamic_exposure import run_cppi, run_exposure, volatility_targets


def test_entry_fee_and_cash_return_match_dollar_accounting():
    path = run_exposure([0.10], [0.60], cash_rate=0.01, cost_bps=10)
    fee = 0.001 * 60 / (1 + 0.001 * 0.60)
    risky = (100 - fee) * 0.60
    cash = 100 - fee - risky
    assert path.fee.iloc[0] == pytest.approx(fee)
    assert path.wealth_end.iloc[0] == pytest.approx(risky * 1.10 + cash * 1.01)
    assert risky + cash + fee == pytest.approx(100)


def test_drift_is_carried_into_the_next_trade():
    path = run_exposure([0.10, 0.0], [0.60, 0.60], cost_bps=0)
    assert path.pretrade_risky.iloc[1] == pytest.approx(66 / 106)
    assert path.turnover.iloc[1] == pytest.approx(66 / 106 - 0.60)


def test_volatility_uses_only_information_available_before_execution():
    returns = np.array([0.01, -0.02, 0.03, -0.04, 0.05, -0.06, 0.07])
    base = volatility_targets(returns, lookback=2, delay=1, target_vol=0.10)
    assert base.forecast_vol.iloc[3] == pytest.approx(np.std(returns[:2], ddof=1) * np.sqrt(252))
    changed = returns.copy()
    changed[3:] = 0.40
    perturbed = volatility_targets(changed, lookback=2, delay=1, target_vol=0.10)
    np.testing.assert_array_equal(base.target_risky.iloc[:5], perturbed.target_risky.iloc[:5])
    assert base.target_risky.iloc[5] != perturbed.target_risky.iloc[5]


def test_flat_forecast_stays_unlevered_and_warmup_holds_cash():
    path = volatility_targets(np.zeros(7), lookback=2, cap=0.8, delay=1)
    np.testing.assert_array_equal(path.target_risky, [0, 0, 0, 0.8, 0.8, 0.8, 0.8])


def test_cppi_known_step_and_large_gap():
    upside = run_cppi([0.10], terminal_floor=80, multiplier=3, cost_bps=0)
    assert upside.target_risky.iloc[0] == pytest.approx(0.60)
    assert upside.wealth_end.iloc[0] == pytest.approx(106)
    gap = run_cppi([-0.40, 0.10], terminal_floor=80, multiplier=3, cost_bps=0)
    np.testing.assert_allclose(gap.wealth_end, [76, 76])
    np.testing.assert_allclose(gap.target_risky, [0.60, 0])
    assert gap.floor_gap.iloc[0] == pytest.approx(-4)


def test_floor_rolls_at_cash_rate_and_zero_cushion_stays_in_cash():
    cash_rate = 0.01
    terminal_floor = 100 * (1 + cash_rate) ** 3
    path = run_cppi(
        [0.20, -0.20, 0.30], terminal_floor=terminal_floor, cash_rate=cash_rate, cost_bps=0
    )
    np.testing.assert_allclose(path.target_risky, 0, atol=1e-14)
    np.testing.assert_allclose(path.wealth_end, 100 * (1 + cash_rate) ** np.arange(1, 4))
    np.testing.assert_allclose(path.floor_end, path.wealth_end)


def test_cppi_delayed_decision_owns_only_a_later_return():
    base = run_cppi([0.0, -0.40, 0.10, 0.10], delay=1, cost_bps=0)
    changed = run_cppi([0.0, 0.40, 0.10, 0.10], delay=1, cost_bps=0)
    np.testing.assert_allclose(base.target_risky.iloc[:3], [0.0, 0.60, 0.60])
    np.testing.assert_array_equal(base.target_risky.iloc[:3], changed.target_risky.iloc[:3])
    assert base.target_risky.iloc[3] == 0
    assert changed.target_risky.iloc[3] > 0


@pytest.mark.parametrize("kwargs", [{"delay": -1}, {"cap": 1.2}, {"multiplier": 0}])
def test_invalid_cppi_policy_is_rejected(kwargs):
    with pytest.raises(ValueError):
        run_cppi([0.01, -0.02], **kwargs)
