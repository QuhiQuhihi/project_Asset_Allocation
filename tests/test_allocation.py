import numpy as np
import pandas as pd
import pytest
from research.allocation import erc, hrp, inverse_vol, run
from research.common import trading_cost, performance


def fixture():
    rng = np.random.default_rng(42)
    return pd.DataFrame(
        rng.normal(0, 0.01, (620, 6)),
        index=pd.bdate_range("2018-01-01", periods=620),
        columns=["SPY", "IEMG", "TLT", "GLD", "SHY", "AGG"],
    )


def test_hand_accounting_and_both_sides():
    # Buy A from cash at 100 bps: cost = a/(1+a).
    fee, trades = trading_cost([0, 0], [1, 0], 100)
    assert fee == pytest.approx(0.01 / 1.01)
    assert trades.sum() + fee == pytest.approx(1)
    # A rises 10%, then rotate entirely to B; sell 1 and buy (1-c).
    c, t = trading_cost([1, 0], [0, 1], 100)
    assert c == pytest.approx(0.02 / 1.01)
    nav = (1 - fee) * 1.1 * (1 - c)
    assert nav == pytest.approx(10890 / 10201)
    assert t[0] == -1 and t[1] == pytest.approx(1 - c)


def test_drift_and_no_trade():
    u = np.array([0.5 * 1.1, 0.5]) / 1.05
    c, t = trading_cost(u, u, 5)
    assert c == pytest.approx(0)
    assert np.abs(t).sum() == pytest.approx(0)
    assert u[0] == pytest.approx(11 / 21)


def test_erc_diagonal_independent_formula():
    c = np.diag([1.0, 4.0, 9.0])
    expected = np.array([1.0, 0.5, 1 / 3])
    expected /= expected.sum()
    np.testing.assert_allclose(erc(c), expected, atol=1e-6)


def test_hrp_two_assets_inverse_variance_and_distance():
    # One split: cluster variances are 1 and 4, so 80/20, independently derived.
    np.testing.assert_allclose(hrp(np.diag([1.0, 4.0])), [0.8, 0.2], atol=1e-12)
    np.testing.assert_allclose(hrp(np.eye(4)), np.ones(4) / 4)


def test_future_changes_do_not_change_targets_or_fills():
    r = fixture()
    a = run(r, start="2020-01-01")
    cut = r.index[-25]
    changed = r.copy()
    changed.loc[changed.index > cut] *= 2
    b = run(changed, start="2020-01-01")
    pd.testing.assert_frame_equal(
        a.trades.query("execution_date<=@cut"), b.trades.query("execution_date<=@cut")
    )
    pd.testing.assert_frame_equal(a.daily.query("date<=@cut"), b.daily.query("date<=@cut"))
    assert (a.trades.information_date < a.trades.execution_date).all()


def test_missing_zero_volatility_and_bad_budgets_fail():
    r = fixture()
    r.iloc[-1, 0] = np.nan
    with pytest.raises(ValueError):
        run(r, start="2020-01-01")
    with pytest.raises(ValueError):
        inverse_vol(np.diag([0.0, 1.0]))
    with pytest.raises(ValueError):
        trading_cost([1], [1.1], 5)
    with pytest.raises(ValueError):
        trading_cost([1], [-0.1], 5)


def test_singular_covariance_is_feasible():
    c = np.ones((3, 3)) + np.eye(3) * 1e-8
    for w in [hrp(c), erc(c)]:
        assert np.isfinite(w).all() and np.min(w) >= 0
        assert w.sum() == pytest.approx(1)


def test_drawdown_includes_initial_loss():
    assert performance([-0.1, 0])["max_drawdown"] == pytest.approx(-0.1)
