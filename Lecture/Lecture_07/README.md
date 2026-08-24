# Week 08 — Recursion and self-similar geometry  🚫 *no class this week*

> **2026.10.28 — still at the conference.** Same arrangement as last week:
> read, run, check yourself, push by Sunday. Week 09 opens with a debrief of
> both weeks.

If Week 07 went smoothly, this one is shorter. If Week 07 was a struggle,
finish it first — nothing here depends on classes, so you lose nothing by
doing them in the other order.

---

## 1. The idea

A recursive function calls itself on a smaller version of the same problem.

```python
def factorial(n):
    if n <= 1:          # BASE CASE   -- stop here
        return 1
    return n * factorial(n - 1)   # RECURSIVE CASE -- smaller problem
```

Every recursive function needs exactly two things:

1. A **base case** — a version of the problem small enough to answer outright.
2. A **recursive case** that moves *toward* the base case.

Miss either one and you get `RecursionError: maximum recursion depth exceeded`.
That error means "your function never reached its base case" — read it as a
logic error, not a limit you need to raise.

📄 `recusion_examples/0_recursion.py`, `2_recursion_limit.py`

### Tracing it

```
factorial(4)
= 4 * factorial(3)
= 4 * (3 * factorial(2))
= 4 * (3 * (2 * factorial(1)))
= 4 * (3 * (2 * 1))            <- base case reached, now it unwinds
= 24
```

The calls stack up on the way down and collapse on the way back. Anything you
write **after** the recursive call runs during that unwinding — on the way back
*up*. This trips people up, so try it:

```python
def countdown(n):
    if n == 0:
        return
    print(n)         # on the way down: 3 2 1
    countdown(n - 1)

def countup(n):
    if n == 0:
        return
    countup(n - 1)
    print(n)         # on the way back up: 1 2 3
```

Same structure, one line moved, opposite output. If you can explain why, you
understand recursion.

## 2. When to use it

Recursion is the natural fit when **the data or the geometry is itself nested
or self-similar**:

- a branching tree — each branch is a smaller tree
- a subdivided surface — each patch subdivides the same way
- a fractal — the definition is literally recursive
- a folder containing folders; a nested list; a graph traversal

For a flat sequence, a `for` loop is simpler and faster. Recursion is not a
badge of sophistication; using it where a loop would do is a cost, not a
flourish.

> **Recursion over structure.** The most useful pattern is not `f(n-1)` but
> recursing into a nested *shape*:
> ```python
> def total(items):
>     result = 0
>     for item in items:
>         if isinstance(item, list):
>             result += total(item)     # a list inside a list -- same problem
>         else:
>             result += item
>     return result
> ```

## 3. Self-similar geometry

### Sierpinski triangle

A triangle, split into three half-size triangles at its corners, each split the
same way. Depth `d` produces `3**d` triangles.

The midpoint of two points is `(a + b) / 2` — with COMPAS you can write that
almost literally:

```python
mid = cg.Point(*[(a[i] + b[i]) / 2 for i in range(3)])
```

📄 `recusion_examples/3-0_sierpinski_compas_preparation.py`,
`3-1_sierpinski_compas.py`, `3-2_sierpinski_compas_conditional.py`

`3-2` is worth reading closely: it stops recursing **conditionally** — some
branches go deeper than others. That single change turns a mechanical fractal
into something that can respond to a site, a load, or an attractor. It is the
difference between a pattern and a design.

### Branching trees

```
      \|/     each branch spawns two shorter branches,
       |      rotated by ± an angle, until depth runs out
```

Segments at depth `d`: `2**d - 1`. The growth is why depth 20 is not a good
idea — that is about a million segments.

📄 `recusion_examples/1_turtle_triangle.py`,
`recusion_examples/heightmap_subdivision.ipynb`

## 4. Recursion and purity

A recursive function is easy to write impurely — appending into a list defined
outside itself:

```python
segments = []                      # a global the function reaches out to

def branch(p, d):
    segments.append(...)           # NOT pure: two calls contaminate each other
    branch(..., d - 1)
```

It works once, then breaks the second time you call it, exactly like the
mutable-default bug in Week 04. The pure version returns its own list and
combines the results of its children:

```python
def branch(p, d):
    if d == 0:
        return []
    return [my_segment] + branch(left, d - 1) + branch(right, d - 1)
```

Slightly more thinking, and it stays in the core layer where it belongs.

## 5. Optional: classic algorithms

`bin_packing/` and `convex_hull/` are notebooks on two classic computational
geometry problems — fitting parts onto a sheet, and finding the outline of a
point cloud. **Not examined**, and no checkpoint depends on them, but both are
excellent final-project material with real fabrication uses.

---

## Checkpoints

```bash
uv run check.py 08
```

| # | Task | Exercises |
| - | ---- | --------- |
| 1 | `factorial(n)` | base case and validation |
| 2 | `flatten(nested)` | recursion over structure, not over a number |
| 3 | `sierpinski(a, b, c, depth)` | self-similar geometry, `3**depth` |
| 4 | `tree_segments(length, angle, depth)` | branching, and staying pure |

Checkpoint 4's tests count segments and check lengths rather than looking at a
picture. Get used to that: **a fractal that looks right and has the wrong
number of branches is still wrong**, and only one of those two facts is visible.

## Exercise

📝 [Branching tree](/Exercise/Lecture_07/README.md)

## Assignment

📝 [A3 — Recursion](/Assignment/4_recursion/README.md) is this week's
assignment and is due Week 09. Checkpoint 4 is a working skeleton for it.

## Self-test

1. What are the two things every recursive function must have?
2. `RecursionError` — what has actually gone wrong?
3. Why does moving `print(n)` above or below the recursive call reverse the output?
4. How many triangles does Sierpinski depth 5 produce? How many segments does a binary tree of depth 12?
5. Why is appending to a list defined outside the function a bug rather than a style choice?

## Before Sunday

```bash
uv run check.py 08
git add -A && git commit -m "Week 08: recursion checkpoints"
git push
```
