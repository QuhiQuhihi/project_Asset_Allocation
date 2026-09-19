# Reproduce the research

[Return to the research overview](../README.md). The strategy notes and saved notebooks can be read without installing an environment. This page is for readers who want to recompute the empirical study or educational allocation and robustness examples.


Use Python 3.12 and the committed uv lockfile. Run from this repository:

```bash
uv sync --locked
uv run python research/acquire.py --download
uv run python -m pytest -q
uv run python research/run_study.py
uv run python research/build_notebook.py
uv run python research/check_artifacts.py
uv run python -m ruff check research tests
uv run python -m ruff format --check research tests
```

The first acquisition downloads only missing snapshots and checks pinned hashes. A revised vendor history fails clearly; restore the matching permitted cache rather than bypassing hashes. For cached/offline reproduction use `uv run --offline python research/acquire.py` followed by the remaining commands without `--download`. To import an existing permitted cache use `uv run python research/acquire.py --from-cache /path/to/cache`. An explicit later refresh uses `uv run python research/refresh_sources.py --end YYYY-MM-DD` (exclusive end, completed sessions only); retain the old manifest, amend the protocol and rerun all artifacts before changing claims.


## Topic notebooks

Each topic notebook is the maintained source of its educational calculation. Run `uv run python research/execute_topics.py` from the project root to execute all eighteen in fresh kernels; `--topic 13-black-litterman` selects one. Original illustrative inputs are included in the notebooks, so these examples do not download market histories. Successful notebooks replace prior files atomically; local HTML previews are saved under ignored `research/preview/topics/`.

The primary ETF experiment retains its dated source manifest, information timing and documented statistical limitations. See [methods](01-methods.md) and [protocol](../research/PROTOCOL.md).
