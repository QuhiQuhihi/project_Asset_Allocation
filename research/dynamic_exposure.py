"""One risky sleeve and remunerated cash: transparent, discrete trading examples.

These constructed teaching experiments do not estimate an investable premium.
Each return belongs to the holdings established BEFORE that return is observed.
"""

import numpy as np
import pandas as pd

from research.common import trading_cost


def _returns(values):
    array = np.asarray(values, dtype=float)
    if array.ndim != 1 or not len(array) or not np.isfinite(array).all() or (array <= -1).any():
        raise ValueError("Need a nonempty finite vector of simple returns greater than -1")
    return array


def _delay(value):
    if not isinstance(value, (int, np.integer)) or isinstance(value, bool) or value < 0:
        raise ValueError("delay must be a nonnegative integer number of complete periods")


def volatility_targets(returns, lookback=20, target_vol=0.10, cap=1.0, delay=1, periods=252):
    """Forecast from r[t-delay-lookback:t-delay]; the resulting weight owns r[t].

    With delay=1, a return observed at one close can influence a trade at the
    NEXT close and therefore the following close-to-close return. Before there
    is enough history the policy owns cash. A zero estimate uses the cap.
    """
    returns = _returns(returns)
    _delay(delay)
    if not isinstance(lookback, (int, np.integer)) or lookback < 2:
        raise ValueError("lookback must be an integer of at least two")
    if not np.isfinite([target_vol, cap, periods]).all() or not (
        target_vol > 0 and 0 <= cap <= 1 and periods > 0
    ):
        raise ValueError("Invalid volatility target, unlevered cap, or annualization")
    rows = []
    for day in range(len(returns)):
        stop = day - delay
        forecast = np.nan
        weight = 0.0
        if stop >= lookback:
            forecast = returns[stop - lookback : stop].std(ddof=1) * np.sqrt(periods)
            weight = min(cap, target_vol / forecast) if forecast > 0 else cap
        rows.append((forecast, weight, stop - 1))
    return pd.DataFrame(rows, columns=["forecast_vol", "target_risky", "last_observed_return"])


def _settings(cash_rate, cost_bps, initial_wealth):
    if not np.isfinite([cash_rate, cost_bps, initial_wealth]).all() or not (
        cash_rate > -1 and 0 <= cost_bps < 10000 and initial_wealth > 0
    ):
        raise ValueError("Invalid cash return, cost, or initial wealth")


def _period(wealth, risky_value, target, risky_return, cash_rate, cost_bps):
    """One rebalance and return; cash transfers are free, risky trades incur fees."""
    pretrade = risky_value / wealth
    fee_fraction, trades = trading_cost([pretrade], [target], cost_bps)
    after_cost = wealth * (1 - fee_fraction)
    risky_after_trade = after_cost * target
    cash_after_trade = after_cost * (1 - target)
    risky_end = risky_after_trade * (1 + risky_return)
    end = risky_end + cash_after_trade * (1 + cash_rate)
    return {
        "wealth_start": wealth,
        "pretrade_risky": pretrade,
        "target_risky": target,
        "fee": wealth * fee_fraction,
        "turnover": float(np.abs(trades).sum()),
        "risky_after_trade": risky_after_trade,
        "cash_after_trade": cash_after_trade,
        "net_return": end / wealth - 1,
        "wealth_end": end,
    }, risky_end


def run_exposure(returns, targets, cash_rate=0.0, cost_bps=5.0, initial_wealth=100.0):
    """Execute supplied beginning-of-period targets, allowing holdings to drift.

    A target is a fraction of POST-FEE wealth. Fees equal cost_bps times actual
    risky dollars traded, and are solved self-consistently before either sleeve
    earns its return. There is an entry fee and no terminal liquidation.
    """
    returns = _returns(returns)
    targets = np.asarray(targets, dtype=float)
    _settings(cash_rate, cost_bps, initial_wealth)
    if (
        targets.shape != returns.shape
        or not np.isfinite(targets).all()
        or ((targets < 0) | (targets > 1)).any()
    ):
        raise ValueError("Targets must match returns and lie between zero and one")
    wealth, risky_value = float(initial_wealth), 0.0
    rows = []
    for risky_return, target in zip(returns, targets, strict=True):
        row, risky_value = _period(wealth, risky_value, target, risky_return, cash_rate, cost_bps)
        wealth = row["wealth_end"]
        rows.append(row)
    return pd.DataFrame(rows)


def run_cppi(
    returns,
    terminal_floor=80.0,
    multiplier=3.0,
    cap=1.0,
    cash_rate=0.0,
    cost_bps=5.0,
    delay=0,
    initial_wealth=100.0,
):
    """Discrete CPPI with a terminal nominal floor discounted at the cash rate.

    A decision uses current PRE-FEE wealth and floor. With delay > 0 that target
    WEIGHT is queued for the stated number of complete return periods; it is
    not recomputed at execution. The initial queue holds cash. Costs, jumps and
    delays can breach the floor; the floor is a reference, never a guarantee.
    """
    returns = _returns(returns)
    _settings(cash_rate, cost_bps, initial_wealth)
    _delay(delay)
    if not np.isfinite([terminal_floor, multiplier, cap]).all() or not (
        terminal_floor >= 0 and multiplier > 0 and 0 <= cap <= 1
    ):
        raise ValueError("Invalid terminal floor, multiplier or unlevered cap")
    floors = terminal_floor / (1 + cash_rate) ** np.arange(len(returns), -1, -1)
    if not np.isfinite(floors).all():
        raise ValueError("Floor discounting overflow")
    wealth, risky_value = float(initial_wealth), 0.0
    decisions, rows = [], []
    for day, risky_return in enumerate(returns):
        cushion = max(wealth - floors[day], 0.0)
        decision = min(cap, multiplier * cushion / wealth)
        decisions.append(decision)
        target = decisions[day - delay] if day >= delay else 0.0
        row, risky_value = _period(wealth, risky_value, target, risky_return, cash_rate, cost_bps)
        row.update(
            floor_start=floors[day],
            floor_end=floors[day + 1],
            cushion_start=cushion,
            decision_risky=decision,
            floor_gap=row["wealth_end"] - floors[day + 1],
        )
        wealth = row["wealth_end"]
        rows.append(row)
    return pd.DataFrame(rows)
