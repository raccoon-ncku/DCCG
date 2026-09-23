# Week 15 (Lecture 09) — Optimization: letting the computer choose

👉[Slides: Optimization](https://slides.rccn.dev/courses/DCCG/DCCG-W15-optimization/)

> Optional material for the Build weeks. Nothing in the final project *requires*
> optimization — but if your project has a "best" version of something (lightest
> beam, tightest packing, least material), this is how you find it instead of
> guessing.

## 1. The idea

So far you have *generated* geometry. Optimization *chooses* geometry: you
describe what "good" means as a number, and an algorithm searches for the
inputs that make that number best.

Three ingredients, and naming them is most of the work:

- **Variables** — what you are allowed to change (beam width, column spacing,
  panel angle).
- **Objective** — the single number to minimise or maximise (weight, cost,
  deflection, daylight).
- **Constraints** — what must stay true regardless (deflection < 5 mm,
  every part fits on the sheet, cost < budget).

If you cannot write the objective as a function that returns one number, you
cannot optimise yet — you are still deciding what you actually want. That is
the same lesson as the executable spec in Week 10, wearing engineering clothes.

## 2. Optimization *is* the dual-mode architecture

This is why the topic sits here and not in a vacuum. An objective function is a
**pure core function**: numbers in, one number out, no viewer, no files. The
optimiser calls it thousands of times, so it *must* be pure and fast — any
printing, drawing, or file IO inside it would be a disaster.

```python
def beam_weight(width, height):
    """Pure: dimensions in, one number out. The optimiser calls this a lot."""
    return width * height * LENGTH * DENSITY
```

Everything you learned in Week 06 about keeping the core clean pays off
directly here. The optimiser is just a very persistent caller.

## 3. Examples

Run them from the repo root:

```bash
uv run Lecture/Lecture_15_optimization/01_beam_optimization_scipy.py
uv run Lecture/Lecture_15_optimization/02_beam_optimization_pymoo.py
```

### `01_beam_optimization_scipy.py` — one objective

Find the lightest rectangular beam that carries a 500 kg load without
deflecting more than 5 mm.

- **Library**: `scipy.optimize` (standard scientific Python)
- **Method**: SLSQP (Sequential Least SQuares Programming)
- **Shape**: one objective, one answer

### `02_beam_optimization_pymoo.py` — competing objectives

Real design rarely has one goal. Here, *light* and *stiff* pull against each
other: the lightest beam is floppy, the stiffest is heavy. There is no single
winner — there is a **Pareto front** of the best available compromises, and
choosing among them is a design decision the maths deliberately leaves to you.

- **Library**: `pymoo` (multi-objective optimization)
- **Method**: NSGA-II (a genetic algorithm)

> The takeaway is not the algorithm. It is that "optimal" is only meaningful
> once you have said *optimal for what*, and that when goals conflict the
> computer hands the trade-off back to you rather than resolving it.

### Legacy examples

`legacy_examples/` has generic optimization classics (knapsack, TSP) with
`ortools` and `deap`. Not maintained for this year; read for interest.

## 4. Setup

`scipy`, `pymoo` and `matplotlib` are light enough to add to the project
environment directly:

```bash
uv add scipy pymoo matplotlib
uv run Lecture/Lecture_15_optimization/01_beam_optimization_scipy.py
```

(These are not in the default `uv.lock` because they are optional — `uv add`
records them in `pyproject.toml`. Commit that change only if your project uses
them.)

The legacy conda environment still works if you prefer it:

```bash
conda env create -f environment_ml.yml && conda activate DCCG_ML
```

## Using it in a final project

The cleanest way to make optimization part of a project:

1. Write your objective as a pure function in your **core** layer.
2. Let the optimiser find the best variables (this replaces you turning
   sliders by hand).
3. Feed those variables back into your normal geometry core to build the
   winning design, and save it as your **artifact**.

The optimiser chooses the numbers; your tested core turns them into geometry.
Same architecture, one new caller.
