"""
Week 07 checkpoints — object-oriented programming.

Edit ONLY this file. Run from the repository root:

    uv run check.py 07

This is a self-paced week. Read test_tasks.py whenever a docstring here is
not specific enough -- and note how much of the "spec" for a class is really
a list of small promises about how it behaves.
"""

import math

import compas.geometry as cg


class Vector2D:
    """A 2D vector.

    Must support:
        Vector2D(3, 4)                  -> an instance with .x and .y
        repr(v)                         -> exactly "Vector2D(3, 4)"
        v1 + v2                         -> a NEW Vector2D
        v1 == v2                        -> True when x and y both match
        v.length                        -> a PROPERTY (no parentheses), 5.0 here
        v.unitized()                    -> a NEW Vector2D of length 1

    Hints
    -----
    - `__repr__` must return a string, not print one.
    - `__add__(self, other)` is what makes `+` work.
    - `length` is derived from x and y, so it is a @property -- if you store it
      in __init__ it goes stale the moment anyone changes .x
    - unitizing a zero-length vector is impossible; raise ValueError.
    """

    def __init__(self, x, y):
        raise NotImplementedError("Vector2D.__init__")


class Rectangle:
    """An axis-aligned rectangle, positioned by its lower-left corner.

    Must support:
        Rectangle(width, height, x=0, y=0)
        r.area                  -> PROPERTY, width * height
        r.perimeter             -> PROPERTY, 2 * (width + height)
        r.contains(px, py)      -> True if the point is inside or on the edge
        repr(r)                 -> "Rectangle(3, 4, at (0, 0))"

    A rectangle with a zero or negative dimension is not a rectangle: raise
    ValueError from the constructor rather than allowing a broken object to
    exist. An object that can never be in an invalid state is one you never
    have to check again.
    """

    def __init__(self, width, height, x=0, y=0):
        raise NotImplementedError("Rectangle.__init__")


class Square(Rectangle):
    """A Rectangle whose sides are equal.

    Must support:
        Square(5)          -> a 5 x 5 rectangle at (0, 0)
        Square(5, x=2)     -> ... at (2, 0)
        s.area             -> 25, inherited, NOT reimplemented
        isinstance(Square(1), Rectangle)   -> True

    Hints
    -----
    - Call `super().__init__(...)` to run Rectangle's constructor.
    - Do NOT redefine `area` or `perimeter`. Inheriting them is the point; a
      second copy of that formula is a second thing that can be wrong.
    """

    def __init__(self, side, x=0, y=0):
        raise NotImplementedError("Square.__init__")


class Wall:
    """The Week 06 wall, as a class -- and still part of the CORE layer.

    Must support:
        wall = Wall(n_courses=8, length=2.0, thickness=0.3,
                    course_height=0.2, offset=0.1)
        wall.height          -> PROPERTY: n_courses * course_height
        wall.to_boxes()      -> list[compas.geometry.Box], bottom course first
        repr(wall)           -> "Wall(8 courses, 1.60 m tall)"

    Geometry rules (identical to Week 06 -- reuse what you worked out then):
        - course i spans z from i*course_height to (i+1)*course_height
        - odd courses (1, 3, 5...) are offset along X by `offset`
        - even courses are centred on x = 0
        - the wall sits on z = 0

    `n_courses` below 1 raises ValueError from the constructor.

    This class must stay PURE: no viewer, no files, no print. A checkpoint
    checks the file for you, the same way Week 06 did.
    """

    def __init__(self, n_courses, length=2.0, thickness=0.3,
                 course_height=0.2, offset=0.1):
        raise NotImplementedError("Wall.__init__")
