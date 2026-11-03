# Lecture 12 — Engineering the Workflow: Test, Review, Scaffold, Ship, and Work with AI

> **Weeks 10 and 13–15.** This is the software-engineering spine of the
> course, in the order you need it:
>
> | Part | Week | The question |
> | --- | --- | --- |
> | [A — Testing](#part-a--testing-week-10) | 10 | how do you know it is right? |
> | [B — Review](#part-b--review-week-13) | 13 | it is right. Is it *good*? |
> | [C — Scaffolding a project](#part-c--scaffolding-a-project-week-13) | 13 | where does everything live, so that tests and review can happen at all? |
> | [D — Shipping with ghuser-builder](#part-d--shipping-grasshopper-components-with-ghuser-builder-week-14) | 14 | how does it reach someone else's Grasshopper? |
> | [E — Working with AI](#part-e--working-with-ai-week-15) | 15 | which of these steps can a machine take, and which can it not? |
>
> AI comes last on purpose: an assistant can write the middle of this pipeline,
> and can only be trusted to once the two ends exist, a test that says what
> correct means and a reviewer who can tell good from passing.

Two folders go with this lecture:

- [`plugin_set/`](plugin_set/README.md): the **worked example**, a plugin set
  developed, tested and shipped outside Rhino. Read Parts A, B and D with it open.
- [`project_template/`](project_template/README.md): the **empty version** of
  the same shape, for you to copy in Part C.

```
  plan         implement        verify         review          ship
 (human)    (you OR an agent)  (pytest)    (human judgment)   (CI → .yak)
   │               │              │              │                │
 executable ──► pure core ──► tests pass? ──► "correct, but ──► ghuser-builder
 spec = tests    module        no: iterate     is it GOOD?"      pipeline
```

---

# Part A — Testing (Week 10)

## 1. Testing geometry with pytest

```bash
uv run pytest Lecture/Lecture_12/plugin_set/tests -q      # the plugin-set specs
uv run pytest Lecture/Lecture_12/test_wall.py -v          # a single file, verbose
```

[`plugin_set/src/compas_studio/staircase.py`](plugin_set/src/compas_studio/staircase.py)
is a **pure function**: numbers in, geometry out. That separation (Week 09) makes
it testable, and lets the same code become a Grasshopper component in Part D.

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
specification for a running-bond wall: units, counts, offsets and tolerances are
all pinned down in a way a prose brief never manages. **A brief you can turn into
a test is a finished brief.** The `spec/test_tasks.py` of each checkpoint was this
all along. Now you write them.

## 3. The test process

A test file is a loop you live in, not something you write at the end:

```
   RED               GREEN              REFACTOR
write one test  ─►  write just enough ─►  tidy the code,   ─► next test
that fails          code to pass it       tests stay green
```

1. **Red.** Write one test for the next thing the function should do, and
   **run it to see it fail**. A test you have never seen fail has told you
   nothing yet: it may be passing for the wrong reason.
2. **Green.** Write the least code that makes it pass. Not the general
   solution; the next step.
3. **Refactor.** Now the tests are a safety net: rename, simplify, delete.
   If they stay green, you changed the code and not its behaviour.

Where it runs:

| When | Command | Catches |
| --- | --- | --- |
| after every change | `uv run pytest -q` | the mistake you made a minute ago |
| before you commit | `uv run pytest -q` again, on a clean save | the file you forgot |
| on every push (Part C) | the same command, on a fresh machine, by CI | "it works on my laptop" |

And when a test fails, **read the failure before touching the code**:

```
>       assert len(bricks) == 12
E       assert 13 == 12
```

The line with `>` is what was claimed. The line with `E` is what happened.
Decide which of the two is wrong, the code or the claim, before you change
either. Changing the test until it passes is not testing.

A bug found later goes the same way: first the test that would have caught it
(red), then the fix (green).

---

# Part B — Review (Week 13)

Tests answer one question. Review answers the others.

| Question | Who answers it |
| --- | --- |
| Is it **correct**? | the tests (automated) |
| Is it **good**: clear names, sane structure, no waste? | a reviewer |
| Was the **spec itself** right? | a reviewer |

## 4. Correct is not good

Open two files side by side:

- [`wall.py`](wall.py) — a first draft, exactly as a small language model
  produced it (Part E shows how). It passes `test_wall.py`. It is also ~150 lines of the model arguing with itself in
  comments, re-deriving the same offset five times.
- [`plugin_set/src/compas_studio/wall.py`](plugin_set/src/compas_studio/wall.py)
  — the reviewed version. Same behaviour, same passing tests, 20 readable lines.

**The tests cannot tell these apart. A reviewer can.** "The AI wrote it" is not a
defence: if you submitted it, you reviewed it, and you own it.

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

Even working alone:

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

The loop is the same whether the author is a classmate, you last month, or an
agent. Write commit messages that say **why**; the diff already shows what:

```
bad:   "update"   "fixed stuff"   "changes to wall.py"
good:  "wall: place only full bricks; half-bricks were sticking past length"
```

### The review process, as steps

1. **Author:** one change per pull request, small enough to read in ten
   minutes. Say in the description *what* it is for and *how you checked it*.
2. **Reviewer:** check out the branch and **run it**: the tests, then the
   thing itself. A review of code you did not run is a review of its
   formatting.
3. **Reviewer:** read the diff against the checklist above. Comment on the
   line, and say what you would do instead, or ask the question you could
   not answer.
4. **Author:** answer every comment, with a change or with a reason. Push to
   the same branch; the PR updates.
5. **Merge** when the tests are green *and* the reviewer can explain the
   change to a third person.

In Week 13 you do this in pairs, on each other's final-project repos: one
real change each, opened as a pull request, reviewed by the other.

---

# Part C — Scaffolding a project (Week 13)

The walkthrough (scaffold, spec, dev, test, on `StudWall`) is
[Week 09 Part C](/Lecture/Lecture_09/README.md#part-c--a-project-that-can-hold-components).
This part is the reference.

## 6. From nothing

The [template](project_template/README.md) is this, plus a first test, a first
component and two CI workflows. Do it once by hand to see there is no magic in it:

```bash
uv init --lib my_tool            # pyproject.toml + src/my_tool/__init__.py
cd my_tool
uv add compas                    # a dependency: written to pyproject.toml, pinned in uv.lock
uv add --dev pytest              # a tool for you, not for your users
mkdir tests components
git init && git add -A && git commit -m "scaffold: empty project"
```

## 7. What each file is for

| File | It answers | You touch it when |
| --- | --- | --- |
| `pyproject.toml` | what is this, which Python, which libraries | you add a dependency (`uv add`, never by hand) |
| `uv.lock` | *exactly* which versions, on every machine | never by hand. Commit it |
| `src/my_tool/__init__.py` | what does this package offer | you add a public function or class |
| `src/my_tool/*.py` | the logic | most of the time |
| `tests/test_*.py` | what does correct mean | **before** you touch `src/` (Part A §3) |
| `components/*/code.py` | how does Grasshopper call it | you add a component |
| `components/*/metadata.json` | its name, inputs and outputs in Grasshopper | the same moment |
| `.github/workflows/test.yml` | run the tests on every push | once |
| `.github/workflows/build-ghuser.yml` | build the components; release on a tag | once (Part D) |

---

# Part D — Shipping Grasshopper components with ghuser-builder (Week 14)

**How does pure Python geometry become something a colleague installs in
Grasshopper, without you ever pasting code into a component by hand?**

## 8. Grasshopper without `rhinoscriptsyntax`

Code typed into a GHPython node, reaching for `rhinoscriptsyntax`, only runs inside
a live Rhino document: it cannot be tested, versioned, or seen by CI or an agent.
COMPAS geometry is plain Python objects, so the core in `src/compas_studio/` runs
and is tested anywhere, and the component shrinks to an adapter: a fixed header
that finds the core, then a few lines that call it and convert with
`compas_rhino.conversions`. See
[`Cs_StudWall/code.py`](plugin_set/components/Cs_StudWall/code.py).

Each component is a folder of three files:

| File | Purpose |
| --- | --- |
| `code.py` | the adapter — a class with `RunScript(self, inputs...)` returning outputs |
| `metadata.json` | name, category, and the input/output parameters (names must match `code.py`) |
| `icon.png` | a 24×24 icon for the Grasshopper ribbon |

## 9. ghuser-builder: build, verify, package

You do **not need Rhino to build components**, nor Windows.
[**ghuser-builder**](https://git.rccn.dev/libs/ghuser-builder) is the lab's
tool for it: one Docker image with one command, `ghuser-build`.

```
components/                         ghuser-build                    dist/
├── Cs_RunningBondWall/             ─────────────►                  ├── ghuser/Cs_RunningBondWall.ghuser
│   ├── code.py                     1. componentize                 ├── ghuser/…
│   ├── metadata.json               2. verify: read every file back └── compas-studio-1.2.3-rh8_0-any.yak
│   └── icon.png  (24×24)           3. package as .yak
```

1. **Componentize.** The [COMPAS componentizer](https://github.com/compas-dev/compas-actions.ghpython_components)
   turns each folder into a `.ghuser` with `GH_IO.dll`, the library Grasshopper
   itself saves files with, on Mono, on Linux.
2. **Verify.** It opens every `.ghuser` again and checks the name, parameters and
   embedded code against your source. A mismatch fails the build. An artifact is
   evidence only after something has read it back. It does **not** compare
   `RunScript` with `metadata.json`; `tests/test_components.py` does that.
3. **Package.** The `.ghuser` files and your core go into one **`.yak`**, the file
   Rhino's Package Manager installs, updates and rolls back.

Three things that follow:

- **One build everywhere.** Your laptop and CI run the same image and command.
- **Pinned tools.** The image tag fixes the Grasshopper file library. A `.ghuser`
  written by a newer `GH_IO` than your user's Rhino will not load, so upgrading is
  a decision, like bumping `uv.lock`.
- **The version is the tag.** `git tag v1.2.3` is the only place it is written.
  `ghuser-build` puts it in the package name and replaces `{{version}}` in `code.py`.

## 10. Run it

**On your laptop** (needs Docker Desktop, OrbStack or colima):

```bash
cd Lecture/Lecture_12/plugin_set
scripts/ghuser                       # components/ -> dist/
ls dist dist/ghuser
```

[`scripts/ghuser`](plugin_set/scripts/ghuser) is one `docker run`, with this folder
mounted, calling `ghuser-build components dist`. If it says *no components
directory*, Docker cannot see the folder: keep the project under your home directory.

**In CI.** [`build-ghuser.yml`](plugin_set/.github/workflows/build-ghuser.yml)
runs the same image as the job's container and the same command, on every push.
The verifier compares each `.ghuser` with its source. It does not compare
`RunScript` with `metadata.json`: `tests/test_components.py` does that. A **tag**
also publishes:

```bash
git tag v0.1.0
git push --tags        # CI builds, verifies, and attaches the .yak to a GitHub Release
```

**On a Mac with Rhino 8, while developing** (no Docker): ghuser-builder's
`local/ghuser_dev.py` points each component at your working copy of `src/`, so you
edit the core and recompute in Grasshopper. Development only; see its README.

## 11. How the core gets into Rhino

A `.ghuser` holds only the adapter, so **Rhino has to find your core somewhere.**
ghuser-builder documents five ways. Two matter for you:

| | How the core travels | Users do | Use it when |
| --- | --- | --- | --- |
| **Vendored** (scenario D) | *inside* the `.yak`, in `lib/` | install one file | your core is pure Python: **the default in this course** |
| **Published** (scenario B) | on pypi.org; the adapter says `# r: my_core=={{version}}` | install the `.yak`; Rhino pip-installs the core on first run | the project is open source and others build on the library |

Vendoring is why every adapter starts with the same dozen lines: they find
`packages/<rhino>/compas-studio/<version>/lib` and put it on Python's path, so each
component loads the core of its own version. Public libraries such as COMPAS still
come from a `# r: compas` line, which Rhino resolves itself.

Two limits: the core must be pure Python, and after updating a package you
**restart Rhino**, because Python keeps the old module loaded.

## 12. Installing, and what a version means

A colleague drags the `.yak` onto a Rhino 8 window, and the components appear in
the Grasshopper ribbon under your `category`.

> ⚠️ **A placed component forgets where it came from.** A later release does
> **not** update instances already sitting in old `.gh` files. Version
> deliberately, and say what changed.

> ⚠️ **Status.** ghuser-builder's own README has a table of what has and has
> not been checked on a real Rhino. Read it before a deadline depends on it,
> and load your first `.yak` in Rhino early, not in Week 17.

## 13. The lighter path: JSON artifact + adapter

For a one-off, the artifact route is enough: dump a COMPAS JSON file and load it
with [`rhino_load.py`](rhino_load.py) in Rhino 8's ScriptEditor (`# r: compas`
installs COMPAS into Rhino's Python). `rhinomcp` also exposes the live document to
an agent as tools, which is good for sketching, but has no tests, no artifact and
no gate.

---

# Part E — Working with AI (Week 15)

This part is about **handing an assistant one stage of the pipeline**. Read it with
[Lecture 11](/Lecture/Lecture_11/README.md), where you build an agent from scratch.

| You built | So an assistant can be given | And cannot get past |
| --- | --- | --- |
| a spec as tests (A) | "make these pass" instead of a paragraph | a red test |
| a review habit (B) | the job of author | you, reading the diff |
| a scaffold (C) | one small pure module in `src/` | the folder structure: it has nowhere to hide logic |
| a verified build (D) | nothing: it runs by itself | the verifier |

## 14. pytest as the reviewer that cannot be fooled

```bash
uv run Lecture/Lecture_12/tdd_agent.py
uv run Lecture/Lecture_11/view.py Lecture/Lecture_12/output/wall.json
```

[`tdd_agent.py`](tdd_agent.py) replaces Lecture 11's reviewer-LLM with pytest: the
coder agent writes `wall.py`, the harness runs the tests, and failures go back
verbatim until green. An LLM reviewer can be argued into approving; a test suite
cannot. The raw `wall.py` it produces is the file you reviewed in Part B §4: it
passes, and it is not good. **Both gates, always: the automatic one for correct,
the human one for good.**

## 15. The agentic development loop

Adding a new component to the plugin set:

```
1. SPEC     you write tests/test_canopy.py            ← the brief, human
2. CORE     agent writes src/compas_studio/canopy.py  ← delegated, but…
3. VERIFY   CI runs pytest on the PR                   ← the gate, automated
4. REVIEW   you read the diff: correct AND good?       ← judgment, human
5. ADAPTER  add components/Cs_Canopy/ (thin code.py)   ← you
6. SHIP     tag → ghuser-builder builds and verifies   ← automated
```

The human sits at the **ends** (what to build, whether it is good, what to ship)
and out of the **middle** (typing, running tests, packaging). The failure this
course is built to prevent is the opposite: a person in the middle, pasting what
the chatbot produced, unable to tell passing-but-bad from good.

## 16. Working with an assistant, day to day

- **Give it the test, not the wish.** "Make `tests/test_canopy.py` pass
  without changing the tests" is a task with an end. "Write a canopy
  generator" is a conversation.
- **One stage, one module.** Ask for a pure function in `src/`. Do not let
  one request touch the core, the adapter and the workflow together: you
  cannot review that diff.
- **It works on a branch.** Its changes arrive as a pull request you read,
  never as edits to `main`.
- **Read what it ran, not only what it wrote.** When a tool asks to execute
  a command, that is the human gate from Lecture 11. `--auto` is for demos.
- **Never let it edit the tests to make them pass.** If the test is wrong,
  that is your decision, made in a separate commit, with a reason.
- **Log what you asked.** The prompts that mattered go in `log.md`
  ([AI policy](/README.md#ai-usage)). At the oral defence you explain every
  line, whoever typed it.

---

## Things to try

1. Add a fourth component end to end (a column grid, a vault). How many rounds
   did the agent need to pass your tests? Which failures were the model's, and
   which were your spec's?
2. Sabotage `plugin_set/src/compas_studio/wall.py` (offset odd courses by a full
   module). Which test catches it?
3. Compare `wall.py` with `plugin_set/src/compas_studio/wall.py`. List five things
   a review catches and a test does not.
4. Break the adapter/metadata agreement: rename an input in `code.py` but not in
   `metadata.json`. Run `scripts/ghuser`, then `uv run pytest`. Which one stops it?
