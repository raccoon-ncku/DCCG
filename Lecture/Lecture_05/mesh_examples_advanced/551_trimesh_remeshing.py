import pathlib
import math
import compas.geometry as cg
from compas_cgal.trimesh import TriMesh
from compas_view2.app import App


FILE = pathlib.Path(__file__).parent / "data" / "Bunny.ply"

# Get the bunny and construct a mesh
bunny = TriMesh.from_ply(FILE)

# Remove unused vertices
bunny.cull_vertices()

# Move the bunny to the origin and rotate it upright.
vector = cg.scale_vector(bunny.centroid, -1)

T = cg.Translation.from_vector(vector)
S = cg.Scale.from_factors([100, 100, 100])
R = cg.Rotation.from_axis_and_angle(cg.Vector(1, 0, 0), math.radians(90))

bunny.transform(R * S * T)
mesh_before = bunny.to_mesh()
mesh_before.transform(cg.Translation.from_vector([0, -10, 0]))

# Remesh
length = bunny.average_edge_length
bunny.remesh(4 * length)
mesh_after = bunny.to_mesh()
mesh_after.transform(cg.Translation.from_vector([0, 10, 0]))

# Visualize
viewer = App()
viewer.add(mesh_before, facecolor=(0.7, 0.7, 0.7))
viewer.add(mesh_after, facecolor=(0.7, 0.7, 0.7))
viewer.run()
