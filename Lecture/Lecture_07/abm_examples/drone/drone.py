from compas.geometry import Box, Frame, Vector, Translation, Rotation


class Drone:
    def __init__(self, init_location=None):
        if init_location is None:
            init_location = Frame.worldXY()
        self.location = init_location
        self.velocity = Vector(0, 0, 0)
        self.acceleration = Vector(0, 0, 0)
        # self.angular_velocity = Rotation()
        # self.angular_acceleration = Rotation()
        self.max_velocity = 20
        self.mass = 10
        self.inertia = 10

    def move(self):
        self.velocity = self.velocity + self.acceleration
        # self.angular_velocity = self.angular_velocity * self.angular_acceleration
        transformation = Translation.from_vector(self.velocity)
        self.location.transform(transformation)
        self.acceleration = Vector(0, 0, 0)

    def rise(self):
        self.acceleration = Vector(0, 0, 1)

    def get_body(self):
        return Box(self.location, 2, 2, 2)


if __name__ == "__main__":
    drone = Drone(Frame.worldXY())
