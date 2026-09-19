# Risk parity: equal capital is not equal risk

A portfolio split equally between stocks and short bonds assigns equal dollars to exposures with very different volatility. Risk parity starts from another question: how should each holding contribute to the variability of the portfolio as a whole?

## Three meanings of balance

Equal weight sets $w_i=1/N$. Inverse volatility sets $w_i\propto1/\sigma_i$, reducing capital in individually volatile assets. Equal risk contribution (ERC) also accounts for covariance. If portfolio volatility is $\sigma_p=\sqrt{w^\top\Sigma w}$, Euler decomposition gives the component contribution

$$RC_i=w_i\frac{(\Sigma w)_i}{\sigma_p},\qquad \sum_i RC_i=\sigma_p.$$

The fraction $w_i(\Sigma w)_i/(w^\top\Sigma w)$ is the share of portfolio variance used for the comparisons. ERC makes these fractions equal. Inverse volatility and ERC coincide for independent assets; arbitrary correlations break that equivalence.

## The construction in this project

The maintained ERC routine solves a positive risk-budget problem, $\frac12x^\top\Sigma x-\sum_i\log x_i$, and normalizes $x$ into weights. Its first-order conditions imply equal unnormalized component contributions. The routine checks the final risk-budget residual instead of accepting an optimizer's success flag alone. The historical strategy uses a tiny covariance regularization and reports its predeclared fallback when a fit fails.

The notebook supplies three original annual volatility and correlation assumptions. It places equal-weight, inverse-volatility and ERC weights alongside their resulting risk shares, then independently checks the diagonal-covariance case. No historical returns, return forecasts, leverage or transaction costs enter this single-period illustration.

## The economic tradeoff

Balancing estimated variance does not balance inflation risk, liquidity risk, credit risk, or the size of a possible tail loss. It also does not fix a desired return. Without leverage, a portfolio that equalizes risk may allocate much of its capital to low-volatility bonds. In a common shock, correlations can move sharply and yesterday's equal risk shares need not survive.

The [empirical comparison](../../docs/02-results.md) therefore reports holdings, drift, turnover and risk-scaled equal-weight controls in addition to volatility. Its cash assumption matters: scaling down a control and assuming zero cash interest is different from holding a short-bond ETF. ERC remains a way to organize a risk budget, whose economic value has to be evaluated separately.

## Further reading

[Maillard, Roncalli and Teïletche, *On the Properties of Equally-Weighted Risk Contributions Portfolios*](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1271972) provides the original methodological context. Compare [maximum diversification](../05-maximum-diversification/README.md), which optimizes a different function of risk.

[Open the worked notebook](study.ipynb) · [Return to all strategies](../../README.md)
