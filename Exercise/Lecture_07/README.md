# Exercises — Week 07 (Object-oriented programming)

> Open-ended practice for classes. The [Week 07 checkpoints](/Lecture/Lecture_07/README.md#checkpoints)
> build `Vector2D`, `Rectangle`, `Square` and `Wall` with a checker; these push
> further. `uv run your_script.py`.

## 1. Vector2D, extended

Beyond the checkpoint version, add:
- a default constructor: `Vector2D()` gives `(0, 0)`;
- a `dot(other)` method returning the dot product;
- a class attribute `name = "Vector2D"` shared by all instances;
- `__mul__` so `v * 3` scales the vector.

Create two vectors and print their sum, their dot product, and `Vector2D.name`.

## 2. Rectangle, extended

Beyond the checkpoint version, add a **class method** `from_two_points(p1, p2)`
that builds a rectangle from two opposite corners. Confirm that `area` and
`perimeter` are read-only properties — assigning to them should fail.

Then ask the design question from the lecture: should `Square` subclass
`Rectangle`, and should a `House` that contains rooms subclass anything? Write
one sentence per case justifying "is-a" vs "has-a".

## 3. Agent-based modelling

Using `drone.py`, `tracing_drone.py` and `dynamic_view_drone.py`, build a
tracing-drone view that combines **attraction and repulsion** behaviour. Each
drone is an object following simple local rules; the interesting behaviour is
emergent.

Run locally (uses the viewer):

```bash
uv run Exercise/Lecture_07/dynamic_view_drone.py
```

This is a natural seed for a final project — many simple objects, local rules,
collective behaviour. See also
[Re-write to OOP](/Exercise/2_re-write_to_oop/README.md).
