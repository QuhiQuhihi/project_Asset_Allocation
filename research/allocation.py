"""Causal allocation targets and exact holdings accounting."""

from dataclasses import dataclass
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, leaves_list
from scipy.spatial.distance import squareform
from scipy.optimize import minimize
from sklearn.covariance import LedoitWolf
from research.common import trading_cost, validate_returns

ASSETS = ["SPY", "IEMG", "TLT", "GLD", "SHY"]


def inverse_vol(cov):
    v = np.diag(cov)
    if not np.isfinite(cov).all() or (v <= 0).any():
        raise ValueError("Positive finite variances required")
    w = 1 / np.sqrt(v)
    return w / w.sum()


def erc(cov):
    c = cov / np.diag(cov).mean()
    n = len(c)

    def f(x):
        return 0.5 * x @ c @ x - np.log(x).sum()

    def jac(x):
        return c @ x - 1 / x

    opt = minimize(
        f,
        np.ones(n),
        jac=jac,
        bounds=[(1e-8, None)] * n,
        method="L-BFGS-B",
        options={"ftol": 1e-14, "gtol": 1e-9, "maxiter": 1000},
    )
    if not opt.success:
        raise ValueError("ERC convergence failure")
    w = opt.x / opt.x.sum()
    rc = w * (cov @ w)
    if np.max(np.abs(rc / rc.sum() - 1 / n)) > 1e-5:
        raise ValueError("ERC risk-budget residual")
    return w


def hrp(cov):
    std = np.sqrt(np.diag(cov))
    if (std <= 0).any() or not np.isfinite(cov).all():
        raise ValueError("Invalid covariance")
    corr = np.clip(cov / np.outer(std, std), -1, 1)
    d = np.sqrt(np.maximum((1 - corr) / 2, 0))
    np.fill_diagonal(d, 0)
    # linkage's 2-D input denotes observations, NOT precomputed distances.
    tree = linkage(squareform(d, checks=True), method="single")
    order = leaves_list(tree).tolist()
    w = np.ones(len(cov))
    groups = [order]

    def variance(indices):
        sub = cov[np.ix_(indices, indices)]
        inv = 1 / np.diag(sub)
        weights = inv / inv.sum()
        return weights @ sub @ weights

    while groups:
        next_groups = []
        for group in groups:
            if len(group) < 2:
                continue
            mid = len(group) // 2
            left, right = group[:mid], group[mid:]
            vl, vr = variance(left), variance(right)
            if vl + vr <= 0:
                raise ValueError("Zero cluster variance")
            alpha = vr / (vl + vr)
            w[left] *= alpha
            w[right] *= 1 - alpha
            next_groups.extend([left, right])
        groups = next_groups
    return w / w.sum()


def targets(history, lookback=252, shrink=False):
    h = history[ASSETS].iloc[-lookback:]
    if len(h) < lookback or len(history) < 252:
        raise ValueError("Insufficient warmup")
    validate_returns(h)
    raw = np.cov(h.to_numpy(), rowvar=False, ddof=1)
    iv = inverse_vol(raw)  # fail on zero-volatility assets before regularizing
    cov = LedoitWolf().fit(h).covariance_ if shrink else raw.copy()
    cov += np.eye(len(cov)) * np.trace(cov) / len(cov) * 1e-8
    eq = np.ones(len(ASSETS)) / len(ASSETS)
    result = {"Equal weight": eq, "Inverse vol": iv, "HRP": hrp(cov)}
    fallback = False
    try:
        result["ERC"] = erc(cov)
    except ValueError:
        result["ERC"] = iv
        fallback = True
    caps = {}
    for name in ["Inverse vol", "ERC", "HRP"]:
        ratio = np.sqrt(result[name] @ cov @ result[name] / (eq @ cov @ eq))
        result["EQ risk " + name] = eq * min(1.0, ratio)
        caps[name] = ratio > 1
    score = sum(
        k * ((1 + history[ASSETS].iloc[-n:]).prod().to_numpy() - 1)
        for n, k in [(21, 12), (63, 4), (126, 2), (252, 1)]
    )
    tactical = np.zeros(5)
    if (score[:4] > 0).all():
        tactical[:4] = 0.25
    else:
        tactical[4] = 1
    result["Defensive momentum"] = tactical
    all_names = list(history.columns)
    expanded = {}
    for name, w in result.items():
        a = np.zeros(len(all_names))
        a[[all_names.index(t) for t in ASSETS]] = w
        expanded[name] = a
    context = np.zeros(len(all_names))
    context[all_names.index("SPY")] = 0.6
    context[all_names.index("AGG")] = 0.4
    expanded["60/40 context"] = context
    diagnostics = {
        "condition_number": np.linalg.cond(raw),
        "erc_fallback": int(fallback),
        **{"cap_" + k: int(v) for k, v in caps.items()},
    }
    return expanded, diagnostics


@dataclass
class Run:
    daily: pd.DataFrame
    weights: pd.DataFrame
    trades: pd.DataFrame
    diagnostics: pd.DataFrame


def run(returns, lookback=252, bps=5, shrink=False, lag=1, start="2020-08-01"):
    validate_returns(returns)
    if lag not in [1, 2]:
        raise ValueError("Supported execution lag is 1 or 2")
    months = returns.index.to_period("M")
    first = np.r_[True, np.asarray(months[1:] != months[:-1])]
    candidates = np.flatnonzero(first & (returns.index >= pd.Timestamp(start)))
    if not len(candidates) or candidates[0] - lag + 1 < max(lookback, 252):
        raise ValueError("Common start lacks warmup")
    # First execution shifted by lag-1; primary comparisons retain the same calendar start.
    decisions = {int(t + lag - 1): int(t - 1) for t in candidates if t + lag - 1 < len(returns)}
    strategies = list(targets(returns.iloc[: candidates[0]], lookback, shrink)[0])
    holdings = {s: np.zeros(returns.shape[1]) for s in strategies}
    daily = []
    weights = []
    trades = []
    diagnostics = []
    for t in range(int(candidates[0]), len(returns)):
        date = returns.index[t]
        r = returns.iloc[t].to_numpy()
        computed = None
        if t in decisions:
            info = decisions[t]
            computed, diag = targets(returns.iloc[: info + 1], lookback, shrink)
            diagnostics.append({"date": date, "information_date": returns.index[info], **diag})
        for s in strategies:
            w = holdings[s].copy()
            cash = 1 - w.sum()
            gross = w @ r
            if abs(cash) < 1e-12:
                cash = 0.0
            if cash < -1e-8:
                raise ValueError("Negative cash violates long-only budget")
            weights.append(
                {"date": date, "strategy": s, **dict(zip(returns.columns, w)), "cash": cash}
            )
            u = w * (1 + r) / (1 + gross)
            fee = 0.0
            turnover = 0.0
            if computed is not None:
                target = computed[s]
                fee, trade = trading_cost(u, target, bps)
                turnover = np.abs(trade).sum()
                holdings[s] = target
                trades.append(
                    {
                        "execution_date": date,
                        "information_date": returns.index[decisions[t]],
                        "strategy": s,
                        **{"target_" + a: v for a, v in zip(returns.columns, target)},
                        **{"trade_" + a: v for a, v in zip(returns.columns, trade)},
                        "cash": 1 - target.sum(),
                        "cost": fee,
                        "turnover": turnover,
                    }
                )
            else:
                holdings[s] = u
            daily.append(
                {
                    "date": date,
                    "strategy": s,
                    "gross": gross,
                    "net": (1 + gross) * (1 - fee) - 1,
                    "cost": fee,
                    "turnover": turnover,
                    "cash": cash,
                    "concentration": np.sum(w * w) + cash * cash,
                }
            )
    return Run(
        pd.DataFrame(daily), pd.DataFrame(weights), pd.DataFrame(trades), pd.DataFrame(diagnostics)
    )
