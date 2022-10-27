from compas.datastructures import Mesh
from compas.geometry import Point, Box
from compas.geometry import Translation, Scale
from compas_view2 import app

box = Box.from_diagonal([(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)])
mesh = Mesh.from_shape(box)

trimesh = Mesh.from_polyhedron(4)
tribox = Box.from_bounding_box(trimesh.bounding_box())

S = tribox.width / box.width

trimesh.transform(Scale.from_factors([S, S, S]))
trimesh.transform(Translation.from_vector(
    Point(0.5, 0.5, 0.5) - Point(0, 0, 0)))

tri = mesh.subdivide(k=3, scheme='tri')
quad = mesh.subdivide(k=3, scheme='quad')
corner = mesh.subdivide(k=3, scheme='corner')
ck = mesh.subdivide(k=3, scheme='catmullclark')
doosabin = mesh.subdivide(k=3, scheme='doosabin')
frames = mesh.subdivide(offset=0.2, scheme='frames', add_windows=True)
loop = trimesh.subdivide(k=3, scheme='loop')

corner.transform(Translation.from_vector([1.2 * 1, 0.0, 0.0]))
loop.transform(Translation.from_vector([1.2 * 2, 0.0, 0.0]))
quad.transform(Translation.from_vector([1.2 * 3, 0.0, 0.0]))
ck.transform(Translation.from_vector([1.2 * 4, 0.0, 0.0]))
doosabin.transform(Translation.from_vector([1.2 * 5, 0.0, 0.0]))
frames.transform(Translation.from_vector([1.2 * 6, 0.0, 0.0]))

viewer = app.App(viewmode="lighted")

viewer.add(tri, show_faces=False, show_lines=True)
viewer.add(corner, facecolor=(0.2, 0.2, 0.2),
           linecolor=(0.0, 0.0, 0.0), opacity=0.3)
viewer.add(loop, facecolor=(0, 1, 1), opacity=1.0)
viewer.add(quad)
viewer.add(ck, facecolor=(1, 0, 0), opacity=0.7)
viewer.add(doosabin, facecolor=(0, 0, 1), opacity=0.7)
viewer.add(frames, facecolor=(1, 1, 1), opacity=1.0)

viewer.show()
