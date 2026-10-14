# Week 09 — Debrief, then Software Engineering I: the dual-mode architecture

> In person again. We open with a **debrief and peer code review** of Weeks 07
> and 08. Bring your checkpoints, working or not. A stuck checkpoint you can
> describe precisely is more useful to the class than a green one you rushed.
>
> ⭐ **Then the hinge of the course.** Everything before it was learning
> Python and geometry. Everything after it (the tests, the agent work, the
> final project) assumes the structure you build today.
>
> `uv run check.py 09`

This lecture has two parts.

- **Part A — reading code, and files.** What an AI assistant actually is, how
  to review the code it (or a classmate) gives you, and how data gets in and
  out of your program through files and JSON. The debrief uses the first half;
  Part B depends on the second.
- **Part B — the dual-mode architecture.** Core → artifact → adapter: the
  structure every project in this course has from now on.

---

# Part A — Reading code, and files

## A1. What an LLM actually is

You have been using an assistant since Week 01, and you just spent two
self-paced weeks working mostly with it. Here is what it is doing, and it is
less than most people assume.

**A language model predicts plausible continuations of text.** Give it your
code and your question, and it produces what tends to follow text like that.
That is the whole mechanism. It is not executing your code, not checking your
units, not reasoning about your wall.

Three consequences that matter this week:

1. **It is a function, not a colleague.** Same input, same distribution of
   outputs. It has no memory of yesterday, and within one conversation it only
   sees what is on screen. If a constraint matters, it has to be in the prompt.
2. **Fluency is not correctness.** Confident prose, tidy variable names and a
   well-formed docstring are properties of the *writing*. They are not evidence
   about the code. This is the single most expensive misunderstanding available
   to you this semester.
3. **It fails silently and plausibly.** A human who does not know says so. A
   model produces its best guess in the same confident voice it uses when
   right — including inventing methods that do not exist and citing papers that
   were never written.

It follows that it is strongest where a mistake is cheap and obvious —
boilerplate, format conversion, a first draft, explaining unfamiliar code — and
weakest where a mistake is silent: numeric detail, units, edge cases, and
anything that depends on facts about your project it cannot see.

In Week 15 you will build the loop that drives one of these, from scratch, and
this description becomes a piece of code you can read.

### Asking well

The quality of what comes back tracks the specificity of the request more than
anything else you control.

| Instead of | Ask |
| ---------- | --- |
| "write a function for rooms" | "Write `summarise_rooms(rooms)` taking a list of dicts with `name` and `area` keys, returning the count, the total area, and the mean. Decide what an empty list should do and say why." |
| "fix this" | "This raises `KeyError: 'area'` on line 12. Here is the traceback and the input. What causes it?" |
| "is this good?" | "What happens for an empty list? For one item? For a negative area?" |
| "explain dictionaries" | "Explain line by line what `counts[word] = counts.get(word, 0) + 1` does." |

Four habits worth building now:

- **State the signature you want** — name, parameters, what comes back. You
  design the interface; let it fill the body.
- **Paste the real error**, complete, as text.
- **Ask one thing.** Four requests in a prompt get four mediocre answers.
- **Ask it to explain rather than produce** when you are trying to learn.
  Accepted-but-not-understood code is a debt, and Week 13 is when it comes due.

> If you cannot describe what you want precisely enough for a model to build
> it, you have not finished thinking about the problem. That difficulty is
> information. In Week 10 this becomes a formal idea: a brief you can turn into
> a test is a finished brief.

The general, non-course version of this — including where *not* to reach for an
assistant — is on the lab wiki:
[AI Assistants](https://kb.rccn.dev/computation/ai-assistants).

### Reviewing code you did not write

You now know enough Python to review it, and that is the job. It is also
exactly what the debrief asks you to do with a classmate's Week 07–08 code.

Most of the time a model lands it. When it misses, it misses in ways that look
fine — which is why review is a procedure and not a feeling.

**The five places to look first** — nearly every bug you will meet this
semester is one of these:

1. **Off-by-one.** `range(1, n)` vs `range(n)`; slice `stop` is excluded.
2. **Mutable default arguments.** `def f(items=[])` — Week 03's trap. Extremely
   common in generated code.
3. **Silent mutation.** A function that says it returns a new list but
   modifies the one you passed in.
4. **Floats compared with `==`.** Looks right, fails on real data.
5. **Confidently wrong constants and formulas.** Degrees where radians belong;
   a plausible-looking formula that is not the one you asked for.

**How to actually review**, in order:

1. Read the *signature and docstring* first. Is this even the function you
   asked for?
2. Read the body and say out loud what each line does. Anything you cannot
   explain is a finding — either the code is unclear or you do not yet
   understand the problem. Both are blockers.
3. Check the edges: empty input, one item, zero, negative numbers.
4. **Run it on an example where you already know the answer.** Not one it
   suggested — one you chose.

> "It ran without an error" is not evidence that it is correct. Silent wrong
> answers are the expensive kind. This is also why Week 10 exists.

## A2. Files

### Paths — use `pathlib`, always

```python
from pathlib import Path

folder = Path("data")
file = folder / "result.json"      # the / operator joins path parts

file.exists()
file.parent
file.name          # 'result.json'
file.stem          # 'result'
file.suffix        # '.json'
folder.mkdir(parents=True, exist_ok=True)   # create it, no error if present
```

Never build paths by gluing strings with `"/"` or `"\\"` — that breaks between
Windows and macOS, and it is the reason half of all "works on my machine"
problems exist.

**Where does a relative path point?** To your *current working directory* — the
folder your terminal is in, not the folder the script is in. To get a path
relative to the script itself:

```python
HERE = Path(__file__).parent
data = HERE / "data" / "input.json"
```

📄 `../python_examples/7.2.1_path.py` … `7.3_pathlib.py`

### Reading and writing

```python
path = Path("notes.txt")

path.write_text("hello")        # simplest possible write
content = path.read_text()      # and read
```

For anything larger, or line by line, use `with`:

```python
with open(path, "w") as f:
    f.write("hello\n")

with open(path) as f:
    for line in f:
        print(line.rstrip())
```

`with` closes the file for you, **even if an error happens inside the block.**
That is the whole reason it exists.

Modes: `"r"` read (default), `"w"` write — **erases the file first** — `"a"`
append.

📄 `../python_examples/7.1.1_write_file.py`, `7.1.2_with_statement.py`, `7.1.3_read_file.py`

## A3. JSON

JSON is a text format for structured data. Nearly every tool reads it, which
is why it is how your geometry will travel between your code, the viewer, git,
and Rhino.

```python
import json
from pathlib import Path

data = {"name": "wall", "courses": 12, "heights": [0.1, 0.2, 0.3]}

Path("wall.json").write_text(json.dumps(data, indent=2))   # write
loaded = json.loads(Path("wall.json").read_text())          # read back
```

`indent=2` makes the file human-readable *and* diffable in git — so a reviewer
can see what changed between two versions of your design. Always use it.

What JSON can hold: `dict`, `list`, `str`, `int`, `float`, `bool`, `None`.
What it cannot: tuples (they come back as lists), sets, and your own classes.

> COMPAS has its own JSON layer — `compas.json_dump` / `compas.json_load` —
> which *can* store geometry objects, meshes and graphs. You met it in Week 04
> and used it on meshes and graphs in Weeks 05–06. Part B is built on it.

## A4. Handling errors on purpose

Week 03 covered *reading* a traceback — bottom line first — and the errors you
meet most. Dictionaries and files add two more to that list:

| Error | Usually means |
| ----- | ------------- |
| `KeyError` | that dictionary key does not exist — use `.get()` if absence is normal |
| `FileNotFoundError` | the path is wrong, or relative to a different folder than you think |

This week is the other half: failure you **expect**, and choose to handle.

```python
try:
    value = int(user_input)
except ValueError:
    print("That was not a number.")
```

Catch only what you can actually handle, and name it. A bare `except:` swallows
everything — including the typo you have not found yet — and turns a loud,
findable bug into a silent, permanent one.

The distinction is worth stating plainly, because it is a design decision you
will make repeatedly in every core you write from now on:

- A missing key that means **your program is broken** should crash. Let it.
- A missing key that is **a normal situation** deserves `.get()` or a `try`.

Silencing the first kind is how a wall with eleven courses gets built.

📄 `../python_examples/try_statement.py`


---

# Part B — The dual-mode architecture

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
   Week 15.)
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

As files (this week's actual layout):

```
Lecture/Lecture_09/checkpoints/
├── core.py       # def stacked_wall(n_courses, length=2.0, thickness=0.3,
│                 #                   course_height=0.2, offset=0.1) -> list[Box]
│                 # def wall_height(n_courses, course_height=0.2) -> float
├── runner.py     # def build_artifact(path, n_courses=8, **kwargs)
│                 # — calls the core, writes output/wall.json
└── spec/
    └── test_tasks.py    # the checkpoint spec (READ ONLY)
```

The **artifact** — `output/wall.json` — is created the first time you run
`build_artifact`; commit it. The **adapter** — a two-line Rhino script that
loads that artifact — is what you write in Week 14, not this week; the
worked example lives at [`Lecture_12/rhino_load.py`](/Lecture/Lecture_12/rhino_load.py)
for anyone who wants to see it early.

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
and from Week 13 it is where CI reports whether your tests passed.

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
uv run check.py 09
```

This week you edit **two** files, because the whole point is that they are
separate:

| File | May contain | May NOT contain |
| ---- | ----------- | --------------- |
| `checkpoints/answers_core.py` | geometry logic | viewer, file IO, `print`, Rhino |
| `checkpoints/answers_runner.py` | calling the core, writing the artifact | geometry logic |

(`core.py` and `runner.py` are the read-only starters; the first
`uv run check.py 09` copies them to the two `answers_*.py` files you edit.)

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

## Self-test

1. Name three bugs that AI-generated Python commonly contains.
2. Why is "it ran without an error" not evidence that code is correct?
3. Why is `Path("data") / "out.json"` better than `"data/" + "out.json"`?
4. What does `with open(...)` do that a plain `open(...)` does not?
5. Name three things a pure function may not do.
6. Why commit the artifact when the code that produced it is already committed?
7. Your `core.py` imports `compas_viewer`. Which of the five problems in §1 has
   come back?
8. What does `uv.lock` give you that `pyproject.toml` alone does not?
9. Someone hands you a project. What is the fastest check that its layering is
   real rather than aspirational?
