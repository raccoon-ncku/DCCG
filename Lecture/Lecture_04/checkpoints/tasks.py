# STARTER FILE — READ ONLY.
#
# `checkpoints/conftest.py` copied me to  answers.py  on first run.
# Edit that file, not this one. If you delete answers.py, the next
# `uv run check.py NN` will regenerate it from this starter.

"""
Week 04 checkpoints — dictionaries, then COMPAS primitives and transformations.

Edit answers.py (copied from this starter). Run from the repository root:

    uv run check.py 04

Checkpoints 1-3 are plain Python: dictionaries, and not mutating what you were
given. Checkpoints 4-8 are geometry. Every function here is PURE: it takes
numbers, dictionaries or geometry in and returns a new value out. No printing,
no viewer, no files. That is not a stylistic preference -- it is what makes
these testable at all, and it is the subject of Week 09.
"""

import math

import compas.geometry as cg


def tally(words):
    """Count how many times each word appears.

    tally(["a", "b", "a"])  ->  {"a": 2, "b": 1}
    tally([])               ->  {}

    Returns
    -------
    dict -- word (str) to count (int)

    Hint: the counting pattern in README section 1.
    """
    raise NotImplementedError("tally")


def invert(mapping):
    """Swap the keys and values of a dictionary.

    invert({"a": 1, "b": 2})  ->  {1: "a", 2: "b"}

    Two values could be the same, in which case one key has to win. The
    specification decides which -- see `test_invert_handles_duplicate_values`
    before you implement this. Do not guess.

    Returns
    -------
    dict
    """
    raise NotImplementedError("invert")


def merge_settings(defaults, overrides):
    """Combine two settings dictionaries, with `overrides` winning.

    merge_settings({"a": 1, "b": 2}, {"b": 99})  ->  {"a": 1, "b": 99}

    NEITHER input dictionary may be modified. This is the whole point of the
    checkpoint: a function that quietly edits its arguments is a bug that
    surfaces somewhere else entirely, long after you have stopped looking.

    Returns
    -------
    dict -- a NEW dictionary
    """
    raise NotImplementedError("merge_settings")


def box_on_ground(x, y, size):
    """Return a cube of edge length `size` SITTING ON the XY plane at (x, y).

    "Sitting on" means its lowest face is exactly at z = 0, and its centre is
    directly above (x, y).

    box_on_ground(0, 0, 2)  ->  a 2x2x2 cube spanning z from 0 to 2

    Returns
    -------
    compas.geometry.Box

    Hint: a COMPAS Box is CENTRED on its frame, so Box(2,2,2) at the origin
    spans z from -1 to +1. Read the warning in README section 5, then work out
    how high the frame has to be.
    """
    raise NotImplementedError("box_on_ground")


def move(shape, dx, dy, dz):
    """Return a COPY of `shape` moved by (dx, dy, dz).

    The original must NOT be modified -- the caller still needs it.

    Returns
    -------
    the same type of shape that was passed in

    Hint: build a Translation, then use the method that returns a new object
    rather than the one that edits in place. README section 3, the `-ed` rule.
    """
    raise NotImplementedError("move")


def rotate_point_about_z(point, degrees):
    """Return a new Point, rotated about the world Z axis through the origin.

    rotate_point_about_z(Point(1, 0, 0), 90)  ->  Point(0, 1, 0)

    `degrees` is in DEGREES, because that is what a human designing a facade
    thinks in. COMPAS is not. Converting at the boundary of your function --
    so the inside is consistently radians -- is the habit to build.

    Returns
    -------
    compas.geometry.Point
    """
    raise NotImplementedError("rotate_point_about_z")


def grid_of_boxes(nx, ny, spacing, size):
    """Return a list of cubes arranged in an nx by ny grid on the ground.

    - `nx` columns along x, `ny` rows along y
    - centres `spacing` apart
    - the first box is centred over (0, 0); the last over
      ((nx-1)*spacing, (ny-1)*spacing)
    - every box has edge length `size` and sits ON the ground (z >= 0)
    - ordered with x changing fastest: (0,0), (1,0), (2,0), (0,1), ...

    Returns
    -------
    list[compas.geometry.Box] -- nx * ny of them

    Hint: reuse box_on_ground(). Reusing your own tested function instead of
    repeating its logic is the cheapest quality win available to you.
    """
    raise NotImplementedError("grid_of_boxes")


def flatten_to_xy(points):
    """Return a new list of Points with z set to 0 -- a projection onto the ground.

    The input list and the Points inside it must NOT be modified.

    flatten_to_xy([Point(1, 2, 9)])  ->  [Point(1, 2, 0)]

    Returns
    -------
    list[compas.geometry.Point]

    Hint: make new Points rather than editing the ones you were given. If you
    write `p.z = 0` you have just silently changed the caller's data -- the
    merge_settings mutation bug from checkpoint 3, now with geometry.
    """
    raise NotImplementedError("flatten_to_xy")
