# Acceptance evidence — 19 September 2026

| Brief criterion | Evidence and boundary |
|---|---|
| Original components and clear question | [Audit](AUDIT.md), per-file [legacy inventory](legacy_inventory.json), original `old` branch; retained/replaced/archived claims distinguished. |
| Versioned appropriate inputs | [Sources](SOURCES.md), [manifest](data/input_manifest.json), pinned hashes. Raw market snapshots require permitted local access; FICC uses a committed constructed fixture. |
| Study actually executed | [Executed notebook](../study.ipynb), [machine-readable summaries](results/), [generated results](../docs/02-results.md). |
| Meaningful comparisons | [Protocol](PROTOCOL.md) and [methods](../docs/01-methods.md) define timing, universe/risk controls or pricing conventions. |
| Consequential defects handled | [Audit](AUDIT.md) connects defects to maintained replacements or withdrawn legacy claims. |
| Numerical/timing/accounting checks | Hand-calculated holdings/fees, future-data perturbation, independent HRP/ERC cases and invalid-input cases; 8 tests. `research/check_artifacts.py` additionally reconciles saved artifacts independently. |
| Uncertainty and sensitivity | Paired block intervals, matched-risk controls, lookback/shrinkage/timing/cost sensitivity, negative headroom retained. |
| Headline consistency | Generated README/results, executed notebook summary and saved headline JSON agree; independent checker reconstructs key values. |
| Environment and executable report | Locked offline sync, lint/format and 8 tests pass; 12 executed notebook cells with 4 embedded figures and no errors. |
| Reproduction and CI | [README commands](../README.md), ignored cached inputs and recoverable checkpoints; CI checks synthetic/public artifacts, not restricted historical reproduction. |
| Maintained files and attribution | `.gitignore` excludes raw/recovery/environment paths; [NOTICE](../NOTICE) retains attribution. Original history is preserved rather than rewritten. |
| Publication boundary | [PUBLICATION.md](../PUBLICATION.md): local artifacts checked; no live publication or complete historical rights/credential clearance. |
| Supported conclusion and next experiment | HRP incremental risk-adjusted value is not established; the primary interval includes zero. [Agenda](RESEARCH_AGENDA.md) is explicitly unrun. |

All completed checks refer to local execution. Provider data accuracy, point-in-time vintages,
actual transaction execution and unrestricted redistribution are not certified. See the
[work log](WORKLOG.md) for commands, recovery and the visual/HTML inspection boundary.
