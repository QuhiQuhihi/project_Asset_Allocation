# Expected-shortfall allocation: optimize the losses that populate the tail

[Open the worked notebook](study.ipynb) · [Project overview](../../README.md)

Variance treats positive and negative departures from a mean symmetrically. An allocator may instead ask how severe losses are in the worst part of a stated scenario distribution. Expected shortfall (ES), also called conditional value-at-risk in this formulation, makes that objective explicit and supports a transparent linear program.

## Give the loss objective a concrete meaning

For portfolio weights $w$, a scenario return vector $r_s$ produces loss $L_s=-r_s^\top w$. With probabilities $p_s$ and confidence level $\alpha$, solve

$$\min_{w,\eta,u}\;\eta+\frac{1}{1-\alpha}\sum_s p_su_s,$$

subject to $u_s\ge-r_s^\top w-\eta$, $u_s\ge0$, $\mathbf1^\top w=1$, $0\le w_i\le0.60$, and $\sum_s p_sr_s^\top w\ge0.003$. The threshold $\eta$ is unrestricted: a portfolio profitable in every scenario can have negative ES. A minimizing threshold is not necessarily the lower empirical VaR when a discrete distribution has a gap.

The notebook sets $\alpha=90\%$ and models one month. Its twelve original outcomes describe growth, quiet markets, equity/credit shocks, inflation stress, rate repricing, trend whipsaw and rebound. Four illustrative sleeves are equity, credit, duration and trend. These are hand-specified return payoffs and probability weights, not historical observations, calibrated probabilities, or a claim that a tradable trend strategy supplies these payoffs. The 0.3% monthly mean floor is a modeling constraint, not a return promise.

## Compare risk objectives on the same information

Minimum ES and minimum variance receive the same scenarios, probabilities, 60% cap and mean-return floor. The variance comparator uses the probability-weighted population covariance of that same finite distribution. Equal weight is a transparent reference. This isolates what the objectives emphasize within the declared decision set, while acknowledging that the constraints can bind differently.

Both optimized portfolios must be evaluated on the same distribution; allowing each rule its own favorable scenarios would defeat the comparison. The notebook therefore reports common nominal 90% ES, nominal volatility, mean and individual scenario returns. Their differences describe one constructed decision, not evidence that ES allocation outperforms in financial markets.

## Make the discrete tail exact

For finite scenarios, ES averages exactly the worst $1-\alpha$ probability mass. If the tail boundary cuts through an observation's probability, only the needed fraction belongs to the tail. Averaging every loss at or above a sample quantile gives the wrong denominator when there are ties. An independent sorted-tail calculation checks the LP objective, and the notebook verifies a two-asset example whose unique optimal weights are 50/50.

## Stress the assumptions that determine the answer

The chapter retains 80%, 90% and 95% ES rules and half/double probabilities for the three declared crash outcomes. It then applies a separate joint-loss stress to every frozen target. This additional stress has no assigned probability and never enters fitting. Report its portfolio loss as a what-if scenario, not as estimated ES or a forecast. A low nominal ES cannot protect against a loss absent from the model.

An implementable research rule would freeze the scenario-generation process, confidence level, constraints and trade timing before the next holding period, with liquidity and costs added explicitly. Rare-event estimation, scenario omission and confidence-level selection can all produce overfitting. Compare [estimation risk](../12-estimation-risk/README.md) and retain alternative outcomes rather than selecting the most favorable chart.

## Sources

[Rockafellar and Uryasev, *Optimization of Conditional Value-at-Risk*](https://sites.math.washington.edu/~rtr/papers/rtr179-CVaR1.pdf) provides the auxiliary-variable optimization formulation. Their [general loss distributions paper](https://sites.math.washington.edu/~rtr/papers/rtr187-CVaR2.pdf) addresses finite probability mass at the tail boundary. [SciPy's HiGHS documentation](https://docs.scipy.org/doc/scipy/reference/optimize.linprog-highs.html) specifies the linear-program interface. The scenario design, stress comparison, checks and figures are original to this project.
