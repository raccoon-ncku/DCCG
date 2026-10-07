import time
import compas
import compas.geometry as cg
import compas.datastructures as cd


# load mesh
mesh = cd.Mesh.from_ply(compas.get('bunny.ply'))
v, f = mesh.to_vertices_and_faces()
print("The mesh has {} vertices.".format(len(v)))

# create Transformation
T = cg.Rotation.from_axis_and_angle(
    [-0.248, -0.786, -0.566], 2.78, point=[1.0, 0.0, 0.0])

# transform points with transform_points
t0 = time.time()
cg.transform_points(v, T)
print("transform_points takes {:.4f} seconds.".format(time.time() - t0))

# transform points with transform_points_numpy
t0 = time.time()
cg.transform_points_numpy(v, T)
print("transform_points_numpy takes {:.4f} seconds.".format(time.time() - t0))
