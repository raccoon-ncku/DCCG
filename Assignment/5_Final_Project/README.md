# Final Project — Fall 2026

Announced 2026.11.18. Start here: [**From the template to a .yak**](WALKTHROUGH.md),
the session that takes the template through every stage, and
[**brick-screen**](https://github.com/rccn-dev/brick-screen), a project finished to
this bar.

## The brief

**Write a Python-based Grasshopper plugin, with or without the help of AI — and make it
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

## Requirements

- Primary language is Python; geometry via COMPAS (other libraries welcome
  alongside it — `trimesh`, `numpy`, `shapely`, `networkx`, `pymoo`, …).
- The core is **parametric**: it takes arguments and behaves sensibly across a
  range of them, not just the one value in your screenshot.
- A working adapter, demonstrated live in Rhino 8 or Grasshopper.
- A GitHub repository. Every member must have at least one commit.
- You may **not** copy an existing project wholesale. Referencing and rewriting
  is fine; cite what you referenced.

## Groups

Individually or in groups of up to 2. Group size does not change the bar, but
larger groups are expected to produce proportionally more.

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

- **Runs headless**
- **Runs inside Rhino 8 / Grasshopper:** through a thin adapter with no design logic.
- **Well-built:** clear structure, sane names, honest documentation.
- **Presented well:** a live demo that shows both modes working, explain the code when asked


## Deadline and submission

- **Presentation**: 2027.01.06, in class or per appointment
- **Upload deadline**: 2027.01.08 23:59
- Submit the repository URL and the `.yak` via Moodle
