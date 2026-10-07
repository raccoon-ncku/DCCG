import random
import compas.geometry as cg
import compas.datastructures as cd
from compas.colors import Color
from compas_viewer import Viewer


# Create a sphere and convert it to a mesh
sphere = cg.Sphere(1, cg.Frame.worldXY())
mesh = cd.Mesh.from_shape(sphere, u=50, v=50)

pts = []

for i in range(3):
    vector = cg.Vector(
        random.random()-0.5,
        random.random()-0.5,
        random.random()-0.5)
    vector.unitize()
    vector.scale(2)
    pts.append(cg.Point(*vector))

for vertex in mesh.vertices():
    vertex_pt = cg.Point(*mesh.vertex_coordinates(vertex))
    color = []
    force = cg.Vector(0,0,0)
    for pt in pts:
        d = cg.distance_point_point(vertex_pt, pt)
        force_component = cg.Vector.from_start_end(vertex_pt, pt)
        force_component.unitize()
        force_component.scale(5/d**2.5)
        force += force_component
        c = d / 4
        color.append(c)
    translation = cg.Translation.from_vector(force)
    vertex_pt.transform(translation)
    mesh.vertex_attributes(vertex, 'xyz', vertex_pt)
    mesh.vertex_attribute(vertex, 'color', Color(*color))


# Viz
viewer = Viewer(show_grid=False)
viewer.scene.add(mesh, use_vertex_color=True)
for pt in pts:
    viewer.scene.add(pt)
viewer.show()

