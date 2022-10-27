import compas
import compas.geometry as cg
import compas.datastructures as cd
from compas_view2.app import App

# Get Mesh
mesh = cd.Mesh.from_obj(compas.get('hypar.obj'))

# Identify boundary faces
fobs = mesh.faces_on_boundary()

# Modify mesh
for fkey in list(mesh.faces()):
    if fkey not in fobs:
        continue

    # Create and transform a new vertex
    cen = cg.Point(*mesh.face_centroid(fkey))
    normal = cg.Vector(*mesh.face_normal(fkey))
    normal.scale(0.3)
    cen.transform(cg.Translation.from_vector(normal))

    # Add the new vertex to the mesh
    new_vertex_key = mesh.add_vertex(x=cen[0], y=cen[1], z=cen[2])

    # Add faces
    fv = mesh.face_vertices(fkey)
    for i in range(-1, len(fv)-1):
        mesh.add_face((fv[i], fv[i+1], new_vertex_key))

    # Delete the old face
    mesh.delete_face(fkey)

# Visualization
viewer = App()
viewer.add(mesh)
viewer.run()
