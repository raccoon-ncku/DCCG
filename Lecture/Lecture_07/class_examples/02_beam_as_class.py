"""A class: one definition, as many objects as you like, each with its own values.

    uv run Lecture/Lecture_07/class_examples/02_beam_as_class.py
"""

import math


class Beam:
    """A timber beam: a centreline and a section, in mm."""

    def __init__(self, name, start, end, width, height):
        # __init__ runs once, when the object is made. self is the new object.
        self.name = name
        self.start = start
        self.end = end
        self.width = width
        self.height = height

    def length(self):
        return math.dist(self.start, self.end)

    def volume(self):
        return self.length() * self.width * self.height


post = Beam("post", (0, 0, 0), (0, 0, 2400), 100, 100)
plate = Beam("plate", (0, 0, 2400), (3600, 0, 2400), 100, 100)

print(post.name, post.length())         # post 2400.0
print(plate.name, plate.length())       # plate 3600.0

# Each object keeps its own values.
post.width = 120
print(post.width, plate.width)          # 120 100

# self is the object before the dot. These two lines do the same thing:
print(post.length())                    # 2400.0
print(Beam.length(post))                # 2400.0

# Forgetting self. is the classic first error. Uncomment to see it:
#   def length(self):
#       return math.dist(start, end)    # NameError: name 'start' is not defined
