"""Lloyd relaxation: move each site to the centroid of its (sampled) Voronoi
cell, repeat. Points become irregular but even.

Cells are computed by sampling, so any site shape works. This is k-means on a
site; the energy never increases. W10 geometric README §10.
"""

import math


def samples(width, height, n=60, inside=None):
    """A grid of sample points over [0, width] x [0, height], optionally filtered."""
    pts = []
    for i in range(n):
        for j in range(n):
            p = ((i + 0.5) * width / n, (j + 0.5) * height / n)
            if inside is None or inside(p):
                pts.append(p)
    return pts


def assign(sites, sample_pts):
    """For each sample, the index of its nearest site."""
    return [min(range(len(sites)), key=lambda k: (s[0] - sites[k][0]) ** 2 + (s[1] - sites[k][1]) ** 2)
            for s in sample_pts]


def energy(sites, sample_pts):
    """Sum of squared distances from every sample to its nearest site."""
    return sum(min((s[0] - p[0]) ** 2 + (s[1] - p[1]) ** 2 for p in sites) for s in sample_pts)


def lloyd(sites, sample_pts, rounds=20):
    """Return (new sites, [energy before each round ..., final energy]).

    Each round: assign samples to their nearest site, move every site to the
    mean of its samples. A site with no samples stays where it is.
    """
    sites = [tuple(p[:2]) for p in sites]
    history = [energy(sites, sample_pts)]
    for _ in range(rounds):
        owner = assign(sites, sample_pts)
        sums = [[0.0, 0.0, 0] for _ in sites]
        for s, k in zip(sample_pts, owner):
            sums[k][0] += s[0]
            sums[k][1] += s[1]
            sums[k][2] += 1
        sites = [(sx / c, sy / c) if c else sites[k] for k, (sx, sy, c) in enumerate(sums)]
        history.append(energy(sites, sample_pts))
    return sites, history


def nearest_spacing(sites):
    """For each site, the distance to its nearest other site."""
    return [min(math.dist(p, q) for q in sites if q is not p) for p in sites]
