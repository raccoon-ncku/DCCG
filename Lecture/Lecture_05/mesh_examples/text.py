from random import random

import compas
from compas.colors import Color
from compas.datastructures import Mesh
from compas_viewer import Viewer

viewer = Viewer()

mesh = Mesh.from_obj(compas.get("faces.obj"))

for face_key in mesh.faces():
    color = Color(random(), random(), random())
    mesh.face_attribute(face_key, 'color', color.rgb)

viewer.scene.add(mesh)

viewer.show()