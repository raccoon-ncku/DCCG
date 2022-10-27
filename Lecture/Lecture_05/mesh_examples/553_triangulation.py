
import numpy as np
import compas.geometry as cg
from compas.datastructures import Mesh
from compas_cgal.triangulation import conforming_delaunay_triangulation as cdt
from compas_cgal.triangulation import refined_delaunay_mesh as rdm
from compas_view2.app import App

# ==============================================================================
# Constraints
# ==============================================================================

boundary = cg.Polygon.from_sides_and_radius_xy(12, 10)
boundary = np.array(boundary, dtype=np.float64)

hole = cg.Polygon.from_sides_and_radius_xy(12, 2)

hole1 = hole.transformed(cg.Translation.from_vector([4, 0, 0]))
hole2 = hole.transformed(cg.Translation.from_vector([-4, 0, 0]))
hole3 = hole.transformed(cg.Translation.from_vector([0, 4, 0]))
hole4 = hole.transformed(cg.Translation.from_vector([0, -4, 0]))

holes = [hole1, hole2, hole3, hole4]

points = [cg.Point(4, 0, 0), cg.Point(-4, 0, 0),
          cg.Point(0, 4, 0), cg.Point(0, -4, 0)]

# Triangulation
# conforming_delaunay_triangulation
V, F = cdt(boundary, points=points, holes=holes)

# refined_delaunay_mesh
cdt_mesh = Mesh.from_vertices_and_faces(V, F)

V, F = rdm(boundary, points=points, holes=holes,
           maxlength=1.0, is_optimized=True)

rdm_mesh = Mesh.from_vertices_and_faces(V, F)

# ==============================================================================
# Viz
# ==============================================================================

viewer = App()
viewer.add(cdt_mesh.transformed(cg.Translation.from_vector([0, -12, 0])))
viewer.add(rdm_mesh.transformed(cg.Translation.from_vector([0, 12, 0])))
viewer.run()
