"""Small validation tools for the constructed allocation research chapters.

These diagnostics do not certify a strategy or replace chronological evaluation.
The PSR/DSR routines implement the original 2014 location-adjusted DSR under
independent observations and an explicitly supplied independent trial count.
"""

from itertools import combinations
from math import comb
from numbers import Integral

import numpy as np
import pandas as pd
from scipy.stats import norm, rankdata


def _integer_array(values, name):
    array = np.asarray(values)
    if array.ndim != 1 or not np.issubdtype(array.dtype, np.integer):
        raise ValueError(f"{name} must be a one-dimensional integer array")
    return array


def purged_train_indices(starts, ends, test_indices, embargo=0):
    """Remove test rows, overlapping label intervals, and a post-label embargo.

    Time is measured in integer bar positions. Each information interval is
    CLOSED [start, end], so even a shared endpoint is conservatively excluded.
    For every test interval, extend its right endpoint by ``embargo`` bars.
    Training intervals intersecting that union are excluded. This is equivalent
    to purging label overlap and then excluding starts in (test_end, test_end+E].
    No observations are shuffled and no feature transformations are fitted here.
    Returned indices may follow the test period: this is a research CV split,
    not a past-only walk-forward split. Supply the latter restriction separately.
    """
    starts = _integer_array(starts, "starts")
    ends = _integer_array(ends, "ends")
    test = _integer_array(test_indices, "test_indices")
    if not len(starts) or starts.shape != ends.shape:
        raise ValueError("starts and ends must have the same nonzero length")
    if np.any(starts < 0) or np.any(ends < starts) or np.any(np.diff(starts) <= 0):
        raise ValueError("starts must increase strictly; each end must follow its start")
    if not len(test) or np.any(test < 0) or np.any(test >= len(starts)):
        raise ValueError("test_indices must contain valid row indices")
    if len(np.unique(test)) != len(test):
        raise ValueError("test_indices must not contain duplicates")
    if isinstance(embargo, bool) or not isinstance(embargo, Integral) or embargo < 0:
        raise ValueError("embargo must be a nonnegative integer number of bars")
    keep = np.ones(len(starts), dtype=bool)
    for row in test:
        # Convert to Python int before adding to avoid fixed-width integer overflow.
        right = int(ends[row]) + int(embargo)
        keep &= ~((starts <= right) & (ends >= starts[row]))
    keep[test] = False
    return np.flatnonzero(keep)


def sharpe_ratio(returns):
    """Per-observation mean / sample standard deviation; no annualization."""
    values = np.asarray(returns, dtype=float)
    if values.ndim not in (1, 2) or len(values) < 3 or not np.isfinite(values).all():
        raise ValueError("returns must be finite, with at least three observations")
    if values.ndim == 2 and values.shape[1] == 0:
        raise ValueError("returns must contain at least one candidate")
    scale = np.std(values, axis=0, ddof=1)
    if np.any(scale <= 0):
        raise ValueError("Sharpe ratio is undefined for a constant return series")
    result = np.mean(values, axis=0) / scale
    return float(result) if values.ndim == 1 else result


def probabilistic_sharpe_ratio(
    observed_sharpe, observations, benchmark_sharpe=0.0, skewness=0.0, kurtosis=3.0
):
    """Original asymptotic PSR; all Sharpe inputs use the observation frequency.

    ``kurtosis`` is Pearson/non-excess kurtosis (Normal = 3). This bounded
    teaching implementation assumes independent observations and finite fourth
    moments. The normal-CDF statistic is not a Bayesian probability of skill.
    """
    inputs = np.array([observed_sharpe, benchmark_sharpe, skewness, kurtosis], dtype=float)
    if not np.isfinite(inputs).all():
        raise ValueError("Sharpe ratios and moments must be finite")
    if isinstance(observations, bool) or not isinstance(observations, Integral) or observations < 3:
        raise ValueError("observations must be an integer of at least three")
    if kurtosis < 1:
        raise ValueError("Use non-excess kurtosis, which must be at least one")
    variance_term = 1 - skewness * observed_sharpe + (kurtosis - 1) * observed_sharpe**2 / 4
    if variance_term <= 0 or not np.isfinite(variance_term):
        raise ValueError("The supplied moments imply an invalid Sharpe standard error")
    standard_error = np.sqrt(variance_term / (observations - 1))
    return float(norm.cdf((observed_sharpe - benchmark_sharpe) / standard_error))


def expected_maximum_sharpe(trial_sharpe_std, independent_trials):
    """2014 expected-max approximation for zero-mean IID Normal trial Sharpes.

    The spread is the standard deviation ACROSS trial Sharpe estimates, in
    per-observation units. It is not portfolio volatility. One trial has exact
    expected maximum zero; for N > 1 use the paper's extreme-value approximation.
    Dependence-adjusted trial counts are not estimated by this function.
    """
    if not np.isfinite(trial_sharpe_std) or trial_sharpe_std < 0:
        raise ValueError("trial_sharpe_std must be finite and nonnegative")
    if (
        isinstance(independent_trials, bool)
        or not isinstance(independent_trials, Integral)
        or independent_trials < 1
    ):
        raise ValueError("independent_trials must be a positive integer")
    if independent_trials == 1 or trial_sharpe_std == 0:
        return 0.0
    first_quantile = norm.isf(1.0 / independent_trials)
    tail_quantile = norm.isf(1.0 / (independent_trials * np.e))
    standardized_max = (1 - np.euler_gamma) * first_quantile + np.euler_gamma * tail_quantile
    return float(trial_sharpe_std * standardized_max)


def deflated_sharpe_ratio(
    observed_sharpe,
    observations,
    trial_sharpe_std,
    independent_trials,
    skewness=0.0,
    kurtosis=3.0,
):
    """PSR relative to the 2014 search-adjusted expected-maximum threshold."""
    threshold = expected_maximum_sharpe(trial_sharpe_std, independent_trials)
    return probabilistic_sharpe_ratio(observed_sharpe, observations, threshold, skewness, kurtosis)


def cscv_diagnostics(returns, n_blocks=8):
    """Evaluate every equal-half combination of contiguous performance blocks.

    Columns must contain the COMPLETE, fixed candidate library on common rows.
    The in-sample winner maximizes per-observation Sharpe; exact ties use the
    first declared column. OOS ranks are ascending, with average ranks for ties.
    The relative rank is rank/(N+1), and logit <= 0 counts at-or-below-median
    outcomes. Identical candidates all have logit zero and provide no ranking
    information: the boundary-inclusive fraction must not be called proof of
    overfitting. CSCV reuses observations and is neither CPCV nor a deployable
    sequence of out-of-sample portfolio returns.
    """
    values = np.asarray(returns, dtype=float)
    if values.ndim != 2 or values.shape[1] < 2:
        raise ValueError("CSCV requires a two-dimensional matrix with at least two candidates")
    if (
        isinstance(n_blocks, bool)
        or not isinstance(n_blocks, Integral)
        or n_blocks < 2
        or n_blocks % 2
        or len(values) % n_blocks
    ):
        raise ValueError("n_blocks must be even, at least two, and divide the observation count")
    if len(values) // 2 < 3 or not np.isfinite(values).all():
        raise ValueError("Each half must have at least three finite observations")
    if comb(n_blocks, n_blocks // 2) > 100_000:
        raise ValueError("This teaching implementation limits enumeration to 100,000 splits")
    blocks = np.split(np.arange(len(values)), n_blocks)
    rows = []
    for training_blocks in combinations(range(n_blocks), n_blocks // 2):
        train = np.concatenate([blocks[i] for i in training_blocks])
        test = np.concatenate([blocks[i] for i in range(n_blocks) if i not in training_blocks])
        train_sr = sharpe_ratio(values[train])
        test_sr = sharpe_ratio(values[test])
        selected = int(np.argmax(train_sr))
        relative_rank = float(rankdata(test_sr, method="average")[selected] / (values.shape[1] + 1))
        rows.append(
            {
                "training_blocks": training_blocks,
                "selected": selected,
                "in_sample_sharpe": float(train_sr[selected]),
                "out_of_sample_sharpe": float(test_sr[selected]),
                "relative_rank": relative_rank,
                "logit": float(np.log(relative_rank / (1 - relative_rank))),
            }
        )
    return pd.DataFrame(rows)
