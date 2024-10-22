import numpy as np
from boid import Boid
from compas.geometry import Frame, Box
from compas_viewer import Viewer

FRAMERATE = 25
MAX_FRAME = 10000
BOID_COUNT = 30

viewer = App(show_grid=False, enable_sidebar=True, width=1600, height=900)

model_objs = []
flock = []

# Create boids
for _ in range(BOID_COUNT):
    frame = Frame(
        np.random.rand(3) * 50,
        (1, 0, 0),
        (0, 1, 0)
    )
    boid = Boid(frame)
    flock.append(boid)
    viewer_obj = viewer.scene.add(boid.get_body())
    model_objs.append(
        {
            "obj": boid,
            "viewer_obj": viewer_obj
        }
    )

# change the behaviour weights
@viewer.slider(title="Alignment", value=50, maxval=100, step=1)
def slide(value):
    value = value / 100
    Boid.alignment_weight = value
    viewer.view.update()

@viewer.slider(title="Cohesion", value=50, maxval=100, step=1)
def slide(value):
    value = value / 100
    Boid.cohesion_weight = value
    viewer.view.update()

@viewer.slider(title="Seperation", value=50, maxval=100, step=1)
def slide(value):
    value = value / 100
    Boid.separation_weight = value
    viewer.view.update()

@viewer.on(interval=1000 / FRAMERATE, frames=MAX_FRAME)
def update(f):
    for obj in model_objs:
        obj["obj"].warp()
        obj["obj"].apply_behaviour(flock)
        obj["obj"].update()
        obj["viewer_obj"]._data = obj["obj"].get_body()
        obj["viewer_obj"].update()


# Visualize
# Add the world box
viewer.scene.add(Box.from_diagonal(((0, 0, 0), (Boid.length, Boid.width, Boid.height))),
           show_lines=True, show_faces=False)
viewer.show()
