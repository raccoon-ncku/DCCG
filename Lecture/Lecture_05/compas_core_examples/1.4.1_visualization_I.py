import random
import compas.geometry as cg
from compas.colors import Color
from compas_viewer import Viewer

geometries = []
for i in range(100):
    point = cg.Point(random.random(), random.random(), random.random())
    geometries.append(point)

# Visualization
viewer = Viewer()
for geometry in geometries:
    viewer.scene.add(geometry, pointcolor=Color.red())
viewer.show()
