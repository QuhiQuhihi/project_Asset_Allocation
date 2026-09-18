# Sources and input provenance

Reviewed 19 September 2026. External source statements, modeling assumptions and computed
results are kept separate. No paper's reported performance is presented as reproduced here.
The corporate-bond quality reference was inspected locally at commit
`1f565f6d7010274ff8feb333b9c05be11ba1dcfa` (README, protocol, sources, evaluation, agenda, publication).

## Observed inputs

[Yahoo Finance historical prices](https://finance.yahoo.com/quote/SPY/history/) via
[yfinance's official API](https://ranaroussi.github.io/yfinance/reference/api/yfinance.Ticker.history.html).
The exact per-ticker URLs, retrieval timestamps, library version, units, row counts and SHA-256
hashes are in [input_manifest.json](data/input_manifest.json). These are USD adjusted closes;
simple returns are decimal changes. Distributions and splits are represented through provider
adjustments and are not independently reconciled with issuer cash-flow ledgers.

Fresh snapshots span 2 July 2018–17 September 2026 (2,064 close observations). Acquisition on
18 September UTC / 19 September KST excluded the still-open 18 September US session. The
[NYSE schedule](https://www.nyse.com/trade/hours-calendars) identifies the core close at 4 p.m.
Eastern. An access timestamp does not establish historical information availability.
No internal missing dates, duplicate sessions or forward fills are accepted. Raw data remain
ignored. Vendor/provider terms still apply; no unrestricted redistribution or commercial-use
permission is asserted. Users need permitted access to restore the same snapshots.

The original August-end snapshot and initial manifest are retained locally. The refresh adds
12 sessions; small overlapping adjusted-price changes are quantified in
[source_refresh.csv](results/source_refresh.csv). No old-vintage primary performance was
computed before this refresh. This is not an independent before/after strategy experiment.

## Methods and attribution

- [SciPy linkage](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html): distinguishes condensed distances from observation arrays; verified against the installed API and independent two-asset calculation.
- [Ledoit–Wolf implementation](https://scikit-learn.org/stable/modules/generated/sklearn.covariance.LedoitWolf.html): identity-target shrinkage used only in the prespecified sensitivity.
- [Keller and Keuning (2017), VAA](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3002624): source of the breadth-momentum idea. The maintained five-ETF defensive rule is an adaptation, not the paper's universe or a replication of its performance.
- López de Prado (2016), *Building Diversified Portfolios that Outperform Out of Sample*, Journal of Portfolio Management 42(4): HRP attribution. The legacy implementation was checked against condensed-distance semantics and known small cases; no source-paper performance is reproduced.

Contribution: correct the accounting and distance-input defects, isolate prior-risk exposure
controls, preserve unfavorable sensitivities and quantify incremental uncertainty. Source
attribution does not establish a novel allocation algorithm.
