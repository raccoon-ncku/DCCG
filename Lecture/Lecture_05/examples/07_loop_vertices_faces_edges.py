import compas
import compas.geometry as cg
import compas.datastructures as cd


mesh = cd.Mesh.from_obj(compas.get('hypar.obj'))

print(mesh.summary())

print("\n\nVertex keys: ")
for vertex in mesh.vertices():
    print(vertex, end=", ")

print("\n\nFace keys: ")
for face in mesh.faces():
    print(face, end=", ")

print("\n\nEdge key pairs: ")
for i, edge in enumerate(mesh.edges()):
    print(i, edge, end=", ")
