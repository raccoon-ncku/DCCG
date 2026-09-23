import compas.geometry as cg
from compas_viewer import Viewer
from compas_viewer.scene import Tag

viewer = Viewer()

u = cg.Vector(4, 1, 0)
v = cg.Vector(2, 5, 0)

# Vector Addition and Cross Product
u_p_v = u + v
u_cp_v = u.cross(v)

# Visualize vectors and their operations
viewer.scene.add(u)
viewer.scene.add(v)
viewer.scene.add(u_p_v)
viewer.scene.add(u_cp_v)
viewer.scene.add(Tag("u", u))
viewer.scene.add(Tag("v", v))
viewer.scene.add(Tag("u + v", u_p_v))
viewer.scene.add(Tag("u x v", u_cp_v))

viewer.show()