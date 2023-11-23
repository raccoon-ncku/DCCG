import compas
from math import radians
import compas.datastructures as cd
import compas.geometry as cg
from compas_view2.app import App
import pathlib

# ==============================================================================
# Get Bunny
# ==============================================================================

before = cd.Mesh.from_ply(compas.get_bunny())

# ==============================================================================
# Clean up
# ==============================================================================

before.cull_vertices()

# ==============================================================================
# Transform
# ==============================================================================

T = cg.Translation.from_vector(
    cg.Point(0, 0, 0) - cg.Point(*before.centroid()))
S = cg.Scale.from_factors([100, 100, 100])
R = cg.Rotation.from_axis_and_angle([1, 0, 0], radians(90))

before.transform(R * S * T)

# ==============================================================================
# Remesh
# ==============================================================================

L = sum(before.edge_length(*edge)
        for edge in before.edges()) / before.number_of_edges()

V, F = cg.trimesh_remesh(before.to_vertices_and_faces(), 3 * L)
after = cd.Mesh.from_vertices_and_faces(V, F)

# ==============================================================================
# Viz
# ==============================================================================

viewer = App()

box = cg.Box.from_bounding_box(before.bounding_box())
dx = 1.5 * box.xsize

viewer.add(before)
viewer.add(after.transformed(cg.Translation.from_vector([dx, 0, 0])))
viewer.run()

path = pathlib.Path(__file__).parent / "mesh.stl"
after.to_stl(path)
