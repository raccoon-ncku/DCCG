from drone import Drone
import compas.geometry as cg

class TracingDrone(Drone):
    attraction_weight = 1
    repulsion_weight = 1

    def __init__(self, init_location=None):
        super().__init__(init_location)
        self.targets = []
        self.negative_targets = []

    def attract(self):
        """
        Move the drone towards the targets
        """
        for target in self.targets:
            vector = target.point - self.location.point
            distance = vector.length
            distance = min(distance, 1)
            vector.unitize()
            vector.scale(self.max_acceleration * self.attraction_weight / distance ** 2)
            self.acceleration += vector

    def repel(self):
        """
        Move the drone away from the negative targets
        """
        for negative_target in self.negative_targets:
            vector = negative_target.point - self.location.point
            distance = vector.length
            distance = min(distance, 1)
            vector.unitize()
            vector.scale(self.max_acceleration * self.repulsion_weight / distance ** 2)
            self.acceleration -= vector

    def update(self):
        """
        Update the location of the drone based on its velocity and acceleration
        """
        self.attract()
        self.repel()
        super().update()


if __name__ == "__main__":
    tracing_drone = TracingDrone()