# Week 05 — COMPAS core: primitives and transformations

> Self-contained. `uv run check.py 05` when you are ready.

From here on, everything is geometry. COMPAS is the library the whole course
is built on — and unusually for a CAD-adjacent tool, it is **plain Python that
runs anywhere**: your terminal, a test suite, a server with no screen, and
also inside Rhino and Grasshopper. That property is what makes the Week 06
architecture possible.

## 0. Install

Nothing to do. `uv sync` already installed COMPAS.

```bash
uv run python -c "import compas; print(compas.__version__)"
```

> If you are following an older tutorial, you will find pages of
> `conda install compas_cgal` instructions. Ignore them. This project pins
> everything in `uv.lock`; adding packages by hand is how you break it.

---

## 1. Points and vectors

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

## 2. Planes and frames

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
build the object *in* the frame. Every element you make from Week 06 onward is
positioned by its frame.

📄 `compas_core_examples/2.1_planes.py`, `3.1_frames.py`, `3.2_frame_constructors.py`

## 3. Shapes

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

## 4. Transformations

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

## 5. Seeing your geometry

```python
from compas_viewer import Viewer

viewer = Viewer()
viewer.scene.add(box)
viewer.show()
```

📄 `compas_core_examples/1.4.1_visualization_I.py`, `1.4.2_visualization_II.py`

**But a viewer is not a test.** It shows you *something*; it does not tell you
that something is right. A wall with 11 courses instead of 12 looks exactly
like a wall. From Week 06 the viewer becomes a convenience, and a saved JSON
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

Unlike the `json` module from Week 04, this preserves actual COMPAS objects.
This file is the **artifact** at the centre of next week's architecture.

## 6. Notebooks (optional)

`compas_iypnb/` has the same material as Jupyter notebooks, if you prefer that
way of exploring. Not required.

## 7. Also here

`algorithm_basic_examples/binary_search.py` — an algorithm worth reading for
its own sake, and a good target for "explain every line" practice.

---

## Checkpoints

```bash
uv run check.py 05
```

| # | Task | Exercises |
| - | ---- | --------- |
| 1 | `box_on_ground(x, y, size)` | frames, and the centred-box trap |
| 2 | `move(shape, dx, dy, dz)` | `Translation`, and `transformed` vs `transform` |
| 3 | `rotate_point_about_z(point, degrees)` | `Rotation`, degrees → radians |
| 4 | `grid_of_boxes(nx, ny, spacing, size)` | nested loops that build real geometry |
| 5 | `flatten_to_xy(points)` | projection, and not mutating your input |

Checkpoints 1 and 3 are precisely the two traps flagged above. They are there
because you will hit them anyway; better here, where something tells you.

## Exercises

📝 [Rotating boxes](/Exercise/Lecture_05/README.md) ·
📝 [Project a box to the XY plane](/Exercise/1_Project_box_to_xy_plane/README.md)

## Self-test

1. `Box(2, 2, 2)` is centred at the origin. What is the z of its lowest face?
2. What is the difference between `v.unitize()` and `v.unitized()`?
3. Why does `Rotation.from_axis_and_angle([0,0,1], 90)` not rotate by 90°?
4. `T * R` and `R * T` differ. Which happens first in each?
5. Why is "it looks right in the viewer" not evidence that it is right?
