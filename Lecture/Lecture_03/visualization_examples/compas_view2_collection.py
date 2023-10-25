from random import random

from compas.geometry import Sphere
from compas.geometry import Polyline
from compas.colors import Color

from compas_view2.app import App
from compas_view2.collections import Collection

viewer = App()

spheres = []
sphere_properties = []

for x in range(5):
    for y in range(5):
        for z in range(5):
            sphere = Sphere([x, y, z], 0.2)
            spheres.append(sphere)
            sphere_properties.append({'u': 20, 'v': 5, 'facecolor': Color(x/5, y/5, z/5), 'linecolor': Color(0.2, 0, 0)})

spherecollection = Collection(spheres, sphere_properties)
viewer.add(spherecollection)

lines = []
line_properties = []
for i in range(100):
    line = Polyline([(random()*5 + 5, random()*5, random()*5), (random()*5 + 5, random()*5, random()*5), (random()*5 + 5, random()*5, random()*5)])
    lines.append(line)
    line_properties.append({'linecolor': Color(random(), random(), random())})

linecollection = Collection(lines, line_properties)
viewer.add(linecollection, linewidth=2)


viewer.show()