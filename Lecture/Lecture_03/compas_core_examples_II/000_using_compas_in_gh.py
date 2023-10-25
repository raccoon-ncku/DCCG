import compas
import compas.geometry as cg

# Modeling and Computation
point = cg.Point(19, 25, 7)

# Visualization
if compas.is_grasshopper():
    a = point
else:
    from compas_view2.app import App
    viewer = App()
    viewer.add(point)
    viewer.run()
