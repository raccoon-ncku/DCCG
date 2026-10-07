import compas
import compas.datastructures as cd
from compas_viewer import Viewer

mesh = cd.Mesh.from_obj(compas.get('hypar.obj'))

viewer = Viewer()
viewer.scene.add(mesh)
viewer.show()
