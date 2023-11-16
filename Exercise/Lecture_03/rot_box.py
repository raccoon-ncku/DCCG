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
            rot = cg.Rotation.from_axis_and_angle([0,0,z], x+y+z)
            translation = cg.Translation.from_vector([x*STEP_X, y*STEP_Y, z*STEP_Z])
            frame = cg.Frame((0,0,0), (1,0,0), (0,1,0))
            frame.transform(rot)
            frame.transform(translation)
            box = cg.Box(frame, STEP_X, STEP_Y, STEP_Z)
            geometries.append(box)
            properties.append({'facecolor': Color(x/SIZE_X, y/SIZE_Y, z/SIZE_Z)})

collection = Collection(geometries, properties)
viewer.add(collection)
viewer.run()