import compas
import compas.geometry as cg

# Modeling and Computation
point = cg.Point(19, 25, 7)

# Visualization
if compas.is_grasshopper():
    a = point
else:
    from compas_viewer import Viewer
    viewer = Viewer()
    viewer.scene.add(point)
    viewer.show()
