from compas_viewer import Viewer
import compas.geometry as cg
from drone import Drone
import random

DRONE_COUNT = 1

viewer = Viewer()

drones = []

for i in range(DRONE_COUNT):
    init_location = cg.Frame(
        (random.randint(0, 50), random.randint(0, 50), 0),
        (1, 0, 0),
        (0, 1, 0)
    )
    drone = Drone(init_location)
    drone.velocity = cg.Vector(0,0,1) # set the initial velocity to 1 in the z direction

    # pass the viewer object to the drone, so it can update its position
    viewer_obj = viewer.scene.add(drone.body)
    drone.set_viewer_obj(viewer_obj)

    drones.append(drone)


@viewer.on(interval=100)
def update(frame):
    for drone in drones:
        drone.move()

        # update the object in the viewer
        drone.viewer_obj.update()


viewer.show()
