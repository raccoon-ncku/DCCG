import compas
import compas.geometry as cg
import compas.datastructures as cd


mesh = cd.Mesh.from_obj(compas.get('hypar.obj'))

# Tags
tags = []
for vertex_key in mesh.vertices():
    tags.append(
        str(mesh.vertex_degree(vertex_key))
    )
# Or a one-line code
# tags = [str(mesh.vertex_degree(vertex_key)) for vertex_key in mesh.vertices()]

# Vertex coordinates
coordinates = [cg.Point(*mesh.vertex_coordinates(vertex_key))
               for vertex_key in mesh.vertices()]


from compas_viewer import Viewer
from compas_viewer.scene import Tag
viewer = Viewer()

viewer.scene.add(mesh)
for i, tag in enumerate(tags):
    viewer.scene.add(
        Tag(tag, coordinates[i])
    )
viewer.show()
