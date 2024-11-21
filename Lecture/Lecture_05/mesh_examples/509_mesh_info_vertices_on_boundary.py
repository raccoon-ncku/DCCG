import compas
import compas.geometry as cg
import compas.datastructures as cd
from compas_viewer import Viewer

mesh = cd.Mesh.from_obj(compas.get('hypar.obj'))

geometries = [mesh]

for vertex_key in mesh.vertices_on_boundary():
    geometries.append(cg.Point(*mesh.vertex_coordinates(vertex_key)))

viewer = Viewer()
for geometry in geometries:
    viewer.scene.add(geometry)
viewer.show()
