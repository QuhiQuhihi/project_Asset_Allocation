# Hierarchical risk parity: allocate across a correlation tree

HRP uses the structure of dependence to organize portfolio construction. Instead of first finding a single vector that minimizes estimated variance, it groups similar assets, orders them by a tree, and divides capital recursively. The resulting hierarchy is a description of the estimated covariance, not a forecast of future market states.

## From correlations to a portfolio

Pairwise correlations are converted into distances, $d_{ij}=\sqrt{(1-\rho_{ij})/2}$. Similar return behavior produces a small distance. Single linkage builds a hierarchy from these distances; the leaf order then groups related assets for recursive bisection.

At a split into left and right clusters, each cluster's variance is estimated using inverse-variance weights inside that cluster. Capital assigned to the left cluster is $v_R/(v_L+v_R)$, with the remainder assigned to the right. The process repeats until every asset receives a weight. This is the recursive-bisection construction used here; it is not the same objective as equal contribution to total portfolio variance.

## What the notebook shows

Four constructed assets form two correlation blocks, with different individual volatilities. A dendrogram makes the grouping visible and a weight comparison shows how the hierarchy differs from inverse volatility. The calculation reuses the maintained HRP implementation.

An independent two-asset check is particularly useful. With two leaves, the split rule gives weights proportional to inverse variance, not inverse volatility. The notebook checks that result and the fully invested, nonnegative budget. It also verifies that SciPy receives a **condensed pairwise-distance vector**: passing a square distance array would instead ask the library to interpret its rows as observations, producing a different clustering problem.

## What the method can and cannot promise

Avoiding a covariance inverse is useful when estimates are noisy or nearly singular. It does not eliminate estimation risk. The hierarchy can change when correlations move, single linkage can join clusters through a narrow connection, and tie handling or alternative distance definitions can affect the ordering. Low-risk assets can dominate the resulting capital allocation.

In this project's [historical ETF study](../../study.ipynb), that last point is substantive: HRP holds considerable SHY exposure. The primary comparison therefore includes an equal-weight control scaled using prior risk estimates. A small drawdown or attractive hierarchy alone does not establish incremental allocation value. The worked notebook explains the construction; the historical report supplies its separate, uncertain empirical assessment.

## Further reading

[Marcos López de Prado, *Building Diversified Portfolios that Outperform Out-of-Sample*](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2708678) introduces HRP. The title is the cited paper's title, not this project's performance conclusion. See also the [SciPy linkage documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html) for its input conventions.

[Open the worked notebook](study.ipynb) · [Return to all strategies](../../README.md)
