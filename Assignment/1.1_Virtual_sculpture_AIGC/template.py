import compas.geometry as cg
from compas_viewer import Viewer

geometries = []

# ==============================
# Replace the following lines with your code
# Remember to use the variable 'geometries' to store your geometries
# ==============================

import random
accumulated_height = 0
for i in range(5):
    box_height = random.randint(5, 8)
    f1 = cg.Frame([0, 0, accumulated_height + box_height/2], [random.random(), random.random(), 0], [0, 1, 0])
    box = cg.Box(f1, 10, 20, box_height)
    geometries.append(box)
    accumulated_height += box_height


# ==============================
# Visualization in Lineart mode
# ==============================

viewer = App(width=512, height=512, show_grid=False)
for geometry in geometries:
    viewer.scene.add(geometry, facecolor=(1, 1, 1), linecolor=(0, 0, 0))
viewer.show()