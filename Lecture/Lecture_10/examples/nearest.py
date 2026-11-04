"""Nearest neighbours: brute force (O(n^2) for all pairs) vs a spatial hash.

The hash files points in grid cells keyed by (floor(x/r), floor(y/r)); a radius
query only looks at 9 cells. Same answers, very different cost.
W10 geometric README §9.
"""

import math
from collections import defaultdict


def within_brute(points, i, r):
    """Indices of points within distance r of points[i] (excluding i). O(n)."""
    p = points[i]
    return sorted(j for j, q in enumerate(points) if j != i and math.dist(p[:2], q[:2]) <= r)


class SpatialHash:
    """A uniform grid of cell size r over 2D points, for radius queries."""

    def __init__(self, points, r):
        if r <= 0:
            raise ValueError("cell size must be positive")
        self.points, self.r = points, r
        self.cells = defaultdict(list)
        for j, q in enumerate(points):
            self.cells[self._key(q)].append(j)

    def _key(self, p):
        return (math.floor(p[0] / self.r), math.floor(p[1] / self.r))

    def within(self, i, r=None):
        """Indices within distance r (default: the cell size) of points[i]."""
        r = self.r if r is None else r
        if r > self.r:
            raise ValueError("query radius larger than the cell size would miss neighbours")
        p = self.points[i]
        cx, cy = self._key(p)
        found = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in self.cells.get((cx + dx, cy + dy), ()):
                    if j != i and math.dist(p[:2], self.points[j][:2]) <= r:
                        found.append(j)
        return sorted(found)


def all_pairs_brute(points, r):
    return {i: within_brute(points, i, r) for i in range(len(points))}


def all_pairs_hashed(points, r):
    grid = SpatialHash(points, r)
    return {i: grid.within(i) for i in range(len(points))}
