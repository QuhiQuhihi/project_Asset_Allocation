# Next research questions

The new [robust allocation chapters](../docs/robust-allocation.md) demonstrate estimation,
validation and selection mechanics. The following empirical extensions remain unrun.

1. **Freeze a bounded allocation family for future evaluation.** Record an economically
   justified universe, primary loss/comparator, training window, cap, stress set and all
   attempted alternatives before collecting a later uninspected sample. Keep the historical
   HRP specification separate; do not choose its best lookback from the sensitivity table.
2. **Separate stable decisions from low-risk concentration.** Apply joint block refits to
   rolling training windows, compare sample covariance with shrinkage and constrained rules,
   and report weight dispersion, concentration and risk-matched incremental outcomes. Include
   regime stresses beyond the finite scenarios illustrated in the teaching notebook.
3. **Make economic implementation realistic.** Pin observed cash yields, point-in-time
   instrument eligibility, distribution records and permitted vintage histories. Account for
   executable spreads, size and rebalancing capacity. Investigate how SHY exposure and cash
   accrual explain the existing ETF comparison.
4. **If adding predictive ML, validate its entire selection process.** Define label intervals
   and feature availability; fit preprocessing and tune parameters within training only.
   Assemble nested or combinatorial purged evaluation where justified, then check chronological
   deployment. The current split-mechanics notebook does not claim this pipeline exists.
5. **Preserve the full search record.** Retain failed trials and common-date return paths.
   Assess sensitivity to dependent trials and serially dependent observations before applying
   selection diagnostics to real allocation strategies. The historical record is incomplete
   for a defensible empirical DSR/PBO claim; synthetic examples do not fill that gap.

A VAA/DAA empirical replication needs its original eligible universes and validated signal
definitions. The current teaching chapters distinguish the ideas without claiming that
replication or promoting a new tactical winner.

The six added allocation mechanisms create separate empirical questions. Black–Litterman needs
dated views and a defensible record of confidence calibration; expected-shortfall allocation
needs scenario coverage and out-of-sample tail evaluation; factor allocation needs time-stamped
loadings and residual-risk estimates. Liability-driven work needs actual obligation schedules
and suitable assets. Volatility targeting and CPPI need executable rebalancing assumptions,
observed cash returns and gap scenarios. Their constructed notebooks explain these decisions;
they do not satisfy those empirical prerequisites or become additional ETF backtest trials.
