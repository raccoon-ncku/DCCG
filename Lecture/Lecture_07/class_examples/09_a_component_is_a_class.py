"""A Grasshopper component is a class. You write it, and Grasshopper calls it.

    uv run Lecture/Lecture_07/class_examples/09_a_component_is_a_class.py

Runs without Rhino: the first block stands in for what Rhino provides, and
solve() sketches what Grasshopper does. The real adapter is
Lecture_12/plugin_set/components/Cs_StudWall/code.py.
"""

import sys
from pathlib import Path


# --- stand-ins: in Rhino these two come from ghpythonlib and compas_rhino ------
class component:
    pass


def line_to_rhino(line):
    return f"<Rhino line, {line.length:.1f} m>"


# --- the core: pure, tested, and no idea that Grasshopper exists ---------------
# A real adapter also starts by putting the core's folder on sys.path.
sys.path.insert(0, str(Path(__file__).parents[2] / "Lecture_12" / "plugin_set" / "src"))
from compas_studio import StudWall  # noqa: E402


# --- the adapter: inherits from Grasshopper's class, holds no logic ------------
class Cs_StudWall(component):
    def RunScript(self, length, height, spacing):
        if not length or not height:                # an unconnected input arrives as None
            return None, None
        wall = StudWall(length, height, spacing) if spacing else StudWall(length, height)
        return [line_to_rhino(line) for line in wall.lines().values()], wall.n_studs


# --- metadata.json: the names on the component's ports -------------------------
METADATA = {"inputs": ["length", "height", "spacing"], "outputs": ["lines", "n_studs"]}


def solve(instance, **connected):
    """A sketch of Grasshopper: read the ports, call RunScript, fill the output ports."""
    arguments = [connected.get(name) for name in METADATA["inputs"]]
    return dict(zip(METADATA["outputs"], instance.RunScript(*arguments)))


node = Cs_StudWall()                                # you never write this line in Grasshopper
print(solve(node))                                  # nothing connected yet
print(solve(node, length=1.2, height=2.4))          # a slider moved: Grasshopper calls again
print(solve(node, length=1.2, height=2.4, spacing=1.2)["n_studs"])
