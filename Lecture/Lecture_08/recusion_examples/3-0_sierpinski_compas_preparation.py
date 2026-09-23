from compas_viewer import Viewer
import compas.geometry as cg
import compas.datastructures as cd

mesh = cd.Mesh.from_polyhedron(4)

(v, f) = mesh.to_vertices_and_faces()

print(v)
print(f)

# Vertex coordinates
coordinates = [cg.Point(*mesh.vertex_coordinates(vertex_key))
               for vertex_key in mesh.vertices()]


viewer = Viewer()
viewer.scene.add(mesh)
viewer.show()
