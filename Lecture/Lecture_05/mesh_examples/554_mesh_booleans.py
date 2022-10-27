import compas
import compas.geometry as cg
import compas.datastructures as cd
import compas_cgal.booleans as c_cgal_bool

b1 = cg.Box(cg.Frame([+4, +4, 2], [1, 0, 0], [0, 1, 0]), 10, 10, 10)
b2 = cg.Box(cg.Frame([-4, -4, -2], [1, 0, 0], [0, 1, 0]), 10, 10, 10)

A = cd.Mesh.from_shape(b1)
B = cd.Mesh.from_shape(b2)

A.quads_to_triangles()
B.quads_to_triangles()

A = A.to_vertices_and_faces()
B = B.to_vertices_and_faces()

# Use best boolean union available depending on context
# V, F = cg.boolean_union_mesh_mesh(A, B)
V, F = c_cgal_bool.boolean_union(A, B)

mesh = cd.Mesh.from_vertices_and_faces(V, F)
print(mesh.summary())

# Draw!
if compas.is_grasshopper():
    a = mesh
else:
    from compas_view2.app import App
    viewer = App()
    viewer.add(mesh)
    viewer.run()
