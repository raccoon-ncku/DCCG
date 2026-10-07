import time
import compas
import compas.geometry as cg
import compas.datastructures as cd


# load mesh
mesh = cd.Mesh.from_ply(compas.get('bunny.ply'))
v, f = mesh.to_vertices_and_faces()
print("The mesh has {} vertices.".format(len(v)))


translation = [1, 2, 3]
A = cg.Translation.from_vector(translation)  # create Translation
axis, angle = [-0.8, 0.35, 0.5], 2.2
B = cg.Rotation.from_axis_and_angle(axis, angle)  # create Rotation
scale_factors = [0.1, 0.3, 0.4]
C = cg.Scale.from_factors(scale_factors)  # create Scale

# Transforming mesh one by one
mesh_1 = mesh.copy()
t0 = time.time()
mesh_1.transform(A)
mesh_1.transform(B)
mesh_1.transform(C)
print("Transforming mesh one by one takes {:.4f} seconds.".format(
    time.time() - t0))


# Transforming mesh with one concatenated matrix
mesh_2 = mesh.copy()
t0 = time.time()
mesh_2.transform(C * B * A)
print("Transforming mesh with one concatenated matrix takes {:.4f} seconds.".format(
    time.time() - t0))
