# Black–Litterman: turning explicit views into measured portfolio tilts

[Open the worked notebook](study.ipynb) · [Project overview](../../README.md)

An allocation process often has a strategic portfolio and a small number of investment views, rather than a reliable forecast for every asset. Black–Litterman supplies a disciplined way to connect those views to portfolio weights. Its practical question is how strongly a portfolio should move away from its starting point when the views themselves are uncertain.

## Start from a declared reference portfolio

This chapter constructs four exposures—global equity, emerging equity, duration and gold—with annual conditional return covariance $\Sigma$. A reference mix of 45%, 15%, 30% and 10% supplies reverse-optimized excess returns $\pi=\delta\Sigma w_0$, with risk aversion $\delta=3$. These inputs are original teaching assumptions. The reference weights are not observed market capitalization weights, and the implied returns are not evidence of a real market equilibrium.

The latent expected return has prior covariance $\tau\Sigma$. Two views are explicit: emerging equity should exceed global equity by 2.5 percentage points, and gold should earn 3.5% excess return. Rows of $P$ describe the exposures; $Q$ contains these forecasts. Diagonal $\Omega$ assigns view-error standard deviations of 1.5 and 2.5 percentage points. These are assumptions about errors in expected-return views, not asset return volatility or calibrated confidence percentages.

The update is

$$\mu=\pi+\tau\Sigma P^\top(P\tau\Sigma P^\top+\Omega)^{-1}(Q-P\pi).$$

If $M$ denotes the remaining uncertainty about the mean, the predictive covariance of a future return is $\Sigma+M$ under the stated independent Gaussian return-noise model. The notebook keeps these two covariance objects separate. Even with no views, $M=\tau\Sigma$; uncertainty does not vanish.

## Convert beliefs into an implementable decision

A long-only, fully invested allocation maximizes $w^\top\mu-\delta w^\top(\Sigma+M)w/2$, with a 60% asset cap. The notebook compares reference, no-view predictive and two-view predictive weights. The no-view predictive allocation need not equal the reference: reverse optimization used $\Sigma$, while the decision now includes mean uncertainty. An independent check recovers the reference when the same original $\Sigma$ is used on both sides.

The resulting targets describe one decision horizon. An empirical strategy would timestamp the reference, views, covariance and uncertainty settings before each trade, then hold the targets over the next declared period. Returns and costs in that next period cannot set the current views or confidence. This chapter reports target weights and belief sensitivity; it has no investment performance series.

## Test confidence before trusting a tilt

The notebook retains four view-error scales and five prior-uncertainty settings. Smaller view error permits larger departures from the prior; larger $\tau$ permits more updating when $\Omega$ stays fixed. A separate identity shows why scaling $\Omega$ in proportion to $\tau$ makes posterior means insensitive to $\tau$, while mean uncertainty still changes.

Regularizing forecasts does not protect a researcher who selects profitable-looking views, confidence levels, or reference portfolios after inspecting a backtest. Keep the view-generation rule and trial record explicit, examine sensitivity, and evaluate any learned views with [appropriate validation](../10-purged-validation/README.md). The [estimation-risk chapter](../12-estimation-risk/README.md) addresses instability in covariance inputs. Scalar Bayes, precision-form, no-view and no-innovation identities independently check this implementation.

## Sources

[Black and Litterman, *Global Portfolio Optimization* (1992)](https://people.duke.edu/~charvey/Teaching/BA453_2005/blacklitterman.pdf) motivates equilibrium-based priors and investor views. [PyPortfolioOpt's official Black–Litterman documentation](https://pyportfolioopt.readthedocs.io/en/latest/BlackLitterman.html) provides a transparent formula reference, including the predictive covariance convention. The notebook implements the algebra directly with NumPy and SciPy; PyPortfolioOpt is not a dependency. The exposure assumptions, sensitivity design and figures are original to this project.
