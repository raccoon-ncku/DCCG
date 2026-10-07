import pathlib
import math
import compas.geometry as cg
from compas.datastructures import Mesh
from compas_cgal.meshing import trimesh_remesh
from compas_viewer import Viewer


FILE = pathlib.Path(__file__).parents[1] / "data" / "bunny.ply"

# Get the bunny and construct a mesh
bunny = Mesh.from_ply(FILE)
bunny.remove_unused_vertices()

# Move the bunny to the origin and rotate it upright.
T = cg.Translation.from_vector(cg.scale_vector(bunny.centroid(), -1))
S = cg.Scale.from_factors([100, 100, 100])
R = cg.Rotation.from_axis_and_angle(cg.Vector(1, 0, 0), math.radians(90))
bunny.transform(R * S * T)

mesh_before = bunny.transformed(cg.Translation.from_vector([0, -10, 0]))

# Remesh to 4x the average edge length
length = sum(bunny.edge_length(edge) for edge in bunny.edges()) / bunny.number_of_edges()
V, F = trimesh_remesh(bunny.to_vertices_and_faces(), 4 * length)
mesh_after = Mesh.from_vertices_and_faces(V, F)
mesh_after.transform(cg.Translation.from_vector([0, 10, 0]))

# Visualize
viewer = Viewer()
viewer.scene.add(mesh_before, facecolor=(0.7, 0.7, 0.7))
viewer.scene.add(mesh_after, facecolor=(0.7, 0.7, 0.7))
viewer.show()
