"""Check every built .ghuser against its source (runs inside the image).

    python3 verify_ghuser.py components build

Reads each file with GH_IO.dll and compares name, description, parameter
counts and embedded code with components/<Name>/. Exits 1 on any mismatch.
"""

import base64
import json
import os
import sys

import clr

clr.AddReference("/opt/ghio/GH_IO")
import System  # noqa: E402
from GH_IO.Serialization import GH_LooseChunk  # noqa: E402


def load(path):
    root = GH_LooseChunk("UserObject")
    root.Deserialize_Binary(System.IO.File.ReadAllBytes(path))
    inner = GH_LooseChunk("UserObject")
    inner.Deserialize_Binary(root.GetByteArray("Object"))
    return root, inner


def count(chunk, name):
    return sum(1 for i in range(chunk.ChunkCount) if chunk.Chunks[i].Name == name)


def check(source_dir, build_dir):
    name = os.path.basename(source_dir)
    meta = json.load(open(os.path.join(source_dir, "metadata.json")))
    code = open(os.path.join(source_dir, "code.py"), encoding="utf-8").read()
    path = os.path.join(build_dir, name + ".ghuser")
    if not os.path.exists(path):
        return [f"{name}: no {name}.ghuser was built"]

    root, inner = load(path)
    problems = []
    if root.GetString("Name") != meta["name"]:
        problems.append(f"{name}: name {root.GetString('Name')!r} != {meta['name']!r}")
    if root.GetString("Description") != meta.get("description"):
        problems.append(f"{name}: description differs from metadata.json")

    embedded = base64.b64decode(inner.FindChunk("Script").GetString("Text")).decode("utf-8")
    if embedded != code:
        problems.append(f"{name}: embedded code differs from code.py")

    params = inner.FindChunk("ParameterData")
    gh = meta.get("ghpython", {})
    for kind, key in (("InputParam", "inputParameters"), ("OutputParam", "outputParameters")):
        want, got = len(gh.get(key, [])), count(params, kind)
        if want != got:
            problems.append(f"{name}: {got} {kind}s, metadata.json declares {want}")
    return problems


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    bundles = sorted(d for d in os.listdir(src) if os.path.isdir(os.path.join(src, d)) and not d.startswith((".", "__")))
    problems = [p for d in bundles for p in check(os.path.join(src, d), out)]
    for d in bundles:
        if not any(p.startswith(d + ":") for p in problems):
            print(f"[verified] {d}.ghuser")
    for p in problems:
        print(f"[FAILED]   {p}")
    sys.exit(1 if problems else 0)
