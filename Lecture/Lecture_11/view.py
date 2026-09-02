"""
Tiny viewer for the geometry files produced in this lecture.

Usage:
    uv run view.py output/02_boxes.json
"""

import sys

from compas import json_load
from compas_viewer import Viewer

path = sys.argv[1] if len(sys.argv) > 1 else "output/02_boxes.json"

geometry = json_load(path)
if not isinstance(geometry, list):
    geometry = [geometry]

viewer = Viewer()
for item in geometry:
    viewer.scene.add(item)
print(f"Showing {len(geometry)} objects from {path}")
viewer.show()
