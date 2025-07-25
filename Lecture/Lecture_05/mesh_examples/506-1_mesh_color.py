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

z_min = float('inf')
z_max = float('-inf')

for vertex in mesh.vertices():
    z_coor = mesh.vertex_coordinates(vertex)[2]
    z_min = min(z_min, z_coor)
    z_max = max(z_max, z_coor)
print(z_min, z_max)

vertexcolor = {}
for vertex in mesh.vertices():
    red_value = 1 - remap_values(
        [mesh.vertex_coordinates(vertex)[2]],
        original_min=z_min,
        original_max=z_max)[0]
    color = Color(red_value,1-red_value,1-red_value)
    vertexcolor[vertex] = color

viewer = Viewer()
viewer.scene.add(mesh, use_vertexcolors=True, vertexcolor=vertexcolor)
viewer.show()
