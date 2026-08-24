# Exercises — Week 08 (Recursion)

> Open-ended practice for recursion. The [Week 08 checkpoints](/Lecture/Lecture_07/README.md#checkpoints)
> cover `factorial`, `flatten`, `sierpinski` and `tree_segments` with a checker;
> this is where you make a recursive structure of your own.
>
> Start from the branching-tree examples in
> [`Lecture_07/recusion_examples/`](/Lecture/Lecture_07/README.md).
> `uv run your_script.py`.

## Branching tree, made your own

The example `branch` function calls itself to draw a tree. Read it until you can
explain every line — including *when* each branch is drawn (on the way down the
recursion, or on the way back up?).

Then introduce variation so it stops looking mechanical:

- add spheres at the branch tips;
- vary branch length, thickness, or colour with depth;
- vary the branching angle, or the number of children per branch;
- **randomly stop** some branches early (seed your randomness so you can
  reproduce a tree you like — the `roll_dice` reproducibility idea again);
- make a branch's behaviour depend on its position or height (an attractor).

That last one is the jump from a fractal to a *design*: look at
`Lecture_07/recusion_examples/3-2_sierpinski_compas_conditional.py` for the same
move applied to a Sierpinski triangle.

Keep the segment-generating part pure (return a list of segments; draw
separately) so it could drop into a Week 06 core and be tested the way
`tree_segments` is. A tree that looks right but has the wrong branch count is
still wrong — and only the count is checkable.
