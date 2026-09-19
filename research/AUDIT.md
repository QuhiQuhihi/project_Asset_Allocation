# Audit — 19 September 2026

Starting commit: `1ab02e830941929c23f030c6eac26bbee6d539a7` (branch `old`). Clean status verified before edits. All root notebooks inspected as JSON without execution; README, helper modules, data inventory and source schemas inspected. Saved outputs are not validation.

Original: educational comparison of MVO, risk parity, HRP, Kelly, diversification, sector momentum/reversal, VAA and DAA, using a shared holdings engine. Audience: Python/quant readers. No historical performance claim is carried forward.

Verified defects from source inspection (not inferred from saved plots):
- `00_mean_variance.ipynb`, cell 9, and `04_max_diversification.ipynb`, cell 9: `relativedelta(month=1)` changes the month field, not a one-month lookback; `.pct_change().fillna(1)` creates 100% simple returns.
- `02_hierachical_risk_parity.ipynb`, cell 10: square correlation-distance matrix passed to linkage as observations instead of condensed distances.
- `03_kelly_criteriom.ipynb`, cell 13: gross price relatives enter a mean/covariance construction. Clipping and normalizing does not validate a constrained log-utility solution.
- `06_vigilant_asset_allocation_with_momentum.ipynb`, cell 10: daily returns passed to a price-ratio momentum function; ratios of returns and inf replacement cannot reproduce price momentum.
- `backtest/backtest_engine.py:27`: credential-like API-key default. It is not used or reproduced. Current maintained code removes the dependency; owner rotation and historical-copy review remain necessary.
- Engine lines 275–290 charge only positive trades; lines 315–327 interpret a missing observation as delisting and liquidate at a stale value. Lines 107–119 infer macro release dates from average lags, which is not documented point-in-time availability.
- Strategies refer to global `engine.date`, defeating isolated engine state.

Disposition: risk parity and HRP are reimplemented with one accounting engine. Equal weight and a contextual 60/40 are retained. VAA's 1/3/6/12-month price-momentum idea becomes a clearly labeled same-universe defensive adaptation, not a replication of its eight-ETF historical portfolio. MVO, Kelly, maximum diversification, sector momentum/reversal and DAA are archived without renewed performance claims. Vendor index exports, PDFs and screenshots remain only in ignored recovery material and original history. The full per-file disposition is `legacy_inventory.json`.

Revised primary question: does HRP improve net return/risk relative to equal weight and a lagged risk-scaled equal-weight control? IV and ERC are prespecified supporting comparisons. Current-vintage ETF adjusted closes make a bounded historical comparison feasible; universe selection, provider revisions, closing execution and zero cash accrual remain important limitations.

Recovery: `git show old:<path>` or ignored `research/private-legacy/<path>`. Original history is intentionally preserved, not publication-cleared.

## Research collection amendment

The original nine subjects now each have a reader-facing note and an executed topic notebook
under `topics/`. Mean–variance, Kelly and maximum-diversification examples use constructed
inputs and analytical checks; the tactical chapters illustrate their signal and exposure rules.
They do not reuse the archived historical curves or add post-selected strategies to the primary
ETF contest. Risk parity and HRP connect the teaching examples to the maintained empirical study.
The main README introduces the research breadth and design; reproduction details moved to
`docs/reproduction.md`. Original-source disposition above describes the preserved legacy files.

## Robust allocation direction

The collection now leads with input uncertainty, information boundaries and research selection,
following the user's requested emphasis on robust allocation and López de Prado's methods.
Three new constructed chapters extend the nine strategy mechanisms. The empirical HRP case
remains available with its original primary comparison and limitations; its headline no longer
determines the root README's structure. Regeneration writes numerical findings to the dedicated
results note, preserving the editorial research map.

Independent review of the new finite-scenario optimizer found that absolute input-validation
tolerances could admit an invalid covariance in extremely small return units. Validation now
normalizes covariance magnitude before symmetry/semidefiniteness checks; tests reject the same
invalid matrix across scales. Known analytic and exhaustive-grid solutions validate the actual
optimization. This repair does not alter the historical ETF strategy engine.
