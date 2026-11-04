import compas.geometry as cg


class Drone:
    # World size
    length = 100
    width = 100
    height = 100

    max_velocity = 1  # unit per frame
    max_acceleration = 0.1  # unit per frame
    location_tolerance = 0.1

    def __init__(self, init_location=None):
        """
        Constructor
        """
        if init_location is None:
            init_location = cg.Frame.worldXY()
        self.location = init_location
        self.velocity = cg.Vector(0, 0, 0)
        self.acceleration = cg.Vector(0, 0, 0)
        self.target = None


    def update(self):
        """
        Update the location of the drone based on its velocity and acceleration
        """

        # Check acceleration
        if self.acceleration.length > self.max_acceleration:
            self.acceleration.unitize()
            self.acceleration.scale(self.max_acceleration)

        self.velocity = self.velocity + self.acceleration
        
        if self.velocity.length > self.max_velocity:
            self.velocity.unitize()
            self.velocity.scale(self.max_velocity)
        
        transformation = cg.Translation.from_vector(self.velocity)
        self.location.transform(transformation)
        self.warp()

        # Reset acceleration
        self.acceleration = cg.Vector(0, 0, 0)

    def rise(self):
        """
        Move the drone upwards
        """
        self.acceleration = cg.Vector(0, 0, self.max_acceleration)


    def get_body(self):
        """
        Get the geometrical representation.
        """
        return cg.Box(self.location, 2, 2, 2)
    
    def warp(self):
        """
        Wrap the boid around the world.
        If the boid is out of the world, move it to the other side.
        """
        new_x, new_y, new_z = self.location.point.x, self.location.point.y, self.location.point.z
        if self.location.point.x > self.length:
            new_x = 0
        elif self.location.point.x < 0:
            new_x = self.length

        if self.location.point.y > self.width:
            new_y = 0
        elif self.location.point.y < 0:
            new_y = self.width

        if self.location.point.z > self.height:
            new_z = 0
        elif self.location.point.z < 0:
            new_z = self.height

        self.location = cg.Frame(
            cg.Point(new_x, new_y, new_z),
            self.location.xaxis,
            self.location.yaxis
        )

