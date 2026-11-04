"""
Step 3: Tools + a loop = an agent.

In step 2 the model answered once and we did the rest. An *agent* is
different: the model can call TOOLS (functions we expose), see the
results, and decide what to do next -- again and again, until it says
it is finished.

The important part of this file is not the model. It is the WHILE LOOP
at the bottom, called the "harness". Frameworks like CrewAI, LangGraph
or Claude Code are, at their core, this loop with more engineering
around it.

    while not done:
        reply = model(messages, tools)
        if reply wants a tool:
            result = run_tool(...)      <- OUR code runs, not the model
            messages.append(result)     <- the model sees what happened
        else:
            done

Run:
    uv run 03_agent_loop.py "a bridge spanning 6 meters between two towers"
    uv run view.py output/03_scene.json
"""

import json
import sys
from pathlib import Path

from compas import json_dump
from compas.geometry import Box, Frame

from llm import MODEL, get_client

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)

task = sys.argv[1] if len(sys.argv) > 1 else "a staircase of 8 steps, each 0.3 m high"

# --- 1. The tools we hand to the model ---------------------------------
# A "tool" is just a description (JSON schema) plus a Python function.
# The model never executes anything -- it can only ASK for a call;
# the harness (us) decides to actually run it.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "place_box",
            "description": (
                "Place one axis-aligned box in the 3D scene. "
                "x/y/z is the CENTER of the box in meters, z points up. "
                "Boxes must rest on the ground (z = zsize/2) or on other boxes."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {"type": "number"},
                    "y": {"type": "number"},
                    "z": {"type": "number"},
                    "xsize": {"type": "number"},
                    "ysize": {"type": "number"},
                    "zsize": {"type": "number"},
                },
                "required": ["x", "y", "z", "xsize", "ysize", "zsize"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "finish",
            "description": "Call this once when the structure is complete.",
            "parameters": {
                "type": "object",
                "properties": {"summary": {"type": "string"}},
                "required": ["summary"],
            },
        },
    },
]

scene = []  # the harness owns the state, not the model


def place_box(x, y, z, xsize, ysize, zsize):
    frame = Frame([x, y, z], [1, 0, 0], [0, 1, 0])
    scene.append(Box(xsize, ysize, zsize, frame=frame))
    return f"ok, box #{len(scene)} placed at ({x}, {y}, {z})"


# --- 2. The conversation setup -----------------------------------------
messages = [
    {
        "role": "system",
        "content": (
            "You are a construction agent. Build the requested structure by "
            "calling place_box, one box per call. Plan positions carefully so "
            "boxes stack correctly (a box resting on the ground has z = zsize/2). "
            "When the structure is complete, call finish. Do not chat."
        ),
    },
    {"role": "user", "content": task},
]

# --- 3. THE HARNESS: the loop that makes it an agent --------------------
client = get_client()
MAX_STEPS = 40  # guardrail: agents can loop forever; always set a budget

for step in range(MAX_STEPS):
    response = client.chat.completions.create(
        model=MODEL, messages=messages, tools=TOOLS, temperature=0, timeout=120
    )
    reply = response.choices[0].message

    if not reply.tool_calls:
        # The model chatted instead of acting -- a classic small-model
        # failure mode. We nudge it back on track.
        print(f"[step {step}] model said: {reply.content!r} -> nudging")
        messages.append({"role": "assistant", "content": reply.content})
        messages.append({"role": "user", "content": "Use the tools. Call finish when done."})
        continue

    # Echo the model's action request back into the history...
    messages.append(
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in reply.tool_calls
            ],
        }
    )

    # ...then execute each requested call and report the result back.
    # Models regularly produce malformed calls (missing arguments, invalid
    # JSON). The harness must never crash on bad input: catch the error and
    # send it BACK to the model, so it can correct itself on the next step.
    finished = False
    for tc in reply.tool_calls:
        try:
            args = json.loads(tc.function.arguments)
            if tc.function.name == "place_box":
                result = place_box(**args)
                print(f"[step {step}] place_box {args} -> {result}")
            elif tc.function.name == "finish":
                result = "scene saved"
                print(f"[step {step}] finish: {args.get('summary', '')}")
                finished = True
            else:
                result = f"error: unknown tool {tc.function.name}"
        except (json.JSONDecodeError, TypeError) as e:
            result = f"error: bad tool call ({e}). Provide all required arguments."
            print(f"[step {step}] {tc.function.name} FAILED -> {result}")
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

    if finished:
        break
else:
    print(f"Stopped: budget of {MAX_STEPS} steps exhausted (guardrail).")

json_dump(scene, OUT / "03_scene.json")
print(f"\n{len(scene)} boxes -> output/03_scene.json")
print("View with:  python view.py output/03_scene.json")
