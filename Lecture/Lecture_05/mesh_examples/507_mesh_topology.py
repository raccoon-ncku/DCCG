from compas_view2.app import App
import compas
import compas.geometry as cg
import compas.datastructures as cd


mesh = cd.Mesh.from_obj(compas.get('hypar.obj'))

fkey = mesh.get_any_face()
n_fkeys = mesh.face_neighbors(fkey)

# Visualization
some_face = cd.Mesh()
v_keys = mesh.face_vertices(fkey)
for v_key in v_keys:
    some_face.add_vertex(
        v_key,
        x=mesh.vertex_coordinates(v_key)[0],
        y=mesh.vertex_coordinates(v_key)[1],
        z=mesh.vertex_coordinates(v_key)[2])
some_face.add_face(v_keys)

n_faces = []
for n_fkey in n_fkeys:
    v_keys = mesh.face_vertices(n_fkey)
    n_mesh = cd.Mesh()
    for v_key in v_keys:
        n_mesh.add_vertex(
            v_key,
            x=mesh.vertex_coordinates(v_key)[0],
            y=mesh.vertex_coordinates(v_key)[1],
            z=mesh.vertex_coordinates(v_key)[2])
    n_mesh.add_face(v_keys)
    n_faces.append(n_mesh)

viewer = App()
viewer.add(mesh, show_faces=False, opacity=0.5)
viewer.add(some_face, facecolor=(0.5, 1, 1))
for n_face in n_faces:
    viewer.add(n_face, facecolor=(0.8, 0, 0), opacity=0.3)
viewer.run()
