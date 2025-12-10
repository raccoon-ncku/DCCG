from compas_viewer import Viewer
import compas.geometry as cg
from ant import Ant
import random

AGENT_COUNT = 100

viewer = Viewer()

ants = []

for i in range(AGENT_COUNT):
    ant = Ant(random.randint(0, 50), random.randint(0, 50))

    # pass the viewer object to the ant, so it can update its position
    viewer_obj = viewer.scene.add(ant.body)
    ant.set_viewer_obj(viewer_obj)

    ants.append(ant)


@viewer.on(interval=100)
def update(frame):
    for ant in ants:
        ant.move()

        # update the object in the viewer
        ant.viewer_obj.update(update_data=True)


viewer.show()
