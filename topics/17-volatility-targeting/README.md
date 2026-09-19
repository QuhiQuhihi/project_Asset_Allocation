# Volatility targeting: a risk budget is a forecast, not a promise

[Open the worked notebook](study.ipynb) · [Project overview](../../README.md)

A portfolio can keep its asset mix unchanged while changing how much total capital it puts at risk. Volatility targeting applies a risk budget to a risky sleeve and leaves the remainder in cash. It is useful to separate this decision from selecting assets: an excellent asset mix can still carry too much risk when its covariance structure changes.

## Translate predicted risk into an exposure

This chapter uses one risky sleeve, a fixed 10% annual volatility budget and a 100% exposure cap:

$$w_t=\min\left(1,\frac{0.10}{\widehat\sigma_t}\right).$$

The estimate is the sample standard deviation of 20 prior daily returns, annualized by $\sqrt{252}$. There is one complete trading-period delay. In zero-based indexing, the position earning return `r[t]` uses `r[t-21:t-1]`: the latest return it can observe is `r[t-2]`. A return observed at one close can change the trade at the next close and the return earned after that. Forecasts with insufficient history hold cash; a zero estimate uses the cap. No full-sample scaling constant or realized-risk matching enters the target.

The cash sleeve earns a hypothetical 3% effective annual rate. The fixed comparator rebalances to 60% risky and 40% cash daily; it is a declared allocation, not a retrospectively risk-matched control. Both begin with 100 in cash, pay 5 basis points per risky dollar bought or sold, permit holdings to drift between closes, and omit terminal liquidation. Cash transfers carry no fee. The implementation solves the fee and post-fee target together, so purchases cannot spend the capital already used to pay costs.

## Follow the forecast through a shock and reversal

The original constructed path supplies 61 warm-up observations and 180 investment periods: calm conditions, an abrupt loss followed by stress, and a sharp rebound followed by quieter returns. It represents no particular market or historical episode. All observations and rule settings are visible; these scenarios demonstrate failure modes rather than estimate their probability.

The notebook displays the forecast, executed weight, wealth, trailing realized volatility and turnover. The 10% rule realizes **16.97%** annualized volatility in this path, versus **16.10%** for the fixed allocation. It enters the first loss with high exposure because prior observations are calm, then owns less of the abrupt rebound. Its higher turnover also incurs more costs. Those are outcomes of this declared path, not evidence that one rule is universally preferable. The rolling volatility panel includes the discrete jumps; the target line is a forecast budget rather than an asserted bound.

## Research questions and checks

A useful follow-up varies forecast window, update frequency, execution delay and cap while retaining every result in a trial ledger. It should include quiet-to-crisis jumps, persistent stress and rapid recovery. Comparing after-cost returns requires controls that separate average exposure from timing skill. A smoother estimator or trading band may reduce turnover but creates another research choice that needs validation.

The notebook checks a hand-calculated purchase with fees and remunerated cash, reconciles portfolio balances, verifies the cap, and perturbs future observations to confirm that earlier weights do not change. The [module](../../research/dynamic_exposure.py) shares the same dollar accounting with [CPPI](../18-cppi/README.md); their allocation signals are different.

## Source and scope

[Moreira and Muir, *Volatility-Managed Portfolios*](https://law.yale.edu/sites/default/files/area/workshop/leo/leo17_moreira.pdf), especially equation (1), studies inverse-**variance** scaling of excess returns. This chapter's bounded inverse-**standard-deviation** target is a distinct, original teaching example. It does not reproduce the paper's empirical results or normalization. The formula, cash convention, trade ledger and constructed scenario are specified here so that readers can inspect the actual implemented rule.
