from compas.geometry import Box, Frame, Vector, Translation, Rotation


class Drone:

    # Static class variables
    max_velocity = 2
    max_acceleration = 0.1
    location_tolerance = 0.1

    def __init__(self, init_location=None):
        """
        Initialize a drone object

        Parameters
        ----------
        init_location : Frame, optional
            The initial location of the drone, by default None
        """

        if init_location is None:
            init_location = Frame.worldXY() # default to world XY plane
        self.location = init_location
        self.body = Box(2,2,2,self.location)
        self.velocity = Vector(0, 0, 0)
        self.acceleration = Vector(0, 0, 0)
        self.target = None

    def set_viewer_obj(self, viewer_obj):
        """
        Set the viewer object for the drone

        Parameters
        ----------
        viewer_obj : Viewer
            The viewer object
        """
        self.viewer_obj = viewer_obj

    def move(self):
        """
        Update the location of the drone based on its velocity and acceleration
        """
        self.velocity = self.velocity + self.acceleration

        # limit the velocity to the maximum velocity
        if self.velocity.length > self.max_velocity:
            self.velocity.unitize()
            self.velocity.scale(self.max_velocity)

        # move the drone, update the body
        transformation = Translation.from_vector(self.velocity)
        self.location.transform(transformation)
        self.body.transform(transformation)

        # reset the acceleration
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

        # if the drone is close enough to the target, do nothing
        if distance < self.location_tolerance:
            return
        
        # otherwise, normalize the vector
        target_direction.unitize()


        # calculate the time and distance needed to stop
        t_stop = self.velocity.length / self.max_acceleration  # minimum time to stop
        d_stop = self.velocity.length * t_stop / 2  # minimum distance to stop

        # if the drone is too close to the target, full deceleration
        if distance < d_stop:
            # full deceleration
            self.acceleration = target_direction * -self.max_acceleration
            return
        else:
            # full acceleration
            self.acceleration = target_direction * self.max_acceleration
            return
