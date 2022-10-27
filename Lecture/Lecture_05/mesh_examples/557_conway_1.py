from compas.geometry import Translation
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
mesh = Mesh.from_polyhedron(6)


# Operators
ambo = mesh_conway_ambo(mesh)
bevel = mesh_conway_bevel(mesh)
dual = mesh_conway_dual(mesh)
expand = mesh_conway_expand(mesh)
gyro = mesh_conway_gyro(mesh)
join = mesh_conway_join(mesh)
kis = mesh_conway_kis(mesh)
meta = mesh_conway_meta(mesh)
needle = mesh_conway_needle(mesh)
ortho = mesh_conway_ortho(mesh)
snub = mesh_conway_snub(mesh)
truncate = mesh_conway_truncate(mesh)


# Viz
T = Translation.from_vector
viewer = App()

viewer.add(ambo)
viewer.add(bevel.transformed(T([3, 0, 0])))
viewer.add(dual.transformed(T([6, 0, 0])))
viewer.add(expand.transformed(T([9, 0, 0])))

viewer.add(gyro.transformed(T([0, 4, 0])))
viewer.add(join.transformed(T([3, 4, 0])))
viewer.add(kis.transformed(T([6, 4, 0])))
viewer.add(meta.transformed(T([9, 4, 0])))

viewer.add(needle.transformed(T([0, 8, 0])))
viewer.add(ortho.transformed(T([3, 8, 0])))
viewer.add(snub.transformed(T([6, 8, 0])))
viewer.add(truncate.transformed(T([9, 8, 0])))

viewer.run()
