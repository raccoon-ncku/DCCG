# STARTER FILE — READ ONLY.
#
# `checkpoints/conftest.py` copied me to  answers.py  on first run.
# Edit that file, not this one. If you delete answers.py, the next
# `uv run check.py NN` will regenerate it from this starter.

"""
Week 05 checkpoints — COMPAS primitives and transformations.

Edit answers.py (copied from this starter). Run from the repository root:

    uv run check.py 05

Every function here is PURE: it takes numbers or geometry in and returns
geometry out. No printing, no viewer, no files. That is not a stylistic
preference -- it is what makes these testable at all, and it is the subject of
next week.
"""

import math

import compas.geometry as cg


def box_on_ground(x, y, size):
    """Return a cube of edge length `size` SITTING ON the XY plane at (x, y).

    "Sitting on" means its lowest face is exactly at z = 0, and its centre is
    directly above (x, y).

    box_on_ground(0, 0, 2)  ->  a 2x2x2 cube spanning z from 0 to 2

    Returns
    -------
    compas.geometry.Box

    Hint: a COMPAS Box is CENTRED on its frame, so Box(2,2,2) at the origin
    spans z from -1 to +1. Read the warning in README section 3, then work out
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
    rather than the one that edits in place. README section 1, the `-ed` rule.
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
    Week 04 mutation bug, now with geometry.
    """
    raise NotImplementedError("flatten_to_xy")
