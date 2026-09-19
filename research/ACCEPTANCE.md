# Acceptance evidence — 19 September 2026

| Brief criterion | Evidence and boundary |
|---|---|
| Original components and clear question | [Audit](AUDIT.md), per-file [legacy inventory](legacy_inventory.json), original `old` branch; retained/replaced/archived claims distinguished. |
| Versioned appropriate inputs | [Sources](SOURCES.md), [manifest](data/input_manifest.json), pinned hashes. Raw market snapshots require permitted local access; FICC uses a committed constructed fixture. |
| Study actually executed | [Executed notebook](../study.ipynb), [machine-readable summaries](results/), [generated results](../docs/02-results.md). |
| Meaningful comparisons | [Protocol](PROTOCOL.md) and [methods](../docs/01-methods.md) define timing, universe/risk controls or pricing conventions. |
| Consequential defects handled | [Audit](AUDIT.md) connects defects to maintained replacements or withdrawn legacy claims. |
| Numerical/timing/accounting checks | Holdings/fees, future-data perturbation, HRP/ERC references, purged interval oracles, selection-statistic identities, constrained portfolio references and invalid-input cases; 25 tests. `research/check_artifacts.py` also reconciles saved artifacts independently. |
| Uncertainty and sensitivity | Paired block intervals, matched-risk controls, lookback/shrinkage/timing/cost sensitivity, negative headroom retained. |
| Headline consistency | Generated results, executed notebook summary and saved headline JSON agree; independent checker reconstructs key values. README introduces the research design and chapter collection. |
| Environment and executable report | Locked environment, lint/format and 25 tests pass; the main report has 12 executed cells and 4 figures, and the 12 topic notebooks have 60 executed cells and 16 figures. |
| Reproduction and CI | [Reproduction commands](../docs/reproduction.md), ignored cached inputs and recoverable checkpoints; CI checks synthetic/public artifacts, not restricted historical reproduction. |
| Maintained files and attribution | `.gitignore` excludes raw/recovery/environment paths; [NOTICE](../NOTICE) retains attribution. Original history is preserved rather than rewritten. |
| Publication boundary | [PUBLICATION.md](../PUBLICATION.md): user-authorized GitHub branch updates; no live blog release or complete historical rights/credential clearance. |
| Supported conclusion and next experiment | HRP incremental risk-adjusted value is not established; the primary interval includes zero. [Agenda](RESEARCH_AGENDA.md) is explicitly unrun. |

All completed checks refer to local execution. Provider data accuracy, point-in-time vintages,
actual transaction execution and unrestricted redistribution are not certified. See the
[work log](WORKLOG.md) for commands, recovery and the visual/HTML inspection boundary.

## Topic-navigation extension

All original subject areas now lead from the root README to a dedicated research note and
an executed notebook. Nine teaching notebooks contain 48 executed code cells and 11
figures. They cover objective/constraint calculations and explicit tactical scenarios rather
than carrying forward unverified legacy performance. Operational instructions moved to a
secondary [reproduction page](../docs/reproduction.md). Research design and principal findings
remain visible before those instructions.

## Robust allocation extension

The three new notebooks add training-sample perturbations and scenario-constrained portfolios,
purged labels and training-only preprocessing, and a complete constructed trial library with
CSCV/PBO and the original PSR/DSR formulation. All five new figures were visually inspected.
The documentation distinguishes local weight stability, finite-scenario protection, chronological
evaluation and selection corrections. It claims neither a full nested ML/CPCV allocation system
nor an empirical DSR/PBO result for the already inspected ETF study.
