# Liability-driven allocation: protect the funded surplus

[Open the worked notebook](study.ipynb) · [Explore the allocation ideas](../../README.md)

An institution with future payment obligations needs more than an attractive asset return. Its assets must support the timing and economic value of those liabilities. This chapter builds a dedicated liability hedge, distinguishes capital from bond face value, and tests what a duration match actually protects.

## Start with dated obligations and a funding budget

The constructed liabilities pay 60 units on 19 September 2030 and 70 units on 19 September 2033. At the 19 September 2026 valuation date, two available zero-coupon bonds mature in September 2028 and September 2036. All times use actual days divided by 365; dates are unadjusted. The base discount curve is flat at a continuously compounded 4% annual rate, shared by assets and liabilities. There is no credit spread, inflation linkage, optionality, tax or transaction cost in this bounded example.

For fixed cash flows, present value, dollar duration and dollar convexity are

$$P=\sum_i C_i e^{-y_i t_i},\qquad DD=\sum_i t_i C_i e^{-y_i t_i},\qquad DC=\sum_i t_i^2 C_i e^{-y_i t_i}.$$

Dollar duration is minus the derivative of present value with respect to a parallel additive shift in continuous zero rates. It measures currency sensitivity, not just a percentage duration.

Initial capital equals liability present value: **104.0163 units**. That budget funds the hedge completely and leaves no independent growth allocation. An underfunded request is rejected; the implementation does not borrow silently or label duration matching as a cure for a funding deficit. If the caller supplies additional capital, the residual is reported as explicit zero-duration cash.

## Match present value and dollar duration

Let $x_1,x_2$ be present-value allocations to the two zero bonds. Solve

$$x_1+x_2=L_0,\qquad t_1x_1+t_2x_2=DD_L.$$

The bond face amounts are $x_i e^{yt_i}$. A nonnegative solution requires the two maturities to bracket the liability's PV-weighted payment time. Equal asset and liability percentage duration alone would be insufficient if their present values differed; matching dollar duration is what removes the first derivative of surplus $S=A-L$.

The cash-flow diagram makes an additional limitation visible. A 2028 asset receipt precedes the promised payments, while the 2036 zero pays after them. Reinvestment, reserved cash or asset sales would be needed along the path. The present experiment neither projects those transactions nor assumes their future costs away. Exact payment matching would instead buy zeros with the liability dates and amounts, if those instruments were available.

## Measure the risk that remains

The notebook compares the duration hedge with holding the same initial capital in cash. Both start with zero surplus. Under a small parallel shift $\delta$,

$$\Delta S\approx-(DD_A-DD_L)\delta+\tfrac12(DC_A-DC_L)\delta^2.$$

The linear term vanishes. In this particular barbell construction, asset dollar convexity exceeds liability dollar convexity, leaving a positive local quadratic term. Exact revaluation across ±200 bps shows the approximation's limits.

Declared steepener, flattener and localized liability-date shocks reveal residual curve-shape risk. The steepener creates a **1.706-unit surplus loss** despite the initial duration match. An exact cash-flow match has zero residual under these rate-only scenarios because both sides use the same dated payments and discount factors. That result does not extend to changing liability amounts, inconsistent discount curves, defaults or liquidity stress.

Independent checks solve the funding equations through a separate linear system, reconcile discounted cash flows, verify the finite-difference surplus derivative, and reject insufficient capital or an unspanned liability duration. Every comparison is an instantaneous revaluation with frozen holdings, not an investment return backtest.

## Connect the hedge to robust allocation

An obligation-based objective avoids choosing a portfolio solely because it won a historical return contest. It still depends on uncertain liability dates, amounts, discounting and instrument availability. The next research step is a common-budget comparison of key-rate and cash-flow matching with payment uncertainty, liquidity costs and rebalancing over time. Those extensions are unrun. [Factor risk allocation](../15-factor-risk-allocation/README.md) provides a related way to express the economic exposures behind asset weights.

## Sources

[William Sharpe (2001)](https://web.stanford.edu/~wfsharpe/art/q2001/q2001.htm) motivates pension allocation around the economic relationship between assets and liabilities. [Dariush Akhtari (2026), Society of Actuaries](https://www.soa.org/communities/investment-and-risk-management/newsletter-articles/2026/january/2026-01-ir-akhtari/) discusses limitations of aggregate duration and the role of cash-flow and liquidity stress testing. The cash flows, valuation formulas, matching example and figures here are original calculations.
