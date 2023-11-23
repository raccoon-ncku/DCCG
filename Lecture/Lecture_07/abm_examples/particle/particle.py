from compas.geometry import Box, Frame, Vector, Translation, Point, closest_point_in_cloud
import numpy as np


class Particle:
    def __init__(self, init_position=None, init_velocity=None):
        if init_position is None:
            init_position = Point(0, 0, 0)
        self.position = Point(*init_position)
        self.position_history = [self.position]
        self.max_speed = 0.5
        self.max_acceleration = 0.1
        if init_velocity is None:
            init_velocity = Vector(0, 0, 1)
        self.velocity = Vector(*init_velocity)

        self.acceleration = Vector(0, 0, 0)

        self.min_distance = 1

    def update(self):
        """
        Calculate acceleration, velocity, and apply the transformation.
        """
        # Gravity
        self.acceleration += Vector(0, 0, -0.1)
        # Limit max acceleration
        if np.linalg.norm(self.acceleration) > self.max_acceleration:
            self.acceleration = (self.acceleration / np.linalg.norm(self.acceleration)) * self.max_acceleration

        # Apply and reset acceleration
        self.velocity += self.acceleration
        self.acceleration = Vector(*np.zeros(3))

        # Limit max speed
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed

        # Apply velocity(transformation)
        self.position = self.position + self.velocity
        self.position_history.append(self.position)

    def get_body(self):
        """
        Get the geometrical representation.
        """
        # geo = Box(self.position, 0.5, 0.5, 0.5)
        geo = Point(*self.position)
        return geo

    def glide_on_mesh(self, mesh, mesh_vertex_coordinates, mesh_vertex_keys):
        distance, _, index = closest_point_in_cloud(self.position, mesh_vertex_coordinates)
        if distance < self.min_distance:
            mesh_v_normal = Vector(*mesh.vertex_normal(mesh_vertex_keys[index]))

            steer = mesh_v_normal.cross(Vector(0, 0, -1).cross(mesh_v_normal))

            self.velocity = steer
