"""Binary search: halve what is left until one answer remains.

find() looks an item up in a sorted list. bisect() finds where a yes/no answer
flips, for any yes/no that flips once; divide_by_length() uses it to split an
arch into ribs of equal length. W10 README §2.
"""

import math


def linear_search(items, target):
    """Index of target in items, or -1, looking at every item in turn."""
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1


def find(items, target, trace=None):
    """Index of target in the sorted list items, or -1.

    trace, if given, is a list that receives the window (left, right) still
    searched before each look.
    """
    left, right = 0, len(items) - 1
    while left <= right:
        if trace is not None:
            trace.append((left, right))
        mid = (left + right) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            left = mid + 1          # the target can only be right of mid
        else:
            right = mid - 1         # ... or left of it
    return -1


def bisect(test, lo, hi, tol=1e-9, trace=None):
    """The x in [lo, hi] where test(x) turns from False to True, within tol.

    test(lo) must be False and test(hi) True; otherwise there is nothing to find.
    """
    if test(lo) or not test(hi):
        raise ValueError("test must be False at lo and True at hi")
    while hi - lo > tol:
        if trace is not None:
            trace.append((lo, hi))
        mid = (lo + hi) / 2
        if test(mid):
            hi = mid
        else:
            lo = mid
    return hi


def parabola(span, rise):
    """The height z(x) of a parabolic arch from x = 0 to x = span."""
    return lambda x: 4 * rise * x * (span - x) / span**2


def arc_length(z, a, b, steps=400):
    """Length of the curve (x, z(x)) from x = a to x = b, as a fine polyline."""
    xs = [a + (b - a) * i / steps for i in range(steps + 1)]
    return sum(math.dist((x0, z(x0)), (x1, z(x1))) for x0, x1 in zip(xs, xs[1:]))


def divide_by_length(z, a, b, n):
    """n + 1 values of x that split the curve from a to b into n pieces of equal length."""
    if n < 1:
        raise ValueError("n must be at least 1")
    total = arc_length(z, a, b)
    xs = [a]
    for k in range(1, n):
        target = total * k / n
        xs.append(bisect(lambda x: arc_length(z, a, x) >= target, a, b, tol=1e-6))
    return xs + [b]
