from compas_viewer import Viewer
import compas.geometry as cg
from drone import Drone
import random

DRONE_COUNT = 10
CHANGE_TARGET_INTERVAL = 500

viewer = Viewer()

drones = []

initial_target = cg.Frame.from_points(
    (random.randint(0, 50), random.randint(0, 50), random.randint(0, 50)),
    (random.randint(0, 50), random.randint(0, 50), random.randint(0, 50)),
    (0, 0, 1)
)

for i in range(DRONE_COUNT):
    init_location = cg.Frame(
        (random.randint(0, 50), random.randint(0, 50), random.randint(0, 50)),
        (1, 0, 0),
        (0, 1, 0)
    )
    drone = Drone(init_location)
    # drone.velocity = cg.Vector(0,0,1) # set the initial velocity to 1 in the z direction
    drone.target = initial_target
    # pass the viewer object to the drone, so it can update its position
    viewer_obj = viewer.scene.add(drone.body)
    drone.set_viewer_obj(viewer_obj)

    drones.append(drone)


@viewer.on(interval=10)
def update(frame):
    if frame % CHANGE_TARGET_INTERVAL == 0:
        new_target = cg.Frame.from_points(
            (random.randint(0, 50), random.randint(0, 50), 0),
            (random.randint(0, 50), random.randint(0, 50), 0),
            (0, 0, 1)
        )
        for drone in drones:
            drone.target = new_target
    for drone in drones:
        drone.linear_approach()
        drone.move()
        # update the object in the viewer
        drone.viewer_obj.update()


viewer.show()
