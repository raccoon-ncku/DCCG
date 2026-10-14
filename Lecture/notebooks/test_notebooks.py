"""Keep the notebooks runnable and git-friendly.

    uv run python -m pytest Lecture/notebooks -q
    uv run --extra timber python -m pytest Lecture/notebooks -q     # the timber ones too

The notebooks live with their week: Lecture/Lecture_NN/notebooks/ and
Lecture/Algorithms/<part>/notebooks/. This folder holds what they share.

1. no committed notebook carries outputs or execution counts
2. every picture a notebook's text points at exists
3. every notebook runs top to bottom, in a real kernel, from its own folder

The compas_timber notebooks need the `timber` extra and are skipped without
it. Nothing is written back: the run happens in memory.
"""

import importlib.util
import json
import re
from pathlib import Path

import nbformat
import pytest
from nbclient import NotebookClient

HERE = Path(__file__).parent
LECTURE = HERE.parent
NOTEBOOKS = sorted(LECTURE.glob("Lecture_*/notebooks/*.ipynb")) + sorted(LECTURE.glob("Algorithms/*/notebooks/*.ipynb"))
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")


def name(path):
    return f"{path.parent.parent.name}/{path.name}"


def test_notebooks_live_with_their_week():
    strays = [p for p in LECTURE.rglob("*.ipynb")
              if p not in NOTEBOOKS and ".ipynb_checkpoints" not in p.parts]
    assert not strays, f"notebooks outside a notebooks/ folder: {strays}"
    assert len(NOTEBOOKS) >= 30


@pytest.mark.parametrize("path", NOTEBOOKS, ids=name)
def test_notebook_has_no_outputs(path):
    nb = json.loads(path.read_text())
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            assert cell.get("outputs") == [], f"{name(path)}: outputs committed (run `uv run nbstripout --install` once)"
            assert cell.get("execution_count") is None


@pytest.mark.parametrize("path", NOTEBOOKS, ids=name)
def test_notebook_pictures_exist(path):
    nb = json.loads(path.read_text())
    for cell in nb["cells"]:
        if cell["cell_type"] == "markdown":
            for link in IMAGE.findall("".join(cell["source"])):
                if not link.startswith("http"):
                    assert (path.parent / link).exists(), f"{name(path)}: missing picture {link}"


@pytest.mark.parametrize("path", NOTEBOOKS, ids=name)
def test_notebook_runs(path):
    if "timber" in path.name and importlib.util.find_spec("compas_timber") is None:
        pytest.skip("needs the timber extra: uv run --extra timber ...")
    nb = nbformat.read(path, as_version=4)
    NotebookClient(nb, timeout=300, kernel_name="python3",
                   resources={"metadata": {"path": str(path.parent)}}).execute()
