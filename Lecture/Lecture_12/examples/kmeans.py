"""k-means: how few panel families does a curved roof need?

Assign each panel (described by its side lengths) to the nearest family
template, move each template to its panels' mean, repeat. Inertia never
increases; more clusters always fit better, so choose k by tolerance
(families_needed). This is Lloyd's algorithm on data. W12 learning README §1.
"""

import numpy as np


def kmeans_pp_init(X, k, rng):
    centres = [X[rng.integers(len(X))]]
    for _ in range(1, k):
        d2 = np.min(((X[:, None, :] - np.array(centres)[None, :, :]) ** 2).sum(axis=2), axis=1)
        centres.append(X[rng.choice(len(X), p=d2 / d2.sum())])
    return np.array(centres, dtype=float)


def kmeans(X, k, n_init=5, max_iter=100, seed=0):
    """Cluster rows of X into k groups.

    Returns (labels, centres, inertia, history) for the best of n_init starts,
    where history is the inertia after each round of that best start.
    """
    X = np.asarray(X, dtype=float)
    if not 1 <= k <= len(X):
        raise ValueError("k must be between 1 and the number of points")
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(n_init):
        centres = kmeans_pp_init(X, k, rng)
        history = []
        for _ in range(max_iter):
            d2 = ((X[:, None, :] - centres[None, :, :]) ** 2).sum(axis=2)
            labels = d2.argmin(axis=1)
            history.append(float(d2[np.arange(len(X)), labels].sum()))
            new = np.array([X[labels == j].mean(axis=0) if (labels == j).any() else centres[j]
                            for j in range(k)])
            if np.allclose(new, centres):
                break
            centres = new
        if best is None or history[-1] < best[2]:
            best = (labels, centres, history[-1], history)
    return best


def roof_panels(n=14, size=14.0, radius=25.0):
    """Side lengths (mm) of the quads of a spherical-cap roof on an n x n plan grid.

    Returns an array of shape (n*n, 2): [width, depth] of each panel, each the
    mean of two opposite edges in 3D.
    """
    h = size / n
    def z(x, y):
        return np.sqrt(radius ** 2 - (x - size / 2) ** 2 - (y - size / 2) ** 2)
    feats = []
    for i in range(n):
        for j in range(n):
            x0, x1, y0, y1 = i * h, (i + 1) * h, j * h, (j + 1) * h
            P = {(a, b): np.array([a, b, z(a, b)]) for a in (x0, x1) for b in (y0, y1)}
            w = (np.linalg.norm(P[x1, y0] - P[x0, y0]) + np.linalg.norm(P[x1, y1] - P[x0, y1])) / 2
            d = (np.linalg.norm(P[x0, y1] - P[x0, y0]) + np.linalg.norm(P[x1, y1] - P[x1, y0])) / 2
            feats.append((w * 1000, d * 1000))
    return np.array(feats)


def worst_deviation(X, labels, centres):
    """Largest |panel side - its family's template side| over all panels (same units as X)."""
    return float(np.abs(X - centres[labels]).max())


def families_needed(X, tolerance, k_max=30, seed=0):
    """Smallest k whose worst deviation is within tolerance. Returns (k, result)."""
    for k in range(1, k_max + 1):
        result = kmeans(X, k, seed=seed)
        if worst_deviation(X, result[0], result[1]) <= tolerance:
            return k, result
    raise ValueError(f"no k up to {k_max} meets a tolerance of {tolerance}")
