# Sector momentum: choosing leaders without confusing rank with trend

Sector rotation asks whether leadership persists long enough to justify moving capital between industries. Relative momentum chooses the strongest sectors; a trend filter decides whether those leaders are attractive in absolute terms. Those decisions can disagree. A sector that loses 10% can still lead a market that loses 20%.

[Open the worked notebook](study.ipynb) · [Back to the research collection](../../README.md)

## Strategy design

The starting point is the original `05_sector_rotation_with_momentum.ipynb`: rank sectors by trailing twelve-month performance, select up to five, and distribute capital equally. Its narrative also proposed requiring sectors to beat the broad market, although the selection code only ranked the series. This chapter makes the benchmark condition explicit and adds a separately identified positive-trend condition. It is a clarified educational specification, not a claim to reproduce the old results.

At information month $t$, the score is a price return, $m_{i,t}=P_{i,t}/P_{i,t-12}-1$. A sector qualifies when its score exceeds both zero and the broad-market score. The highest-scoring five qualifying sectors share the portfolio equally; if none qualifies, the portfolio holds cash. Ties use a stable name order. The benchmark is a comparison series and cannot accidentally become a selected sector.

This design distinguishes the **selection budget** from the **risk budget**. Five available slots do not force five holdings. When only three sectors qualify, each receives one third, which increases concentration relative to a diversified sector benchmark. The cash fallback removes market exposure in the exercise; it is not evidence that a trend filter will exit before an actual drawdown.

## What the notebook shows

Six constructed sector paths and a constructed market path make the ranking visible. At month 12, Technology, Industrials and Financials return 24%, 18% and 12%, respectively, versus the market's 10%. They qualify for equal weights. The other sectors demonstrate why “positive” and “better than the market” are different tests. A second, declining-market scenario shows that relative winners can still fail the absolute filter.

The final exercise separates information, execution and ownership: the month-12 signal trades at month 13 and first earns the month-13-to-14 return. A large intervening move cannot be counted as a gain or loss on a position that did not yet exist. The notebook reconciles the subsequent 2.33% gross basket return with entry and exit costs of five basis points per traded notional, and checks that changing future prices cannot change the original selection.

## Questions for further research

The central hypothesis is persistent sector leadership after realistic costs, not simply a visually smooth ranking. A historical study would need point-in-time sector definitions, distribution-adjusted prices, an explicit rebalance calendar, and turnover-aware comparisons against equal-sector and broad-market portfolios. Sector reclassifications, correlated industry exposures, market beta and momentum crashes can dominate the apparent benefit. The twelve-month horizon, five-position cap and added filters should be compared under a predeclared design rather than selected after observing performance.

All displayed paths and results are **constructed educational examples**, not a fresh market backtest. Continue to [sector reversal](../09-sector-reversal/README.md) to see why buying recent losers is a different timing hypothesis.
