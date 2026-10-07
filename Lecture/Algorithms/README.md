# Algorithms (Weeks 10–12)

Part IV of the course in one place: the algorithms *behind* the tools. Weeks
05–06 gave you the data structures (mesh, graph); Week 09 gave you the
architecture (pure core → artifact → adapter). This section fills the core with
real algorithms, three families of them, each written from scratch in plain
Python and numpy so that the library version, or the one an AI writes for you,
is something you can **read and check** rather than trust.

| Week | Part | Tutorials | Run |
| --- | --- | --- | --- |
| **10** | [Geometric algorithms](geometric/README.md) | smoothing · curvature · geodesics · Catmull–Clark · planar panels · contouring · Delaunay/Voronoi · convex hull · nearest neighbours · Lloyd relaxation · CGAL tour | `uv run pytest Lecture/Algorithms/geometric/tests` |
| **11** | [Simulation](simulation/README.md) | cellular automata (and towers) · boids · diffusion-limited aggregation | `uv run pytest Lecture/Algorithms/simulation/tests` |
| **12** | [Optimization](optimization/README.md) | random search · hill climbing · simulated annealing · genetic algorithm · scipy / pymoo | `uv run pytest Lecture/Algorithms/optimization/tests` |
| **12** | [Learning](learning/README.md) | k-means panel rationalisation · regression surrogate · overfitting | `uv run pytest Lecture/Algorithms/learning/tests` |

Week 10 is also the **testing** week: the second half is
[Lecture 12, Part A](/Lecture/Lecture_12/README.md#part-a--testing-week-10)
(pytest, properties not pictures, the failure path). Every algorithm here is the
worked example for it. The tests are written the way that lecture teaches, and
several of them are mathematical theorems (Gauss–Bonnet, the empty circle)
used as free, exact checks.

## Step by step: the notebooks

Notebooks 05–09 in [`Lecture/notebooks/`](/Lecture/notebooks/README.md) unpack
one algorithm per part (curvature and smoothing, Delaunay → Voronoi → Lloyd,
cellular automata, simulated annealing, k-means), printing every intermediate
result and drawing each step, then calling the tested tutorial module to
confirm.

## How every tutorial is built

Each part is a folder with the same four things:

```
<part>/
├── README.md         the lecture: idea, figure, code excerpt, what the tests check
├── tutorials/*.py    one algorithm per file, pure functions, ~30–150 lines
├── tests/            property tests:  uv run pytest Lecture/Algorithms/<part>/tests
└── figures/          make_figures.py + the SVGs it writes, drawn BY CALLING tutorials/
```

Nothing is hand-drawn: every number on every figure is computed by the code you
are reading. And nothing needs more than the course environment. scikit-learn,
pymoo and the diffusion models are optional extras, each in its own folder.

## Three questions that run through the section

1. **How do you know it is right?** A theorem, a known case, an invariant, a
   comparison with brute force. Never "the picture looks right".
2. **What does it cost?** The convex hull (O(n log n) vs O(n³)) and nearest
   neighbours (a spatial hash vs O(n²)) are where *how* you compute something
   decides whether you can compute it at all.
3. **Is one run evidence?** Simulations and stochastic searches vary from run to
   run. Their tests average over seeds and compare under equal budgets, because
   one lucky run proves nothing.

## Also in this repository

| Where | What |
| --- | --- |
| [`Lecture_05/mesh_applications/`](/Lecture/Lecture_05/README.md#12-mesh-in-architecture-four-applications) | form finding, truss analysis, scan-to-mesh, cloth: algorithms applied to meshes |
| [`Lecture_06/graph_applications/`](/Lecture/Lecture_06/README.md#11-graphs-in-architecture-three-applications) | space syntax, egress, street betweenness, timber frames: algorithms applied to graphs |
| [`Lecture_07/abm_examples/`](/Lecture/Lecture_07/abm_examples/) | ants and drones: agent-based models as objects |
| [`Classic_Algorithms/`](/Lecture/Classic_Algorithms/) | the convex hull as a notebook |
| [`Lecture_10/`](/Lecture/Lecture_10/README.md) | optional: trained models (diffusion, CLIP) as design ingredients |

## For the final project

Most strong projects are one algorithm from this section, wrapped in the Week 09
architecture: a pure core that runs it, tests in this style, an artifact, and a
Grasshopper component built with the Week 14 pipeline. Pick the algorithm whose
*question* you care about (even spacing, least material, fewest panel types,
what grows), not the one with the best screenshot.
