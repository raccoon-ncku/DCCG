import compas.datastructures as cd
from compas_viewer import Viewer

# Create an empty mesh
mesh = cd.Mesh()

a = mesh.add_vertex()  # x,y,z coordinates are optional and default to 0,0,0
b = mesh.add_vertex(x=1)
c = mesh.add_vertex(x=1, y=1)
d = mesh.add_vertex(y=1)

mesh.add_face([a, b, c, d])

print(mesh.summary())

# Visualize the mesh
viewer = Viewer()
viewer.scene.add(mesh)
viewer.show()
