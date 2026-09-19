"""Train-only covariance portfolios and a finite-scenario variance objective.

The stress set is an explicit modeling choice, not a confidence region or a
replication of a published robust-optimization algorithm.
"""

import numpy as np
from scipy.optimize import minimize
from sklearn.covariance import LedoitWolf

from research.allocation import hrp


def minimum_worst_variance(covariances, cap=1.0):
    """Solve min_w max_s w'C_s w on the capped, long-only unit simplex."""
    covs = np.asarray(covariances, dtype=float)
    if covs.ndim != 3 or covs.shape[1] != covs.shape[2] or not len(covs):
        raise ValueError("Expected one or more square covariance matrices")
    n = covs.shape[1]
    if n < 2 or not np.isfinite(covs).all() or not 1 / n <= cap <= 1:
        raise ValueError("Invalid covariance values or infeasible cap")
    variances = np.diagonal(covs, axis1=1, axis2=2)
    if (variances <= 0).any():
        raise ValueError("Positive variances required")
    # Validate relative to covariance magnitude, including very small return units.
    scaled = covs / variances.max()
    if not np.allclose(scaled, scaled.transpose(0, 2, 1), atol=1e-12, rtol=0):
        raise ValueError("Covariance matrices must be symmetric")
    if np.linalg.eigvalsh(scaled).min() < -1e-12:
        raise ValueError("Positive semidefinite matrices required")
    # Common scaling improves numerical conditioning without changing the optimum.
    scaled /= np.diagonal(scaled, axis1=1, axis2=2).mean()
    initial = np.full(n, 1 / n)
    risk0 = np.einsum("i,sij,j->s", initial, scaled, initial).max()

    def constraint(x):
        return x[-1] - np.einsum("i,sij,j->s", x[:-1], scaled, x[:-1])

    def constraint_jac(x):
        return np.column_stack((-2 * np.einsum("sij,j->si", scaled, x[:-1]), np.ones(len(scaled))))

    opt = minimize(
        lambda x: x[-1],
        np.r_[initial, risk0],
        jac=lambda x: np.r_[np.zeros(n), 1.0],
        method="SLSQP",
        bounds=[(0, cap)] * n + [(0, None)],
        constraints=[
            {
                "type": "eq",
                "fun": lambda x: x[:-1].sum() - 1,
                "jac": lambda x: np.r_[np.ones(n), 0.0],
            },
            {"type": "ineq", "fun": constraint, "jac": constraint_jac},
        ],
        options={"ftol": 1e-12, "maxiter": 1000},
    )
    if not opt.success or abs(opt.x[:-1].sum() - 1) > 1e-8 or constraint(opt.x).min() < -1e-8:
        raise ValueError("Portfolio optimization failed to satisfy its constraints")
    return opt.x[:-1]


def covariance_scenarios(cov):
    """Baseline plus two fixed stresses built solely from the training estimate.

    One adds a common covariance component at unchanged marginal volatility.
    The other raises volatility in the first half of the ordered universe.
    """
    cov = np.asarray(cov, dtype=float)
    vol = np.sqrt(np.diag(cov))
    correlated = 0.5 * cov + 0.5 * np.outer(vol, vol)
    scale = np.ones(len(cov))
    scale[: len(cov) // 2] = 1.5
    sector_stress = cov * np.outer(scale, scale)
    return np.stack([cov, correlated, sector_stress])


def allocation_candidates(training_returns, cap=0.35):
    """Five fixed candidates; no validation/test observations enter this function."""
    train = np.asarray(training_returns, dtype=float)
    if train.ndim != 2 or train.shape[0] < 3 or train.shape[1] < 3 or not np.isfinite(train).all():
        raise ValueError("Need a finite training return matrix")
    sample = np.cov(train, rowvar=False, ddof=1)
    if (np.diag(sample) <= 0).any():
        raise ValueError("Constant assets cannot supply estimated risk")
    shrunk = LedoitWolf().fit(train).covariance_
    return {
        "Equal weight": np.full(train.shape[1], 1 / train.shape[1]),
        "Sample GMV": minimum_worst_variance([sample]),
        "Shrunk capped GMV": minimum_worst_variance([shrunk], cap),
        "HRP": hrp(sample),
        "Scenario capped GMV": minimum_worst_variance(covariance_scenarios(shrunk), cap),
    }
