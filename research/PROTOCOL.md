# Allocation protocol — 19 September 2026

Written before running this renovation's primary evaluation. No independent preregistration;
the history was already studied in the SVD project. This is retrospective research.

**Question:** Does HRP add risk-adjusted value beyond equal weight, including equal weight
scaled using prior covariance to the HRP target risk? Mechanism: diversified covariance
structure; competing explanation: holding more low-risk assets. Primary endpoint: HRP minus
its risk-scaled equal-weight control's net annualized mean/volatility ratio, under zero assumed
cash interest, January 2025–17 September 2026. An interval above zero and a positive incremental
annual mean after matched costs would motivate new data, not establish tradable alpha.

Inputs: pinned Yahoo adjusted-close snapshots, 2018-07-02–2026-09-17. Universe in fixed order:
SPY, IEMG, TLT, GLD, SHY. These surviving ETFs existed before this window; this is a convenience
universe, not survivorship-free selection. AGG supplies a contextual SPY/AGG 60/40.
All NYSE sessions must be present and positive. No filling, inception backfilling or inferred
delisting proceeds. Adjusted returns incorporate distributions; no additional dividend credit.

Comparators: equal weight, inverse volatility, equal risk contribution (ERC), HRP; a separate
VAA-inspired defensive adaptation and 60/40 context. Sample covariance uses 252 preceding
returns; positive-variance check and tiny relative diagonal regularization (1e-8 of mean
variance) precede allocation. ERC solves a positive convex risk-budget problem. Failure or
infeasible output falls back to inverse volatility and is counted. HRP uses single linkage on
condensed sqrt((1-correlation)/2), leaf ordering, recursive bisection and inverse-variance
cluster risk. No leverage or shorting; weights sum to one. All position limits are the budget
constraint [0,1]. Risk-scaled controls hold min(1, predicted strategy vol / predicted EQ vol)
of EQ and the rest non-interest-bearing cash. Cap binding is reported.

Tactical supporting rule: compute 12 R21 + 4 R63 + 2 R126 + R252 from compounded prices/returns.
If each of SPY, IEMG, TLT and GLD has positive score, allocate equally to those four; otherwise
hold SHY. This repairs the legacy ratio-of-returns mistake. It is an adaptation to this universe,
not a full VAA or DAA replication; SHY has rate risk and is not a risk-free return series.

Execution: first session of each month from August 2020, information ends at previous close;
trade at that session's close, new holdings first earn the following day's return. Old holdings
earn execution-day returns and drift. Entry starts from cash and is charged; no terminal sale.
Exact self-financing fee c solves c = a sum |(1-c)w-u| for risky targets w and pretrade u;
cash is residual, cost per bought OR sold dollar. Net return = (1+gross)(1-c)-1. Save targets,
information/execution dates, daily earning weights, signed trades, cash, costs and returns.

Cash assumption: zero nominal accrual, no financing; reported total returns equal excess
returns only relative to this assumed zero cash benchmark. Mean/volatility is explicitly rf0,
not an estimate of excess return over observed Treasury bills. Sensitivity to real cash yields
requires a new pinned series; the resulting limitation particularly affects scaled controls.

Common dates: August 2020–17 September 2026 full post-warmup, January 2025–17 September 2026 primary late
segment. Also show 2022 as a prespecified adverse-rate-period description, not independent proof.
Return/volatility/drawdown, concentration, turnover, cash exposure and gross/net results.
Paired circular blocks of 21 sessions, 2,000 resamples, seed 20260919; blocks 5 and 63 secondary.
Intervals condition on fitted paths and do not refit strategies or correct selection. One
primary HRP-versus-scaled-EQ test; all others exploratory pointwise diagnostics.

Bounded sensitivities: 126/504 lookbacks, Ledoit–Wolf covariance, 0/10 bps costs versus 5 primary,
and one extra execution session. Same evaluation dates and controls. Additional constant
annual cost headroom = gross strategy-minus-control annual arithmetic mean; preserve negatives.
Also compute linearized per-traded-dollar differential-cost break-even only where incremental
turnover is positive. Negative/zero turnover differences do not define a positive cost ceiling.
No best-variant replacement of the primary.

Recovery: `uv run python research/run_study.py`; cached inputs immutable; daily artifacts under
`research/results/paths/` are ignored, summary CSVs and original PNGs maintained. Rebuild notebook
with `uv run python research/build_notebook.py` after calculations. Raw rights remain with provider.

## Data amendment before evaluation

The user authorized refreshing inputs during implementation, before primary results were computed. On 19 September 2026 KST, download through the last completed US close (17 September; exclusive end 18 September). September is partial. Original protocol is retained in `protocol_versions/initial_20260919.md`; initial manifest and raw snapshots remain available. This expands the late segment by 12 sessions and may revise overlapping adjusted prices. Source revision diagnostics are saved; no initial performance result is claimed.

## Research-direction amendment after the historical evaluation

The project now leads with robust asset allocation and research selection risk, at the user's
request. This amendment follows inspection of the ETF results; it is not a preregistration and
does not replace the historical primary comparison above. The README introduces the research
questions and chapter collection; numerical ETF findings remain generated in the results note.

Three separate constructed chapters cover label purging/embargo, CSCV/PBO and the original
PSR/DSR formulation, and training-only allocation under estimation uncertainty. The allocation
example fixes five rules, a 35% cap, 126 training observations, 252 independent shifted-world
test observations, two explicit training-derived stress transformations and 120 bootstrap
refits. Seeds and all model inputs appear in its notebook. Its stress set is an assumption,
not a statistical coverage region; no candidate is promoted from the observed comparison.

The validation chapters specify their own complete illustrative inputs and trial library.
They do not add an empirical selection correction to the previously inspected ETF paths.
The full historical research search is not reconstructed, so an empirical deflated Sharpe or
PBO claim for that study would be unsupported. All new examples are method demonstrations,
not new evidence of allocation alpha. The [robust research design](../docs/robust-allocation.md)
distinguishes implemented methods from the future empirical study.
