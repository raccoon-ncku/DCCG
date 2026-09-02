#! python 3
# r: compas
"""
The Rhino ADAPTER: the only file in this workflow that touches Rhino.

Run this INSIDE Rhino 8 (command: ScriptEditor, open this file, F5).
The two magic comments above tell Rhino's script editor to use CPython 3
and to pip-install `compas` into Rhino's Python automatically.

All the intelligence lives outside Rhino: the core module (wall.py,
staircase.py) is pure COMPAS, developed and TESTED headlessly -- by you,
by an agent, by CI. What crosses the boundary into Rhino is only a
verified geometry artifact (a compas JSON file). This file just loads
and converts it. Keep adapters this boring on purpose: boring code that
cannot fail needs no tests.

    core (pure python + tests)  ->  artifact (.json)  ->  adapter (this file)
"""

import rhinoscriptsyntax as rs
import scriptcontext as sc

from compas import json_load
from compas.geometry import Box
from compas_rhino.conversions import box_to_rhino

# Ask for the artifact produced by the headless workflow,
# e.g. Lecture_12/output/wall.json or Lecture_11/output/04_result.json
path = rs.OpenFileName("Select a compas JSON artifact", "JSON (*.json)|*.json||")
if path:
    geometry = json_load(path)
    if not isinstance(geometry, list):
        geometry = [geometry]

    added = 0
    for item in geometry:
        if isinstance(item, Box):
            sc.doc.Objects.AddBox(box_to_rhino(item))
            added += 1

    sc.doc.Views.Redraw()
    print(f"Added {added} of {len(geometry)} objects from {path}")
