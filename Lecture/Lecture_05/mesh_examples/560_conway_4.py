import compas.geometry as cg
from compas.datastructures import Mesh
import compas_cgal.meshing
from compas.datastructures import (
    mesh_conway_ambo,
    mesh_conway_bevel,
    mesh_conway_dual,
    mesh_conway_expand,
    mesh_conway_gyro,
    mesh_conway_join,
    mesh_conway_kis,
    mesh_conway_meta,
    mesh_conway_needle,
    mesh_conway_ortho,
    mesh_conway_snub,
    mesh_conway_truncate
)

from compas_view2.app import App


# Mesh
sphere = cg.Sphere(cg.Point(1, 1, 1), 1)
sphere = Mesh.from_shape(sphere, u=30, v=30)
sphere.quads_to_triangles()

s = sphere.to_vertices_and_faces()
s = compas_cgal.meshing.remesh(s, 0.3, 10)
mesh = Mesh.from_vertices_and_faces(*s)


# Operators
mesh = mesh_conway_ambo(mesh_conway_truncate(mesh_conway_ambo(mesh)))


# Viz
viewer = App()
viewer.add(mesh)
viewer.run()
