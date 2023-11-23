from compas_view2.app import App
import compas.geometry as cg
from drone import Drone
import random

FRAMERATE = 1
MAX_FRAME = 1000
DRONE_COUNT = 10

viewer = App()

model_objs = []

for i in range(DRONE_COUNT):
    init_location = cg.Frame(
        (random.randint(0, 50), random.randint(0, 50), 0),
        (1, 0, 0),
        (0, 1, 0)
    )
    drone = Drone(init_location)
    drone.rise()
    viewer_obj = viewer.add(drone.get_body())

    model_objs.append(
        {
            "obj": drone,
            "viewer_obj": viewer_obj
        }
    )


@viewer.on(interval=1000 / FRAMERATE, frames=MAX_FRAME)
def update(f):
    for obj in model_objs:
        obj["obj"].move()
        obj["viewer_obj"]._data = obj["obj"].get_body()
        obj["viewer_obj"].update()


viewer.show()
