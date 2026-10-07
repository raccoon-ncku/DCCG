"""A timber frame as a graph (compas_timber): beams are nodes, joints are edges.

    uv run --extra timber Lecture/Lecture_06/graph_applications/timber_frame.py

Centrelines (mm) -> beams -> joint candidates classified L / T / X -> joints
chosen by a rule (a dict) -> joinery -> a BTLx file for CNC machines.
Headless this covers butt/miter/tenon joints and BTLx; lap, notch and dovetail
joints and cut geometry need Rhino. W06 README §11.
"""

import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from compas.geometry import Line
from compas.tolerance import Tolerance
from compas_timber.connections import JointTopology, LButtJoint, TButtJoint
from compas_timber.elements import Beam
from compas_timber.fabrication import BTLxWriter
from compas_timber.model import TimberModel

TOPOLOGY_NAMES = {
    JointTopology.TOPO_L: "L",
    JointTopology.TOPO_T: "T",
    JointTopology.TOPO_X: "X",
}

# The design decision: which joint for which way two beams meet.
# X crossings would be lap joints (XLapJoint) -- which need Rhino to cut,
# so headlessly we leave them as candidates and report them.
JOINT_RULE = {
    JointTopology.TOPO_L: LButtJoint,
    JointTopology.TOPO_T: TButtJoint,
}


def stud_wall(length=3600, height=2400, spacing=600, opening=(1200, 3000, 900, 2000), brace=True):
    """Centrelines (mm) of a stud wall: plates, studs, a window, a brace.

    opening = (x0, x1, sill height, header height). Studs that would cross
    the opening are replaced by short cripple studs above and below it.

    Returns {name: Line}.
    """
    x0, x1, sill, head = opening
    lines = {
        "bottom_plate": Line([0, 0, 0], [length, 0, 0]),
        "top_plate": Line([0, 0, height], [length, 0, height]),
        "sill": Line([x0, 0, sill], [x1, 0, sill]),
        "header": Line([x0, 0, head], [x1, 0, head]),
    }
    for i, x in enumerate(range(0, length + 1, spacing)):
        if x0 < x < x1:
            lines[f"cripple_{i}_low"] = Line([x, 0, 0], [x, 0, sill])
            lines[f"cripple_{i}_high"] = Line([x, 0, head], [x, 0, height])
        else:
            lines[f"stud_{i}"] = Line([x, 0, 0], [x, 0, height])
    if brace:
        lines["brace"] = Line([0, 0, 0], [x0, 0, height])
    return lines


def category(name):
    """plate / stud / opening / brace -- the role a centreline plays in the wall.

    Classifying single lines BEFORE they become beams is the first step of the
    topology-first workflow used in robotic timber research (e.g. the Spatial
    Timber Assemblies and Buga Wood projects): decide what each member IS,
    then let rules decide how members meet.
    """
    for prefix, cat in (("bottom_plate", "plate"), ("top_plate", "plate"), ("stud", "stud"),
                        ("cripple", "stud"), ("sill", "opening"), ("header", "opening"),
                        ("brace", "brace")):
        if name.startswith(prefix):
            return cat
    return "other"


def build_model(lines, width=60, height=120):
    """Beams from centrelines, joints from the rule. Returns (model, report)."""
    # tell the model its unit, and a tolerance that makes sense in mm
    model = TimberModel(tolerance=Tolerance(unit="MM", absolute=1e-3))
    for name, line in lines.items():
        beam = Beam.from_centerline(line, width, height, z_vector=[0, 1, 0])
        beam.name = name
        beam.attributes["category"] = category(name)
        model.add_element(beam)

    model.connect_adjacent_beams()
    candidates = list(model.joint_candidates)
    topologies = Counter(TOPOLOGY_NAMES.get(c.topology, str(c.topology)) for c in candidates)

    pairs = Counter(
        " - ".join(sorted(e.attributes["category"] for e in c.elements)) for c in candidates
    )
    joints, left_open = Counter(), []
    for candidate in candidates:
        joint = JOINT_RULE.get(candidate.topology)
        a, b = candidate.elements
        if joint is None:
            left_open.append((a.name, b.name, TOPOLOGY_NAMES.get(candidate.topology)))
            continue
        if joint is TButtJoint:
            # a T joint has an order: the beam that ENDS (main) butts into the
            # one that runs through (cross). Ask the candidate which is which.
            main, cross = (a, b) if _ends_at(a, b) else (b, a)
            joint.create(model, main, cross)
        else:
            joint.create(model, a, b)
        joints[joint.__name__] += 1

    errors = model.process_joinery()
    report = {
        "beams": len(list(model.beams)),
        "graph": (model.graph.number_of_nodes(), model.graph.number_of_edges()),
        "topologies": dict(topologies),
        "category_pairs": dict(pairs),
        "joints": dict(joints),
        "not_joined": left_open,
        "joinery_errors": [str(e) for e in errors],
    }
    return model, report


def _ends_at(a, b, tol=1.0):
    """True if one end of beam a lies on beam b's centreline (a butts into b)."""
    line = b.centerline
    for end in (a.centerline.start, a.centerline.end):
        closest = line.closest_point(end)
        if closest.distance_to_point(end) < tol + max(b.width, b.height) / 2:
            return True
    return False


def write_btlx(model, path):
    """Write the BTLx fabrication file. Returns {processing type: count}.

    The count is read back from the XML we just wrote -- parsing the artifact
    rather than trusting what we meant to put in it.
    """
    xml = BTLxWriter().model_to_xml(model)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(xml)
    counts = Counter()
    for element in ET.fromstring(xml).iter():
        if element.tag.endswith("Processings"):
            counts.update(child.tag.split("}")[-1] for child in element)
    return dict(counts)


def joints_per_beam(model):
    """{beam name: number of joints} -- a degree count on the model's graph."""
    return {beam.name: len(model.get_joints_for_element(beam)) for beam in model.beams}


if __name__ == "__main__":
    model, report = build_model(stud_wall())
    print(f"beams {report['beams']}; model graph: {report['graph'][0]} nodes, {report['graph'][1]} edges")
    print(f"how beams meet: {report['topologies']}")
    print(f"which roles meet: {report['category_pairs']}")
    print(f"joints made:    {report['joints']}")
    print(f"left for Rhino: {report['not_joined']}")
    print(f"joinery errors: {len(report['joinery_errors'])}")
    busiest = max(joints_per_beam(model).items(), key=lambda kv: kv[1])
    print(f"most-joined beam: {busiest[0]} ({busiest[1]} joints)")
    out = Path(__file__).parent / "output"
    n = write_btlx(model, out / "stud_wall.btlx")
    print(f"BTLx written: output/stud_wall.btlx -- machining: {n}")
