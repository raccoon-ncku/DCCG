import compas
import compas.datastructures as cd
from compas_viewer import Viewer
import pathlib

mesh = cd.Mesh.from_obj(compas.get('hypar.obj'))
mesh = mesh.subdivide(k=2, scheme='quad')
viewer = Viewer()

viewer.scene.add(mesh)
viewer.show()

path = pathlib.Path(__file__).parent / "mesh.stl"
mesh.quads_to_triangles()
mesh.to_stl(path)
