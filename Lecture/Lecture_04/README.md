# Week 04 — Dictionaries, tuples, and COMPAS core

Two halves this week.

**First**, the last pieces of core Python you need before geometry:
dictionaries (how you attach *meaning* to data) and tuples (fixed records,
like a coordinate). Dictionaries matter more than they look: from next week
on, every vertex, edge and face you work with carries one.

**Second**, COMPAS: points, vectors, frames, shapes and the transformations
that move them. This is the geometry kernel the rest of the course is built
on.

---

## 1. Dictionaries

A list is indexed by position. A dictionary is indexed by a **key** you choose.

```python
room = {
    "name": "studio",
    "area": 45.0,
    "floor": 2,
}

room["name"]              # 'studio'
room["area"] = 47.5       # change a value
room["height"] = 3.2      # add a new key
del room["floor"]         # remove one
```

Keys are usually strings. Values can be anything, including lists and other
dictionaries.

### Reading safely

```python
room["colour"]              # KeyError -- crashes
room.get("colour")          # None -- no crash
room.get("colour", "grey")  # 'grey' -- a default
"area" in room              # True
```

Use `[...]` when a missing key means your program is broken and should stop.
Use `.get(...)` when a missing key is a normal, expected situation. Choosing
deliberately between those two is a small piece of engineering judgment.

### Looping

```python
for key in room:                     # keys
    print(key)

for key, value in room.items():      # keys AND values -- the common one
    print(key, "=", value)

for value in room.values():
    print(value)
```

📄 `python_examples/3.2.1_dictionary.py`, `3.2.2_update_dictionary.py`,
`3.2.3_dictionary_iteration.py`

### The counting pattern

Worth memorising — it turns up constantly:

```python
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
```

### Dictionaries in geometry

This is why we care. A mesh vertex is not just a point; it is a point *with
attributes* — a colour, a load, a material, a fabrication ID. COMPAS stores
exactly that, as dictionaries, on every vertex and face. Next week builds on
this directly: a mesh is the first place in this course where dictionaries do
real geometric work.

## 2. Tuples

A tuple is an unchangeable list, written with parentheses:

```python
point = (3.0, 4.0, 0.0)
x, y, z = point            # unpacking
```

Use a tuple when the collection is a fixed record (a coordinate, an RGB
colour) rather than a growing sequence. Tuples can be dictionary keys; lists
cannot:

```python
cells = {}
cells[(2, 3)] = "occupied"     # a grid cell, keyed by (column, row)
cells[[2, 3]] = "occupied"     # TypeError: unhashable type: 'list'
```

That last trick turns up next week: a mesh edge is identified by a tuple of
two vertex keys, `(u, v)`.

`for key, value in room.items()` was tuple unpacking all along: `.items()`
hands you one `(key, value)` tuple at a time.

📄 `python_examples/3.3_tuples.py`

---

## COMPAS core

From here on, everything is geometry. COMPAS is the library the whole course
is built on, and unusually for a CAD-adjacent tool it is **plain Python that
runs anywhere**: your terminal, a test suite, a server with no screen, and
also inside Rhino and Grasshopper. That property is what makes the Week 09
architecture possible.

### Install

Nothing to do. `uv sync` already installed COMPAS.

```bash
uv run python -c "import compas; print(compas.__version__)"
```

> If you are following an older tutorial, you will find pages of
> `conda install compas_cgal` instructions. Ignore them. This project pins
> everything in `uv.lock`; adding packages by hand is how you break it.

---

## 3. Points and vectors

```python
import compas.geometry as cg

point = cg.Point(19, 25, 7)
vector = cg.Vector(1, 0, 5)

point.x, point.y, point.z      # by name
vector[0], vector[1], vector[2] # or by index -- both work
```

A **Point** is a location. A **Vector** is a direction and a length. They hold
the same three numbers and mean completely different things:

```python
point + vector    # a Point -- "start here, move that way"
point - point     # a Vector -- "the step from one to the other"
vector + vector   # a Vector
```

"Rotate a point about the origin" moves it. "Rotate a vector" only changes its
direction — it has no position to move. Getting these two confused is the
source of a whole category of geometry bugs that look like the object is in the
wrong place for no reason.

```python
v = cg.Vector(3, 4, 0)
v.length            # 5.0
v.unitized()        # a NEW vector of length 1
v.unitize()         # modifies v IN PLACE, returns None
```

> ⚠️ **The `-ed` rule.** Across all of COMPAS: `unitize()`/`transform()`/`scale()`
> change the object in place; `unitized()`/`transformed()`/`scaled()` return a
> new one and leave the original alone. One letter, completely different
> behaviour. When a shape mysteriously moves twice, this is usually why.

📄 `compas_core_examples/1.1_points_and_vectors.py`, `1.2_…operations.py`, `1.3_vector_operations.py`

### Vector maths you will actually use

```python
a.dot(b)      # scalar. 0 means perpendicular. Sign tells you "same side?"
a.cross(b)    # a vector perpendicular to BOTH -- this is how you build a frame
a.angle(b)    # radians
```

## 4. Planes and frames

A **Plane** is a point plus a normal. A **Frame** is a point plus an x-axis and
a y-axis — a full local coordinate system.

```python
frame = cg.Frame(
    cg.Point(15, 24, 3),      # origin
    cg.Vector(1, 0, 0),       # x-axis
    cg.Vector(0, 1, 0),       # y-axis
)

frame.point     # origin
frame.xaxis     # normalised automatically
frame.yaxis
frame.zaxis     # computed for you: xaxis cross yaxis

cg.Frame.worldXY()     # the global origin frame -- the default everywhere
```

**A frame is the single most useful idea in this course.** Rather than
computing rotated coordinates by hand, you place a frame where you want it and
build the object *in* the frame. Every element you make from here on is positioned
by its frame.

📄 `compas_core_examples/2.1_planes.py`, `3.1_frames.py`, `3.2_frame_constructors.py`

## 5. Shapes

```python
box = cg.Box(2, 3, 4)                     # xsize, ysize, zsize, centred on worldXY
box = cg.Box(2, 3, 4, frame=some_frame)   # ... or on a frame you choose

box.xsize, box.ysize, box.zsize
box.volume        # 24.0
box.frame.point   # the CENTRE of the box
box.points        # its 8 corners

cg.Sphere(radius=2)
cg.Cylinder(radius=1, height=5)
```

> ⚠️ **A COMPAS box is centred on its frame, not resting on it.** `Box(2,3,4)`
> spans z from **-2 to +2**, not 0 to 4. To sit a box on the ground, lift its
> frame by half its height. Half the "why is my tower buried in the floor"
> problems in this course are this one fact.

📄 `compas_core_examples/5.1_shapes.py`

## 6. Transformations

A transformation is a 4×4 matrix. You almost never write one out; you build it
with a constructor and apply it.

```python
import math

T = cg.Translation.from_vector([5, 0, 0])
R = cg.Rotation.from_axis_and_angle([0, 0, 1], math.radians(45))
S = cg.Scale.from_factors([2, 2, 2])

moved = box.transformed(T)      # a NEW box
box.transform(T)                # or modify in place
```

> ⚠️ **Angles are radians.** `math.radians(45)` converts. Passing 45 directly
> asks for 45 radians ≈ 2578°, which is roughly 138° — wrong, but plausible
> enough that you may not notice.

### Combining transformations

Multiply them. **Order matters**, and it reads right-to-left — the rightmost
happens first:

```python
X = T * R          # rotate FIRST, then translate
Y = R * T          # translate first, then rotate -- a different result
```

Rotate-then-translate spins the object where it stands and then moves it.
Translate-then-rotate swings it around the origin like a planet. Both are
useful; picking the wrong one is a classic bug.

```python
X.inverted()                    # undo a transformation
cg.Transformation()             # identity: changes nothing
```

📄 `6.1_transformation.py`, `6.2_transformation_class.py`, `6.3.1_transform_I.py`,
`107_inverse_transformation.py`, `108_premultiply_transformations.py`,
`109_pre_vs_post_multiplication.py`

### Rotations, several ways

```python
cg.Rotation.from_axis_and_angle([0, 0, 1], angle)
cg.Rotation.from_euler_angles([rx, ry, rz])
cg.Rotation.from_frame_to_frame(frame_a, frame_b)
```

📄 `116_several_ways_to_construct_rotation.py`, `118_…euler_angles.py`,
`119_…axis_angle_vector.py`

### Frame-to-frame: the one that saves you

To move an object from one coordinate system into another:

```python
X = cg.Transformation.from_frame_to_frame(local_frame, target_frame)
```

Design your element once at the origin, then place copies wherever you like.
This is how a parametric assembly is built.

📄 `102_point_in_frame.py`, `112_transform_multiple.py`, `113_transform_multiple_2.py`

## 7. Seeing and saving your geometry

```python
from compas_viewer import Viewer

viewer = Viewer()
viewer.scene.add(box)
viewer.show()
```

📄 `compas_core_examples/1.4.1_visualization_I.py`, `1.4.2_visualization_II.py`

**But a viewer is not a test.** It shows you *something*; it does not tell you
that something is right. A wall with 11 courses instead of 12 looks exactly
like a wall. From Week 09 the viewer becomes a convenience, and a saved JSON
artifact plus a test becomes the evidence.

If the viewer crashes or refuses to open on your machine — a graphics-driver
problem, not a Python one — you can complete every checkpoint in this course
without it.

### Saving geometry

```python
import compas

compas.json_dump(boxes, "output/boxes.json")     # geometry objects, not plain JSON
boxes = compas.json_load("output/boxes.json")
```

Unlike Python's plain `json` module, this preserves actual COMPAS objects,
and it works the same for a Box, a list of Boxes, or (next week) a whole mesh
with all its attributes. In Week 09 this file becomes the **artifact** at the
centre of the course's architecture.

## 8. Also here (optional)

- [`notebooks/`](notebooks/) has the same COMPAS-core material as Jupyter
  notebooks, with interactive 3D (frames, transformations). Not required. To
  run them: `uv run Lecture/notebooks/copy_to_mywork.py 04`, then
  `uv run jupyter lab MyWork/notebooks`
  ([more](/Lecture/notebooks/README.md#how-to-run-them)).
- `algorithm_basic_examples/binary_search.py` is an algorithm worth reading for
  its own sake, and a good target for "explain every line" practice.
- File handling (`pathlib`, `with open`, plain `json`) is in
  [`../python_examples/`](../python_examples/) as reference. Week 09 teaches it
  properly, at the point where you need it.

---

## Checkpoints

```bash
uv run check.py 04
```

| # | Task | Exercises |
| - | ---- | --------- |
| 1 | `tally(words)` | the counting pattern |
| 2 | `invert(mapping)` | dict iteration, and a case the spec has to decide |
| 3 | `merge_settings(defaults, overrides)` | copying vs mutating |
| 4 | `box_on_ground(x, y, size)` | frames, and the centred-box trap |
| 5 | `move(shape, dx, dy, dz)` | `Translation`, and `transformed` vs `transform` |
| 6 | `rotate_point_about_z(point, degrees)` | `Rotation`, degrees → radians |
| 7 | `grid_of_boxes(nx, ny, spacing, size)` | nested loops that build real geometry |
| 8 | `flatten_to_xy(points)` | projection, and not mutating your input |

Checkpoints 4 and 6 are precisely the two traps flagged above (the centred box
and the radians). They are there because you will hit them anyway; better
here, where something tells you. Checkpoints 3, 5 and 8 are the same lesson
three times: **do not change what you were given.**

## Exercises

📝 [Rotating boxes](/Exercise/Lecture_04/README.md) ·
📝 [Project a box to the XY plane](/Exercise/1_Project_box_to_xy_plane/README.md)

## Self-test

1. When should you use `dict.get(key)` instead of `dict[key]`?
2. Why can `(2, 3)` be a dictionary key when `[2, 3]` cannot?
3. `Box(2, 2, 2)` is centred at the origin. What is the z of its lowest face?
4. What is the difference between `v.unitize()` and `v.unitized()`?
5. Why does `Rotation.from_axis_and_angle([0,0,1], 90)` not rotate by 90°?
6. `T * R` and `R * T` differ. Which happens first in each?
7. Why is "it looks right in the viewer" not evidence that it is right?
