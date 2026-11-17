# Final Project — Fall 2026

Announced 2026.11.18. Start here: [**From the template to a .yak**](WALKTHROUGH.md),
the session that takes the template through every stage, and
[**brick-screen**](https://github.com/rccn-dev/brick-screen), a project finished to
this bar.

## The brief

**Write a Python-based Grasshopper plugin, with the help of AI — and make it
professional, reproducible, and maintainable.**

Pick a piece of parametric geometry worth turning into a reusable component (a wall
bond, a stair, a packing tool, a facade pattern, anything with real logic):

- **Professional:** a pure COMPAS core with no Rhino imports, plus a thin Grasshopper
  adapter. A *tool* someone else could install, not a script that draws one picture.
- **Reproducible:** it runs without Rhino and produces the same verified result every
  time, with tests that prove it and CI that runs them.
- **Maintainable:** clear structure, code you can explain, and a build pipeline so a
  new version is one command.

Start it from [ghuser-template](https://github.com/rccn-dev/ghuser-template)
and build it with ghuser-builder (worked examples:
[brick-screen](https://github.com/rccn-dev/brick-screen),
[`plugin_set/`](/Lecture/Lecture_14/plugin_set/README.md)). **Submit the `.yak`**
from `uv run scripts/ghuser.py --version <x.y.z>`: one file, the core inside, tested by
installing it in a restarted Rhino with your dev link removed. A Rhino `.rhp` plugin or a
standalone library with a loader script are also fine.

## Required architecture

```
your-project/
├── src/<your_package>/    # 1. CORE: pure Python + COMPAS, no viewer, no file IO, no Rhino
├── tests/                 #    pytest: the executable spec for your core
├── runner.py              #    calls the core, writes the artifact (file IO lives here)
├── output/<artifact>.json # 2. ARTIFACT: committed, reviewable
├── components/<Name>/     # 3. ADAPTERS: code.py + metadata.json + icon.png
├── scripts/               #    dev.py (linked into Grasshopper), ghuser.py (the .yak)
├── README.md              # what it does, how to install, how to run both ways
└── pyproject.toml
```

The template gives you all of it but `runner.py` and `output/`; add those as
[brick-screen](https://github.com/rccn-dev/brick-screen) does (Week 09 Part C explains
why). The test: **delete `components/` and your project must still work.** Uninstall
Rhino and your tests must still pass.

## Requirements

- Primary language is Python; geometry via COMPAS (other libraries welcome
  alongside it — `trimesh`, `numpy`, `shapely`, `networkx`, `pymoo`, …).
- The core is **parametric**: it takes arguments and behaves sensibly across a
  range of them, not just the one value in your screenshot.
- At least **6 meaningful tests** covering properties (counts, dimensions,
  monotonicity, no gaps/overlaps) and at least one failure path (invalid input
  raises rather than returning junk).
- A working adapter, demonstrated live in Rhino 8 or Grasshopper.
- A GitHub repository. Every member must have at least one commit.
- You may **not** copy an existing project wholesale. Referencing and rewriting
  is fine; cite what you referenced.

## Groups

Individually or in groups of up to 4. Group size does not change the bar, but
larger groups are expected to produce proportionally more.

## AI usage

The [course rules](/README.md#ai-usage) apply, and they are enforced at the
presentation: explain every line, disclose in a `log.md`, verify rather than trust.

## Milestones

| When | Milestone |
| ---- | --------- |
| 2026.11.18 | Brief announced; your repository made from the template, in class |
| 2026.11.25 | **Proposal + in-class pitch** (2 min): what it does, who'd use it, what the core function signature looks like |
| 2026.12.09 | **Iteration 1 review** — core + tests running headless, green in CI; first pull request reviewed by your partner |
| 2026.12.23 | **Iteration 2 review** — adapter working in Rhino/GH through `dev.py` |
| 2026.12.30 | **Feature freeze** — the `.yak` installs in a restarted Rhino; docs, tests, packaging only |
| 2027.01.06 | **Final presentation + live demo** |

## Deliverables

- The GitHub repository, matching the structure above
- The `.yak`, attached to a tagged release (`git tag v1.0.0`)
- `README.md` with install + run instructions for **both** modes
- The committed artifact (`output/*.json`)
- Images or video of the result, in both headless and Rhino/GH contexts
- A short reflection (~300 words): where the AI helped, where it misled you,
  and what your tests caught that your eyes did not

## Assessment

**This project is your entire grade (100%).** The only other requirement is the Weeks
01–09 checkpoints, a gate and not a score ([grading](/README.md#grading)). It is judged
as a whole:

- **Runs headless:** a pure core plus a committed artifact, no Rhino required.
- **Runs inside Rhino 8 / Grasshopper:** through a thin adapter with no design logic.
- **Verifiably correct:** meaningful tests, ideally running in CI.
- **Well-built:** clear structure, sane names, honest documentation.
- **Presented well:** a live demo that shows both modes working.

A modest tool that is well-built, tested and runs in both modes beats an ambitious one
that only works on its author's laptop. **Process is worth more than the artifact.**

## Deadline and submission

- **Presentation**: 2027.01.06, in class
- **Repository frozen**: 2027.01.10 23:59
- Submit the repository URL and the `.yak` via Moodle

## Ideas and inspiration

- A wall / facade / bond generator with real fabrication constraints
- A stair or ramp generator that validates against building-code rules
- A packing or nesting tool for sheet-material fabrication
- A structural sizing tool driven by an optimizer (see [W12 optimization](/Lecture/Lecture_12/README.md#part-a--optimization-letting-the-computer-choose))
- A mesh-relaxation or form-finding component
- A pathfinding / circulation analysis tool on a Graph
- A semantic image search over a reference library (see [Week 15](/Lecture/Lecture_15/neural/README.md))
- An L-system / recursive growth system with fabrication-aware output

Good projects usually start from something you did by hand fifty times in Rhino.
