# Mean–variance allocation: what is a return forecast worth?

Mean–variance allocation makes a portfolio's tradeoff explicit: how much estimated return is worth an additional unit of risk? The method connects individual assets through their covariance, so an asset with a modest expected return can still be valuable if it diversifies the rest of the portfolio.

## The portfolio decision

Let $w$ be portfolio weights, $\mu$ expected simple returns and $\Sigma$ their covariance at the same horizon. For a required return $m$, the chapter solves

$$\min_w w^\top\Sigma w\quad\text{subject to}\quad w^\top\mu=m,\quad\mathbf1^\top w=1,\quad w\geq0.$$

Repeating this decision across attainable returns traces a frontier. Its efficient portion starts at the global minimum-variance portfolio: below that portfolio's expected return, another feasible mix can offer more estimated return with no more variance. No leverage, short positions or risk-free borrowing are permitted here. A frontier is conditional on the assumptions supplied to it, not a forecast of achieved investment performance.

## What the notebook investigates

The example supplies three **constructed asset assumptions**, with annual expected returns of 8%, 4.5% and 3%, annual volatilities of 18%, 8% and 2.5%, and an explicit positive-definite correlation matrix. It solves the long-only frontier, displays portfolio weights at selected objectives and checks every budget and return constraint.

A second exercise maximizes $w^\top\mu-\frac\lambda2w^\top\Sigma w$ for a fixed risk penalty, then changes just one expected return by one percentage point. The covariance and constraints stay fixed. The change in weights isolates sensitivity to the return estimate; it is not a second historical strategy result. A separate diagonal-covariance example checks minimum-variance weights against the inverse-variance closed form.

## What to look for

Increasing the target return moves the feasible portfolios toward assets assigned higher expected returns and can concentrate capital in the asset assigned the largest expected return. A stable optimizer cannot make an uncertain mean estimate reliable. Real research therefore needs training-only estimates, defensible constraints, shrinkage or other stabilization, and evaluation against a simple allocation under the same timing and costs.

The project's [ETF study](../../study.ipynb) deliberately tests risk-based construction without adding a contest over noisy mean forecasts. This chapter restores mean–variance as a substantive teaching topic; it does not rehabilitate the original notebook's historical results. Its expected-return and covariance assumptions are original numerical illustrations, not current market estimates.

## Further reading

[Harry Markowitz, *Foundations of Portfolio Theory*](https://www.nobelprize.org/uploads/2018/06/markowitz-lecture.pdf) develops the portfolio-choice framework. The [SciPy constrained minimization reference](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html) documents the numerical solver used in the worked example.

[Open the worked notebook](study.ipynb) · [Return to all strategies](../../README.md)
