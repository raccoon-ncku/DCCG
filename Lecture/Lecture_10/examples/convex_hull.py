"""Convex hull: Andrew's monotone chain.

Sort the points, walk left-right and back, dropping every point that makes a
right turn (one cross product). O(n log n), all of it in the sort.
W10 geometric README §8.
"""


def cross(o, a, b):
    """z of (a - o) x (b - o). > 0: o->a->b turns left (counter-clockwise)."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points):
    """Return the hull vertices, counter-clockwise, as a list of [x, y, 0].

    Collinear points on the hull's edges are left out: only the corners.
    Fewer than three distinct points cannot have a hull -- ValueError.
    """
    pts = sorted({(p[0], p[1]) for p in points})
    if len(pts) < 3:
        raise ValueError("a hull needs at least three distinct points")

    def half(seq):
        chain = []
        for p in seq:
            while len(chain) >= 2 and cross(chain[-2], chain[-1], p) <= 0:
                chain.pop()                   # the middle point is not a corner
            chain.append(p)
        return chain

    lower = half(pts)
    upper = half(reversed(pts))
    hull = lower[:-1] + upper[:-1]            # each chain ends where the other starts
    if len(hull) < 3:
        raise ValueError("all points are collinear: there is no hull")
    return [[x, y, 0.0] for x, y in hull]


def area(polygon):
    """Signed area (shoelace formula). Positive for counter-clockwise."""
    n = len(polygon)
    return 0.5 * sum(polygon[i][0] * polygon[(i + 1) % n][1] - polygon[(i + 1) % n][0] * polygon[i][1]
                     for i in range(n))
