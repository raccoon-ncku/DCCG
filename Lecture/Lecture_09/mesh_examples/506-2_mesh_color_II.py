import math
import compas.datastructures as cd
import compas.geometry as cg
from compas.itertools import remap_values
from compas.colors import Color
from compas_viewer import Viewer
import pathlib
from random import random
filepath = pathlib.Path(__file__).parent / "data" / "Bunny.ply"

mesh = cd.Mesh.from_ply(filepath)
R = cg.Rotation.from_axis_and_angle(cg.Vector(1, 0, 0), math.radians(90))
S = cg.Scale.from_factors([100, 100, 100])
mesh.transform(R * S)

facecolor = {}
for face in mesh.faces():
    normal = mesh.face_normal(face)
    # Map normal [-1, 1] to color [0, 1]
    # x -> red, y -> green, z -> blue
    r = (normal[0] + 1) * 0.5
    g = (normal[1] + 1) * 0.5
    b = (normal[2] + 1) * 0.5
    facecolor[face] = Color(r, g, b)

viewer = Viewer()
viewer.scene.add(mesh, facecolor=facecolor)
viewer.show()
