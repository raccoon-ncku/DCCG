import compas.geometry as cg
from compas_viewer import Viewer

# Box is created from a frame and xsize, ysize, zsize
box = cg.Box(1, 2, 4, cg.Frame.worldXY())

# Sphere is created from a point and radius
sphere = cg.Sphere(1, cg.Frame([5, 0, 0], [-0.45, 0.1, 0.3], [1, 0, 0]))

# Cylinder is created from a circle and height
cylinder = cg.Cylinder(0.5, 0.6, cg.Frame([10, 0, 0], [-0.45, 0.1, 0.3], [1, 0, 0]))

geometries = [box, sphere, cylinder]

# Visualization
viewer = Viewer()
for geometry in geometries:
    viewer.scene.add(geometry)
viewer.show()
