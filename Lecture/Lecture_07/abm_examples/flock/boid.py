from compas.geometry import Box, Frame, Vector, Translation, Point
import numpy as np


class Boid:

    def __init__(self, init_position=None):
        if init_position is None:
            init_position = Frame.worldXY()
        self.position = init_position

        self.max_speed = 0.5
        self.max_acceleration = 0.1

        vec = (np.random.rand(3) - 0.5) * self.max_speed * 2
        self.velocity = Vector(*vec)

        self.acceleration = Vector(*np.zeros(3))

        self.perception = 10

        self.width = 50
        self.length = 50
        self.height = 50

        self.alignment_weight = 1
        self.cohesion_weight = 1
        self.separation_weight = 1

    def update(self):
        """
        Calculate acceleration, velocity, and apply the transformation.
        """

        # Limit max acceleration
        if np.linalg.norm(self.acceleration) > self.max_acceleration:
            self.acceleration = (
                self.acceleration / np.linalg.norm(self.acceleration)) * self.max_acceleration

        # Apply and reset acceleration
        self.velocity += self.acceleration
        self.acceleration = Vector(*np.zeros(3))

        # Limit max speed
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / \
                np.linalg.norm(self.velocity) * self.max_speed

        # Apply velocity(transformation)
        self.position.transform(Translation.from_vector(self.velocity))

    def get_body(self):
        """
        Get the geometrical representation.
        """
        # geo = Box(self.position, 0.5, 0.5, 0.5)
        geo = self.position.point
        return geo

    def apply_behaviour(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)

        self.acceleration += alignment * self.alignment_weight
        self.acceleration += cohesion * self.cohesion_weight
        self.acceleration += separation * self.separation_weight

    def warp(self):
        new_x, new_y, new_z = self.position.point.x, self.position.point.y, self.position.point.z
        if self.position.point.x > self.length:
            new_x = 0
        elif self.position.point.x < 0:
            new_x = self.length

        if self.position.point.y > self.width:
            new_y = 0
        elif self.position.point.y < 0:
            new_y = self.width

        if self.position.point.z > self.height:
            new_z = 0
        elif self.position.point.z < 0:
            new_z = self.height

        self.position = Frame(
            Point(new_x, new_y, new_z),
            self.position.xaxis,
            self.position.yaxis
        )

    def align(self, boids):
        steering = Vector(*np.zeros(3))
        total = 0
        avg_vector = Vector(*np.zeros(3))
        for boid in boids:
            if np.linalg.norm(boid.position.point - self.position.point) < self.perception:
                avg_vector += boid.velocity
                total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = Vector(*avg_vector)
            avg_vector = (avg_vector / np.linalg.norm(avg_vector)
                          ) * self.max_speed
            steering = avg_vector - self.velocity

        return steering

    def cohesion(self, boids):
        steering = Vector(*np.zeros(3))
        total = 0
        center_of_mass = Point(*np.zeros(3))
        for boid in boids:
            if np.linalg.norm(boid.position.point - self.position.point) < self.perception:
                center_of_mass += boid.position.point
                total += 1
        if total > 0:
            center_of_mass /= total
            center_of_mass = Vector(*center_of_mass)
            vec_to_com = center_of_mass - self.position.point
            if np.linalg.norm(vec_to_com) > 0:
                vec_to_com = (
                    vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed
            steering = vec_to_com - self.velocity

        return steering

    def separation(self, boids):
        steering = Vector(*np.zeros(3))
        total = 0
        avg_vector = Vector(*np.zeros(3))
        for boid in boids:
            distance = np.linalg.norm(
                boid.position.point - self.position.point)
            if self.position.point != boid.position.point and distance < self.perception:
                diff = self.position.point - boid.position.point
                diff /= distance
                avg_vector += diff
                total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = Vector(*avg_vector)
            if np.linalg.norm(steering) > 0:
                avg_vector = (
                    avg_vector / np.linalg.norm(steering)) * self.max_speed
            steering = avg_vector - self.velocity

        return steering
