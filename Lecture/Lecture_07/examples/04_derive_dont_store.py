"""@property: a value computed from the others, read like an attribute.

    uv run Lecture/Lecture_07/examples/04_derive_dont_store.py
"""

import math


class StoredBeam:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = math.dist(start, end)         # computed once, now


class Beam:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @property
    def length(self):
        return math.dist(self.start, self.end)      # computed every time you ask


stale = StoredBeam((0, 0, 0), (0, 0, 2400))
fresh = Beam((0, 0, 0), (0, 0, 2400))
stale.end = (0, 0, 3000)
fresh.end = (0, 0, 3000)
print("stored: ", stale.length)                     # 2400.0: wrong, and silent
print("derived:", fresh.length)                     # 3000.0

# No parentheses, and it refuses assignment: there is nothing stored to overwrite.
try:
    fresh.length = 5000
except AttributeError as error:
    print("AttributeError:", error)
