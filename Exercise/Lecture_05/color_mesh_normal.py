import compas.datastructures as cd
import compas.geometry as cg
import pathlib
import math
from compas.colors import Color
from compas_viewer import Viewer

fp = pathlib.Path(__file__).parent / "data" / "Bunny.ply"

mesh = cd.Mesh.from_ply(fp)
S = cg.Scale.from_factors([100, 100, 100])
R = cg.Rotation.from_axis_and_angle(cg.Vector(1, 0, 0), math.radians(90))
mesh.transform(S * R)

for vertex in mesh.vertices():
    try:
        v_normal = mesh.vertex_normal(vertex)
        color = Color(
            abs(v_normal[0]),
            abs(v_normal[1]),
            abs(v_normal[2])
            )
        mesh.vertex_attribute(vertex, 'color', color)
    except:
        continue
    

viewer = Viewer()
viewer.scene.add(mesh, use_vertex_color=True)
viewer.show()