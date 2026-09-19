# Factor risk allocation: diversify the economic exposures

[Open the worked notebook](study.ipynb) · [Explore the allocation ideas](../../README.md)

Four asset labels do not necessarily represent four independent sources of risk. Equities, credit and other growth-sensitive assets can react to the same economic shock. This chapter looks through capital weights to factor exposures, then implements an explicit economic exposure policy with constrained asset weights.

## Capital, exposure and risk are different objects

The constructed annual excess-return model is

$$r=Bf+\epsilon,\qquad \Sigma=BFB^\top+D,\qquad z=B^\top w.$$

Here $B$ maps asset weights $w$ into factor exposures $z$; $F$ is the factor covariance and $D$ is the residual covariance. Residuals are uncorrelated with the factors. The example uses two constructed return proxies interpreted as growth-sensitive and duration risk, with annual volatilities of 16% and 7%, correlation −0.25, and four independent asset residuals. These are assumed economic loadings, not estimated exposures to observed GDP or yield changes.

Equal capital across Equity A, Equity B, Credit and Duration produces **93.1% of total portfolio variance from the Growth factor**. The notebook then imposes a policy exposure target of 0.40 Growth and 0.90 Duration. Those units are betas to the declared return factors; they are not percentages of wealth or risk.

## Implement the policy without changing its meaning

The allocation minimizes residual variance subject to exact exposures, full funding, nonnegative positions and a 65% asset cap:

$$\min_w w^\top Dw\quad\text{subject to}\quad B^\top w=z^*,\quad \mathbf1^\top w=1,\quad 0\le w_i\le0.65.$$

At fixed exposures, factor variance is constant, so this also minimizes total variance within the feasible policy set. An infeasible request raises an explicit error. The result puts **41.7% of capital in Credit and 50.0% in Duration**. It deliberately accepts greater asset concentration to change the economic exposures. This is exposure targeting, not a factor risk-parity optimizer.

For correlated factors, signed variance contributions are $c_j=z_j(Fz)_j$; the residual contributes $w^\top Dw$. These sum to total variance. Cross-covariance is retained and shared between the relevant factor components. A hedging factor can have a negative contribution, and changing the factor basis changes the attribution. The notebook checks a small example with contributions 0.91 and −0.08 rather than silently clipping the negative component.

The policy's variance shares are 48.8% Growth, 46.8% Duration and 4.4% residual. This near balance follows from the specified exposures and covariance; it is not evidence that the policy solved equal risk budgets. Its lower model volatility is also not a return advantage or a matched-risk performance comparison.

## Challenge the model before treating it as diversification

Two fixed stresses hold portfolio weights constant: increase factor correlation to +0.50, or increase growth loadings on Credit and Duration. Correlation changes risk without changing exposure; loading error changes the economic policy without any trade. These are declared scenarios, not confidence bounds.

A factor model can organize a large universe with fewer inputs, but factor selection, proxy construction and exposure estimation can still overfit. A real implementation needs training-only estimates, residual-correlation checks, turnover and trading costs, and stable economic definitions across evaluation periods. This chapter supplies no historical return premium or optimized investor policy.

Independent checks reconstruct variance through the full asset covariance, recover a hand-calculated residual-risk optimum, preserve negative contributions and reject impossible exposures. Compare [asset risk parity](../02-risk-parity/README.md) for asset-level risk budgets and [estimation risk](../12-estimation-risk/README.md) for input stability.

## Sources

[William Sharpe (2001), *Budgeting and Monitoring the Risk of Defined Benefit Pension Funds*](https://web.stanford.edu/~wfsharpe/art/q2001/q2001.htm) supplies the factor-model and economic risk-budgeting context. [Ronen Israel and Adrienne Ross, *Measuring Portfolio Factor Exposures: A Practical Guide*](https://images.aqr.com/-/media/AQR/Documents/Insights/Trade-Publications/Measuring-Portfolio-Factor-Exposures-A-Practical-Guide.pdf) discusses factor definitions and implementation differences. The allocation problem, constructed inputs, tests and figures here are original.
