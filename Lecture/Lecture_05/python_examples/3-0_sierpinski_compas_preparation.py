from compas_view2.shapes import Text
from compas_view2.app import App
import compas.geometry as cg
import compas.datastructures as cd

mesh = cd.Mesh.from_polyhedron(4)

(v, f) = mesh.to_vertices_and_faces()

print(v)
print(f)

# Tags
tags = []
for vertex_key in mesh.vertices():
    tags.append(
        str(vertex_key)
    )
# Vertex coordinates
coordinates = [cg.Point(*mesh.vertex_coordinates(vertex_key))
               for vertex_key in mesh.vertices()]


viewer = App()

viewer.add(mesh)
for i, tag in enumerate(tags):
    viewer.add(
        Text(tag, coordinates[i])
    )
viewer.run()
