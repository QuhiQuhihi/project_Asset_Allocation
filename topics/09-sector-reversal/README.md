# Sector reversal: recent losers and long-term losers are different bets

Reversal asks whether a recent price move partly unwinds. A short-horizon loser strategy can express a temporary dislocation hypothesis; buying sectors that have underperformed for a year can instead load on persistent distress or a different economic cycle. Reversing the sort order of a momentum signal does not establish that the same horizon should work in reverse.

[Open the worked notebook](study.ipynb) · [Back to the research collection](../../README.md)

## Strategy design

The original `08_sector_rotation_with_reverse_momentum.ipynb` sorted twelve-month scores ascending to select laggards, while some of its prose still described the winner strategy. This chapter keeps the twelve-month loser rule visible and places a one-month reversal hypothesis beside it. That comparison makes the research question explicit rather than treating “reverse momentum” as one universal strategy.

Both rules are long-only sector baskets. At information month $t$, the short-horizon strategy selects the two lowest one-month price returns; the long-horizon comparison selects the two lowest twelve-month returns. Each chosen sector receives 50%. A twelve-month winner basket shows whether the shorter reversal rule can even overlap with conventional momentum. The construction uses price ratios and no external forecasts, leverage or short positions.

The experiment holds each selected basket for one subsequent monthly interval after an explicit execution delay. A signal observed at the month-12 close executes at month 13 and first owns the return ending at month 14. Entry and exit each cost ten basis points of traded notional. This coarse delay is intentional: it makes the distinction between a signal and an immediately tradable price visible. A future daily-data study would need a more realistic calendar and fill model.

## What the notebook shows

Six constructed sector histories produce different short- and long-horizon rankings. Technology and Financials are twelve-month leaders but the latest month's losers. Energy and Utilities are twelve-month laggards but have already risen in the latest month. The one-month loser basket therefore coincides with the annual winner basket and differs entirely from the annual loser basket.

Two alternative futures share exactly the same information set. A rebound gives the short-horizon loser basket a 5% gross return; continuation gives it a 5% gross loss. Neither future can alter the signal. The notebook calculates shares, entry fees, liquidation proceeds and net returns for both baskets, then reconciles those cash flows with the direct weighted-return formula. These paired scenarios illustrate sensitivity to the reversal hypothesis without pretending to estimate its likelihood.

## What would make the hypothesis convincing?

A real study would specify signal and holding horizons before testing, compare returns after bid–ask costs and market impact, and distinguish temporary price pressure from worsening fundamentals. Sector ETFs are correlated baskets: a loser strategy can carry substantial market, industry and volatility exposure. Monthly observations can hide an early rebound before the assumed trade, and a strategy chosen from many horizons can look compelling through selection alone.

All paths and results are **constructed educational scenarios**, not a fresh backtest or evidence of a profitable reversal premium. The useful takeaway is a design distinction: horizon, direction and execution are separate choices. Return to [sector momentum](../06-sector-momentum/README.md) to compare ranking and trend filters under the same ownership discipline.
