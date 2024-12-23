import compas.geometry as cg
import compas.datastructures as cd
from compas_viewer import Viewer

box_frame = cg.Frame((3, 0, 0), (1, 2, 3), (-1, 3, 4))
box = cg.Box(3, 2, 4, box_frame)
mesh_box = cd.Mesh.from_shape(box)

# Polygon
p1 = [0, 0, 0]
p2 = [1, 0, 0]
p3 = [1, 1, 0]
p4 = [0, 0, 0]
polygon = cg.Polygon([p1, p2, p3])
mesh_polygon = cd.Mesh.from_polygons([polygon])

# Some modules return mesh as (vertices, faces)
# mesh = cd.Mesh.from_vertices_and_faces(vertices, faces)

# Draw!
viewer = Viewer()
viewer.scene.add([mesh_box, mesh_polygon])
viewer.show()
