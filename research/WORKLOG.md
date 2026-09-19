# Renovation work log

Started 2026-09-19 in WSL as daham. Original commit `1ab02e830941929c23f030c6eac26bbee6d539a7` is preserved on `old`; active branch `renovation`. No remote operations.

Reference inspected: corporate-bond project at `1f565f6d7010274ff8feb333b9c05be11ba1dcfa`, README, protocol, sources, evaluation, agenda, publication review.

Initial phase: audit and protocol, before primary evaluation. Outputs: `research/results/`, `research/figures/`, `study.ipynb`; raw snapshots stay ignored in `research/data/raw/`. Reruns overwrite only generated artifacts. Notebook replaced atomically after successful clean-kernel execution.

Recovery: `uv sync --locked`; `uv run python research/acquire.py` (data projects); `uv run python research/run_study.py`; `uv run python research/build_notebook.py`; `uv run pytest -q`; `uv run python research/check_artifacts.py`. Acquisition reuses valid per-ticker hashes and stops on changed sources.

User authorized fresh data. Refreshing through last completed US close, 2026-09-17 (retrieval begins 2026-09-18 16:25 UTC; Sep 18 session still open). Initial protocol/manifest preserved, initial performance not evaluated. New primary end will be documented before evaluation.

## Completed verification — 19 September 2026 KST

- `uv sync --locked --offline`: succeeded using the installed Linux Python 3.12 environment and cached dependencies.
- `uv run python research/refresh_sources.py --end 2026-09-18`: fresh Yahoo snapshots through 17 September; 12 added sessions. `uv run python research/acquire.py`: all pinned hashes verified from local cache. Original vintages retained.
- `uv run python research/run_study.py`: completed numerical study; the notebook build also reran its maintained entry point.
- `uv run python research/build_notebook.py`: successful fresh-kernel execution, 12 code cells, 4 embedded quantitative figures, zero cell errors. Notebook headline matches generated results. HTML preview has embedded figures and tables.
- `uv run python -m pytest -q`: **8 passed**.
- `uv run python -m ruff check research tests` and `uv run python -m ruff format --check research tests`: passed.
- `uv run python research/check_artifacts.py`: public links/notebook checks, current source/code/output hashes and independent saved-output calculations passed.
- All 4 generated PNGs inspected; exact sample/convention labels checked. HTML structure inspected programmatically; no full browser/site layout certification.

The exact final numerical conclusions are in [generated results](../docs/02-results.md).
[Acceptance evidence](ACCEPTANCE.md) records coverage and boundaries. Local checks exercise the
committed CI commands; no remote GitHub workflow, push, deployment or live blog publication was run.
The maintained Git tree omits raw vendor histories, ignored recovery material, environments and
caches. Historical credential/rights boundaries remain in [publication review](../PUBLICATION.md).

Final Git review: original `old` reference verified; maintained Markdown links resolve within the staged tree. Tracked evidence hashes match staged bytes, and raw/recovery/environment paths are absent. `.gitattributes` preserves Linux source line endings and exact hashed CSV serializer bytes. Staged whitespace checks pass.

## Research reading collection

The README now leads with portfolio objectives, all nine original strategy topics, their
economic differences, the ETF universe and the comparison design. Each topic has its own
research note and notebook; operational commands live in `docs/reproduction.md`. A bounded
result marker prevents research regeneration from replacing the editorial introduction.

All nine teaching notebooks executed in fresh kernels: 48 code cells, 11 figures,
zero cell errors. Inputs are explicit constructed illustrations, except references to the
separately completed historical study. Known-answer and timing assertions run inside the
examples. All topic figures were visually inspected. The five optimization/risk chapters had
an additional independent mathematical review; equality-constraint wording and Kelly payoff
units were clarified. Tactical chapters distinguish momentum/reversal horizons and VAA/DAA
signal roles without claiming full published-strategy replication.

`uv run python research/execute_topics.py --topic <directory>` executed every chapter;
`uv run python research/build_notebook.py` regenerated the main report and provenance;
`uv run python research/check_artifacts.py`, Ruff check and format check all passed. The
primary calculation and its headline finding are unchanged. New topic notes and notebook
Markdown links are included in the public artifact check.

## Robust allocation revision — 19 September 2026

The user requested a robust allocation direction inspired by Marcos López de Prado's work.
The root README now introduces estimation stability, information leakage and backtest selection,
then links all nine original strategy chapters. The historical ETF case remains a supporting
record. Its generated numerical paragraph no longer rewrites the README.

Added three original constructed notebooks: label purging/embargo with training-only preprocessing
and held-out raw-data perturbations; a complete 128-candidate IID null search with CSCV/PBO and
original-2014 PSR/DSR; and five fixed allocation rules with covariance shrinkage, concentration
caps, finite-scenario minimax variance and 120 complete bootstrap refits. The separate research
design states which methods are implemented and which empirical extensions remain unrun.

Verification completed in the locked Linux environment:

- `uv run python -m pytest -q`: **25 passed**, including 17 new focused validation/optimization tests.
- Ruff lint and format checks pass across `research` and `tests`.
- All three new chapters executed in fresh kernels: **12 code cells, 5 figures**, zero errors.
  Their figures were visually inspected and their HTML previews contain the expected tables and
  embedded plots. An independent review corrected covariance-validation tolerances for tiny
  return units; the final estimation notebook was rerun after that correction.
- `research/run_study.py` and `research/build_notebook.py` regenerated the empirical report and
  provenance. The ETF calculation and numerical conclusion remain unchanged.
- `research/check_artifacts.py` passed public links, all **12 topic notebooks**, the main report,
  source/code/output hashes and independent historical accounting checks. Across the collection:
  **13 notebooks, 72 executed code cells, 20 figures**.

Recovery uses the existing pipeline and `research/execute_topics.py --topic <directory>`.
Successful notebooks replace prior files atomically; previews remain under ignored
`research/preview/`. These examples require no new vendor data or dependencies. The existing
September 17 adjusted-price vintage remains the separate historical input. No empirical DSR/PBO
claim, full nested predictive allocation model or completed future holdout is asserted.

## Allocation breadth extension — 19 September 2026

Starting commit `8363ed3070`, clean working tree. The user requested additional allocation
ideas with the existing level of research quality. Six chapters were added: Black–Litterman,
expected shortfall, factor-risk allocation, liability-driven allocation, volatility targeting
and CPPI. Each has an economic question, original constructed inputs, explicit portfolio rule,
independent numerical checks, sensitivity/failure examples, source references and executed plots.

Outputs: `topics/13-black-litterman/` through `topics/18-cppi/`, with reusable calculations under
`research/` and focused tests under `tests/`. New examples use the existing locked dependencies
and require no market-data download. Each notebook can be restarted independently with
`uv run python research/execute_topics.py --topic <directory>`; successful files replace prior
versions atomically and previews remain under ignored `research/preview/topics/`. After research
modules and the protocol stabilize, regenerate the core metadata and main report, then run full
artifact checks. Existing `old` and the prior published `renovation` commit preserve recovery.

Completed checks: `uv run python -m pytest -q` reports **49 passed**; Ruff lint and format
checks pass. Six new notebooks executed in fresh kernels, **34 code cells and 13 figures**,
with every plot visually inspected. Bayesian and tail-loss calculations received additional
review of covariance scale and objective normalization; invalid inputs and reference solutions
are tested across return units. Plot review moved legends outside data and removed crowded
minor ticks, followed by notebook re-execution.

The main report and source/code/artifact hashes were regenerated after all research modules
stabilized. Full artifact checks passed: all **18 topic notebooks**, their overview links,
the main report, current source/output hashes and independent historical accounting. The
collection now contains **19 notebooks, 106 executed code cells and 33 figures**. The original
ETF headline is unchanged. Notebook HTML previews remain local and ignored; this review does
not claim a live browser certification of GitHub rendering.

At the user's request, the main README presents the project's own research direction without
personal attribution to an external professor. Method citations remain in detailed research
notes and the source register. The overview groups fifteen allocation ideas by decision type
and keeps the three validation/estimation chapters as a separate research path.
