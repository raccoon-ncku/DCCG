
import random
import compas.geometry as cg
import compas


class Walker():
    def __init__(self):
        self.current_coor = cg.Point(0, 0, 0)
        self.radius = 1

    def walking(self):
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
        height = self.current_coor[2]
        step_size = abs(random.gauss(height * 0.1, 1))
        direction.scale(step_size)
        self.current_coor.transform(cg.Translation.from_vector(direction))

        # Determine its radius
        self.radius = abs(step_size - self.radius)

    def draw(self):
        return cg.Sphere(self.current_coor, self.radius)

if __name__ == "__main__":
    from compas_view2.app import App
    walker = Walker()

    geometries = []

    for i in range(100):
        walker.walking()
        geometries.append(walker.draw())


    viewer = App()
    for geometry in geometries:
        viewer.add(geometry)
    viewer.run()
