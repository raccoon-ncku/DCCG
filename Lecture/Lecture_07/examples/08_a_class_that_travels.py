"""compas.json_dump can save your own class, if it inherits from compas.data.Data.

    uv run Lecture/Lecture_07/examples/08_a_class_that_travels.py

This is how an object gets from your core to a JSON artifact and on to Rhino.
"""

import compas
from compas.data import Data


class Plain:
    def __init__(self, length):
        self.length = length


try:
    compas.json_dumps(Plain(2400))
except TypeError as error:
    print("TypeError:", error)


class Beam(Data):
    def __init__(self, length, width, name=None):
        super().__init__(name=name)                 # Data looks after the name
        self.length = length
        self.width = width

    def __repr__(self):
        return f"Beam({self.name!r}, {self.length}, {self.width})"

    @property
    def __data__(self):
        """What to save: plain values, with the same names __init__ takes."""
        return {"length": self.length, "width": self.width}


post = Beam(2400, 100, name="post")
text = compas.json_dumps(post)
print(text)

back = compas.json_loads(text)
print(type(back).__name__, back.length, back.width)     # Beam 2400 100
