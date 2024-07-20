import random
import compas.geometry as cg
from compas_viewer import Viewer

geometries = []
for i in range(100):
    point = cg.Point(random.random(), random.random(), random.random())
    geometries.append(point)

# Visualization
viewer = Viewer()
viewer.scene.add(geometries)
viewer.show()
