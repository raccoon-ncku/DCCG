"""
Step 2: The LLM as a component INSIDE your program.

In step 1 the output was prose for a human. Here we force the model to
answer in JSON so that *code* can consume the answer: the model designs
a stack of boxes, and COMPAS builds the actual geometry.

This is the smallest useful pattern: the LLM never touches your program
directly -- it only produces DATA, which you validate before using.

Run:
    uv run 02_structured.py "a spiral staircase of 12 steps, going up counter-clockwise"
    uv run view.py output/02_boxes.json
"""

import json
import re
import sys
from pathlib import Path

from compas import json_dump
from compas.geometry import Box, Frame

from llm import chat, get_client

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

brief = sys.argv[1] if len(sys.argv) > 1 else "a staircase of 10 steps rising to 3 meters"

# --- 1. Ask for data, not prose ---------------------------------------
# We describe the exact schema we want. With small models, being strict
# and giving one concrete example ("few-shot") works far better than
# abstract instructions.
messages = [
    {
        "role": "system",
        "content": (
            "You are a geometry generator. You output ONLY a JSON object, "
            "no explanations, no markdown fences.\n"
            "Schema:\n"
            '{"boxes": [{"x": 0.0, "y": 0.0, "z": 0.15, '
            '"xsize": 1.0, "ysize": 0.3, "zsize": 0.3}]}\n'
            "x, y, z are the CENTER of each box in meters; z points up; "
            "boxes must rest on top of each other or the ground (z=0), never float."
        ),
    },
    {"role": "user", "content": f"Generate the boxes for: {brief}"},
]

reply = chat(client := get_client(), messages)
print("--- raw model output ---")
print(reply.content)

# --- 2. NEVER trust model output: parse defensively -------------------
# Even when told not to, models sometimes wrap JSON in ```fences``` or
# add a sentence. Real harnesses always sanitize before parsing.
text = reply.content.strip()
match = re.search(r"\{.*\}", text, re.DOTALL)  # grab the outermost {...}
if not match:
    raise SystemExit("Model did not return JSON. Try running again or rephrase the brief.")
data = json.loads(match.group(0))

# --- 3. Validate, then build real geometry ----------------------------
boxes = []
for i, b in enumerate(data["boxes"]):
    for key in ("x", "y", "z", "xsize", "ysize", "zsize"):
        if key not in b:
            raise SystemExit(f"Box {i} is missing '{key}': {b}")
    frame = Frame([b["x"], b["y"], b["z"]], [1, 0, 0], [0, 1, 0])
    boxes.append(Box(b["xsize"], b["ysize"], b["zsize"], frame=frame))

json_dump(boxes, OUT / "02_boxes.json")
print(f"\nBuilt {len(boxes)} COMPAS boxes -> output/02_boxes.json")
print("View them with:  python view.py output/02_boxes.json")
