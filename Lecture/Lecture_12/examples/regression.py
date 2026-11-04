"""Regression: a surrogate model, and overfitting.

Least squares on log-features recovers the beam law deflection ~ L^4 h^-3 from
noisy "simulations". Polynomials of rising degree show training error falling
while test error rises. numpy only. W12 learning README §2.
"""

import numpy as np


def fit_linear(X, y):
    """Least squares with an intercept. Returns coefficients [c, b1, b2, ...]."""
    A = np.column_stack([np.ones(len(X)), np.asarray(X, dtype=float)])
    coef, *_ = np.linalg.lstsq(A, np.asarray(y, dtype=float), rcond=None)
    return coef


def predict_linear(coef, X):
    return coef[0] + np.asarray(X, dtype=float) @ coef[1:]


def r2(y, y_hat):
    y, y_hat = np.asarray(y), np.asarray(y_hat)
    return float(1 - ((y - y_hat) ** 2).sum() / ((y - y.mean()) ** 2).sum())


def beam_experiments(n=60, noise=0.05, seed=0, w=2.0, E=11e9, b=0.1):
    """Simulated 'measurements': span L (m), depth h (m), deflection (mm) with noise."""
    rng = np.random.default_rng(seed)
    L = rng.uniform(2.0, 8.0, n)
    h = rng.uniform(0.15, 0.45, n)
    I = b * h ** 3 / 12
    defl = 5 * (w * 1000) * L ** 4 / (384 * E * I) * 1000          # w in kN/m -> N/m; result in mm
    defl *= np.exp(rng.normal(0, noise, n))                        # multiplicative noise
    return L, h, defl


def fit_power_law(L, h, defl):
    """Fit log(defl) = c + a log(L) + e log(h). Returns (c, a, e)."""
    X = np.column_stack([np.log(L), np.log(h)])
    return tuple(fit_linear(X, np.log(defl)))


def split(n, test_fraction=0.3, seed=0):
    """Random train/test index split."""
    idx = np.random.default_rng(seed).permutation(n)
    cut = int(round(n * (1 - test_fraction)))
    return idx[:cut], idx[cut:]


def polynomial_errors(x, y, degrees, train, test):
    """{degree: (train RMSE, test RMSE)} for polynomial fits on the train points."""
    out = {}
    for d in degrees:
        coef = np.polyfit(x[train], y[train], d)
        rmse = lambda idx: float(np.sqrt(np.mean((np.polyval(coef, x[idx]) - y[idx]) ** 2)))  # noqa: E731
        out[d] = (rmse(train), rmse(test))
    return out


def daylight_samples(n=18, noise=0.06, seed=1):
    """A smooth 'true' curve (daylit fraction vs window-to-wall ratio) plus noise."""
    rng = np.random.default_rng(seed)
    x = np.sort(rng.uniform(0.05, 0.9, n))
    y = 1 - np.exp(-3.2 * x) + rng.normal(0, noise, n)
    return x, y
