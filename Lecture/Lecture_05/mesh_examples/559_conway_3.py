import compas.geometry as cg
from compas.datastructures import Mesh
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
box = cg.Box(cg.Frame.worldXY(), 1, 1, 1)
mesh = Mesh.from_shape(box)


# Operators
mesh = mesh_conway_ambo(mesh_conway_kis(mesh_conway_ambo(mesh)))


# Viz
viewer = App()
viewer.add(mesh)
viewer.run()
