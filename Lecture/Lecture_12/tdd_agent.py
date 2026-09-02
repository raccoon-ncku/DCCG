"""
Test-driven agent: pytest is the reviewer now.

In Lecture 11 the reviewer was another LLM -- helpful, but it can be
wrong, and it can be talked into approving. A test suite cannot. This
script closes the software-engineering loop:

    HUMAN (planner)   writes test_wall.py -- the executable spec
    CODER agent       writes wall.py
    HARNESS           runs pytest, feeds failures back verbatim
    ...repeat until green...
    HUMAN (reviewer)  reads the green code and judges its QUALITY

Notice the division of labor: the tests decide CORRECT, the human
decides GOOD. Tests can't see naming, structure, or wasted effort --
that review is still yours.

Run:
    python tdd_agent.py
    python tdd_agent.py --auto      (skip the human gate; for demos)
    python ../Lecture_11/view.py output/wall.json
"""

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "Lecture_11"))  # reuse the course LLM helper
from llm import chat, get_client

OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

AUTO = "--auto" in sys.argv[1:]
MAX_ROUNDS = 6

CODER_SYSTEM = """You are a Python programmer writing a COMPAS 2.x module.
Rules:
- Output exactly ONE python code block (```python ... ```), nothing else.
- Allowed imports: math, compas.geometry.
- Build geometry with this API only:
    from compas.geometry import Box, Frame
    Frame([x, y, z], [1, 0, 0], [0, 1, 0])   # a frame at center point x,y,z
    Box(xsize, ysize, zsize, frame=frame)     # box centered on that frame
- The module must define the function the tests import. No main block,
  no prints, no file IO -- a pure module.
- Units are meters, z points up. A box resting on the ground has center z = zsize/2.
- Write clean code: clear names, brief comments. A human reviews it after the tests pass."""

spec = (HERE / "test_wall.py").read_text()

client = get_client()
messages = [
    {"role": "system", "content": CODER_SYSTEM},
    {
        "role": "user",
        "content": "Write `wall.py` so that this pytest spec passes:\n\n" + spec,
    },
]


def run_pytest():
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "test_wall.py", "-q", "--no-header"],
        capture_output=True, text=True, timeout=120, cwd=HERE,
    )
    return proc.returncode, (proc.stdout + proc.stderr).strip()


for round_no in range(1, MAX_ROUNDS + 1):
    print(f"\n{'=' * 60}\nROUND {round_no}\n{'=' * 60}")

    reply = chat(client, messages)
    messages.append({"role": "assistant", "content": reply.content})
    match = re.search(r"```(?:python)?\s*\n(.*?)```", reply.content, re.DOTALL)
    if not match:
        messages.append({"role": "user", "content": "Output one ```python``` block."})
        continue
    code = match.group(1)
    print(code)

    # Human gate: pytest will IMPORT this module, which executes it.
    if not AUTO:
        answer = input("\nRun the tests against this code? [Enter = yes / n = reject] ")
        if answer.strip().lower().startswith("n"):
            comment = input("Your feedback for the coder: ")
            messages.append({"role": "user", "content": f"Human rejected the code: {comment}"})
            continue

    (HERE / "wall.py").write_text(code)
    returncode, output = run_pytest()
    print(f"\n--- pytest ---\n{output[-1500:]}")

    if returncode == 0:
        print(f"\nGREEN after {round_no} round(s). Now do the HUMAN review of wall.py:")
        print("the tests proved it is correct -- is it also good code?")
        # Produce a viewable artifact from the verified module.
        subprocess.run(
            [
                sys.executable, "-c",
                "from wall import running_bond_wall\n"
                "from compas import json_dump\n"
                "json_dump(running_bond_wall(3.0, 1.5), 'output/wall.json')\n"
                "print('artifact -> output/wall.json')",
            ],
            cwd=HERE,
        )
        print("View with:  python ../Lecture_11/view.py output/wall.json")
        break

    # Feed the failures back verbatim -- pytest output is precise,
    # honest feedback, better than any prose we could write.
    messages.append(
        {"role": "user", "content": f"Tests failed:\n{output[-1500:]}\nFix wall.py."}
    )
else:
    print(f"\nStopped: {MAX_ROUNDS} rounds without green (guardrail).")
    print("Options, in order of preference: improve the failing test's message, "
          "simplify the spec, or implement the tricky part yourself.")
