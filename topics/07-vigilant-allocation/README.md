# Vigilant allocation: rank strength, count weakness

A portfolio can have an attractive leading asset while weakness spreads through the rest of its opportunity set. Vigilant Asset Allocation (VAA) makes that breadth information part of the allocation decision: relative momentum selects holdings, while the number of weak assets controls the defensive allocation. Keller and Keuning introduced this combination in [their 2017 VAA paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3002624).

[Open the worked notebook](study.ipynb) · [Back to the research collection](../../README.md)

## Strategy design

The chapter separates three operations: measure each asset's price momentum, count non-positive scores in the risky universe, and rank eligible holdings within the risky and defensive universes. The notebook uses the unscaled score

$$M_t=12R_{1,t}+4R_{3,t}+2R_{6,t}+R_{12,t},\qquad R_{h,t}=P_t/P_{t-h}-1.$$

The heavier weight on recent performance makes the score react more quickly to a reversal than a twelve-month return alone. Its numerical value is a composite score, not a forecast annual return. A common positive rescaling would preserve both rankings and the zero threshold. Crucially, inputs are prices: dividing one daily return by another is a different quantity and can become undefined near zero.

The worked rule has four fictional risky assets, two defensive assets, one risky holding and a breadth threshold of one. If every risky score is positive, hold the strongest risky asset. If any risky score is non-positive, hold the strongest defensive asset. A separate threshold-of-two illustration shows a 50% defensive allocation when exactly one risky score is weak. This fractional illustration describes the breadth mechanism; it does not reproduce every portfolio-size rounding rule in the published variants.

## What the notebook shows

Three constructed scenarios share twelve-month histories with an explicitly altered final month. The first has broad positive momentum. The second leaves the strongest risky asset unchanged but makes one other asset weak. The third introduces broader declines. Score and weight charts show why a change outside the selected holding can change the entire portfolio. A constant-growth path supplies an independent arithmetic check of the four-horizon formula; a flat asset checks that zero counts as weak.

The notebook also checks portfolio budgets, invalid input rejection and future-price invariance. Signal, execution and first earned return are separate steps. No performance metric is inferred from these signal snapshots, and a defensive asset is not assumed to be risk-free merely because it occupies the defensive sleeve.

## Interpretation and boundaries

Breadth adds an exposure decision to an asset-selection decision. It can reduce participation when deterioration is widespread, but its threshold can also trigger frequent exits and late re-entry. Universe composition matters: adding a weak asset can change exposure even if that asset would never win the ranking. Correlation among the monitored assets affects how much independent information the count contains.

This chapter renews the original `06_vigilant_asset_allocation_with_momentum.ipynb` topic with a readable price-based calculation. All inputs are **constructed educational paths**; this is neither a fresh backtest nor a verified replication of a named VAA historical portfolio. The repository's separate empirical study uses its own declared defensive-momentum adaptation. Continue to [DAA and canary signals](../08-defensive-allocation/README.md) to see what changes when the monitored universe differs from the investment universe.
