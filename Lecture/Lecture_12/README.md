# Lecture 12 — Engineering the Workflow: Tests, Review, Git, and Deploy

> **Weeks 10, 13 and 14.** This is the software-engineering spine of the course.
> Lecture 11 showed that an agent can *write* geometry code. This lecture is the
> harder half: **how do you know it is right, how do you keep it right while
> other authors (human or AI) touch it, and how does it reach your actual design
> tools as something a colleague can install?**
>
> These skills mattered before AI. They matter *more* now, not less — when you
> did not type the code, verification and review are all you have.

The whole lecture is organised around one worked example:
[`plugin_set/`](plugin_set/README.md) — a real Grasshopper plugin set
(`compas_studio`) developed, tested, and deployed **entirely outside Rhino**.
Read this lecture with that folder open.

```
  plan         implement        verify         review          ship
 (human)    (you OR an agent)  (pytest)    (human judgment)   (CI → .ghuser)
   │               │              │              │                │
 executable ──► pure core ──► tests pass? ──► "correct, but ──► componentize
 spec = tests    module        no: iterate     is it GOOD?"      pipeline
```

---

# Part A — Testing (Week 10)

## 1. Testing geometry with pytest

```bash
uv run pytest Lecture/Lecture_12/plugin_set/tests -q      # the plugin-set specs
uv run pytest Lecture/Lecture_12/test_staircase.py -v     # a single file, verbose
```

[`plugin_set/src/compas_studio/staircase.py`](plugin_set/src/compas_studio/staircase.py)
is a **pure function**: numbers in, geometry out. No viewer, no file IO, no
Rhino. That separation — the habit from Week 06 — is exactly what makes it
testable, and what will let the same code become a Grasshopper component in
Part C without changing a line.

The craft of testing geometry, all visible in
[`plugin_set/tests/`](plugin_set/tests/):

- **Test properties, not pictures.** You cannot assert "looks like a
  staircase", but you can assert step count, monotonic ascent, total run,
  nothing floating, no brick past the wall's end, correct Euler characteristic.
  If every invariant holds, the picture takes care of itself.
- **Never `==` on floats.** Computed geometry carries floating-point noise; use
  `pytest.approx` or an explicit tolerance. (The lesson from Week 02, now load-
  bearing.)
- **Test the failure path.** A good function raises on nonsense input instead of
  returning junk. Every core in the plugin set has a
  `test_rejects_nonsense_input`.

## 2. Tests are an executable spec

Read [`plugin_set/tests/test_wall.py`](plugin_set/tests/test_wall.py) as a
**specification** for a running-bond wall: precise, complete, machine-checkable.
Compare it with the prose briefs you wrote in Lecture 11 — no ambiguity about
units, counts, offsets, or tolerances survives translation into a test.

This is the planner's real skill, and the through-line of the whole course:
**a brief you can turn into a test is a finished brief; if you cannot write the
test, you have not finished planning.** It is the same claim the Week 01–09
checkpoints made — the `test_tasks.py` beside each `tasks.py` was this, with
training wheels. Now you write them.

---

# Part B — Review and the test-driven agent (Week 13)

## 3. pytest as the reviewer that cannot be fooled

```bash
uv run Lecture/Lecture_12/tdd_agent.py
uv run Lecture/Lecture_11/view.py Lecture/Lecture_12/output/wall.json
```

[`tdd_agent.py`](tdd_agent.py) replaces Lecture 11's reviewer-LLM with pytest:
the coder agent writes `wall.py`, the harness runs the tests, and failures go
back verbatim until green. An LLM reviewer can be wrong, or argued into
approving; a test suite cannot. This is the single most important upgrade to the
Lecture 11 loop.

But note precisely what the tests do and do not settle:

| Question | Who answers it |
| --- | --- |
| Is it **correct**? | the tests (automated) |
| Is it **good** — clear names, sane structure, no waste? | **you** |
| Was the **spec itself** right? | **you** |

## 4. Correct is not good — the review that remains

Open two files side by side:

- [`wall.py`](wall.py) — the raw output of a small model. It passes
  `test_wall.py`. It is also ~150 lines of the model arguing with itself in
  comments, re-deriving the same offset five times.
- [`plugin_set/src/compas_studio/wall.py`](plugin_set/src/compas_studio/wall.py)
  — the reviewed version. Same behaviour, same passing tests, 20 readable lines.

**The tests cannot tell these apart. A reviewer can.** That gap — everything
that is true of good code but invisible to a test — is what human review is for,
and it does not go away because an AI wrote the code. In this course's final
reviews, "the AI wrote it" is not a defence: if you submitted it, you reviewed
it, and you own it.

### A review checklist

Whether the author is a classmate or an agent, review the same way:

1. **Spec first.** Does it do what was asked — exactly, including units and edge
   cases (0 steps? a wall shorter than one brick?).
2. **Read for intent.** Can you explain every line? If not, the code is unclear
   or you do not yet understand the problem — both are blockers.
3. **Names and structure.** Would a stranger understand it? Is logic separated
   from IO? Is anything computed twice?
4. **Trust nothing implicit.** Magic numbers, silent unit assumptions, unhandled
   failure paths — this is where geometry bugs hide.
5. **Verify independently.** Run the tests yourself; open the artifact; measure
   something. Do not take the author's word, or the agent's.

## 5. Where review actually happens: git and pull requests

Review is a *workflow*, not a feeling, and git is where the workflow lives. The
discipline, even working alone:

```bash
git switch -c feature/canopy-component      # never work on main
# ... write the test, write the core, commit in small steps ...
git add -A && git commit -m "canopy: taper radius toward the apex"
git push -u origin feature/canopy-component
```

Then open a **pull request** on GitHub. The PR is the unit of review:

- it shows a **diff** — the exact change, reviewable line by line, by you or a
  teammate, *before* it becomes permanent;
- CI runs the tests on it automatically (Part C) and marks it red or green;
- the **artifact changes in the diff too** — a reviewer sees not just the code
  but what the geometry *became*, because the committed `.json`/`.ghuser`
  changed;
- nothing reaches `main` until tests pass and a human approves.

This is exactly how you supervise an agent that opens PRs: the loop is
*propose → CI checks → you review the diff → merge or send back*. You stay the
reviewer; the machine stays the author. Write commit messages that say **why**,
not what — the diff already shows what:

```
bad:   "update"   "fixed stuff"   "changes to wall.py"
good:  "wall: place only full bricks; half-bricks were sticking past length"
```

---

# Part C — Deploy: shipping a Grasshopper plugin set (Week 14)

Now the question the whole course has pointed at: **how does pure Python
geometry become a plugin a colleague can install — without you ever pasting code
into Grasshopper by hand?**

## 6. The layered workflow, productised

```
┌──────────────────────────────────────────────────────────────┐
│ 1. CORE      src/compas_studio/*.py — pure Python + COMPAS   │  tested by pytest,
│              numbers in, geometry out, no Rhino              │  built by CI,
│              runs anywhere: laptop, CI, agent harness        │  developed outside Rhino
├──────────────────────────────────────────────────────────────┤
│ 2. SPEC      tests/*.py — the executable brief                │  the CI gate
├──────────────────────────────────────────────────────────────┤
│ 3. ADAPTER   components/Cs_*/code.py — import core, call,     │  thin, boring,
│              convert to Rhino geometry. No logic here.        │  no tests needed
├──────────────────────────────────────────────────────────────┤
│ 4. ARTIFACT  Cs_*.ghuser — the installable component,        │  built by CI on a tag,
│              produced by CI on a Windows runner, no Rhino     │  attached to a Release
└──────────────────────────────────────────────────────────────┘
```

The principle in one line, unchanged since Week 06: **keep the intelligence out
of the host application.** Develop and verify headlessly; let Rhino only
receive results.

## 7. Grasshopper without `rhinoscriptsyntax`

The usual way to write a GH component — type Python into a GHPython node,
reaching for `rhinoscriptsyntax` — produces code that only runs inside a live
Rhino document: untestable, unversionable, invisible to CI and to agents.

We refuse that. COMPAS geometry is **plain Python objects** — a `Box` is a `Box`
with or without Rhino — so the core in `src/compas_studio/` runs and is tested
on any machine. Grep it: no `rhinoscriptsyntax`, no `import Rhino`. The
Grasshopper component becomes a four-line adapter that imports one core function
and converts its output with `compas_rhino.conversions`. See
[`components/Cs_RunningBondWall/code.py`](plugin_set/components/Cs_RunningBondWall/code.py):
there is no geometry logic in it to get wrong.

Each component is a folder of three files:

| File | Purpose |
| --- | --- |
| `code.py` | the adapter — a class with `RunScript(self, inputs...)` returning outputs |
| `metadata.json` | name, category, and the input/output parameters (names must match `code.py`) |
| `icon.png` | a 24×24 icon for the Grasshopper ribbon |

## 8. The Python → `.ghuser` pipeline (COMPAS componentizer)

You do not build components on your laptop, and — the surprising part — you do
**not need Rhino to build them**. The
[COMPAS GHPython componentizer](https://github.com/compas-dev/compas-actions.ghpython_components)
is a GitHub Action that turns each folder in `components/` into a matching
`Cs_*.ghuser` file, on a Windows CI runner, fetching the Grasshopper IO assembly
through NuGet. No Rhino, no display, no manual step.

Two workflows in
[`plugin_set/.github/workflows/`](plugin_set/.github/workflows/) split the two
jobs — this is the CI/CD half of the diagram:

- **`test.yml`** (CI) runs on every push and pull request, on a plain Linux
  runner, because the core is pure: `pip install -e ".[dev]"` then `pytest`.
  This is the gate — nothing merges red.
- **`build.yml`** (CD) runs only on a version **tag**, on `windows-latest`, and
  invokes the componentizer:

  ```yaml
  - uses: compas-dev/compas-actions.ghpython_components@v5
    with:
      source: components
      target: build
      interpreter: cpython     # Rhino 8; use "ironpython" for Rhino 7
  ```

  The `.ghuser` files become a downloadable artifact and are attached to the
  GitHub Release.

Cutting a release is then a deliberate act:

```bash
git tag v0.1.0
git push --tags        # CI builds and publishes the .ghuser files
```

A studio-mate installs the set by dropping the `.ghuser` files into their
Grasshopper `UserObjects` folder — no repo, no Python, no setup.

> ⚠️ **A `.ghuser` forgets its origin.** Once placed in a document it becomes a
> plain GHPython node; a later release does **not** auto-update instances
> already sitting in old `.gh` files. Version deliberately and tell users what
> changed. (A real limitation, worth knowing before you depend on it.)

## 9. The lighter path: JSON artifact + adapter

The full plugin pipeline is worth it for something you will reuse and share. For
a one-off — verify a design headlessly, then look at it once in Rhino — the
Lecture-11/12 artifact route is enough: dump a `compas` JSON file and load it
with [`rhino_load.py`](rhino_load.py) inside Rhino 8's ScriptEditor (`# r: compas`
installs COMPAS into Rhino's Python automatically). Same principle, less
ceremony: intelligence stays outside; Rhino receives a verified artifact.

Also worth knowing (outlook): a Grasshopper Python component can `import
compas_studio` and call the core **live** with sliders as inputs — same tested
core, no artifact in between; and `rhinomcp` exposes the live Rhino document to
an agent as tools (the Lecture 11 step-3 pattern), powerful for sketching but
with no tests, no artifact, no gate — prefer the pipeline for anything you need
to trust.

---

# Part D — The agentic development loop, understood not followed

Everything above assembles into one loop. It is the loop a tool like Claude
Code runs — and the reason to build it by hand across this course is so that
when you use such a tool you are **directing** it, not obeying it.

Adding a new component to the plugin set:

```
1. SPEC     you write tests/test_canopy.py            ← the brief, human
2. CORE     agent writes src/compas_studio/canopy.py  ← delegated, but…
3. VERIFY   CI runs pytest on the PR                   ← the gate, automated
4. REVIEW   you read the diff: correct AND good?       ← judgment, human
5. ADAPTER  add components/Cs_Canopy/ (thin code.py)   ← you
6. SHIP     tag → componentizer builds Cs_Canopy.ghuser ← automated
```

Notice where the human sits: at the **ends** (what to build, whether it is good,
what to ship) and out of the **middle** (typing the geometry, running the tests,
packaging the file). That division is the entire point. The failure mode this
course is built to prevent is the opposite one — a person in the *middle*,
pasting whatever the chatbot produced, understanding none of the stages, unable
to tell a passing-but-bad result from a good one or a green CI run from a
correct design.

You can run every stage of this loop by hand now. That is what lets you hand
the middle to a machine without handing over your judgment.

## Continuous integration recap

Because the core is pure and tested, a robot runs your tests on every commit and
builds your components on every release. You did not configure a magic service;
you wrote two small YAML files (`test.yml`, `build.yml`) that do exactly what you
would do by hand, on someone else's computer, every time — which is all CI/CD
ever is.

## Things to try

1. Add a fourth component end to end (a column grid, a vault). How many rounds
   did the agent need to pass your tests? Which failures were the model's, and
   which were your spec's?
2. Sabotage `plugin_set/src/compas_studio/wall.py` (offset odd courses by a full
   module) and watch which test catches it. A spec is only as good as what it
   catches.
3. Open a pull request against your own plugin set and read your own diff as if a
   stranger wrote it. What would you send back?
4. Break the adapter/metadata agreement: rename an input in `code.py` but not in
   `metadata.json`. What does the componentizer do?
5. Compare `wall.py` and `plugin_set/src/compas_studio/wall.py` line by line.
   Everything different between them is something review catches and tests do
   not. List five of those things.
