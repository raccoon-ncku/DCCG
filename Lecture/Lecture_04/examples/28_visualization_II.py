from compas.geometry import Sphere
from compas.colors import Color
from compas_viewer import Viewer


viewer = Viewer()

for x in range(5):
    for y in range(5):
        for z in range(5):
            sphere = Sphere(0.2,point=[x, y, z])
            viewer.scene.add(sphere,
                             facecolor=Color(x/5, y/5, z/5),)


viewer.show()