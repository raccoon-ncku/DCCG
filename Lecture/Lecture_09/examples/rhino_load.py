#! python 3
# r: compas
"""
The Rhino ADAPTER: run this INSIDE Rhino 8 (ScriptEditor, open this file, F5).

The two comments above tell Rhino to use CPython 3 and to install `compas`.
It only loads a verified JSON artifact and converts it:

    core (pure python + tests)  ->  artifact (.json)  ->  adapter (this file)
"""

import rhinoscriptsyntax as rs
import scriptcontext as sc

from compas import json_load
from compas.geometry import Box
from compas_rhino.conversions import box_to_rhino

# Ask for the artifact produced by the headless workflow,
# e.g. Lecture_13/output/wall.json or Lecture_15/agents/output/04_result.json
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
