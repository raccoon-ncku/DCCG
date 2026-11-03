"""A constructor that refuses nonsense, and a second way to make the object.

    uv run Lecture/Lecture_07/class_examples/05_refuse_and_construct.py
"""

import math


class Beam:
    def __init__(self, name, start, end, width=100, height=100):
        if math.dist(start, end) == 0:
            raise ValueError(f"{name}: a beam needs two different ends")
        if width <= 0 or height <= 0:
            raise ValueError(f"{name}: section must be positive, got {width}x{height}")
        self.name = name
        self.start = start
        self.end = end
        self.width = width
        self.height = height

    def __repr__(self):
        return f"Beam({self.name!r}, {self.start} -> {self.end})"

    @classmethod
    def post(cls, name, x, y, height, section=100):
        """A second constructor. cls is the class itself, so this makes a Beam."""
        return cls(name, (x, y, 0), (x, y, height), section, section)


print(Beam.post("corner", 0, 0, 2400))      # Beam('corner', (0, 0, 0) -> (0, 0, 2400))

for bad in (("a", (0, 0, 0), (0, 0, 0)), ("b", (0, 0, 0), (0, 0, 1), -100)):
    try:
        Beam(*bad)
    except ValueError as error:
        print("ValueError:", error)

# You have used one of these all term: Beam.from_centerline in compas_timber,
# Mesh.from_obj and Frame.worldXY in COMPAS.
