"""Constructed allocation examples: factor exposures and dated liabilities.

Factor covariances use annual decimal-return units. Liability discounting uses
continuously compounded annual zero rates and times in years. No market inputs.
"""

import numpy as np
from scipy.optimize import linprog, minimize


def _vector(value, name):
    result = np.asarray(value, dtype=float)
    if result.ndim != 1 or not len(result) or not np.isfinite(result).all():
        raise ValueError(f"{name} must be a nonempty finite vector")
    return result


def _covariance(value, size, name):
    result = np.asarray(value, dtype=float)
    if result.shape != (size, size) or not np.isfinite(result).all():
        raise ValueError(f"Invalid {name} shape or values")
    scale = max(float(np.abs(result).max()), np.finfo(float).tiny)
    if not np.allclose(result / scale, result.T / scale, rtol=0, atol=1e-12):
        raise ValueError(f"{name} must be symmetric")
    if np.linalg.eigvalsh(result / scale).min() < -1e-12:
        raise ValueError(f"{name} must be positive semidefinite")
    return result


def factor_decomposition(weights, loadings, factor_cov, residual_cov):
    """Variance attribution for r = B f + epsilon, Cov(f, epsilon) = 0.

    Factor component j is z_j (F z)_j, z = B' w. Correlated factors can
    have negative contributions; the residual is a separate variance component.
    Contributions sum to variance, not volatility; none is clipped to zero.
    """
    w = _vector(weights, "weights")
    b = np.asarray(loadings, dtype=float)
    if b.ndim != 2 or b.shape[0] != len(w) or b.shape[1] < 1 or not np.isfinite(b).all():
        raise ValueError("Invalid asset-by-factor loadings")
    f = _covariance(factor_cov, b.shape[1], "factor covariance")
    d = _covariance(residual_cov, len(w), "residual covariance")
    exposures = b.T @ w
    components = exposures * (f @ exposures)
    residual = float(w @ d @ w)
    return {
        "exposures": exposures,
        "factor_variance": components,
        "residual_variance": residual,
        "variance": float(components.sum() + residual),
    }


def exposure_target_allocation(loadings, residual_cov, target, cap=1.0):
    """Minimum residual variance subject to exact exposures and full funding.

    This is exposure targeting, not equal factor risk contribution. At an exact
    target z, z'Fz is constant, so minimizing residual variance also minimizes
    total variance within the feasible target set. Infeasibility raises clearly.
    """
    target = _vector(target, "target exposures")
    b = np.asarray(loadings, dtype=float)
    if b.ndim != 2 or b.shape[1] != len(target) or not np.isfinite(b).all():
        raise ValueError("Invalid asset-by-factor loadings")
    n = b.shape[0]
    if not n or not np.isfinite(cap) or cap <= 0 or cap > 1 or n * cap < 1:
        raise ValueError("Infeasible long-only weight cap")
    d = _covariance(residual_cov, n, "residual covariance")
    if np.trace(d) <= 0:
        raise ValueError("Positive residual risk is required")
    constraints = np.vstack([np.ones(n), b.T])
    values = np.r_[1.0, target]
    # Remove redundant equalities only after verifying their consistency by LP.
    feasible = linprog(
        np.zeros(n), A_eq=constraints, b_eq=values, bounds=[(0, cap)] * n, method="highs"
    )
    if not feasible.success:
        raise ValueError("Target exposures are infeasible under the allocation constraints")
    _, singular, vh = np.linalg.svd(constraints, full_matrices=True)
    rank = int((singular > singular[0] * 1e-12).sum())
    independent = vh[:rank]
    equality_values = independent @ feasible.x
    scaled = d / np.trace(d)
    result = minimize(
        lambda w: float(w @ scaled @ w),
        feasible.x,
        jac=lambda w: 2 * scaled @ w,
        bounds=[(0, cap)] * n,
        constraints={
            "type": "eq",
            "fun": lambda w: independent @ w - equality_values,
            "jac": lambda w: independent,
        },
        method="SLSQP",
        options={"ftol": 1e-13, "maxiter": 1000},
    )
    if (
        not result.success
        or np.max(np.abs(constraints @ result.x - values)) > 1e-8
        or result.x.min() < -1e-9
        or result.x.max() > cap + 1e-9
    ):
        raise ValueError("Factor-target allocation failed numerical validation")
    return result.x


def cashflow_measures(times, amounts, zero_rates):
    """PV, dollar duration and dollar convexity for deterministic cash flows.

    Dollar duration is -dPV/d(delta), where delta is a parallel additive shift
    to continuously compounded zero rates. Dollar convexity is d2PV/d(delta)2.
    Cash-flow dates and amounts remain frozen during all shifts.
    """
    t = _vector(times, "cash-flow times")
    cf = _vector(amounts, "cash-flow amounts")
    rates = np.asarray(zero_rates, dtype=float)
    if len(t) != len(cf) or (t <= 0).any() or (cf < 0).any() or cf.sum() <= 0:
        raise ValueError("Positive future times and nonnegative funded cash flows required")
    if rates.ndim == 0:
        rates = np.full_like(t, rates)
    if rates.shape != t.shape or not np.isfinite(rates).all():
        raise ValueError("Rates must be a finite scalar or one per cash flow")
    pv_cashflows = cf * np.exp(-rates * t)
    if not np.isfinite(pv_cashflows).all() or pv_cashflows.sum() <= 0:
        raise ValueError("Invalid discounted cash flows")
    pv = float(pv_cashflows.sum())
    dollar_duration = float(t @ pv_cashflows)
    return {
        "pv": pv,
        "duration": dollar_duration / pv,
        "dollar_duration": dollar_duration,
        "dollar_convexity": float(t**2 @ pv_cashflows),
    }


def match_liability_zeros(liability_times, liability_amounts, asset_times, zero_rate, capital):
    """Match PV and dollar duration with two long-only zero-coupon bonds.

    Capital must cover liability PV. The hedge uses exactly that PV; any excess
    remains in zero-duration cash, without silently borrowing to close a deficit.
    Two distinct asset maturities must bracket the liability's PV-weighted time.
    """
    if np.asarray(zero_rate).ndim != 0 or not np.isfinite(zero_rate):
        raise ValueError("The base curve must be a finite flat continuous rate")
    liabilities = cashflow_measures(liability_times, liability_amounts, zero_rate)
    times = _vector(asset_times, "asset maturities")
    if len(times) != 2 or (times <= 0).any() or times[1] <= times[0]:
        raise ValueError("Two increasing positive asset maturities required")
    if not np.isfinite(capital) or capital < liabilities["pv"] - 1e-10:
        raise ValueError("Insufficient capital for the fully funded liability hedge")
    duration = liabilities["duration"]
    if duration < times[0] - 1e-12 or duration > times[1] + 1e-12:
        raise ValueError("Liability duration is outside the long-only maturity range")
    # Amounts here are present-value dollars, not bond face values or weights.
    market_values = liabilities["pv"] * np.array(
        [
            (times[1] - duration) / (times[1] - times[0]),
            (duration - times[0]) / (times[1] - times[0]),
        ]
    )
    return {
        "market_values": market_values,
        "face_values": market_values * np.exp(zero_rate * times),
        "cash": max(0.0, float(capital - liabilities["pv"])),
        "liability_pv": liabilities["pv"],
    }
