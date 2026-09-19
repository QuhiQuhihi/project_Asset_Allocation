"""Transparent Black–Litterman updates and finite-scenario expected shortfall.

These are teaching calculations for explicitly supplied one-period inputs, not
estimators of market equilibrium, scenario probabilities, or view confidence.
"""

from dataclasses import dataclass

import numpy as np
from scipy.optimize import linprog, minimize


def _covariance(value, name="covariance", positive_definite=False):
    matrix = np.asarray(value, dtype=float)
    if (
        matrix.ndim != 2
        or matrix.shape[0] != matrix.shape[1]
        or not matrix.size
        or not np.isfinite(matrix).all()
    ):
        raise ValueError(f"{name} must be a finite symmetric square matrix")
    magnitude = np.max(np.abs(matrix))
    normalized = matrix / magnitude if magnitude > 0 else matrix
    if not np.allclose(normalized, normalized.T, atol=1e-12, rtol=1e-10):
        raise ValueError(f"{name} must be symmetric")
    eigenvalues = np.linalg.eigvalsh(normalized)
    if eigenvalues[0] < -1e-12 or (positive_definite and eigenvalues[0] <= 0):
        raise ValueError(f"{name} has invalid eigenvalues")
    return matrix


def _vector(value, length, name):
    vector = np.asarray(value, dtype=float)
    if vector.shape != (length,) or not np.isfinite(vector).all():
        raise ValueError(f"{name} must have {length} finite entries")
    return vector


def _probabilities(probabilities, count):
    if count < 1:
        raise ValueError("At least one scenario is required")
    values = (
        np.full(count, 1 / count)
        if probabilities is None
        else _vector(probabilities, count, "probabilities")
    )
    if np.any(values < 0) or not np.isclose(values.sum(), 1, atol=1e-12, rtol=1e-10):
        raise ValueError("Probabilities must be nonnegative and sum to one")
    return values / values.sum()  # Remove only round-off in an already valid vector.


def _cap(max_weight, count):
    if not np.isfinite(max_weight) or not 1 / count <= max_weight <= 1:
        raise ValueError("The weight cap must lie between 1 / assets and 1")
    return float(max_weight)


@dataclass(frozen=True)
class BlackLittermanResult:
    implied_mean: np.ndarray
    posterior_mean: np.ndarray
    mean_covariance: np.ndarray
    predictive_covariance: np.ndarray


def black_litterman(covariance, reference_weights, risk_aversion, picks, views, omega, tau=0.05):
    """Condition a Gaussian prior on linear noisy views of expected excess returns.

    Sigma describes return noise conditional on the unknown mean. The prior mean
    is delta * Sigma * reference_weights, and its uncertainty is tau * Sigma.
    Return M = Var(mean | views), separately from predictive Var(return | views)
    = Sigma + M. A no-view update preserves the prior, including its uncertainty.
    Omega is the covariance of view errors, not an investor confidence percentage.
    """
    covariance = _covariance(covariance, positive_definite=True)
    count = len(covariance)
    reference = _vector(reference_weights, count, "reference_weights")
    if np.any(reference < 0) or not np.isclose(reference.sum(), 1, atol=1e-10):
        raise ValueError("Reference weights must be long-only and sum to one")
    if not np.isfinite(risk_aversion) or risk_aversion <= 0:
        raise ValueError("Risk aversion must be positive")
    if not np.isfinite(tau) or tau <= 0:
        raise ValueError("tau must be positive")
    picks = np.asarray(picks, dtype=float)
    if picks.ndim != 2 or picks.shape[1] != count or not np.isfinite(picks).all():
        raise ValueError("picks must have one column per asset")
    views = _vector(views, len(picks), "views")
    omega = np.asarray(omega, dtype=float)
    if omega.shape != (len(picks), len(picks)):
        raise ValueError("omega must have one row and column per view")
    implied = risk_aversion * covariance @ reference
    prior_covariance = tau * covariance
    if len(picks):
        omega = _covariance(omega, "omega", positive_definite=True)
        cross_covariance = prior_covariance @ picks.T
        view_covariance = picks @ cross_covariance + omega
        gain = np.linalg.solve(view_covariance, cross_covariance.T).T
        posterior = implied + gain @ (views - picks @ implied)
        mean_covariance = prior_covariance - gain @ cross_covariance.T
    else:
        posterior, mean_covariance = implied.copy(), prior_covariance.copy()
    mean_covariance = (mean_covariance + mean_covariance.T) / 2
    return BlackLittermanResult(implied, posterior, mean_covariance, covariance + mean_covariance)


def quadratic_allocation(mean, covariance, risk_aversion=1.0, max_weight=1.0, min_return=None):
    """Long-only, fully invested maximum quadratic utility; optional mean floor.

    A supplied min_return is tested against the mean argument. Use
    minimum_variance_allocation for a pure minimum-variance objective with an
    independently supplied return forecast and optional return floor.
    """
    covariance = _covariance(covariance)
    count = len(covariance)
    mean = _vector(mean, count, "mean")
    if not np.isfinite(risk_aversion) or risk_aversion <= 0:
        raise ValueError("Risk aversion must be positive")
    return _quadratic_solve(mean, covariance, risk_aversion, max_weight, mean, min_return)


def minimum_variance_allocation(covariance, mean, min_return=None, max_weight=1.0):
    """Minimize variance with the same mean floor and cap as a scenario ES rule."""
    covariance = _covariance(covariance)
    mean = _vector(mean, len(covariance), "mean")
    return _quadratic_solve(np.zeros(len(mean)), covariance, 1.0, max_weight, mean, min_return)


def _quadratic_solve(objective_mean, covariance, delta, cap, constraint_mean, min_return):
    count = len(covariance)
    cap = _cap(cap, count)
    bounds = [(0.0, cap)] * count
    if min_return is not None and not np.isfinite(min_return):
        raise ValueError("min_return must be finite")
    feasible = linprog(
        np.zeros(count),
        A_ub=None if min_return is None else -constraint_mean[None, :],
        b_ub=None if min_return is None else [-min_return],
        A_eq=np.ones((1, count)),
        b_eq=[1.0],
        bounds=bounds,
        method="highs",
    )
    if not feasible.success:
        raise ValueError("The return floor and weight constraints are infeasible")
    constraints = [{"type": "eq", "fun": lambda w: w.sum() - 1, "jac": lambda w: np.ones(count)}]
    if min_return is not None:
        constraints.append(
            {
                "type": "ineq",
                "fun": lambda w: constraint_mean @ w - min_return,
                "jac": lambda w: constraint_mean,
            }
        )
    scale = max(np.max(np.abs(delta * covariance)), np.max(np.abs(objective_mean)))
    if scale == 0:
        scale = 1.0
    result = minimize(
        lambda w: (delta * w @ covariance @ w / 2 - objective_mean @ w) / scale,
        feasible.x,
        jac=lambda w: (delta * covariance @ w - objective_mean) / scale,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"ftol": 1e-12, "maxiter": 1000},
    )
    if (
        not result.success
        or abs(result.x.sum() - 1) > 1e-8
        or (min_return is not None and constraint_mean @ result.x < min_return - 1e-8)
    ):
        raise RuntimeError(f"Quadratic allocation failed: {result.message}")
    return result.x


def empirical_expected_shortfall(losses, alpha=0.95, probabilities=None):
    """Average the worst exactly (1-alpha) probability mass, splitting boundary ties.

    Positive loss means a loss. Negative expected shortfall is allowed when even
    the worst tail is profitable. alpha=0 returns the unconditional mean loss.
    """
    losses = np.asarray(losses, dtype=float)
    if losses.ndim != 1 or not np.isfinite(losses).all():
        raise ValueError("losses must be a finite vector")
    if not np.isfinite(alpha) or not 0 <= alpha < 1:
        raise ValueError("alpha must lie in [0, 1)")
    probabilities = _probabilities(probabilities, len(losses))
    order = np.argsort(-losses, kind="stable")
    mass = probabilities[order]
    preceding_mass = np.r_[0.0, np.cumsum(mass)[:-1]]
    included_mass = np.minimum(mass, np.maximum(0, 1 - alpha - preceding_mass))
    return float(included_mass @ losses[order] / (1 - alpha))


@dataclass(frozen=True)
class ExpectedShortfallResult:
    weights: np.ndarray
    expected_shortfall: float
    threshold: float
    mean_return: float


def expected_shortfall_allocation(
    returns, alpha=0.95, probabilities=None, max_weight=1.0, min_return=None
):
    """Rockafellar–Uryasev finite-scenario LP, with explicit scenario probabilities.

    Variables are weights, a free loss threshold, and nonnegative excess losses.
    A minimizing threshold need not equal the lower empirical VaR when the loss
    distribution has a gap; the objective is still exactly expected shortfall.
    """
    returns = np.asarray(returns, dtype=float)
    if returns.ndim != 2 or not returns.shape[1] or not np.isfinite(returns).all():
        raise ValueError("returns must be a finite scenarios-by-assets matrix")
    scenarios, count = returns.shape
    probabilities = _probabilities(probabilities, scenarios)
    if not np.isfinite(alpha) or not 0 <= alpha < 1:
        raise ValueError("alpha must lie in [0, 1)")
    cap = _cap(max_weight, count)
    mean = probabilities @ returns
    objective = np.r_[np.zeros(count), 1.0, probabilities / (1 - alpha)]
    inequalities = np.column_stack([-returns, -np.ones(scenarios), -np.eye(scenarios)])
    limits = np.zeros(scenarios)
    if min_return is not None:
        if not np.isfinite(min_return):
            raise ValueError("min_return must be finite")
        inequalities = np.vstack([inequalities, np.r_[-mean, np.zeros(scenarios + 1)]])
        limits = np.r_[limits, -min_return]
    result = linprog(
        objective,
        A_ub=inequalities,
        b_ub=limits,
        A_eq=np.r_[np.ones(count), np.zeros(scenarios + 1)][None, :],
        b_eq=[1.0],
        bounds=[(0.0, cap)] * count + [(None, None)] + [(0.0, None)] * scenarios,
        method="highs",
    )
    if not result.success:
        raise ValueError(f"Expected-shortfall allocation failed: {result.message}")
    weights = result.x[:count]
    direct = empirical_expected_shortfall(-returns @ weights, alpha, probabilities)
    if not np.isclose(direct, result.fun, atol=1e-8, rtol=1e-7):
        raise RuntimeError("LP objective disagrees with independently sorted tail losses")
    return ExpectedShortfallResult(weights, direct, float(result.x[count]), float(mean @ weights))
