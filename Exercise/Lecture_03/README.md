# Exercises — Week 05 (COMPAS core)

> Open-ended geometry practice. The [Week 05 checkpoints](/Lecture/Lecture_03/README.md#checkpoints)
> cover the mechanics with a checker; these ask you to *make* something.
>
> These use the viewer, so run them locally: `uv run your_script.py`. If the
> viewer will not open on your machine, build a headless version that saves a
> COMPAS JSON artifact instead (Week 06 style) and you lose nothing.

## 1. Rotating boxes

Create a ring of boxes rotating incrementally around the Z axis, each a
different colour. Use `Rotation.from_axis_and_angle` (remember: **radians** —
`math.radians(deg)`), and colour by index.

![](https://app.rccn.dev/assets/dccg/imgs/exercise_rot_box.jpg)

Push it: make the rotation *and* the height vary together, so the boxes spiral
upward. This is a good candidate to later refactor into a pure core function
(`spiral_of_boxes(count, ...) -> list[Box]`) for Week 06.

## 2. Box projection

Project a box onto a plane. `compas.geometry.Projection.from_plane_and_point()`
builds a projection transformation; apply it to the box's corner points and draw
the flattened result.

![](https://app.rccn.dev/assets/dccg/imgs/exercise_box_projection.gif)

See also the companion exercise
[Project a box to the XY plane](/Exercise/1_Project_box_to_xy_plane/README.md),
and the checkpoint `flatten_to_xy`, which is the pure-function version of the
same idea.

Tip: read the `compas.geometry.Box` and `Projection` docs on
[compas.dev](https://compas.dev) — reading library documentation you are about
to depend on is a course habit, not an optional extra.
