"""A beam as a dictionary. It works; these are the places it starts to hurt.

    uv run Lecture/Lecture_07/class_examples/01_beam_as_dict.py
"""

import math


def make_beam(start, end, width, height):
    return {"start": start, "end": end, "width": width, "height": height, "length": math.dist(start, end)}


def volume(beam):
    return beam["length"] * beam["width"] * beam["height"]


post = make_beam((0, 0, 0), (0, 0, 2400), 100, 100)
print("volume:", volume(post) / 1e9, "m3")           # 0.024 m3

# 1. Two copies of one fact drift apart. Move the end and the length stays old.
post["end"] = (0, 0, 3000)
print("length after moving the end:", post["length"])  # 2400.0, and the beam is 3000 long

# 2. Nothing stops nonsense. This beam has no length and a negative width.
broken = make_beam((0, 0, 0), (0, 0, 0), -100, 100)
print("volume of nonsense:", volume(broken))         # -0.0, no complaint

# 3. Printing tells you nothing about what it is, only what is in it.
print(post)

# 4. What keys does a beam have? Which functions work on one? Only reading all
#    the code will tell you. Nothing ties volume() to this dictionary.
