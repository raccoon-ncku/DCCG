import compas.datastructures as cd
from compas_view2.app import App
import pathlib

# pathlib is an object-oriented filesystem paths module
# which is available for Python > 3.4
filepath = pathlib.Path(__file__).parent / "data" / "Bunny.ply"

mesh = cd.Mesh.from_ply(filepath)
# mesh = cd.Mesh.from_stl(filepath)
# mesh = cd.Mesh.from_obj(filepath)
# mesh = cd.Mesh.from_off(filepath)

print(mesh.summary())

viewer = App()
viewer.add(mesh)
viewer.run()
