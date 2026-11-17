"""Every component's code.py and metadata.json must agree.

The build does not compare them: a renamed input still builds, and only shows
up in Grasshopper, as an input that never arrives. This catches it on any machine.
"""

import ast
import json
import re
from pathlib import Path

import pytest

COMPONENTS = sorted(p for p in (Path(__file__).parent.parent / "components").iterdir() if p.is_dir())


@pytest.mark.parametrize("folder", COMPONENTS, ids=lambda p: p.name)
def test_code_and_metadata_agree(folder):
    tree = ast.parse((folder / "code.py").read_text(encoding="utf-8"))
    adapter = next(node for node in tree.body if isinstance(node, ast.ClassDef))
    assert adapter.name == folder.name, "the class must be named after its folder"

    run = next(node for node in adapter.body if isinstance(node, ast.FunctionDef) and node.name == "RunScript")
    parameters = [arg.arg for arg in run.args.args][1:]         # without self
    inputs = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))["ghpython"]["inputParameters"]
    assert parameters == [port["name"] for port in inputs], "RunScript and metadata.json name different inputs"


@pytest.mark.parametrize("folder", COMPONENTS, ids=lambda p: p.name)
def test_package_name_is_the_one_the_yak_is_built_as(folder):
    # A PACKAGE that differs from yak-name builds fine and finds no core once installed.
    pyproject = (folder.parent.parent / "pyproject.toml").read_text(encoding="utf-8")
    yak_name = re.search(r'^yak-name\s*=\s*"([^"]+)"', pyproject, re.M).group(1)
    package = re.search(r'^PACKAGE, VERSION = "([^"]+)"', (folder / "code.py").read_text(encoding="utf-8"), re.M)
    assert package and package.group(1) == yak_name, "PACKAGE in code.py must be yak-name in pyproject.toml"


# What the componentizer accepts (ghuser-builder's pinned componentize_cpy.py).
TYPE_HINTS = {
    "none", "ghdoc", "float", "bool", "int", "complex", "str", "datetime", "guid", "color", "point", "vector",
    "plane", "interval", "uvinterval", "box", "transform", "line", "circle", "arc", "polyline", "rectangle",
    "curve", "mesh", "surface", "subd", "brep", "geometrybase",
}
ACCESS = {"item", "list", "tree", 0, 1, 2}
EXPOSURE = {-1, 2, 4, 8, 16, 32, 64, 128}  # -1 hidden; 2 the panel's first row, 4 the second, ...


@pytest.mark.parametrize("folder", COMPONENTS, ids=lambda p: p.name)
def test_metadata_uses_values_the_build_accepts(folder):
    meta = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
    assert meta.get("category") and meta.get("subcategory"), "category is the tab, subcategory the panel in it"
    assert meta.get("exposure", 2) in EXPOSURE
    for port in meta["ghpython"]["inputParameters"]:
        assert port.get("typeHintID", "ghdoc") in TYPE_HINTS, f"{port['name']}: unknown typeHintID"
        assert port.get("scriptParamAccess", 0) in ACCESS, f"{port['name']}: access is item, list or tree"


@pytest.mark.parametrize("folder", COMPONENTS, ids=lambda p: p.name)
def test_icon_is_a_24_pixel_png(folder):
    head = (folder / "icon.png").read_bytes()[:24]
    assert head[:8] == b"\x89PNG\r\n\x1a\n", "icon.png must be a PNG"
    assert (int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")) == (24, 24)


@pytest.mark.parametrize("folder", COMPONENTS, ids=lambda p: p.name)
def test_runscript_returns_one_value_per_output(folder):
    tree = ast.parse((folder / "code.py").read_text(encoding="utf-8"))
    run = next(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == "RunScript")
    outputs = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))["ghpython"]["outputParameters"]
    for ret in (node for node in ast.walk(run) if isinstance(node, ast.Return) and node.value is not None):
        returned = len(ret.value.elts) if isinstance(ret.value, ast.Tuple) else 1
        assert returned == len(outputs), f"line {ret.lineno} returns {returned} values for {len(outputs)} outputs"


@pytest.mark.parametrize("folder", COMPONENTS, ids=lambda p: p.name)
def test_the_names_rhino_writes_into_runscript_exist(folder):
    # Rhino writes hints like `spans: System.Collections.Generic.List[float]` into the
    # signature when a component is placed; without these imports it fails at once.
    tree = ast.parse((folder / "code.py").read_text(encoding="utf-8"))
    imported = {alias.name for node in tree.body if isinstance(node, ast.Import) for alias in node.names if not alias.asname}
    assert {"Grasshopper", "Rhino", "System"} <= imported, "import Grasshopper, Rhino and System below the dashes"
