from compas.datastructures import Mesh
from compas.geometry import Point, Box
from compas.geometry import Translation, Scale
from compas_viewer import Viewer

box = Box.from_diagonal([(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)])
mesh = Mesh.from_shape(box)

trimesh = Mesh.from_polyhedron(4)
tribox = trimesh.aabb()

S = tribox.width / box.width

trimesh.transform(Scale.from_factors([S, S, S]))
trimesh.transform(Translation.from_vector(
    Point(0.5, 0.5, 0.5) - Point(0, 0, 0)))

tri = mesh.subdivided(k=3, scheme='tri')
quad = mesh.subdivided(k=3, scheme='quad')
corner = mesh.subdivided(k=3, scheme='corner')
ck = mesh.subdivided(k=3, scheme='catmullclark')
doosabin = mesh.subdivided(k=3, scheme='doosabin')
frames = mesh.subdivided(offset=0.2, scheme='frames', add_windows=True)
loop = trimesh.subdivided(k=3, scheme='loop')

corner.transform(Translation.from_vector([1.2 * 1, 0.0, 0.0]))
loop.transform(Translation.from_vector([1.2 * 2, 0.0, 0.0]))
quad.transform(Translation.from_vector([1.2 * 3, 0.0, 0.0]))
ck.transform(Translation.from_vector([1.2 * 4, 0.0, 0.0]))
doosabin.transform(Translation.from_vector([1.2 * 5, 0.0, 0.0]))
frames.transform(Translation.from_vector([1.2 * 6, 0.0, 0.0]))

viewer = Viewer(viewmode="lighted")

viewer.scene.add(tri, show_faces=False, show_lines=True)
viewer.scene.add(corner, facecolor=(0.2, 0.2, 0.2),
           linecolor=(0.0, 0.0, 0.0), opacity=0.3)
viewer.scene.add(loop, facecolor=(0, 1, 1), opacity=1.0)
viewer.scene.add(quad)
viewer.scene.add(ck, facecolor=(1, 0, 0), opacity=0.7)
viewer.scene.add(doosabin, facecolor=(0, 0, 1), opacity=0.7)
viewer.scene.add(frames, facecolor=(1, 1, 1), opacity=1.0)

viewer.show()
