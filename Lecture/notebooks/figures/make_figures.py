"""Save one figure per notebook for the notebooks README (instructor tool).

    uv run --extra timber Lecture/notebooks/figures/make_figures.py

Each picture is an SVG that the notebook itself draws: the notebook is run in
a kernel and the figure whose title contains the text below is written to
this folder. Nothing is drawn here, so the README cannot show something a
notebook does not produce. Never edit the SVGs by hand: change the notebook
and run this again.

Without the timber extra the compas_timber figures are left as they are.

The Week 05 notebooks are not here: their previews are the lecture's own
drawn figures in Lecture_05/figures/.
"""

import importlib.util
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

HERE = Path(__file__).parent
LECTURE = HERE.parent.parent

# notebook (under Lecture/) -> text in the title of the figure to keep
PICK = {
    "Lecture_06/notebooks/01_bfs_and_paths": "hops from the entry",
    "Lecture_06/notebooks/02_floor_plan": "metres to the nearest exit",
    "Lecture_06/notebooks/03_two_graphs_of_one_frame": "node = member",
    "Lecture_06/notebooks/04_bricks_and_mortar": "the same two bricks as a graph",
    "Lecture_06/notebooks/05_brick_wall_assembly": "one chain of supports",
    "Lecture_06/notebooks/06_street_network": "betweenness: orange carries the most trips",
    "Lecture_06/notebooks/08_timber_stud_wall": "beams are nodes, meetings are edges",
    "Lecture_06/notebooks/09_timber_frame_to_site": "gable: y across, z up",
    "Algorithms/geometric/notebooks/01_curvature_smoothing": "mean radius over 30 rounds",
    "Algorithms/geometric/notebooks/02_voronoi_lloyd": "Voronoi cells",
    "Algorithms/simulation/notebooks/01_cellular_automata": "population per floor",
    "Algorithms/optimization/notebooks/01_simulated_annealing": "best so far, one seed",
    "Algorithms/learning/notebooks/01_kmeans": "round 2",
}


def figures_of(path):
    """Every SVG the notebook draws, in order."""
    nb = nbformat.read(str(path), as_version=4)
    NotebookClient(nb, timeout=300, kernel_name="python3",
                   resources={"metadata": {"path": str(path.parent)}}).execute()
    return [output["data"]["image/svg+xml"]
            for cell in nb.cells if cell.cell_type == "code"
            for output in cell.get("outputs", []) if "image/svg+xml" in output.get("data", {})]


def main():
    have_timber = importlib.util.find_spec("compas_timber") is not None
    missing = []
    for name, title in PICK.items():
        if "timber" in name and not have_timber:
            print("skipped", name, "(needs --extra timber)")
            continue
        found = [svg for svg in figures_of(LECTURE / f"{name}.ipynb") if title in svg]
        if not found:
            missing.append(f"{name}: no figure titled {title!r}")
            continue
        target = HERE / (name.replace("/notebooks/", "-").replace("/", "-") + ".svg")
        target.write_text(found[0])
        print("wrote", target.name)
    if missing:
        sys.exit("\n".join(missing))


if __name__ == "__main__":
    main()
