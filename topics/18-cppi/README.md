# CPPI: allocate a cushion and expose the gap risk

[Open the worked notebook](study.ipynb) · [Project overview](../../README.md)

Constant proportion portfolio insurance (CPPI) ties risky investment to the distance between portfolio wealth and a chosen floor. Its appeal is a direct link between a funding objective and risk taking. Its weakness is equally concrete: a price can jump past the level at which the strategy would have reduced exposure.

## Define the floor before defining the cushion

The terminal nominal objective is 80 per initial 100 after $T=80$ trading periods. Cash earns a hypothetical 3% effective annual rate, converted to a daily simple return $r_c$. At the start of period $t$, the floor is the value of cash needed to meet that objective:

$$F_t=\frac{80}{(1+r_c)^{T-t}},\qquad C_t=\max(V_t-F_t,0),\qquad w_t=\min\left(1,\frac{3C_t}{V_t}\right).$$

This floor grows at exactly the cash rate and reaches 80 at maturity. It is not a constant nominal 80 at every prior date, a percentage drawdown stop, or a promise backed by an option or guarantor. The multiplier is three and exposure cannot exceed wealth. When the observed cushion is zero, a fresh decision is entirely cash.

The decision uses pre-fee wealth. A 5 basis point charge applies to each risky dollar bought or sold; the executed target is a fraction of post-fee wealth. Costs therefore consume part of the cushion rather than being paid by external capital. Holdings drift between rebalances and cash earns its stated return. Cash transfers are free, entry costs count, and terminal liquidation is omitted. With an extra period of delay, the already decided weight is queued, not recomputed from the later portfolio value. A stale queued order can remain risky for one period after a breach; the notebook exposes that behavior instead of adding an undocumented emergency override.

## Compare paths with the same risky-asset endpoint

The constructed experiment compares a gradual 40% decline spread across 20 periods with a single 40% jump followed by flat prices. Both share an initial rise and the same subsequent recovery, so the risky asset has the same terminal wealth in both paths. Immediate and delayed CPPI decisions trade each path. A fixed 60% risky allocation provides an additional accounting comparator.

Gradual rebalancing keeps the immediate CPPI portfolio above its floor in this scenario. The discrete gap leaves it below the floor and moves subsequent fresh decisions into cash, missing the recovery. Without fees, cash growth or a binding cap, the one-period cushion change is $C_{t+1}=C_t(1+m r_t)$; a drop exceeding $1/m$ therefore exhausts the cushion before another trade. The notebook verifies the arithmetic directly: starting at 100 with a floor of 80 and multiplier three, 60 is risky; a 40% loss leaves 76. Positive cash returns, fees, caps and delayed decisions change the exact threshold, not the existence of jump risk.

## Make the implementation reviewable

The notebook displays the risky paths, four CPPI wealth paths, risky exposures and distance to the growing floor. Its small table reports terminal wealth, minimum floor gap, executed turnover and fees. Checks cover the analytic loss, zero-cushion cash funding, exact floor growth, delayed decision ownership and conservation of dollars.

A robust extension varies gap size, multiplier, update interval, execution delay and funding assumptions as a declared scenario set. It should also consider default risk in the supposed safe asset and transaction availability during stress. These examples quantify a specified mechanism; they do not estimate protection probabilities or recommend a protected product.

## Source and related ideas

[Perold and Sharpe, *Dynamic Strategies for Asset Allocation*](https://rpc.cfainstitute.org/research/financial-analysts-journal/1988/dynamic-strategies-for-asset-allocation) places CPPI alongside buy-and-hold, constant-mix and option-based portfolio insurance. The finite-horizon floor convention, original scenarios and discrete dollar ledger in this chapter are specified independently. [Volatility targeting](../17-volatility-targeting/README.md) controls predicted risk rather than a wealth cushion; [Kelly growth](../04-kelly-growth/README.md) begins from a different objective again.
