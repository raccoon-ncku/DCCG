# Week 06 — Software Engineering I: the dual-mode architecture

> ⭐ **This is the hinge of the course.** Everything before it was learning
> Python. Everything after it — the agent work, the tests, the final project —
> assumes the structure you build today.
>
> `uv run check.py 06`

## 1. The problem

Here is a script of the kind everyone writes at this point:

```python
from compas.geometry import Box, Frame
from compas_viewer import Viewer

viewer = Viewer()
for i in range(12):
    h = 0.1 + i * 0.05
    box = Box(1, 0.5, h, frame=Frame([0, 0, i * 0.3], [1,0,0], [0,1,0]))
    viewer.scene.add(box)
viewer.show()
```

It works. It also has no future, for five separate reasons:

1. **You cannot test it.** The interesting logic — the heights, the spacing —
   is welded to a window. To check the geometry you must look at it.
2. **You cannot reuse it.** Want this wall inside Grasshopper? Rewrite it.
3. **You cannot version it meaningfully.** Git stores the code, but no record
   of what it produced. "Did my change break anything?" is unanswerable.
4. **An agent cannot work on it.** No return value, no result to inspect — a
   coding agent is blind to whether it succeeded. (This becomes concrete in
   Week 11.)
5. **It cannot run anywhere but your laptop.** No CI, no server, no headless
   machine.

Every one of those follows from a single mistake: **the geometry logic and the
program's contact with the outside world are tangled together.**

## 2. The fix: three layers

```
┌────────────────────────────────────────────────────────────┐
│ 1. CORE      pure Python + COMPAS. Numbers in, geometry    │  tested by pytest
│              out. No viewer, no file IO, no print, no      │  written by you
│              Rhino. Runs anywhere.                         │  or by an agent
├────────────────────────────────────────────────────────────┤
│ 2. ARTIFACT  COMPAS JSON. The verified result, produced    │  committed to git
│              headlessly. Previewable without Rhino.        │  reviewable in a diff
├────────────────────────────────────────────────────────────┤
│ 3. ADAPTER   a thin script for Rhino 8 / Grasshopper that  │  boring on purpose
│              loads the artifact (or calls the core) and    │  contains NO logic
│              converts. Deleting it changes nothing.        │
└────────────────────────────────────────────────────────────┘
```

As files:

```
project/
├── core.py       # def running_bond_wall(length, height, ...) -> list[Box]
├── runner.py     # calls the core, writes output/wall.json
├── output/
│   └── wall.json # the artifact
├── view.py       # optional: open the artifact in compas_viewer
├── adapters/
│   └── rhino_load.py
└── tests/
    └── test_core.py
```

**The one-sentence rule: keep the intelligence out of the host application.**
Rhino and Grasshopper only ever *receive* results.

### How to tell if you got it right

- Delete `adapters/` → everything still works.
- Uninstall Rhino → the tests still pass.
- `import core` on a machine with no screen → no error.
- Someone reviewing your pull request can see what the geometry *became*,
  because the artifact changed in the diff.

If any of those fail, a layer has leaked.

## 3. What "pure" means, exactly

A pure function:

- depends only on its arguments (no globals, no reading files, no clock, no
  unseeded randomness),
- returns its result rather than printing or drawing it,
- changes nothing outside itself (no writing files, no editing its inputs).

```python
# NOT pure -- reads a global, prints, draws
SPACING = 0.3
def make_wall(n):
    for i in range(n):
        print(f"course {i}")
        viewer.scene.add(Box(...))

# Pure -- everything it needs comes in; everything it does comes out
def make_wall(n_courses, spacing=0.3):
    """Return a list of Boxes, one per course."""
    return [Box(1, 0.5, 0.1, frame=Frame([0, 0, i * spacing], [1,0,0], [0,1,0]))
            for i in range(n_courses)]
```

The second version can be tested, reused in Grasshopper, called by an agent,
and run on a server. Same geometry. The difference is entirely structural.

> **Randomness and time are impurities too.** `random.random()` and
> `datetime.now()` make a function give different answers on different runs,
> which makes it untestable. Pass a `seed` in as an argument (Week 03) and
> the function becomes reproducible without becoming boring.

## 4. Artifacts

```python
import compas

compas.json_dump(boxes, "output/wall.json")   # write
boxes = compas.json_load("output/wall.json")  # read back, as real Boxes
```

Why bother, when you could just re-run the script?

- It is **evidence**. It is what you actually produced, not what you hoped.
- It is **reviewable**. A diff shows the geometry changed even when the code
  change looked harmless.
- It is **portable**. Rhino, Grasshopper, a classmate, and CI all read the same
  file. No shared environment needed.
- It is the **hand-off point** between the part that must be correct (core) and
  the part that must be convenient (viewer, Rhino).

Commit your artifacts. They are small, and they are the record of your work.

## 5. Git, at working strength

You have been committing. Now use it as a safety net so you can be reckless
inside a branch and safe on `main`.

```bash
git switch -c feature/wall-bond     # start a branch
# ... edit, run check.py, commit as you go ...
git add -A && git commit -m "wall: alternate course offset"
git push -u origin feature/wall-bond
```

Then open a **pull request** on GitHub. Even working alone, this is worth it:
the PR page is where you re-read your own diff before it becomes permanent,
and from Week 14 it is where CI reports whether your tests passed.

**Writing a commit message.** Say *why*, not *what* — the diff already shows
what.

```
bad:   "update"  /  "fixed stuff"  /  "changes to wall.py"
good:  "wall: offset odd courses by half a brick"
       "core: raise on zero-length walls instead of returning []"
```

**What not to commit:** `.venv/`, `__pycache__/`, `.env` files with API keys,
100MB meshes. Check `.gitignore` before your first big commit.

**When it goes wrong:**
```bash
git status              # always start here
git diff                # what changed, unstaged
git restore <file>      # throw away changes to one file
git log --oneline -10   # recent history
```

## 6. Environments, and why the lockfile matters

`uv.lock` records the exact version of every package, including the ones your
packages depend on. `uv sync` reproduces that set precisely. This is what makes
"works on my machine" a solvable problem instead of a joke: your machine, mine,
and GitHub's CI runner all get byte-identical dependencies.

```bash
uv sync           # match the lockfile exactly
uv add numpy      # add a dependency -- and commit BOTH changed files
```

`pyproject.toml` and `uv.lock` are source code. Commit them together.

---

## Checkpoints

```bash
uv run check.py 06
```

This week you edit **two** files, because the whole point is that they are
separate:

| File | May contain | May NOT contain |
| ---- | ----------- | --------------- |
| `checkpoints/core.py` | geometry logic | viewer, file IO, `print`, Rhino |
| `checkpoints/runner.py` | calling the core, writing the artifact | geometry logic |

| # | Task |
| - | ---- |
| 1 | `core.stacked_wall(n_courses, ...)` — a real parametric element |
| 2 | `core.wall_height(...)` — a derived value, computed not measured |
| 3 | `core` stays pure — checked by reading your file, not by running it |
| 4 | `runner.build_artifact(path, ...)` — core → JSON, round-tripped |

Checkpoint 3 is unusual and worth understanding: it **parses your `core.py`
and inspects its import statements.** You cannot satisfy it by being careful at
runtime; the forbidden import must not be in the file at all. Architecture
rules are much more useful when something enforces them — otherwise they decay
into good intentions within about two weeks.

## Assignment

📝 [A2 — Parametric element as a pure core + artifact](/Assignment/1_virtual_sculpture/README.md)
is released this week and is exactly this structure, at a larger size.

## Self-test

1. Name three things a pure function may not do.
2. Why commit the artifact when the code that produced it is already committed?
3. Your `core.py` imports `compas_viewer`. Which of the five problems in §1 has
   come back?
4. What does `uv.lock` give you that `pyproject.toml` alone does not?
5. Someone hands you a project. What is the fastest check that its layering is
   real rather than aspirational?
