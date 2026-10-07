"""Diffusion-limited aggregation: random walkers stick where they touch.

Walkers launch just outside the cluster and are relaunched if they stray;
both speed it up without changing the result. fractal_dimension() is ~1.7.
W11 simulation README §3.
"""

import math
import random

NEIGHBOURS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def grow(n=600, seed=0, sticky_order=True):
    """Grow a cluster of n cells on a square lattice. Returns [(x, y), ...] in arrival order."""
    rnd = random.Random(seed)
    cluster = [(0, 0)]
    occupied = {(0, 0)}
    radius = 1.0
    while len(cluster) < n:
        a = rnd.uniform(0, 2 * math.pi)
        launch = radius + 3
        x, y = int(round(launch * math.cos(a))), int(round(launch * math.sin(a)))
        while True:
            dx, dy = rnd.choice(NEIGHBOURS)
            x, y = x + dx, y + dy
            if x * x + y * y > (radius + 15) ** 2:          # strayed: relaunch
                a = rnd.uniform(0, 2 * math.pi)
                x, y = int(round(launch * math.cos(a))), int(round(launch * math.sin(a)))
                continue
            if (x, y) in occupied:
                continue
            if any((x + ex, y + ey) in occupied for ex, ey in NEIGHBOURS):
                cluster.append((x, y))
                occupied.add((x, y))
                radius = max(radius, math.hypot(x, y))
                break
    return cluster


def radius_of_gyration(cells):
    cx = sum(x for x, _ in cells) / len(cells)
    cy = sum(y for _, y in cells) / len(cells)
    return math.sqrt(sum((x - cx) ** 2 + (y - cy) ** 2 for x, y in cells) / len(cells))


def fractal_dimension(cells):
    """Slope of log(mass) vs log(radius of gyration) over the growth history.

    A filled disc has dimension 2 (mass grows with r^2). DLA clusters measure
    about 1.7 -- "between a line and a surface", which is the precise sense in
    which they are branchy.
    """
    xs, ys = [], []
    for m in (50, 100, 200, 400, len(cells)):
        if m <= len(cells):
            xs.append(math.log(radius_of_gyration(cells[:m])))
            ys.append(math.log(m))
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    return sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / sum((a - mx) ** 2 for a in xs)
