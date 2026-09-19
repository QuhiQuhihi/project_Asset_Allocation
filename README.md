# Robust asset allocation: designing portfolios that survive estimation error

A portfolio should have an economic reason to exist and remain useful when its estimated inputs are wrong. This project studies **robust asset allocation**: how to construct exposures, limit sensitivity to noisy estimates, and evaluate a strategy without mistaking repeated experimentation for investment skill.

The research direction draws on **Marcos López de Prado's work on financial machine learning and backtest overfitting**, alongside portfolio theory and covariance estimation. The central idea is to examine the whole decision process: the universe, estimated risks, constraints, validation periods, attempted alternatives and implementation costs. HRP, shrinkage, purging and selection diagnostics address different failure modes; none makes a strategy immune to overfitting.

## Start with robust research design

| Question | What the worked example lets you inspect | Read | Explore |
|---|---|---|---|
| **How stable are the allocations?** | Compare equal weight, sample minimum variance, shrunk capped portfolios, HRP and a finite-scenario allocation. Refit under training-sample perturbations and evaluate a constructed correlation shift. | [Estimation risk](topics/12-estimation-risk/README.md) | [Notebook](topics/12-estimation-risk/study.ipynb) |
| **Has validation seen information it should not know?** | Track overlapping forward-return labels, purge intersecting training events and apply a stated embargo. Distinguish this research split from past-only walk-forward evaluation. | [Purged validation](topics/10-purged-validation/README.md) | [Notebook](topics/10-purged-validation/study.ipynb) |
| **How much did searching inflate the result?** | Select among a fully recorded constructed strategy library; inspect CSCV/PBO, probabilistic Sharpe and deflated Sharpe under explicit assumptions. | [Backtest selection](topics/11-backtest-selection/README.md) | [Notebook](topics/11-backtest-selection/study.ipynb) |

Start with **estimation risk** to see how research choices become portfolio weights, then follow the two validation chapters to examine the evidence supporting those choices. The [robust allocation research design](docs/robust-allocation.md) connects the examples to a complete strategy: economic objective, bounded candidates, chronological estimation, implementation costs and a genuinely future evaluation period.

## Explore the allocation ideas

These nine chapters supply the portfolio objectives and investment rules that robust research must evaluate. Each introduces the economic mechanism and links to a worked notebook with explicit illustrative inputs. Read them as candidates to understand and challenge, rather than a menu of backtested winners.

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

The first five chapters examine how objectives and dependence estimates determine weights. The four tactical chapters examine when signals should change asset selection or risk exposure. In each case ask which estimated quantity drives the decision, how that decision changes under plausible errors, and which simple allocation supplies a fair comparison.

## A historical case for applying the discipline

The [ETF research report](study.ipynb) compares equal weight, inverse volatility, ERC and HRP on **SPY, IEMG, TLT, GLD and SHY**, with a separate defensive-momentum adaptation and SPY/AGG 60/40 context. The pinned adjusted-price vintage spans **2 July 2018–17 September 2026**. Monthly decisions use earlier information, weights drift between trades, and costs apply to both buys and sells.

This case illustrates why exposure controls matter: a portfolio can reduce volatility by owning more short-duration bonds or cash. Prior-risk-scaled equal weight provides a more informative construction comparison than a headline return alone. The [findings and sensitivities](docs/02-results.md) retain uncertainty, adverse periods and unfavorable outcomes; [methods](docs/01-methods.md) explain the accounting and cash assumptions.

The history has already been inspected. It is **retrospective evidence**, and its intervals do not correct for the full history of research choices. The new constructed robustness examples are separate experiments; they do not turn this ETF record into an untouched holdout or provide an empirical deflated Sharpe ratio for it.

## Research materials

[Robust allocation design](docs/robust-allocation.md) · [Dated ETF protocol](research/PROTOCOL.md) · [Sources and attribution](research/SOURCES.md) · [Next research questions](research/RESEARCH_AGENDA.md) · [Reproduce the calculations](docs/reproduction.md)

The original notebooks are preserved on `old`. The [original-method audit](research/AUDIT.md) and [publication notes](PUBLICATION.md) document provenance and the treatment of historical material. The research aim is a defensible allocation decision with visible limits, rather than the strongest result available from a reused sample.
