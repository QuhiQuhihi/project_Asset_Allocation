# Robust allocation under estimation error

[Open the worked notebook](study.ipynb) · [Project overview](../../README.md)

An allocation can fit its estimated covariance matrix extremely well and still make an unstable investment decision. Small changes in a sample can move optimized weights toward a different asset; a correlation shift can remove the diversification the optimizer expected. This chapter studies those two failure modes directly.

## Design the decision before inspecting the outcome

The experiment constructs six assets with shared market and group factors. It supplies 126 training observations and 252 independent test observations from a world with stronger common-factor exposure. Expected returns are zero. The purpose is to evaluate risk estimation and portfolio decisions, not to discover an apparent return premium.

Five rules face the same training sample: equal weight, sample minimum variance, Ledoit–Wolf minimum variance with a 35% asset cap, HRP, and capped minimum worst-scenario variance. The equal-weight and uncapped rules identify the effects of estimation and constraints; no claim attributes all differences to the covariance estimator alone. Every setting is fixed in the notebook, including the order of assets that defines a group stress.

For the scenario rule, solve

$$\min_{w,t} t \quad\text{subject to}\quad w^\top\Sigma_s w\le t\ \forall s,\quad \mathbf{1}^\top w=1,\quad 0\le w_i\le0.35.$$

The three covariance scenarios are the training-only shrunk estimate, a blend toward a fully correlated covariance with unchanged marginal volatilities, and a 50% volatility increase in the first three assets. Positive semidefinite matrices make each variance constraint convex. The uncertainty set is an explicit economic assumption; it is not an estimated coverage region. This original example does not claim to reproduce a named robust-optimization paper.

## Inspect stability as well as estimated risk

The notebook reports training volatility, worst declared-scenario volatility, independent test volatility, evaluator-only true test risk, and concentration. It then resamples complete training-day vectors 120 times and refits every estimator and allocation. Half-L1 distance from the initial target weights measures sensitivity to the observed sample. It is not realized portfolio turnover: no holdings have drifted and no trades have been executed.

The independent test world never determines the portfolios, cap, or scenario set. Its true covariance is visible only because this is a constructed experiment. A real study cannot observe that oracle. The bootstrap describes local estimation sensitivity; it does not cover every structural break. Equal weight avoids estimation-driven target changes while retaining market risk. HRP avoids expected-return estimation and matrix inversion, but still depends on sample correlations and clustering choices.

## Connect the example to robust strategy research

Constraints and shrinkage restrict how strongly a portfolio can react to noisy estimates. Stress objectives make the protected scenarios explicit. Neither corrects for selecting a rule after inspecting many backtests. Read [purged validation](../10-purged-validation/README.md) for overlapping-label leakage and [selection diagnostics](../11-backtest-selection/README.md) for multiple trials. The [research design](../../docs/robust-allocation.md) connects these checks to walk-forward allocation, matched-risk controls, costs and an honest research record.

The numerical checks include an analytic diagonal-covariance optimum, a binding-cap solution, a dense-grid two-scenario comparison, covariance-scale invariance and future-data perturbation. The notebook retains every candidate without declaring a winner.

## Sources

[López de Prado's HRP paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2708678) supplies the hierarchical method. [Scikit-learn's Ledoit–Wolf documentation](https://scikit-learn.org/stable/modules/generated/sklearn.covariance.LedoitWolf.html) specifies the analytical identity-target estimator and its original 2004 reference; this differs from constant-correlation shrinkage. [SciPy's SLSQP documentation](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html) describes the constrained solver. The constructed experiment and scenario set are original to this repository.
