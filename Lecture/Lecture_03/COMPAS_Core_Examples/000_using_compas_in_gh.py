import compas
import compas.geometry as cg

# Modeling and Computation
point = cg.Point(19,25,7)

geometries = [point]

# Visualization
if compas.is_grasshopper():
    a = geometries
else:
    from compas_view2.app import App
    viewer = App()
    for geometry in geometries:
        viewer.add(geometry)
    viewer.run()
