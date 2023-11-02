import compas.geometry as cg
from compas.colors import Color
from compas_view2.app import App
from compas_view2.collections import Collection

SIZE_X = 10
SIZE_Y = 10
SIZE_Z = 10
STEP_X = 5
STEP_Y = 5
STEP_Z = 5
viewer = App()
geometries = []
properties = []
for x in range(SIZE_X):
    for y in range(SIZE_Y):
        for z in range(SIZE_Z):
            pt = cg.Point(x*STEP_X, y*STEP_Y, z*STEP_Z)
            frame = cg.Frame(pt, (1,0,0), (0,1,0))
            box = cg.Box(frame, 1, 1, 1)
            geometries.append(box)
            properties.append({'facecolor': Color(x/SIZE_X, y/SIZE_Y, z/SIZE_Z)})

collection = Collection(geometries, properties)
viewer.add(collection)
viewer.run()