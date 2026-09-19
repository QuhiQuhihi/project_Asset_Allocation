# Backtest selection: how much apparent skill came from the search?

Changing an allocation's lookback, asset universe, covariance estimator or defensive threshold creates more opportunities to discover an attractive historical result. A reproducible winning notebook is therefore only part of the research record. The rejected candidates and the process that selected the winner also matter.

## Three questions, three diagnostics

The **probabilistic Sharpe ratio (PSR)** evaluates an observed Sharpe against a stated benchmark using sample length, skewness and non-excess kurtosis. The **original 2014 deflated Sharpe ratio (DSR)** raises that benchmark to an estimated maximum from a search over independent candidate trials. Both use per-observation Sharpe units:

$$\operatorname{PSR}(SR_0)=\Phi\!\left(\frac{(\widehat{SR}-SR_0)\sqrt{T-1}}{\sqrt{1-\widehat\gamma_3\widehat{SR}+(\widehat\gamma_4-1)\widehat{SR}^{2}/4}}\right).$$

Here $\gamma_4$ is Pearson kurtosis, equal to 3 for Normal returns. These are asymptotic normal-CDF statistics under the stated assumptions, not posterior probabilities that an allocation has genuine skill or will make money. See [Bailey and López de Prado's 2014 paper](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf).

**Combinatorially symmetric cross-validation (CSCV)** asks whether the best candidate in one half of a performance history retains a favorable relative ranking in the other half. Across all equal-half combinations of contiguous blocks, the notebook records the selected candidate's out-of-sample rank $r$, transforms $r/(N+1)$ to a logit, and reports the fraction at or below the median. This is a finite-library PBO diagnostic, following [Bailey, Borwein, López de Prado and Zhu](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf).

## A complete constructed search

The notebook declares 128 independent null candidates, 504 observations for selection and 504 independent observations for a subsequent check. Every return is drawn from the same zero-mean Normal distribution with daily standard deviation 1%. The fixed seed, generator, complete candidate identifiers and matrix hashes are displayed. No candidate has population skill by construction. These are **synthetic performance series**, not 128 backtested ETF rules or allocation prescriptions.

The selected candidate's attractive training statistic is compared with its independent test result. CSCV uses eight blocks and all 70 equal-half splits of the selection sample. Exact in-sample ties select the first declared candidate; out-of-sample ties receive average ranks. A score exactly at the median is included in the reported boundary. Identical candidates therefore provide no ranking information and must not be interpreted as proof of overfitting.

The DSR example uses the sample spread of **all** candidate Sharpe estimates and the declared 128 independent trials. A second table varies a hypothetical trial count while holding that spread fixed. It demonstrates sensitivity to incomplete disclosure; it does not estimate the effective number of trials in correlated portfolio searches.

## What changes in an allocation research process?

Keep a trial ledger before looking at results: hypothesis, universe vintage, estimator, lookback, constraints, cost assumptions, selection metric and every attempted specification. Keep exploratory search separate from the final future evaluation. A changed rule after seeing that evaluation starts a new research decision.

Real allocation candidates usually share assets and dates; overlapping holding periods also create serial dependence. The independent-trial assumption and simple $T$-based standard error used here cannot be transferred mechanically. CSCV splits reuse observations, so 70 splits are not 70 independent experiments; the notebook deliberately reports no binomial confidence interval or deployable return path. It does not implement CPCV.

The public ETF history was already inspected, and its complete earlier search history is unavailable. **This project does not assign an empirical DSR or PBO certificate to that study.** These tools make selection assumptions inspectable; they do not remove structural change, weak economic premises or missing trials.

[Open the worked notebook](study.ipynb) · [Review information leakage](../10-purged-validation/README.md) · [Return to the research map](../../README.md)
