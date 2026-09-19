# Asset allocation: from portfolio objectives to investment rules

Asset allocation determines which risks a portfolio owns, how strongly it owns them, and when that exposure changes. This project explores those decisions through nine approaches: mean–variance optimization, risk parity, hierarchical risk parity, Kelly growth, maximum diversification, sector momentum, vigilant allocation, defensive allocation, and sector reversal.

The methods answer different questions. A minimum-risk portfolio does not necessarily maximize growth; a well-diversified portfolio can still lose when correlations rise; a tactical rule can reduce exposure while paying for frequent reversals. The purpose of the collection is to understand these tradeoffs and examine whether a strategy's additional complexity earns a measurable benefit.

## Explore the strategies

Each chapter introduces the economic idea, defines the portfolio rule, and develops a worked notebook. The topic notebooks use explicit illustrative inputs to make the mechanics visible. Risk parity and HRP also connect to the completed historical ETF comparison below.

| Topic | Research question and contents | Read | Explore |
|---|---|---|---|
| **1. Mean–variance allocation** | How does a return objective change the minimum-risk mix? Construct the efficient frontier and examine sensitivity to expected returns. | [Research note](topics/01-mean-variance/README.md) | [Notebook](topics/01-mean-variance/study.ipynb) |
| **2. Risk parity** | Does equal capital mean equal risk? Compare equal weight, inverse volatility, and equal risk contribution using marginal portfolio risk. | [Research note](topics/02-risk-parity/README.md) | [Notebook](topics/02-risk-parity/study.ipynb) |
| **3. Hierarchical risk parity** | Can correlation clusters organize diversification? Follow distance construction, a dendrogram, and recursive cluster allocation. | [Research note](topics/03-hierarchical-risk-parity/README.md) | [Notebook](topics/03-hierarchical-risk-parity/study.ipynb) |
| **4. Kelly growth allocation** | How much capital should an estimated edge receive? Derive expected log growth and study fractional exposure when probabilities are uncertain. | [Research note](topics/04-kelly-growth/README.md) | [Notebook](topics/04-kelly-growth/study.ipynb) |
| **5. Maximum diversification** | What changes when the objective is diversification rather than minimum variance? Compare the diversification ratio and resulting exposures. | [Research note](topics/05-maximum-diversification/README.md) | [Notebook](topics/05-maximum-diversification/study.ipynb) |
| **6. Sector momentum** | Should recent sector leadership persist? Build a relative-strength ranking, a trend gate, and an explicit delayed decision. | [Research note](topics/06-sector-momentum/README.md) | [Notebook](topics/06-sector-momentum/study.ipynb) |
| **7. Vigilant allocation** | Can weakening participation warn against risk? Combine weighted price momentum with breadth inside the risky universe. | [Research note](topics/07-vigilant-allocation/README.md) | [Notebook](topics/07-vigilant-allocation/study.ipynb) |
| **8. Defensive allocation** | Can a separate warning universe guide the risk budget? Distinguish canary signals from asset selection and defensive holdings. | [Research note](topics/08-defensive-allocation/README.md) | [Notebook](topics/08-defensive-allocation/study.ipynb) |
| **9. Sector reversal** | When might recent losers recover? Contrast a short-horizon contrarian ranking with momentum and consider turnover and persistent losses. | [Research note](topics/09-sector-reversal/README.md) | [Notebook](topics/09-sector-reversal/study.ipynb) |

For a first pass, compare **mean–variance**, **risk parity**, and **maximum diversification**: each changes the objective while holding the idea of a portfolio fixed. Then read **HRP** for a different use of dependence, **Kelly** for a different definition of success, and the four tactical chapters for decisions that change with market signals.

## How the allocation research is designed

### Separate portfolio construction from market timing

The construction study compares equal weight, inverse volatility, equal risk contribution (ERC), and HRP on the same eligible assets. It asks whether estimating individual risks and correlations improves the portfolio beyond a simple equal allocation. ERC balances estimated risk contributions; HRP divides risk across a hierarchy of correlated assets. Neither requires a forecast of each asset's expected return.

Tactical allocation asks a separate question: whether recent price information should change which assets are held or the amount of capital exposed to risk. The completed historical study includes one bounded defensive-momentum adaptation. The VAA and DAA chapters explain their respective breadth and canary ideas, but their worked examples are not full replications or additional winning backtests.

### Give every asset an economic role

| Asset | Exposure | Why it matters to the comparison |
|---|---|---|
| SPY | US equities | Equity growth and drawdown exposure |
| IEMG | Emerging-market equities | A second equity region with distinct risks, but substantial shared equity exposure |
| TLT | Long US Treasury bonds | Duration exposure whose diversification depends on the inflation/rate environment |
| GLD | Gold | A different source of market risk with time-varying correlations |
| SHY | Short US Treasury bonds | Low-volatility defensive exposure that still bears interest-rate risk |

The input sample runs from **2 July 2018 through 17 September 2026**. AGG supplies a separate **60% SPY / 40% AGG** reference. That portfolio provides familiar context; the same-universe equal-weight portfolio supplies the direct construction control. ETF selection is fixed and retrospective, and SHY is not interchangeable with risk-free cash.

### Ask whether lower risk comes from better diversification or less exposure

A strategy can look attractive by concentrating in short-duration bonds. For each estimated allocation, the study therefore adds an equal-weight control scaled to its **forecast** risk using information available before trading. The scaling is capped at 100%; unused capital remains in cash. This controls an important exposure difference while allowing realized risks to differ.

Risk estimates use the preceding **252 daily returns**. Portfolios rebalance monthly, with information ending before the execution close; new holdings first earn the next session's return. Existing weights drift between trades. Costs are **5 basis points per bought or sold dollar**, including entry, and cash earns an explicitly assumed zero return. These assumptions matter especially when a control holds substantial cash.

The common portfolio evaluation begins in August 2020. The main incremental comparison uses January 2025 onward, accompanied by dependence-aware uncertainty, lookback and covariance sensitivity, an additional execution delay, and a fixed range of trading costs. These are retrospective comparisons, not an untouched live test. [Read the full research design](docs/01-methods.md).

## What the completed ETF study shows

<!-- RESEARCH_RESULT:START -->
In January 2025–17 September 2026, HRP minus its prior-risk-scaled equal-weight control has a net annualized mean/volatility difference of **+0.649**, with paired 95% block interval **[-0.649, +1.954]**. This does not establish incremental risk-adjusted value under this universe, zero cash interest and cost assumptions.
<!-- RESEARCH_RESULT:END -->

![Incremental risk-adjusted comparison](research/figures/incremental.png)

The interpretation depends on the holdings as well as the headline statistic. HRP allocates heavily to SHY; lower volatility alone is therefore not evidence that its hierarchy predicts markets better. The risk-scaled comparison and sensitivity results help separate that exposure choice from the contribution of portfolio construction. The full report shows net wealth, drawdowns, weights, turnover, costs and uncertainty, including unfavorable results.

**Continue to the [research findings](docs/02-results.md) or the [complete executed study](study.ipynb).** The worked topic notebooks explain mechanisms; this report supplies the historical evidence for the bounded primary experiment.

## Research materials

[Experimental protocol](research/PROTOCOL.md) · [Data and literature](research/SOURCES.md) · [Further research questions](research/RESEARCH_AGENDA.md) · [Reproduce the calculations](docs/reproduction.md)

The original notebooks are preserved on `old`. These renewed chapters replace their public teaching path without inheriting unverified performance claims. Data vintage, cash assumptions, surviving-ETF selection and execution limits are documented with the study. See the [original-method audit](research/AUDIT.md) and [publication notes](PUBLICATION.md) for provenance and historical material.
