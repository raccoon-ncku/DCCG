from compas_view2.app import App
from compas.geometry import Pointcloud
from compas.datastructures import Mesh
from compas_cgal.triangulation import delaunay_triangulation

points = Pointcloud.from_bounds(8, 5, 0, 17)
triangles = delaunay_triangulation(points)
mesh = Mesh.from_vertices_and_faces(points, triangles)

viewer = App()
viewer.add(mesh)
viewer.run()
