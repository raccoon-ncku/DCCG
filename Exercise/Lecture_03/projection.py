import compas.geometry as cg
import random
plane = cg.Plane((0, 0, 0), (0, 0, 1))
center_of_projection = cg.Point(10, 15, 15)
projection = cg.Projection.from_plane_and_point(plane, center_of_projection)


box_frame = cg.Frame([8, 8, 8], [-0.45, 2.1, 0.3], [1, 0, 0])
box = cg.Box(box_frame, 3, 3, 3)


pts = []
for pt in box.vertices:
    pts.append(pt.transformed(projection))

from compas_viewer import Viewer
from compas_view2.shapes import Text

viewer = Viewer()
viewer.view.camera.position = center_of_projection
viewer.view.camera.target = (0, 0, 0)
viewer.scene.add(box, opacity=0.5)
viewer.scene.add(center_of_projection)

for i, pt in enumerate(box.vertices):
    viewer.scene.add(Text(str(i), pt, height=30))

for pt in pts:
    # viewer.scene.add(pt)
    viewer.scene.add(cg.Line(center_of_projection, pt))

for i in range(4):
    viewer.scene.add(cg.Line(pts[i], pts[(i+1)%4]), linewidth=3)
    viewer.scene.add(cg.Line(pts[i+4], pts[(i+1)%4+4]), linewidth=3)
for pair in ((0, 4), (1, 7), (2, 6), (3, 5)):
    viewer.scene.add(cg.Line(pts[pair[0]], pts[pair[1]]), linewidth=3)
viewer.show()
