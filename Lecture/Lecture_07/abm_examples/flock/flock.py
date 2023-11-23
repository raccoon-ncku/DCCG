import numpy as np
from boid import Boid
from compas.geometry import Frame

from compas_view2.app import App

FRAMERATE = 25
MAX_FRAME = 10000
DRONE_COUNT = 50

viewer = App()

model_objs = []
flock = []

for _ in range(DRONE_COUNT):
    frame = Frame(
        np.random.rand(3) * 50,
        (1, 0, 0),
        (0, 1, 0)
    )
    boid = Boid(frame)
    flock.append(boid)
    viewer_obj = viewer.add(boid.get_body())
    model_objs.append(
        {
            "obj": boid,
            "viewer_obj": viewer_obj
        }
    )


@viewer.on(interval=1000 / FRAMERATE, frames=MAX_FRAME)
def update(f):
    for obj in model_objs:
        obj["obj"].warp()
        obj["obj"].apply_behaviour(flock)
        obj["obj"].update()

        obj["viewer_obj"]._data = obj["obj"].get_body()
        obj["viewer_obj"].update()


viewer.show()
