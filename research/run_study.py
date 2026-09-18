"""Execute the frozen allocation comparison from pinned cached prices."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
from research.allocation import run
from research.common import (
    ROOT,
    RESULTS,
    FIGURES,
    load_returns,
    performance,
    block_interval,
    table,
    plot_style,
    write_metadata,
)


def main():
    r = load_returns()
    out = RESULTS / "paths"
    out.mkdir(parents=True, exist_ok=True)
    result = run(r)
    for name in ["daily", "weights", "trades", "diagnostics"]:
        getattr(result, name).to_csv(out / f"{name}.csv", index=False)
    perf = []
    periods = {
        "full": ("2020-08-01", "2026-09-18"),
        "late": ("2025-01-01", "2026-09-18"),
        "2022": ("2022-01-01", "2023-01-01"),
    }
    for period, (begin, end) in periods.items():
        d = result.daily.query("@begin <= date < @end")
        for s, g in d.groupby("strategy"):
            perf.append(
                {
                    "period": period,
                    "strategy": s,
                    **performance(g.net),
                    "gross_mean": g.gross.mean() * 252,
                    "annual_turnover": g.turnover.mean() * 252,
                    "annual_cost_fraction": g.cost.mean() * 252,
                    "mean_cash": g.cash.mean(),
                    "mean_concentration": g.concentration.mean(),
                }
            )
    perf = pd.DataFrame(perf)
    perf.to_csv(RESULTS / "performance.csv", index=False)
    comparisons = []
    late = result.daily.query('date >= "2025-01-01"')
    net = late.pivot(index="date", columns="strategy", values="net")
    for s in ["HRP", "ERC", "Inverse vol"]:
        for control in ["Equal weight", "EQ risk " + s]:
            for block in [5, 21, 63]:
                comparisons.append(
                    {
                        "strategy": s,
                        "control": control,
                        "metric": "mean_over_vol_rf0",
                        **block_interval(net[s], net[control], "sharpe", block),
                    }
                )
    comp = pd.DataFrame(comparisons)
    comp.to_csv(RESULTS / "paired_intervals.csv", index=False)
    headroom = []
    gross = late.pivot(index="date", columns="strategy", values="gross")
    turn = late.pivot(index="date", columns="strategy", values="turnover")
    for s in ["HRP", "ERC", "Inverse vol"]:
        b = "EQ risk " + s
        delta = (gross[s] - gross[b]).mean() * 252
        dt = (turn[s] - turn[b]).mean() * 252
        ci = block_interval(gross[s], gross[b])
        headroom.append(
            {
                "strategy": s,
                "control": b,
                "annual_gross_headroom_bps": delta * 1e4,
                "lower95_bps": ci["lower95"] * 252e4,
                "upper95_bps": ci["upper95"] * 252e4,
                "annual_incremental_turnover": dt,
                "linear_cost_ceiling_bps_per_dollar": delta / dt * 1e4 if dt > 0 else np.nan,
            }
        )
    pd.DataFrame(headroom).to_csv(RESULTS / "cost_headroom.csv", index=False)
    variants = {
        "primary": {},
        "lookback126": {"lookback": 126},
        "lookback504": {"lookback": 504},
        "shrinkage": {"shrink": True},
        "cost0": {"bps": 0},
        "cost10": {"bps": 10},
        "extra_session_lag": {"lag": 2},
    }
    sensitivity = []
    for name, kw in variants.items():
        x = result if name == "primary" else run(r, **kw)
        d = x.daily.query('date >= "2025-01-01"').pivot(
            index="date", columns="strategy", values="net"
        )
        for s in ["HRP", "ERC", "Inverse vol", "Defensive momentum"]:
            b = "EQ risk " + s if s != "Defensive momentum" else "Equal weight"
            sensitivity.append(
                {
                    "variant": name,
                    "strategy": s,
                    "control": b,
                    "ratio_difference": performance(d[s])["mean_over_vol_rf0"]
                    - performance(d[b])["mean_over_vol_rf0"],
                    "annual_mean_difference": (d[s] - d[b]).mean() * 252,
                    "vol_difference": (d[s].std() - d[b].std()) * np.sqrt(252),
                    "erc_fallbacks": x.diagnostics.erc_fallback.sum(),
                }
            )
    pd.DataFrame(sensitivity).to_csv(RESULTS / "sensitivity.csv", index=False)
    diag = result.diagnostics
    pd.DataFrame(
        [
            {
                "rebalances": len(diag),
                "erc_fallbacks": diag.erc_fallback.sum(),
                "max_cov_condition": diag.condition_number.max(),
                **{c: diag[c].mean() for c in diag if c.startswith("cap_")},
            }
        ]
    ).to_csv(RESULTS / "implementation.csv", index=False)
    plt = plot_style()
    primary = ["Equal weight", "Inverse vol", "ERC", "HRP", "EQ risk HRP"]
    full = result.daily.pivot(index="date", columns="strategy", values="net")
    wealth = (1 + full).cumprod()
    fig, ax = plt.subplots()
    wealth[primary].plot(ax=ax)
    ax.set(
        ylabel="Net wealth (entry capital = 1)",
        xlabel="Close date",
        title=f"Allocation, {full.index.min():%Y-%m-%d}–{full.index.max():%Y-%m-%d}; 5 bp trades",
    )
    fig.tight_layout()
    fig.savefig(FIGURES / "wealth.png", dpi=150)
    plt.close(fig)
    fig, ax = plt.subplots()
    (wealth[primary] / wealth[primary].cummax().clip(lower=1) - 1).plot(ax=ax)
    ax.set(
        ylabel="Drawdown (fraction)",
        xlabel="Close date",
        title="Drawdown including initial capital",
    )
    fig.tight_layout()
    fig.savefig(FIGURES / "drawdown.png", dpi=150)
    plt.close(fig)
    fig, ax = plt.subplots()
    w = result.weights.query('strategy=="HRP"').set_index("date")
    w[["SPY", "IEMG", "TLT", "GLD", "SHY", "cash"]].plot.area(ax=ax)
    ax.set(
        ylabel="Fraction of NAV",
        xlabel="Earning date",
        title="HRP exposures, including drifting weights",
    )
    fig.tight_layout()
    fig.savefig(FIGURES / "exposures.png", dpi=150)
    plt.close(fig)
    c = comp.query('block==21 and control != "Equal weight"').copy()
    fig, ax = plt.subplots()
    ax.errorbar(
        c.estimate,
        np.arange(len(c)),
        xerr=np.vstack([c.estimate - c.lower95, c.upper95 - c.estimate]),
        fmt="o",
        capsize=4,
    )
    ax.set_yticks(np.arange(len(c)), c.strategy)
    ax.axvline(0, color="#555", ls="--")
    ax.set(
        xlabel="Net mean/volatility difference (zero cash benchmark)",
        title=f"2025-01-01–{full.index.max():%Y-%m-%d} vs risk-scaled EQ; 95% block intervals",
    )
    fig.tight_layout()
    fig.savefig(FIGURES / "incremental.png", dpi=150)
    plt.close(fig)
    headline = comp.query('strategy=="HRP" and control=="EQ risk HRP" and block==21').iloc[0]
    status = (
        "does not establish" if headline.lower95 <= 0 else "provides conditional sample evidence of"
    )
    findings = (
        f"""# Does portfolio construction earn its complexity?\n\nIn January 2025–17 September 2026, HRP minus its prior-risk-scaled equal-weight control has a net annualized mean/volatility difference of **{headline.estimate:+.3f}**, with paired 95% block interval **[{headline.lower95:+.3f}, {headline.upper95:+.3f}]**. This {status} incremental risk-adjusted value under this universe, zero cash interest and cost assumptions.\n\nThis is a retrospective ETF study. Cash-heavy risk portfolios can look safer simply because they hold SHY or reduce exposure. The matched-risk control uses only past covariance, with a cap at 100%; realized risks need not match. A mean/volatility ratio with zero assumed cash interest is not an observed risk-free-adjusted Sharpe ratio.\n\n## Late-segment comparison\n\n"""
        + table(
            perf.query('period=="late"')[
                ["strategy", "cagr", "volatility", "max_drawdown", "annual_turnover", "mean_cash"]
            ]
        )
        + """\nReturns and risks are decimal annual rates; drawdowns are fractions. Turnover includes buys and sells.\n\n![Incremental result](../research/figures/incremental.png)\n\n## What changes the answer\n\n"""
        + table(
            pd.DataFrame(sensitivity).query('strategy=="HRP"')[
                ["variant", "ratio_difference", "annual_mean_difference", "vol_difference"]
            ]
        )
        + """\nAll variants remain visible; no winning replacement is selected. These comparisons reuse the same history and are not independent trials. The defensive momentum adaptation is separate from covariance estimation, and the 60/40 portfolio is contextual because its universe differs.\n\n## Economic boundary\n\n"""
        + table(pd.DataFrame(headroom))
        + f"""\nThe annual headroom is a gross incremental constant-cost budget, not an observed fee. The per-dollar ceiling is a first-order approximation only when extra turnover is positive. Negative headroom is retained. ERC fallback occurred {int(diag.erc_fallback.sum())} times over {len(diag)} rebalances.\n\nA stronger conclusion needs a prospectively fixed universe, an uninspected sample, observed cash yields and executable spread/size evidence. Adjusted prices may be revised, distributions are reinvested by proxy, closing fractional fills are assumed, and the study does not reconstruct delistings. See [protocol](../research/PROTOCOL.md), [inputs and methods](01-methods.md), [source register](../research/SOURCES.md), and [next experiment](../research/RESEARCH_AGENDA.md).\n"""
    )
    (ROOT / "docs/02-results.md").write_text(findings)
    readme = ROOT / "README.md"
    if readme.exists():
        parts = readme.read_text().split("\n\n", 2)
        readme.write_text(parts[0] + "\n\n" + findings.split("\n\n")[1] + "\n\n" + parts[2])
    (RESULTS / "headline.json").write_text(
        __import__("json").dumps(
            {
                "estimate": headline.estimate,
                "lower95": headline.lower95,
                "upper95": headline.upper95,
            },
            indent=2,
        )
        + "\n"
    )
    write_metadata(
        {
            "lookback": 252,
            "cost_bps": 5,
            "seed": 20260919,
            "primary": "HRP minus EQ risk HRP; late mean/vol rf0",
        }
    )
    print(findings.split("\n\n")[1])


if __name__ == "__main__":
    main()
