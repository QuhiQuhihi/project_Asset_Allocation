# Does portfolio construction earn its complexity?

In January 2025–17 September 2026, HRP minus its prior-risk-scaled equal-weight control has a net annualized mean/volatility difference of **+0.649**, with paired 95% block interval **[-0.649, +1.954]**. This does not establish incremental risk-adjusted value under this universe, zero cash interest and cost assumptions.

This is a retrospective ETF study. Cash-heavy risk portfolios can look safer simply because they hold SHY or reduce exposure. The matched-risk control uses only past covariance, with a cap at 100%; realized risks need not match. A mean/volatility ratio with zero assumed cash interest is not an observed risk-free-adjusted Sharpe ratio.

## Late-segment comparison

| strategy | cagr | volatility | max_drawdown | annual_turnover | mean_cash |
| --- | --- | --- | --- | --- | --- |
| 60/40 context | 0.121685 | 0.106896 | -0.112452 | 0.158916 | 0 |
| Defensive momentum | 0.0155946 | 0.0678281 | -0.100231 | 9.43665 | 0 |
| EQ risk ERC | 0.0631003 | 0.0388663 | -0.0287602 | 0.268061 | 0.638605 |
| EQ risk HRP | 0.03123 | 0.0189566 | -0.0142771 | 0.132893 | 0.822514 |
| EQ risk Inverse vol | 0.0651788 | 0.0395678 | -0.0286638 | 0.230299 | 0.62954 |
| ERC | 0.0735657 | 0.0377768 | -0.0256551 | 0.390153 | 0 |
| Equal weight | 0.175443 | 0.108417 | -0.0792407 | 0.311087 | 0 |
| HRP | 0.0357752 | 0.0154672 | -0.0103531 | 0.0666061 | 0 |
| Inverse vol | 0.0760606 | 0.0383892 | -0.0276876 | 0.305928 | 0 |

Returns and risks are decimal annual rates; drawdowns are fractions. Turnover includes buys and sells.

![Incremental result](../research/figures/incremental.png)

## What changes the answer

| variant | ratio_difference | annual_mean_difference | vol_difference |
| --- | --- | --- | --- |
| primary | 0.648643 | 0.00433863 | -0.00348942 |
| lookback126 | 0.602394 | 0.00551378 | -0.00226649 |
| lookback504 | 0.736922 | -0.000347644 | -0.00719516 |
| shrinkage | 0.269455 | -0.021372 | -0.0182346 |
| cost0 | 0.647346 | 0.00430549 | -0.00348925 |
| cost10 | 0.649942 | 0.00437179 | -0.00348961 |
| extra_session_lag | 0.656365 | 0.00437256 | -0.00353865 |

All variants remain visible; no winning replacement is selected. These comparisons reuse the same history and are not independent trials. The defensive momentum adaptation is separate from covariance estimation, and the 60/40 portfolio is contextual because its universe differs.

## Economic boundary

| strategy | control | annual_gross_headroom_bps | lower95_bps | upper95_bps | annual_incremental_turnover | linear_cost_ceiling_bps_per_dollar |
| --- | --- | --- | --- | --- | --- | --- |
| HRP | EQ risk HRP | 43.0549 | -147.598 | 254.24 | -0.0662871 | — |
| ERC | EQ risk ERC | 98.1822 | -12.6565 | 218.695 | 0.122092 | 804.166 |
| Inverse vol | EQ risk Inverse vol | 101.59 | -9.07145 | 224.982 | 0.0756284 | 1343.28 |

The annual headroom is a gross incremental constant-cost budget, not an observed fee. The per-dollar ceiling is a first-order approximation only when extra turnover is positive. Negative headroom is retained. ERC fallback occurred 0 times over 74 rebalances.

A stronger conclusion needs a prospectively fixed universe, an uninspected sample, observed cash yields and executable spread/size evidence. Adjusted prices may be revised, distributions are reinvested by proxy, closing fractional fills are assumed, and the study does not reconstruct delistings. See [protocol](../research/PROTOCOL.md), [inputs and methods](01-methods.md), [source register](../research/SOURCES.md), and [next experiment](../research/RESEARCH_AGENDA.md).
