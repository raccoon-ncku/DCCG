from compas_viewer import Viewer
import compas.geometry as cg
from tracing_drone import TracingDrone
import random

FRAMERATE = 20
MAX_FRAME = 10000
DRONE_COUNT = 20

TARGET_COUNT = 5
NEGATIVE_TARGET_COUNT = 5

viewer = App(show_grid=False, enable_sidebar=True, width=1600, height=900)

model_objs = []

targets = []
negative_targets = []

# Create targets
for i in range(TARGET_COUNT):
    target = cg.Frame(
        (random.randint(0, TracingDrone.length),
         random.randint(0, TracingDrone.width),
         random.randint(0, TracingDrone.height)),
        (1, 0, 0),
        (0, 1, 0)
    )
    targets.append(target)
    viewer.scene.add(cg.Sphere(target.point, 1), facecolor=(0, 0.7, 0))

# Create negative targets
for i in range(NEGATIVE_TARGET_COUNT):
    negative_target = cg.Frame(
        (random.randint(0, TracingDrone.length),
         random.randint(0, TracingDrone.width),
         random.randint(0, TracingDrone.height)),
        (1, 0, 0),
        (0, 1, 0)
    )
    negative_targets.append(negative_target)
    viewer.scene.add(cg.Sphere(negative_target.point, 1), facecolor=(0.7, 0, 0))


for i in range(DRONE_COUNT):
    # Create drones
    init_location = cg.Frame(
        (random.randint(0, TracingDrone.length), random.randint(0, TracingDrone.width), 0),
        (1, 0, 0),
        (0, 1, 0)
    )
    drone = TracingDrone(init_location)
    drone.targets = targets
    drone.negative_targets = negative_targets

    # Add the geometrical representation to the viewer
    viewer_obj = viewer.scene.add(drone.get_body())

    # Add the drone to the model_objs list
    # Seperate the drone object and the viewer object
    # So that we can update the drone object and the viewer object seperately
    model_objs.append(
        {
            "obj": drone,
            "viewer_obj": viewer_obj
        }
    )

# change the behaviour weights
@viewer.slider(title="attraction", value=10, maxval=10, step=1)
def slide(value):
    value = value 
    TracingDrone.attraction_weight = value
    viewer.view.update()

# change the behaviour weights
@viewer.slider(title="repulsion", value=10, maxval=10, step=1)
def slide(value):
    value = value 
    TracingDrone.repulsion_weight = value
    viewer.view.update()

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
