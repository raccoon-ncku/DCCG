"""
Arash A. Adel
Modified by CC. Yen

1. Add probability to steer the steps

2. Add probability to influence the density of the
spheres according to height values or a percentage
of the total number of spheres

3. Investigate different coloring schemes

4. Implement rules for defining the radius of the
upcoming sphere based on the previously generated
sphere

5. Implement rules for defining the radius of the
upcoming sphere based on the distance of its center
to the center of the previously generated sphere

6. Implement moving rules
"""

import math
import random
import compas.geometry as cg
import compas



def walking(current_coor, previous_radius):
    """Perform walking."""

    # Probability to steer the steps
    steer_prob = random.random()
    acceleration = [0, 0, 0]
    if steer_prob < 0.2:
        acceleration[0] = random.gauss(3, 1.7)
        acceleration[1] = random.gauss(0, 0.7)
        acceleration[2] = random.gauss(0, 0.7)
    elif steer_prob < 0.5:
        acceleration[0] = random.gauss(0, 1.7)
        acceleration[1] = random.gauss(3, 0.7)
        acceleration[2] = random.gauss(0, 0.7)
    else:
        acceleration[0] = random.gauss(0, 0.7)
        acceleration[1] = random.gauss(0, 0.7)
        acceleration[2] = random.gauss(3, 0.7)

    direction = cg.Vector(*acceleration)
    direction.unitize()

    # probability to influence the density of the
    # spheres according to height values
    # -> Determine the step size
    height = current_coor[2]
    step_size = math.sqrt(math.pow(random.gauss(height * 0.1, 1), 2))
    direction.scale(step_size)
    new_coor = current_coor.transformed(cg.Translation.from_vector(direction))

    # Determine its radius
    # There is no math.abs() in IronPython
    radius = math.sqrt(math.pow((step_size - previous_radius), 2))

    # Determine its color?

    # Draw the sphere
    sphere_id = cg.Sphere(new_coor, radius)

    return sphere_id, new_coor, radius



previous_radius = 1
current_coor = cg.Point(0, 0, 0)
geometries = []
for i in range(100):
    sphere, current_coor, previous_radius = walking(
        current_coor, previous_radius)
    geometries.append(sphere)

if compas.is_grasshopper():
    a = geometries
else:
    from compas_view2.app import App
    viewer = App()
    for geometry in geometries:
        viewer.add(geometry)
    viewer.run()

