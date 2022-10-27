from compas.geometry import Point, Box, Sphere, Translation
from compas.geometry import bounding_box
from compas.datastructures import Mesh

from compas_cgal.booleans import boolean_union
from compas_cgal.booleans import boolean_difference
from compas_cgal.booleans import boolean_intersection
from compas_cgal.meshing import remesh

from compas_view2.app import App

# Make a box and a sphere
box = Box.from_width_height_depth(2, 2, 2)
box = Mesh.from_shape(box)
box.quads_to_triangles()

A = box.to_vertices_and_faces()

sphere = Sphere(Point(1, 1, 1), 1)
sphere = Mesh.from_shape(sphere, u=30, v=30)
sphere.quads_to_triangles()

B = sphere.to_vertices_and_faces()
B = remesh(B, 0.3, 10)

# Create a bounding box to organize visualization
bbox = bounding_box(box.vertices_attributes('xyz') +
                    sphere.vertices_attributes('xyz'))
bbox = Box.from_bounding_box(bbox)
width = bbox.xsize


# Compute the boolean union
V, F = boolean_union(A, B)
union = Mesh.from_vertices_and_faces(V, F)


# Compute the boolean difference
V, F = boolean_difference(A, B)
difference = Mesh.from_vertices_and_faces(V, F)


# Compute the boolean intersection
V, F = boolean_intersection(A, B)
intersection = Mesh.from_vertices_and_faces(V, F)


# Visualize
viewer = App()

viewer.add(box, facecolor=(1, 0, 0), opacity=0.5)
viewer.add(sphere, facecolor=(0, 0, 1), opacity=0.5)
viewer.add(union.transformed(Translation.from_vector(
    [1 * 1.5 * width, 0, 0])), facecolor=(1, 0, 1))
viewer.add(difference.transformed(Translation.from_vector(
    [2 * 1.5 * width, 0, 0])), show_faces=False, show_lines=True, linecolor=(1, 0, 0))
viewer.add(intersection.transformed(Translation.from_vector(
    [2 * 1.5 * width, 0, 0])), facecolor=(0, 1, 0))

viewer.run()
