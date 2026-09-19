# Defensive allocation: separate the warning signal from the holdings

Defensive Asset Allocation (DAA) separates **what to own** from **what to monitor**. Momentum ranks the investment universe, while a designated canary universe determines how much capital moves to defense. Keller and Keuning introduced that distinction in [their 2018 DAA paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3212862), extending their earlier VAA design.

[Open the worked notebook](study.ipynb) · [Back to the research collection](../../README.md)

## Three roles in the portfolio

The risky universe supplies prospective return-generating holdings. The canary universe supplies warning indicators. The defensive universe supplies the assets held when exposure is reduced. These are logical roles: in some published designs an instrument can belong to more than one universe, so “canary” does not universally mean “never investable.” This exercise makes the sets disjoint to make their separate jobs visible.

Each asset receives the same four-horizon price-momentum score, $12R_1+4R_3+2R_6+R_{12}$. The two canaries represent emerging-equity and aggregate-bond exposure, echoing the economic roles of the paper's selected canary pair. They are constructed index paths rather than actual ETF data. If $b$ canaries have non-positive scores, the illustration assigns $\min(1,b/2)$ to defense. Thus zero, one and two weak canaries imply 0%, 50% and 100% defense. The remaining capital is divided equally between the two highest-ranked risky assets; the strongest defensive asset receives the defensive budget.

This threshold of two and the fractional mixing rule define the exercise. They are not universal DAA parameters or a complete replication of the paper's portfolio-slot conventions. Selecting a risky holding uses relative rank only: a weak risky score does not independently veto a holding when the canaries remain positive.

## What the notebook shows

Four controlled scenarios expose the design distinction. First, every signal is positive. Then one canary declines while investment candidates are unchanged. A third scenario weakens both canaries. Finally, risky assets deteriorate while both canaries remain healthy. The resulting defensive fractions are 0%, 50%, 100% and 0%.

A VAA-style comparison uses the same breadth threshold but counts weakness in the risky universe. Its allocations differ because it observes a different set of signals. The comparison does not establish that either detector is better. The notebook checks that changing a canary affects the exposure budget without changing risky rankings, verifies the price-momentum arithmetic independently, and keeps future prices outside the information set.

## Research implications

A canary rule can remain defensive while the investment universe recovers, or stay exposed while that universe declines. Those are testable tradeoffs, not implementation errors by themselves. Bond canaries and bond defensive holdings also respond to rates and credit conditions; a protective label does not remove duration risk. Correlated canaries can create an illusion of multiple independent warnings.

The original `07_defensive_asset_allocation_with_momentum_monthly.ipynb` used its own canary and defensive choices. This chapter preserves that topic while stating a clean, separate specification. All results are **constructed educational scenarios**, not a fresh backtest or a verified DAA replication. Any empirical extension should predeclare the canary selection procedure and compare missed losses, missed recoveries, turnover and concentration on a genuinely later sample.
