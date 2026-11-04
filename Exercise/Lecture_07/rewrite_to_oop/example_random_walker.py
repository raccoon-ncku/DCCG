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


class Walker():
    def __init__(self, coordinate, radius):
        self.current_coordinate = coordinate
        self.radius = radius
        self.body = self._draw_body()

    def walk(self):
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
        height = self.current_coordinate[2]
        step_size = abs(random.gauss(height * 0.1, 1))
        direction.scale(step_size)
        self.current_coordinate.transform(cg.Translation.from_vector(direction))

        # Determine its radius
        self.radius = abs(step_size - self.radius)

        # Draw the sphere
        self.body = self._draw_body()

    def _draw_body(self):
        return cg.Sphere(self.current_coordinate, self.radius)


walker = Walker(cg.Point(0, 0, 1), 1)
geometries = []
for i in range(100):
    walker.walk()
    geometries.append(walker.body)

if compas.is_grasshopper():
    a = geometries
else:
    from compas_viewer import Viewer

    viewer = Viewer()
    for geometry in geometries:
        viewer.scene.add(geometry)
    viewer.show()
