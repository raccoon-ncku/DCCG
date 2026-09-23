# STARTER FILE — READ ONLY.
# Edit  answers_core.py  instead (auto-created from this file on first run).

"""
Week 06 — THE CORE LAYER.

Rules for this file, enforced by checkpoint 3:

    ALLOWED    : math, compas, compas.geometry, your own logic
    NOT ALLOWED: compas_viewer, json, pathlib, os, sys, any rhino module,
                 print(), open(), or writing files

If you find yourself wanting any of those, the thing you want belongs in
runner.py. That split is the entire lesson of this week.
"""

import compas.geometry as cg


def stacked_wall(n_courses, length=2.0, thickness=0.3, course_height=0.2, offset=0.1):
    """Build a wall as a stack of box-shaped courses, alternating in offset.

    The wall runs along X, is `thickness` deep in Y, and grows upward in Z.

    - `n_courses` boxes, stacked one directly on the next
    - course i spans z from  i * course_height  to  (i+1) * course_height
    - every course is `length` long and `thickness` deep
    - ODD-numbered courses (1, 3, 5, ...) are shifted along X by `offset`;
      even ones (0, 2, 4, ...) are centred on x = 0
    - the bottom of the wall sits on z = 0

    Parameters
    ----------
    n_courses : int    -- how many courses; must be at least 1
    length : float     -- length of each course along X
    thickness : float  -- depth along Y
    course_height : float -- height of one course
    offset : float     -- X shift applied to odd courses

    Returns
    -------
    list[compas.geometry.Box] -- bottom course first

    Raises
    ------
    ValueError -- if n_courses is less than 1

    Hint: reuse what you learned in Week 05 about a Box being CENTRED on its
    frame. And remember `i % 2` from Week 03 -- that is your odd/even test.
    """
    raise NotImplementedError("stacked_wall")


def wall_height(n_courses, course_height=0.2):
    """Return the total height of a wall, WITHOUT building it.

    wall_height(10, 0.2)  ->  2.0

    A derived quantity like this belongs in the core next to the thing it
    describes -- so that a caller (an adapter, a cost estimate, a test) can ask
    the question without paying to construct the geometry.

    Raises
    ------
    ValueError -- if n_courses is less than 1
    """
    raise NotImplementedError("wall_height")
