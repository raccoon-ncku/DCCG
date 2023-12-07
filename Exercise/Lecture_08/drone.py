from compas.geometry import Box, Frame, Vector, Translation, Rotation


class Drone:
    max_velocity = 20
    max_acceleration = 1
    location_tolerance = 0.1

    def __init__(self, init_location=None):
        """
        Constructor
        """
        if init_location is None:
            init_location = Frame.worldXY()
        self.location = init_location
        self.velocity = Vector(0, 0, 0)
        self.acceleration = Vector(0, 0, 0)
        self.target = None


    def update(self):
        """
        Update the location of the drone based on its velocity and acceleration
        """
        self.velocity = self.velocity + self.acceleration
        if self.velocity.length > self.max_velocity:
            self.velocity.unitize()
            self.velocity.scale(self.max_velocity)
        transformation = Translation.from_vector(self.velocity)
        self.location.transform(transformation)
        self.acceleration = Vector(0, 0, 0)

    def rise(self):
        """
        Move the drone upwards
        """
        self.acceleration = Vector(0, 0, self.max_acceleration)


    def get_body(self):
        return Box(self.location, 2, 2, 2)

