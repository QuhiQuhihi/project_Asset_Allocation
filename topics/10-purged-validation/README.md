# Purged validation: when has an allocation label finished?

A monthly allocation model can be trained on a forward monthly return, a downside-risk label or the future relative return of stocks and bonds. Consecutive labels then reuse some of the same market observations. Removing a test **row** from training does not remove the future returns shared with adjacent training labels. A robust design needs an explicit information timeline before it needs a more elaborate learner.

## The allocation decision

Suppose a learned signal changes the risky-asset budget. Its training label spans bars $[s_i,e_i]$, while the signal's features are available at $s_i$. For a held-out label $[s_j,e_j]$, this chapter excludes a training observation whenever

$$s_i\le e_j\quad\text{and}\quad e_i\ge s_j.$$

Intervals are **closed**: shared endpoints are conservatively purged. An optional embargo of $E$ integer bars extends each held-out interval's right endpoint to $e_j+E$. For disjoint test intervals the code uses their union, preserving unrelated observations between them. An embargo is a declared dependence buffer; its length must follow the information horizon rather than the most favorable validation score.

## What the notebook investigates

The constructed example has 36 decision dates, five-bar forward log-return labels and features using the current and previous three bars. Six adjacent decisions form the test fold. The notebook shows which training labels overlap that fold, then applies a three-bar post-label embargo. That buffer also prevents the first subsequent training feature from using a return inside the held-out information interval in this particular example.

The resulting split keeps 17 training observations. A separate oracle builds sets of individual information bars and verifies every included and excluded interval. The figure distinguishes test rows, purged rows, embargoed rows and retained training rows.

The worked regression fits a scaler and a fixed ridge model using retained training observations only. A large perturbation of the held-out raw returns leaves those training features, labels and fitted coefficients unchanged. Omitting the embargo exposes subsequent training features to that perturbation; fitting the scaler to all rows exposes its mean as well. These checks isolate two different information paths without presenting a toy regression score as an investment result.

## How this supports robust allocation

A cross-validation split can contain training observations **after** the test period. Purging does not turn that split into a chronological investment simulation, nor does a finite buffer guarantee independence under long-memory or changing market processes. A deployment study still needs past-only estimation, known-at-the-time inputs and an untouched future evaluation period.

When selecting lookbacks, covariance estimators or signal thresholds, an outer evaluation fold must stay outside the inner selection loop. Fit scaling, feature selection and model parameters within each training fold; refit after selecting the setting using only the outer training data. The notebook demonstrates the information boundaries and a training-only fit, **not a complete nested search or combinatorial purged cross-validation system**.

The existing [risk-based ETF case study](../../study.ipynb) does not train on forward labels. Its prior-only covariance and execution checks answer a different timing question. This chapter supplies the additional design needed when introducing supervised allocation signals.

## Sources and next chapter

Marcos López de Prado's [author overview of purging, embargo and CPCV](https://www.quantresearch.org/Innovations.htm) identifies their different roles. His [*Advances in Financial Machine Learning*](https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086), Chapters 7, 9 and 12, develops validation and model-selection design. This chapter provides an original, deliberately small interval implementation and numerical example.

[Open the worked notebook](study.ipynb) · [Continue to backtest selection](../11-backtest-selection/README.md) · [Return to the research map](../../README.md)
