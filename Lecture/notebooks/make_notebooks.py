"""Build the .ipynb notebooks from their .py sources (instructor tool).

    uv run --with jupytext Lecture/notebooks/make_notebooks.py           # write
    uv run --with jupytext Lecture/notebooks/make_notebooks.py --check   # verify only

The `NN_*.py` files are the SOURCE: plain Python in "percent" format, where
`# %%` starts a code cell and `# %% [markdown]` a text cell. They are what Zed
runs, and what git diffs well. The `.ipynb` files are GENERATED from them for
Jupyter and VS Code, always with no outputs. Never edit an .ipynb by hand:
edit the .py and rebuild.

jupytext is used only here, through `uv run --with`, so it is not a project
dependency and does not touch uv.lock.
"""

import sys
from pathlib import Path

import jupytext

HERE = Path(__file__).parent
KERNEL = {"name": "python3", "display_name": "Python 3 (ipykernel)", "language": "python"}


def build(source):
    nb = jupytext.read(source, fmt="py:percent")
    nb.metadata = {"kernelspec": KERNEL, "language_info": {"name": "python"}}
    for i, cell in enumerate(nb.cells):
        cell.metadata = {}
        cell.id = f"cell-{i:02d}"        # stable ids: rebuilding gives an identical file
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
    return jupytext.writes(nb, fmt="ipynb")


def main(check=False):
    stale = []
    for source in sorted(HERE.glob("[0-9][0-9]_*.py")):
        target = source.with_suffix(".ipynb")
        text = build(source)
        if check:
            if not target.exists() or target.read_text() != text:
                stale.append(target.name)
        else:
            target.write_text(text)
            print("wrote", target.name)
    if check:
        if stale:
            print("out of date (run make_notebooks.py):", ", ".join(stale))
            sys.exit(1)
        print("all notebooks match their .py sources")


if __name__ == "__main__":
    main(check="--check" in sys.argv)
