import compas
import compas.geometry as cg
import compas.datastructures as cd

b1 = cg.Box(10, 10, 10, cg.Frame([+4, +4, 2], [1, 0, 0], [0, 1, 0]))
b2 = cg.Box(10, 10, 10, cg.Frame([-4, -4, -2], [1, 0, 0], [0, 1, 0]))

A = cd.Mesh.from_shape(b1)
B = cd.Mesh.from_shape(b2)

A.quads_to_triangles()
B.quads_to_triangles()

A = A.to_vertices_and_faces()
B = B.to_vertices_and_faces()

# Use best boolean union available depending on context
# V, F = cg.boolean_union_mesh_mesh(A, B)
V, F = cg.boolean_union_mesh_mesh(A, B)

mesh = cd.Mesh.from_vertices_and_faces(V, F)
print(mesh.summary())

# Draw!
from compas_viewer import Viewer
viewer = Viewer()
viewer.scene.add(mesh)
viewer.show()
