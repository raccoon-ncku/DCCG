"""Keep the notebook collection honest and git-friendly.

    uv run python -m pytest Lecture/notebooks -q

1. every NN_*.py source has its generated .ipynb, and the other way round
2. no committed .ipynb carries outputs or execution counts (git-friendly)
3. every .ipynb's code is exactly its .py's code: nobody edited the generated
   file by hand (edit the .py, then run make_notebooks.py)
4. every notebook runs top to bottom without an error

No jupytext needed: the percent format is simple enough to read directly.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent
SOURCES = sorted(HERE.glob("[0-9][0-9]_*.py"))
NOTEBOOKS = sorted(HERE.glob("[0-9][0-9]_*.ipynb"))


def code_cells_from_percent(path):
    cells, kind, lines = [], None, []
    for line in path.read_text().splitlines():
        if line.startswith("# %%"):
            if kind == "code":
                cells.append("\n".join(lines).strip())
            kind = "markdown" if "[markdown]" in line else "code"
            lines = []
        else:
            lines.append(line)
    if kind == "code":
        cells.append("\n".join(lines).strip())
    return cells


def test_every_source_has_a_notebook():
    assert [p.stem for p in SOURCES] == [p.stem for p in NOTEBOOKS]
    assert len(SOURCES) >= 9


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_notebook_has_no_outputs(path):
    nb = json.loads(path.read_text())
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            assert cell.get("outputs") == [], f"{path.name}: outputs committed (run `uv run nbstripout {path}`)"
            assert cell.get("execution_count") is None


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_notebook_matches_its_source(path):
    nb = json.loads(path.read_text())
    in_notebook = ["".join(c["source"]).strip() for c in nb["cells"] if c["cell_type"] == "code"]
    assert in_notebook == code_cells_from_percent(path.with_suffix(".py")), (
        f"{path.name} differs from its .py: edit the .py, then "
        "`uv run --with jupytext Lecture/notebooks/make_notebooks.py`"
    )


@pytest.mark.parametrize("path", SOURCES, ids=lambda p: p.name)
def test_notebook_runs(path):
    result = subprocess.run([sys.executable, path.name], cwd=HERE, capture_output=True, text=True, timeout=300)
    assert result.returncode == 0, result.stderr[-2000:]
