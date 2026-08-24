# Exercise — Re-write to OOP  (Week 07 companion)

> Open-ended practice alongside the [Week 07](/Lecture/Lecture_08/README.md)
> checkpoints.

Take an earlier procedural script — one of your Python-week exercises, or the
provided `example_random_walker.py` — and re-express it with classes.

The random walker is the ideal candidate: it has **state** (position, radius)
and **behaviour** (take a step), which is exactly when a class earns its place.
Turn the loose variables and functions into a `Walker` object that remembers
what it is between steps:

```bash
uv run Exercise/2_re-write_to_oop/example_random_walker.py
```

Then extend the walker's rules — steering probabilities, radius based on height
or on the previous sphere, a colour scheme. The header comment in the file lists
several directions to try.

Aim for a `Walker` whose geometry logic is pure enough to belong in a Week 06
core: it should be able to *produce* a list of spheres without knowing whether a
viewer exists.
