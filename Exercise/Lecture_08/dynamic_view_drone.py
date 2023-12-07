from compas_view2.app import App
import compas.geometry as cg
from drone import Drone
import random

FRAMERATE = 20
MAX_FRAME = 1000
DRONE_COUNT = 10

viewer = App()

model_objs = []

for i in range(DRONE_COUNT):
    # Create drones
    init_location = cg.Frame(
        (random.randint(0, 50), random.randint(0, 50), 0),
        (1, 0, 0),
        (0, 1, 0)
    )
    drone = Drone(init_location)

    # Add the geometrical representation to the viewer
    viewer_obj = viewer.add(drone.get_body())

    # Add the drone to the model_objs list
    # Seperate the drone object and the viewer object
    # So that we can update the drone object and the viewer object seperately
    model_objs.append(
        {
            "obj": drone,
            "viewer_obj": viewer_obj
        }
    )


@viewer.on(interval=1000 / FRAMERATE, frames=MAX_FRAME)
def update(f):
    """
    This function is called every frame
    """
    for obj in model_objs:
        # Update the drone object
        obj["obj"].rise()
        obj["obj"].update()

        # Update the viewer object
        obj["viewer_obj"]._data = obj["obj"].get_body()
        obj["viewer_obj"].update()


viewer.show()
