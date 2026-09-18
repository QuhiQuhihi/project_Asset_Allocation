# From an allocation formula to an investable accounting experiment

A covariance estimator does not earn a return. Holdings earn returns, trade, pay costs and
drift. This distinction determines the experiment: all estimators feed the same engine, and
simple controls share dates, information and trading assumptions.

## Inputs and information

SPY, IEMG, TLT, GLD and SHY give a compact equity, emerging-equity, long-rate, gold and
short-rate universe. They were chosen for interpretable exposures, not inferred optimality.
AGG appears only in the contextual 60/40. SHY is a bond fund with rate risk; residual cash
instead earns an explicit assumed zero return. The source register describes revised adjusted
prices. These do not supply historical order books, delisting outcomes or a point-in-time
universe.

Let r_t be the vector of simple daily returns, and Sigma the covariance of the previous 252
returns. Equal weight uses 1/N. Inverse volatility uses weights proportional to 1/sigma_i.
ERC solves min_x .5 x' Sigma x - sum(log x_i), then normalizes x; its first-order conditions
equalize x_i (Sigma x)_i. This explains the independent diagonal-covariance test.

HRP first converts correlations to distances sqrt((1-rho)/2). SciPy needs a condensed
pairwise-distance vector; a square array means observations. After single-linkage ordering,
recursive bisection assigns each child inversely to its inverse-variance-weighted cluster
variance. The two-asset case reduces to inverse variance, not inverse volatility. A tiny
relative diagonal regularization stabilizes semidefinite samples. Failures are reported.

## Exposure versus construction

For each estimated strategy w, a control scales equal weight q by
min(1, sqrt(w' Sigma w / (q' Sigma q))). This uses only prior information and leaves residual
cash. It approximately matches forecast risk, not realized future risk. Low volatility caused
by SHY concentration must not be sold as a universally better covariance model.

The separate defensive rule uses compounded 21/63/126/252-session price momentum. The
legacy code divided daily returns by older daily returns; that is a different quantity and
could explode near zero. The new rule is explicitly a limited VAA-inspired adaptation.

## Timing and accounting

At the first session's close, trade targets computed through the previous close. Old holdings
earn that session; new weights first earn the following close-to-close return. Pretrade weights
u_i = w_i (1+r_i)/(1+w'r). For cost rate a, solve c=a sum |(1-c) target_i-u_i|.
Both sides of a rotation pay; a full switch can trade almost twice NAV. Cash is residual, so
there is no hidden borrowing or uncharged cash trade. Costs are illustrative, not measured spreads.

A hand calculation begins with 1 cash and a 1% per-side rate. Entry costs .01/1.01. After a
10% gain in the first asset, a complete switch costs .02/1.01 of pretrade NAV. Remaining NAV is
10890/10201 = 1.0675423978. The unit test checks this independently of the engine loop.

## Reading the evidence

The late segment is January 2025–17 September 2026 (partial September); all strategies share
428 sessions. Bootstrap intervals pair identical blocks across strategies. They measure
conditional path uncertainty, not the uncertainty of selecting this universe or refitting the
entire procedure. Full-history and 2022 outcomes are descriptive checks. No variant replaces
the primary after inspection. [Results and implications](02-results.md) · [Exact protocol](../research/PROTOCOL.md).
