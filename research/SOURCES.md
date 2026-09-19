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
- [Ledoit–Wolf implementation](https://scikit-learn.org/stable/modules/generated/sklearn.covariance.LedoitWolf.html): identity-target shrinkage used in the ETF sensitivity and the separate constructed estimation-risk example.
- [Keller and Keuning (2017), VAA](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3002624): source of the breadth-momentum idea. The maintained five-ETF defensive rule is an adaptation, not the paper's universe or a replication of its performance.
- López de Prado (2016), *Building Diversified Portfolios that Outperform Out of Sample*, Journal of Portfolio Management 42(4): HRP attribution. The legacy implementation was checked against condensed-distance semantics and known small cases; no source-paper performance is reproduced.

Contribution: correct the accounting and distance-input defects, isolate prior-risk exposure
controls, preserve unfavorable sensitivities and quantify incremental uncertainty. Source
attribution does not establish a novel allocation algorithm.

## Strategy reading collection

The topic notebooks contain their own original constructed covariance, return, probability or
signal inputs; these are teaching exercises, not newly acquired observations. Topic READMEs link
method-specific primary references and clearly separate illustrations from the completed ETF
study. The new notes restore all nine original subject areas without restoring vendor exports
or unverified historical outputs. Additional methodological references: [Markowitz's Nobel lecture](https://www.nobelprize.org/uploads/2018/06/markowitz-lecture.pdf),
[Maillard, Roncalli and Teïletche on ERC](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1271972),
[López de Prado on HRP](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2708678),
[Kelly's original article](https://onlinelibrary.wiley.com/doi/abs/10.1002/j.1538-7305.1956.tb03809.x),
and [Choueifaty on maximum diversification](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4063676).
The source abstracts and official documentation support attribution; the notebook calculations
are original examples and do not reproduce the cited papers' empirical performance claims.

## Robust allocation extension

The [research design](../docs/robust-allocation.md) links the original HRP paper, the author's
financial ML book, [Bailey et al. on CSCV/PBO](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf)
and [Bailey and López de Prado's original 2014 DSR paper](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf).
The worked examples implement stated equations on original constructed inputs. The author-hosted
papers support methodological attribution, not claims of empirical allocation success here.
The PSR/DSR example states IID assumptions and the distinction between a supplied independent
trial count and the unknown effective number of attempts in a real research history.

The finite-scenario allocation is an original educational minimax-variance example, using
training-only covariance transformations, a declared cap and the official SciPy SLSQP solver.
Its covariance-shrinkage target is identity, not the constant-correlation target from a
different Ledoit–Wolf paper. Seeds, sample sizes, candidate rules and scenario definitions
are visible in the [notebook](../topics/12-estimation-risk/study.ipynb). No additional vendor
observations are acquired for these three new method chapters, and no constructed input is
presented as current market data.
