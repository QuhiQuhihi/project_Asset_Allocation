# Designing a robust allocation strategy

[Project overview](../README.md) · [Estimation example](../topics/12-estimation-risk/study.ipynb) · [Validation example](../topics/10-purged-validation/study.ipynb) · [Selection example](../topics/11-backtest-selection/study.ipynb)

The research question is: **does an allocation decision remain useful after accounting for input uncertainty, information timing, strategy selection and implementation costs?** A high return on an inspected history is an observation to explain. The desired contribution is a decision rule whose economic purpose and failure conditions are clear.

The framework connects economic reasoning, portfolio construction, information boundaries and explicit treatment of strategy selection. The project develops original worked examples and a separately documented historical case to examine those decisions. Combining well-known methods does not by itself establish an investable strategy; each method needs an appropriate comparison and evidence for its intended use.

## 1. Define the economic job and the candidate family

Separate strategic construction from tactical decisions. A minimum-variance allocation seeks low portfolio variance; ERC balances estimated contributions to risk; HRP organizes dependence hierarchically; Kelly optimizes expected log growth. A momentum or canary rule changes exposure in response to signals. These objectives should not be judged solely by whichever statistic happens to look strongest.

For a new empirical study, record the eligible instruments, economic roles, objective, constraints, rebalancing clock and primary comparison before evaluating candidates. Each change to universe, lookback, signal, covariance estimator, linkage, cap, risk target or cost model belongs in the research record, including abandoned variants. A narrow family can still be overfit if the researcher repeatedly changes the family after observing results.

The fifteen allocation chapters expose these choices. They are illustrative mechanisms with different objectives and controls, not a common performance contest.

The expanded collection makes six additional sources of model risk concrete:

| Allocation idea | The decision it changes | What a robust study must challenge |
|---|---|---|
| [Black–Litterman](../topics/13-black-litterman/README.md) | How a prior and investor views determine expected returns and weights | Confidence in a view, dependence among views, prior calibration, and reusing the same evidence in both prior and views |
| [Expected shortfall](../topics/14-expected-shortfall/README.md) | How severe tail losses enter the objective | Omitted scenarios, their probabilities, tail level, return constraints and sensitivity of the optimized weights |
| [Factor risk](../topics/15-factor-risk-allocation/README.md) | Which common economic exposures the holdings should deliver | Loading errors, correlated factors, residual risk and whether the assets can achieve the desired exposures |
| [Liability-driven allocation](../topics/16-liability-driven-allocation/README.md) | How assets support dated obligations | Funding requirements, cash-flow uncertainty, nonparallel rate changes, convexity, inflation and liquidity |
| [Volatility targeting](../topics/17-volatility-targeting/README.md) | How much capital belongs in a risky sleeve | Forecast delay, cash returns, exposure caps, transaction costs and risk changes faster than rebalancing |
| [CPPI](../topics/18-cppi/README.md) | How the cushion above a floor sets risky exposure | Multiplier choice, discrete price gaps, fees, floor funding and loss of participation after the cushion disappears |

These concerns determine the example's comparison. A liability hedge should be judged against its obligation; a tail-loss allocator against its declared loss distribution; an exposure overlay against its stated risk and implementation rule. None should inherit a claim of robustness merely from its name or from outperforming an unrelated benchmark.

## 2. Limit how much noisy estimates can change the decision

Expected returns are difficult to estimate; avoiding them removes one source of error but leaves uncertainty in volatilities, correlations and the universe itself. Shrinkage deliberately trades some fit to the sample for a better-conditioned risk estimate. Exposure caps restrict concentration. Hierarchies replace a direct covariance inversion with clustering and recursive allocation, while introducing dependence on distance, linkage and ordering decisions.

The [estimation-risk chapter](../topics/12-estimation-risk/README.md) compares five fixed rules on constructed data. Its scenario allocation minimizes the worst variance across a declared finite set of training-derived covariance matrices. That protects against the specified scenarios, not every future distribution. It reports weight perturbations, concentration and risk under a separately constructed correlation shift. The cap and scenario transformations are visible assumptions, not parameters chosen by the resulting test performance.

Bootstrap complete cross-asset observations and refit the whole decision to measure local estimation sensitivity. Under dependent market observations, a suitable block scheme matters. Stable weights can still load on a common economic risk; low weight variation alone does not establish diversification or return quality.

## 3. Match validation to the information structure

For a trading simulation, maintain a chronological chain: estimate with available training data, freeze the decision, execute after its information cutoff, then measure returns actually earned by those holdings. Any learned scaling, covariance, feature selection or hyperparameter choice belongs inside the appropriate training stage. If tuning is necessary, an inner training/validation process chooses settings; an outer evaluation assesses the resulting selection process.

A predictive tactical model may label an observation by its next 21-session return. Neighboring labels then share future price changes. Splitting rows without checking these intervals can place overlapping outcomes in training and evaluation. **Purging** removes training labels that intersect test label intervals. An explicitly sized **embargo** removes additional nearby observations where the design calls for it. Neither repairs future-aware features, revised economic releases or a universe selected using later survival.

The [purged-validation example](../topics/10-purged-validation/README.md) makes these intervals inspectable. It is a split-mechanics exercise, not an implemented nested ML allocator or a complete combinatorial purged cross-validation system. A split that includes training observations after a test block is a research resampling device; it is not an executable historical trading path. Walk-forward evaluation remains the chronological deployment check. Fixed covariance allocation without forward-return labels does not automatically need purged supervised-learning folds.

## 4. Evaluate the search, not just its selected winner

If many variants are inspected, the reported maximum inherits selection bias. A full candidate-return matrix permits a **combinatorially symmetric cross-validation (CSCV)** exercise: choose the best in-sample candidate in each block partition and inspect its rank on the complementary observations. The resulting PBO diagnostic summarizes how often that selected candidate ranks below the specified out-of-sample threshold within this resampling experiment. It depends on the candidate library, partition and metric; it is not a posterior probability that a trading strategy is false.

The probabilistic Sharpe ratio addresses uncertainty relative to a benchmark under stated return-distribution assumptions. The original deflated Sharpe approach adjusts the benchmark for selection using an expected maximum and an assumed number of independent trials. Per-period Sharpe units, sample size, skewness, non-excess kurtosis and trial dependence matter. A trial count made up after the search cannot reconstruct missing experiments.

The [selection chapter](../topics/11-backtest-selection/README.md) implements these calculations on a complete constructed null library and shows an independent constructed evaluation. The IID design makes the assumptions visible. Real financial returns may require serial-dependence adjustments and more careful treatment of effective independent trials. CSCV/PBO, DSR and chronological testing answer related but distinct questions. They do not convert repeated inspection into new information.

## 5. Compare decisions after exposure and implementation costs

Keep equal weight as a direct same-universe control. Add an exposure-matched control where the proposed rule materially changes estimated risk or cash holdings. Freeze the matching rule using prior information; do not retrospectively scale portfolios to identical realized volatility. Familiar allocations with different assets can provide context without becoming equivalent construction controls.

Track information dates, execution dates, drifting weights, buys, sells, cash and costs. A marginal improvement can disappear when holdings are traded. Assess drawdown, concentration, turnover and adverse regimes alongside the predeclared primary metric. A sensitivity table should retain every variant and never silently replace the primary with its best row.

The [historical ETF case](01-methods.md) implements these accounting and comparison principles using the refreshed 17 September 2026 price vintage. Its paired block intervals condition on fitted return paths; they neither refit the full research process nor correct for all selection. Its zero-interest cash assumption and surviving-ETF universe remain limitations. No unrecorded empirical PBO or DSR is inferred from that study.

## What is implemented and what remains a new experiment

| Component | Available evidence | Boundary |
|---|---|---|
| Allocation objectives, views, liabilities and tactical rules | Fifteen worked allocation chapters | Constructed illustrations with distinct objectives; no universal ranking or complete published-strategy replications |
| Estimation sensitivity and finite-scenario allocation | Five rules, full bootstrap refits, shifted test distribution and independent numerical checks | Constructed world; no live allocation or empirical performance claim |
| Purging and embargo | Explicit label intervals, split diagnostics and overlap checks | Split mechanics; no nested predictive strategy or full CPCV path assembly |
| Search-aware evaluation | Complete synthetic library, CSCV/PBO, PSR/DSR and independent test | Assumption-dependent illustration; no selection-corrected claim about the ETF record |
| Historical portfolio accounting | Same-universe controls, delayed execution, drifting holdings, costs and sensitivity | Reused history with revised adjusted prices; not untouched evidence |
| Future validation | Defined in the [research agenda](../research/RESEARCH_AGENDA.md) | Not yet collected or evaluated |

## Primary references

- [López de Prado (2016), Building Diversified Portfolios that Outperform Out-of-Sample](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2708678): HRP.
- [López de Prado, Advances in Financial Machine Learning, publisher page](https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086): financial ML validation and research design. The worked split is an original implementation, not a reproduction of book text.
- [Bailey, Borwein, López de Prado and Zhu, The Probability of Backtest Overfitting](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf): CSCV/PBO.
- [Bailey and López de Prado, The Deflated Sharpe Ratio](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf): the original selection-adjusted Sharpe methodology.
- [Scikit-learn's Ledoit–Wolf reference](https://scikit-learn.org/stable/modules/generated/sklearn.covariance.LedoitWolf.html): the identity-target estimator used here and its original 2004 paper.
