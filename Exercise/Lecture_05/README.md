# Exercises — Week 09 (Mesh)

> Open-ended mesh practice. The [Week 09 checkpoints](/Lecture/Lecture_05/README.md#checkpoints)
> build and deform a grid mesh with a checker; these two exercises are looser
> and more visual.
>
> They use the viewer — run locally with `uv run your_script.py`. Example
> starting points are in
> [`Lecture_05/mesh_examples/`](/Lecture/Lecture_05/README.md).

## 1. Colour a mesh by normal direction

Load a mesh (the Stanford bunny in `Lecture_05/mesh_examples/data/` is a good
one), iterate over its vertices, and colour each by its normal direction using
`mesh.vertex_normal(key)`.

![](https://app.rccn.dev/assets/dccg/imgs/exercise_normal_color.png)

Wrap the normal lookup in `try` / `except ValueError` — a degenerate vertex has
no valid normal, and handling that instead of crashing is the failure-path
habit from Week 04.

This is the same "data living on geometry" idea as the `colour_by_height`
checkpoint, driven by a different attribute.

## 2. Deform a mesh with attractors

Start from a sphere or a grid. Place a few attractor points in space. Move each
vertex according to its distance to the nearest attractor, and colour it by that
distance.

![](https://app.rccn.dev/assets/dccg/imgs/exercise_deform_mesh.png)

Note what stays true no matter how far you push the vertices: the **topology
never changes** — same vertices, same faces — exactly as the `deform_by_wave`
checkpoint demonstrated. That invariance is the whole reason a mesh is the right
data structure for this.

This exercise is closely related to **Assignment A2** (the parametric element)
and to `Lecture_05/mesh_applications/` — a good place to find a final-project
direction.
