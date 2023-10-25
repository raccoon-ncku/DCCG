import random
import compas.geometry as cg

geometries = []
for i in range(100):
    point = cg.Point(random.random(), random.random(), random.random())
    geometries.append(point)


# Visualization
from compas_view2.app import App
viewer = App()
for geometry in geometries:
    viewer.add(geometry)
viewer.run()
