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
> AI comes **last** on purpose. An assistant can write the middle of this
> pipeline. It can only be trusted to once the two ends exist: a test that
> says what correct means, and a reviewer who can tell good from passing.
> Build the pipeline first, then hand part of it over.
>
> These skills mattered before AI. They matter *more* now, not less: when you
> did not type the code, verification and review are all you have.

Two folders go with this lecture:

- [`plugin_set/`](plugin_set/README.md): the **worked example**. A real
  Grasshopper plugin set (`compas_studio`) developed, tested and shipped
  entirely outside Rhino. Read Parts A, B and D with it open.
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
uv run pytest Lecture/Lecture_12/test_staircase.py -v     # a single file, verbose
```

[`plugin_set/src/compas_studio/staircase.py`](plugin_set/src/compas_studio/staircase.py)
is a **pure function**: numbers in, geometry out. No viewer, no file IO, no
Rhino. That separation — the habit from Week 09 — is exactly what makes it
testable, and what will let the same code become a Grasshopper component in
Part D without changing a line.

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
Compare it with a brief written in prose: no ambiguity about units, counts,
offsets, or tolerances survives translation into a test.

This is the planner's real skill, and the through-line of the whole course:
**a brief you can turn into a test is a finished brief; if you cannot write the
test, you have not finished planning.** It is the same claim the Week 01–09
checkpoints made — the `spec/test_tasks.py` one folder down from each
`tasks.py` was this, with training wheels. Now you write them.

## 3. The test process

A test file is not something you write at the end, to prove you finished. It
is a loop you live in, and it has three beats:

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

Where it runs, from fastest to most public:

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

A bug found later goes the same way round: first write the test that would
have caught it (red), then fix it (green). The bug cannot come back
unnoticed, and the spec is now one sentence more precise.

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

The loop is *propose → CI checks → a person reads the diff → merge or send
back*. It is the same loop whether the author is a classmate, you last
month, or (Part E) an agent. Write commit messages that say **why**,
not what — the diff already shows what:

```
bad:   "update"   "fixed stuff"   "changes to wall.py"
good:  "wall: place only full bricks; half-bricks were sticking past length"
```

---

### The review process, as steps

Reviewing is a skill with a procedure, like testing:

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

Until now your code lived in the course repo, one script per exercise. A
project is different in one way that matters: **other things have to find
your code.** pytest has to import it. CI has to install it. A Grasshopper
component has to call it. A reviewer has to know where to look. A *scaffold*
is the folder structure that makes all four possible, set up once, before
there is much code to move.

## 6. The shape

```
my_tool/
├── pyproject.toml            what this is, and what it needs
├── src/my_tool/              1. CORE      pure Python + COMPAS, no Rhino
├── tests/                    2. SPEC      pytest
├── components/Mt_*/          3. ADAPTERS  one folder per Grasshopper component
├── scripts/ghuser            4. BUILD     Part D
└── .github/workflows/        5. PIPELINE  test on every push; build, and release on a tag
```

It is the Week 09 architecture (core → artifact → adapter), given
addresses. [`plugin_set/`](plugin_set/README.md) is this shape with three
components in it; [`project_template/`](project_template/README.md) is this
shape with one, waiting to be renamed.

Why `src/`? With the package one level down, the only way to import
`my_tool` is to have **installed** it. So your tests run against the same
thing a user will get, not against whatever happens to be in the current
folder. That is the "works on my laptop" bug, removed by a folder name.

## 7. Scaffold it, two ways

**From nothing**, to see that there is no magic in it:

```bash
uv init --lib my_tool            # pyproject.toml + src/my_tool/__init__.py
cd my_tool
uv add compas                    # a dependency: written to pyproject.toml, pinned in uv.lock
uv add --dev pytest              # a tool for you, not for your users
mkdir tests components
git init && git add -A && git commit -m "scaffold: empty project"
```

Five commands, and you have an installable Python package with a locked
environment and a history. Open `pyproject.toml` and read it: every line is
something you just said.

**From the template**, which is the same thing plus the parts that take
longer to type (a first test, a first component, the two CI workflows):

```bash
cp -R Lecture/Lecture_12/project_template ~/code/canopy_kit
cd ~/code/canopy_kit
# rename the four things listed in its README, then:
uv sync
uv run pytest                    # 8 passed: the scaffold works before you have written anything
git init && git add -A && git commit -m "scaffold: from the DCCG template"
```

Start your final project this way, **outside the course repo**, as a
repository of its own.

## 8. What each file is for

| File | It answers | You touch it when |
| --- | --- | --- |
| `pyproject.toml` | what is this, which Python, which libraries | you add a dependency (`uv add`, never by hand) |
| `uv.lock` | *exactly* which versions, on every machine | never by hand. Commit it |
| `src/my_tool/__init__.py` | what does this package offer | you add a public function |
| `src/my_tool/*.py` | the logic | most of the time |
| `tests/test_*.py` | what does correct mean | **before** you touch `src/` (Part A §3) |
| `components/*/code.py` | how does Grasshopper call it | you add a component |
| `components/*/metadata.json` | its name, inputs and outputs in Grasshopper | the same moment |
| `.github/workflows/test.yml` | run the tests on every push | once |
| `.github/workflows/build-ghuser.yml` | build the components; release on a tag | once (Part D) |
| `.gitignore` | what must not be committed (`.venv/`, `dist/`) | rarely |
| `README.md` | what it is, how to run it, how to install it | when any of those change |

**Python 3.9.** The template says `requires-python = ">=3.9"` and its CI
runs the tests on 3.9, although your laptop has 3.13. Rhino 8 runs CPython
3.9, so that is where your core will finally execute. Test on the Python
you ship to.

## 9. The first hour of a project

In this order. Each step is checked by the one after it.

1. **Scaffold** (§7) and make the first commit while everything is empty and
   green.
2. **Push** to a new GitHub repository. Watch the `tests` workflow run. You
   now have CI before you have code, which is the cheap moment to get it.
3. **One test** for the smallest true thing about your design (Part A).
   See it fail.
4. **One function** in `src/` that makes it pass.
5. **Branch, pull request, review** (Part B), even alone. The habit is
   easier to keep than to start.
6. **One component** that calls that function, and a build (Part D).

By the end of that hour nothing impressive exists. But every later hour
lands in a place that is already tested, reviewed, built and versioned,
and that is what makes the later hours fast.

---

# Part D — Shipping Grasshopper components with ghuser-builder (Week 14)

Now the question the whole course has pointed at: **how does pure Python
geometry become something a colleague installs in Grasshopper, without you
ever pasting code into a component by hand?**

## 10. The layered workflow, productised

```
┌──────────────────────────────────────────────────────────────┐
│ 1. CORE      src/compas_studio/*.py — pure Python + COMPAS   │  tested by pytest,
│              numbers in, geometry out, no Rhino              │  developed outside Rhino
├──────────────────────────────────────────────────────────────┤
│ 2. SPEC      tests/*.py — the executable brief                │  the CI gate
├──────────────────────────────────────────────────────────────┤
│ 3. ADAPTER   components/Cs_*/code.py — find the core, call,   │  thin, boring,
│              convert to Rhino geometry. No logic here.        │  no tests needed
├──────────────────────────────────────────────────────────────┤
│ 4. PACKAGE   compas-studio-1.2.3-rh8_0-any.yak — components   │  built and verified by
│              + the core, one file, installed from Rhino       │  ghuser-builder, no Rhino
└──────────────────────────────────────────────────────────────┘
```

The principle in one line, unchanged since Week 09: **keep the intelligence
out of the host application.** Develop and verify headlessly; let Rhino only
receive results.

## 11. Grasshopper without `rhinoscriptsyntax`

The usual way to write a GH component — type Python into a GHPython node,
reaching for `rhinoscriptsyntax` — produces code that only runs inside a live
Rhino document: untestable, unversionable, invisible to CI and to agents.

We refuse that. COMPAS geometry is **plain Python objects** — a `Box` is a `Box`
with or without Rhino — so the core in `src/compas_studio/` runs and is tested
on any machine. Grep it: no `rhinoscriptsyntax`, no `import Rhino`. The
Grasshopper component becomes an adapter: a fixed header that finds the core,
then a few lines that import one core function and convert its output with
`compas_rhino.conversions`. See
[`components/Cs_RunningBondWall/code.py`](plugin_set/components/Cs_RunningBondWall/code.py):
there is no geometry logic in it to get wrong.

Each component is a folder of three files:

| File | Purpose |
| --- | --- |
| `code.py` | the adapter — a class with `RunScript(self, inputs...)` returning outputs |
| `metadata.json` | name, category, and the input/output parameters (names must match `code.py`) |
| `icon.png` | a 24×24 icon for the Grasshopper ribbon |

## 12. ghuser-builder: build, verify, package

You do **not need Rhino to build components**, nor Windows.
[**ghuser-builder**](https://git.rccn.dev/libs/ghuser-builder) is the lab's
tool for it: one Docker image with a single command, `ghuser-build`, that
does three things to a `components/` folder.

```
components/                         ghuser-build                    dist/
├── Cs_RunningBondWall/             ─────────────►                  ├── ghuser/Cs_RunningBondWall.ghuser
│   ├── code.py                     1. componentize                 ├── ghuser/…
│   ├── metadata.json               2. verify: read every file back └── compas-studio-1.2.3-rh8_0-any.yak
│   └── icon.png  (24×24)           3. package as .yak
```

1. **Componentize.** The [COMPAS componentizer](https://github.com/compas-dev/compas-actions.ghpython_components)
   (Gramazio Kohler Research) turns each folder into a `.ghuser` file using
   `GH_IO.dll`, the library Grasshopper itself saves files with. In the
   image that library runs on Mono, on Linux.
2. **Verify.** The image does not trust its own output. It opens every
   `.ghuser` again and checks the name, the parameters and the embedded code
   against your source. A mismatch fails the build, and nothing ships. This
   is Part A's idea applied to a build: an artifact is evidence only after
   something has read it back.
3. **Package.** The `.ghuser` files, plus your core library, go into one
   **`.yak`**: Rhino's package format, the thing its Package Manager
   installs, updates and rolls back.

Three ideas from earlier weeks, now doing real work:

- **One build everywhere.** Your laptop and CI run the same image and the
  same command. There is no "it built on my machine".
- **Pinned tools.** The image tag fixes the Grasshopper file library and the
  componentizer version. A `.ghuser` written by a newer `GH_IO` than your
  user's Rhino is the classic *component will not load* bug, so upgrading is
  a decision, like bumping `uv.lock` (Week 09).
- **The version is the tag.** `git tag v1.2.3` is the only place the version
  is written. `ghuser-build` puts it into the package name and into every
  component (it replaces `{{version}}` in `code.py`).

## 13. Run it

**On your laptop** (needs Docker Desktop, OrbStack or colima):

```bash
cd Lecture/Lecture_12/plugin_set
scripts/ghuser                       # components/ -> dist/
ls dist dist/ghuser
```

[`scripts/ghuser`](plugin_set/scripts/ghuser) is six lines: `docker run`,
with this folder mounted, calling `ghuser-build components dist`. Read it.
If it says *no components directory*, Docker cannot see the folder: keep the
project somewhere under your home directory, which Docker shares by default.

**In CI.** [`build-ghuser.yml`](plugin_set/.github/workflows/build-ghuser.yml)
runs the same image as the job's container and the same command. Every push
builds and verifies, so a component whose `code.py` and `metadata.json`
disagree fails within a minute of the commit, not in front of a user. A
**tag** also publishes:

```bash
git tag v0.1.0
git push --tags        # CI builds, verifies, and attaches the .yak to a GitHub Release
```

**On a Mac with Rhino 8, while developing** (no Docker): ghuser-builder's
`local/ghuser_dev.py` builds with Rhino's own libraries and can point each
component straight at your working copy of `src/`, so you edit the core and
recompute in Grasshopper without reinstalling. Development only: releases
always come from CI. See the ghuser-builder README.

## 14. How the core gets into Rhino

A `.ghuser` contains the adapter's code and nothing else. The adapter says
`from compas_studio import running_bond_wall`, and **Rhino has to find
`compas_studio` somewhere.** ghuser-builder documents five ways (its
*deploy scenarios*). Two matter for you:

| | How the core travels | Users do | Use it when |
| --- | --- | --- | --- |
| **Vendored** (scenario D) | *inside* the `.yak`, in `lib/` | install one file | your core is pure Python: **the default in this course** |
| **Published** (scenario B) | on pypi.org; the adapter says `# r: my_core=={{version}}` | install the `.yak`; Rhino pip-installs the core on first run | the project is open source and others build on the library |

Vendoring is why every adapter in the plugin set starts with the same dozen
lines: they find `packages/<rhino>/compas-studio/<version>/lib` and put it on
Python's path, so each component loads the core **of its own package
version**. It is boilerplate, it is identical in every component, and it is
the price of "install one file, configure nothing". Public libraries such as
COMPAS still come from a `# r: compas` line, which Rhino resolves itself.

Two limits worth knowing before you rely on it: the core must be pure Python
(nothing compiled), and after updating a package you **restart Rhino**,
because Python keeps the old module loaded.

## 15. Installing, and what a version means

A colleague drags the `.yak` onto a Rhino 8 window, or finds it in the
Package Manager if you published it. Components appear in the Grasshopper
ribbon under your `category`. A new release shows up as an update; the old
one can be reinstalled.

> ⚠️ **A placed component forgets where it came from.** Once on a canvas it
> is a plain script component; a later release does **not** update instances
> already sitting in old `.gh` files. Version deliberately, and say what
> changed. (A real limit of the format, worth knowing before you depend on it.)

> ⚠️ **Status.** ghuser-builder's own README has a table of what has and has
> not been checked on a real Rhino. Read it before a deadline depends on it,
> and load your first `.yak` in Rhino in Week 14, not in Week 17.

## 16. The lighter path: JSON artifact + adapter

The full plugin pipeline is worth it for something you will reuse and share. For
a one-off — verify a design headlessly, then look at it once in Rhino — the
artifact route is enough: dump a `compas` JSON file and load it
with [`rhino_load.py`](rhino_load.py) inside Rhino 8's ScriptEditor (`# r: compas`
installs COMPAS into Rhino's Python automatically). Same principle, less
ceremony: intelligence stays outside; Rhino receives a verified artifact.

Also worth knowing (outlook): a Grasshopper Python component can `import
compas_studio` and call the core **live** with sliders as inputs — same tested
core, no artifact in between; and `rhinomcp` exposes the live Rhino document to
an agent as tools (Part E), powerful for sketching but with no tests, no
artifact, no gate — prefer the pipeline for anything you need to trust.

---

---

# Part E — Working with AI (Week 15)

You have used an assistant all term. This part is about something narrower
and more useful: **handing it a stage of the pipeline**, now that the
pipeline exists. Read it with [Lecture 11](/Lecture/Lecture_11/README.md),
where you build an agent from scratch.

Everything in Parts A–D is what makes that safe:

| You built | So an assistant can be given | And cannot get past |
| --- | --- | --- |
| a spec as tests (A) | "make these pass" instead of a paragraph | a red test |
| a review habit (B) | the job of author | you, reading the diff |
| a scaffold (C) | one small pure module in `src/` | the folder structure: it has nowhere to hide logic |
| a verified build (D) | nothing: it runs by itself | the verifier |

## 17. pytest as the reviewer that cannot be fooled

```bash
uv run Lecture/Lecture_12/tdd_agent.py
uv run Lecture/Lecture_11/view.py Lecture/Lecture_12/output/wall.json
```

[`tdd_agent.py`](tdd_agent.py) replaces Lecture 11's reviewer-LLM with pytest:
the coder agent writes `wall.py`, the harness runs the tests, and failures go
back verbatim until green. An LLM reviewer can be wrong, or argued into
approving; a test suite cannot. This is the single most important upgrade to the
Lecture 11 loop.

The raw `wall.py` this produces is the file you reviewed in Part B §4: it
passes, and it is not good. Tests bound what an agent can get wrong. They do
not make its output worth keeping. **Both gates, always: the automatic one
for correct, the human one for good.**

## 18. The agentic development loop, understood not followed

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
6. SHIP     tag → ghuser-builder builds and verifies   ← automated
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

## 19. Working with an assistant, day to day

The loop above is the formal version. The habits that carry it into ordinary
use of Claude Code, Copilot or Cursor on your project:

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

## Continuous integration recap

Because the core is pure and tested, a robot runs your tests on every commit and
builds, verifies and packages your components on every push, and publishes them on every release. You did not configure a magic service;
you wrote two small YAML files (`test.yml`, `build-ghuser.yml`) that do exactly what you
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
   `metadata.json`, and run `scripts/ghuser`. Which of the three steps stops it?
5. Compare `wall.py` and `plugin_set/src/compas_studio/wall.py` line by line.
   Everything different between them is something review catches and tests do
   not. List five of those things.
6. Scaffold a project from nothing with `uv init --lib` and from the template.
   Diff the two `pyproject.toml` files. What did the template add, and why?
7. Review a classmate's pull request **without running it**, then run it.
   What did running show that reading did not?
