from compas.geometry import Box, Frame, Vector, Translation, Rotation


class Drone:
    max_velocity = 20
    max_acceleration = 1
    location_tolerance = 0.1

    def __init__(self, init_location=None):
        if init_location is None:
            init_location = Frame.worldXY()
        self.location = init_location
        self.velocity = Vector(0, 0, 0)
        self.acceleration = Vector(0, 0, 0)
        self.target = None


    def move(self):
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

    def linear_approach(self):
        """
        Move the drone towards the target
        """

        # if there is no target, stop
        if self.target is None:
            return

        # calculate the vector from the drone to the target
        target_direction = self.target.point - self.location.point
        distance = target_direction.length
        target_direction.unitize()
        current_direction = self.velocity.copy()
        current_direction.unitize()

        # calculate the time and distance needed to stop
        t_stop = self.velocity.length / self.max_acceleration  # minimum time to stop
        d_stop = self.velocity.length * t_stop / 2  # minimum distance to stop

        # determine the acceleration needed to reach the target

        # if the drone is close enough to the target, stop
        if distance < self.location_tolerance:
            self.target = None
            return

        # if the drone is too
        if distance < d_stop:
            # full deceleration
            self.acceleration = target_direction * -self.max_acceleration



    def get_body(self):
        return Box(self.location, 2, 2, 2)

