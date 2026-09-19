# Maximum diversification: optimize the diversification ratio

Maximum diversification distinguishes the sum of individual risk exposures from the risk that remains after they are combined. Its objective is the diversification ratio: the weighted average of individual volatilities divided by portfolio volatility.

$$DR(w)=\frac{w^\top\sigma}{\sqrt{w^\top\Sigma w}}.$$

Here $\sigma_i=\sqrt{\Sigma_{ii}}$ and both numerator and denominator use the same horizon. The ratio is dimensionless. If all assets are perfectly positively correlated, their long-only combination has ratio one. With equal-volatility independent assets, equal weight has ratio $\sqrt N$.

## Why it differs from minimum variance

Minimum variance focuses on the denominator. It may concentrate in an individually safe asset even if that position offers little diversification. Maximum diversification also accounts for the individual volatility carried by the portfolio. An asset can receive weight because it provides a distinct source of risk rather than because its standalone variance is low.

ERC has yet another objective: balancing each asset's contribution to total portfolio risk. The three rules can agree in special symmetric cases, but they need not agree for realistic correlations and heterogeneous volatilities. Comparing their weight vectors is more informative than labeling all three simply “risk based.”

## The worked experiment

The notebook supplies three constructed annual volatilities and a positive-definite correlation matrix. It finds long-only, fully invested portfolios for maximum diversification and minimum variance, and compares them with inverse volatility and ERC. A table shows the diversification ratio, annual volatility and concentration of each allocation. A plot makes the different capital budgets visible.

For the unconstrained problem, an interior solution is proportional to $\Sigma^{-1}\sigma$. The notebook checks this expression where it is nonnegative and therefore feasible. It independently verifies the equal-volatility, independent-asset limiting case. Numerical optimizer success alone is not the validation.

## What to investigate in an empirical study

A higher estimated diversification ratio does not imply a higher expected return, safer tail exposure, or a smaller drawdown. Correlation estimates and changing volatilities influence both sides of the ratio, and rebalancing can cost more than a small estimated advantage is worth. Practical constraints may prevent an interior solution and must be included in the optimization rather than applied through arbitrary clipping afterward.

The project's completed historical contest focuses on a bounded set of allocation estimators. This renewed chapter is an original numerical explanation of maximum diversification, not a new empirical winner added after observing the results. A future comparison should fix its estimation window, constraints, benchmark, costs and incremental endpoint before evaluating it.

[Yves Choueifaty, *Towards Maximum Diversification*](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4063676) supplies the methodological reference. Compare [risk parity](../02-risk-parity/README.md) and [mean–variance allocation](../01-mean-variance/README.md) for the different objectives.

[Open the worked notebook](study.ipynb) · [Return to all strategies](../../README.md)
