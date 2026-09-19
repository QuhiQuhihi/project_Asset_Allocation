# Kelly allocation: growth, exposure and uncertain probabilities

Kelly allocation asks how much wealth to commit when outcomes repeat and wealth compounds. Maximizing the expected payoff of a single opportunity can favor a large bet that is destructive to repeated wealth growth. Expected logarithmic wealth captures the multiplicative consequence of losses.

## Start with a solvable case

For an even-money opportunity, betting a fraction $f$ of capital changes total wealth by $+f$ with probability $p$ and by $-f$ otherwise. Its expected log growth per round is

$$g(f)=p\log(1+f)+(1-p)\log(1-f).$$

With no short exposure, $0\leq f<1$, the interior optimum is $f^*=2p-1$ when $p>1/2$. A constructed win probability of 55% therefore implies a 10% fraction. The remaining capital is held without interest in this exercise. This exact calculation provides a reference for the numerical optimizer.

## Why fractional exposure enters the discussion

The optimum assumes that the probabilities and payoffs are known and remain applicable. If the true win probability is 51% while a portfolio was sized for 55%, the same exposure can have negative expected log growth. The notebook plots both growth curves and compares the full fraction with a half fraction. Halving exposure is a choice to reduce sensitivity and loss size; it does not guarantee positive growth under a wrong model.

## From a bet to an allocation

For a vector of simple asset returns $r_s$ in scenario $s$, probabilities $p_s$ and cash residual $1-\mathbf1^\top w$, the corresponding illustration maximizes

$$\sum_s p_s\log(1+w^\top r_s),\qquad w\geq0,\quad\mathbf1^\top w\leq1.$$

The notebook includes an original five-scenario, two-asset example. It checks that every scenario has positive gross wealth and that the cash and risky weights respect the budget. Probabilities, return scenarios and horizon are specified directly; no annual growth rate or market-optimal allocation is inferred.

This differs from feeding gross price relatives into a mean/covariance formula and then clipping and normalizing the result. The log objective, wealth domain and feasible set are part of the model. A quadratic approximation can be useful under additional assumptions, but it should not be presented as the exact constrained solution.

## Research limits

Scenario omission, unstable expected returns, serial dependence, costs and borrowing constraints all change the economic interpretation. The original legacy Kelly performance is not reused. This chapter provides a checked growth-allocation illustration; adding Kelly to the empirical contest would require its own prespecified estimation and evaluation design.

[J. L. Kelly Jr., *A New Interpretation of Information Rate* (1956)](https://onlinelibrary.wiley.com/doi/abs/10.1002/j.1538-7305.1956.tb03809.x) is the original methodological reference. Compare [mean–variance allocation](../01-mean-variance/README.md) for a different objective and set of assumptions.

[Open the worked notebook](study.ipynb) · [Return to all strategies](../../README.md)
