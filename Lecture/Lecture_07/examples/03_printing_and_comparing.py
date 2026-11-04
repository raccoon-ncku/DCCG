"""Double-underscore methods plug your class into Python's own syntax.

    uv run Lecture/Lecture_07/examples/03_printing_and_comparing.py
"""

import math


class Plain:
    def __init__(self, name):
        self.name = name


print(Plain("post"))                    # <__main__.Plain object at 0x...>: useless in a list of 200


class Beam:
    def __init__(self, name, start, end, width, height):
        self.name = name
        self.start = start
        self.end = end
        self.width = width
        self.height = height

    def __repr__(self):
        """What print, lists and error messages show. Write one on every class."""
        return f"Beam({self.name!r}, {math.dist(self.start, self.end):.0f} mm, {self.width}x{self.height})"

    def __eq__(self, other):
        """Makes == compare values. Without it, == asks: is this the very same object?"""
        return (self.start, self.end, self.width, self.height) == (other.start, other.end, other.width, other.height)


a = Beam("a", (0, 0, 0), (0, 0, 2400), 100, 100)
b = Beam("b", (0, 0, 0), (0, 0, 2400), 100, 100)
print([a, b])                           # [Beam('a', 2400 mm, 100x100), Beam('b', 2400 mm, 100x100)]
print(a == b)                           # True: same size and place, whatever the name


class Vector2D:
    """The same idea for arithmetic: define __add__ and + works."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)      # a NEW vector; the inputs stay as they were


print(Vector2D(1, 2) + Vector2D(10, 20))                         # Vector2D(11, 22)
