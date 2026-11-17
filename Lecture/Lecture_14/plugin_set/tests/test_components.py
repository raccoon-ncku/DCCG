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
