# STARTER FILE — READ ONLY.
#
# `checkpoints/conftest.py` copied me to  answers.py  on first run.
# Edit that file, not this one. If you delete answers.py, the next
# `uv run check.py NN` will regenerate it from this starter.

"""
Week 08 checkpoints — recursion and self-similar geometry.

Edit answers.py (copied from this starter). Run from the repository root:

    uv run check.py 08

Every function here must be recursive AND pure: no list defined outside the
function that the calls append into. See README section 4 for why.
"""

import math

import compas.geometry as cg


def factorial(n):
    """Return n! = n * (n-1) * ... * 1, recursively.

    factorial(0) -> 1     (this is the mathematical convention, not a mistake)
    factorial(5) -> 120

    A negative number has no factorial: raise ValueError.

    Hint: base case first, then the recursive case. If you get RecursionError,
    your recursive case is not moving toward the base case.
    """
    raise NotImplementedError("factorial")


def flatten(nested):
    """Flatten an arbitrarily nested list into a single flat list.

    flatten([1, [2, [3, 4]], 5])  ->  [1, 2, 3, 4, 5]
    flatten([])                   ->  []

    The nesting can be any depth, so a fixed number of loops will not do --
    this is recursion over STRUCTURE rather than over a number, which is the
    more useful of the two patterns.

    Hint: loop over the items. If an item is itself a list, flatten it and
    extend; otherwise append it. `isinstance(item, list)` is your test.
    """
    raise NotImplementedError("flatten")


def sierpinski(a, b, c, depth):
    """Return the triangles of a Sierpinski subdivision.

    Each triangle is a tuple of three compas.geometry.Point objects.

    - depth 0 -> [(a, b, c)]                 the triangle itself, 1 of them
    - depth 1 -> 3 triangles, each at one corner, half the size
    - depth d -> 3**d triangles

    The rule: find the midpoints of the three edges, then recurse on the three
    corner triangles (a, ab, ca), (ab, b, bc), (ca, bc, c). The middle triangle
    is the hole and is NOT recursed into.

    Parameters
    ----------
    a, b, c : compas.geometry.Point
    depth : int -- 0 or greater; negative raises ValueError

    Returns
    -------
    list[tuple[Point, Point, Point]]

    Hint: the midpoint of two Points p and q is
        cg.Point(*[(p[i] + q[i]) / 2 for i in range(3)])
    Build your result by CONCATENATING what the three recursive calls return.
    """
    raise NotImplementedError("sierpinski")


def tree_segments(length, angle_degrees, depth, scale=0.7):
    """Return the line segments of a 2D branching tree, growing upward from the origin.

    Each segment is a tuple (start_point, end_point) of compas.geometry.Point.

    Rules
    -----
    - depth 0 -> []                       (no tree at all)
    - depth 1 -> one trunk, from (0,0,0) straight up to (0, length, 0)
    - at the tip of every branch, two shorter branches grow: one rotated
      +angle_degrees, one rotated -angle_degrees (about the Z axis), each
      `scale` times the length of its parent
    - a tree of depth d has 2**d - 1 segments

    Parameters
    ----------
    length : float          -- length of the trunk
    angle_degrees : float   -- branching angle, in DEGREES
    depth : int             -- 0 or greater; negative raises ValueError
    scale : float           -- how much each generation shrinks

    Returns
    -------
    list[tuple[Point, Point]]

    Hints
    -----
    - Write a small recursive helper that takes (start_point, direction_vector,
      length, depth) -- passing the direction along is much easier than
      accumulating a total angle.
    - Rotate a direction vector with
        cg.Rotation.from_axis_and_angle([0, 0, 1], math.radians(angle))
      and `vector.transformed(R)`.
    - Stay pure: return a new list from each call and concatenate. Do NOT
      append into a list defined outside the function.
    """
    raise NotImplementedError("tree_segments")
