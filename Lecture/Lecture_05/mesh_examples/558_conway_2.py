from compas.geometry import Translation
import compas.datastructures as cd
import compas
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

from compas_viewer import Viewer


# Mesh
mesh = cd.Mesh.from_polyhedron(20)
mesh = cd.Mesh.from_obj(compas.get('hypar.obj'))

# Operators
mesh = mesh_conway_ambo(mesh)
mesh = mesh_conway_truncate(mesh)
mesh = mesh.thickened(0.1)


# Viz
viewer = Viewer()
viewer.scene.add(mesh)
viewer.show()
