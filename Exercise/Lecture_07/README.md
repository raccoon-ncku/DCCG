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

## 3. Re-write to OOP

[Turn an earlier script into classes](/Exercise/Lecture_07/rewrite_to_oop/README.md).
