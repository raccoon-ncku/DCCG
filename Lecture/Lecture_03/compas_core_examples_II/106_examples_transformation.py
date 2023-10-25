"""Transformation examples
"""
import compas.geometry as cg

axis, angle = [0.2, 0.4, 0.1], 0.3
R = cg.Rotation.from_axis_and_angle(axis, angle)
print("Rotation:\n", R)

translation_vector = [5, 3, 1]
T = cg.Translation.from_vector(translation_vector)
print("Translation:\n", T)

scale_factors = [0.1, 0.3, 0.4]
S = cg.Scale.from_factors(scale_factors)
print("Scale:\n", S)

point, normal = [0.3, 0.2, 1], [0.3, 0.1, 1]
R = cg.Reflection.from_plane((point, normal))
print("Reflection:\n", R)

point, normal = [0, 0, 0], [0, 0, 1]
perspective = [1, 1, 0]
P = cg.Projection.from_plane_and_point((point, normal), perspective)
print("Perspective projection:\n", R)

angle, direction = 0.1, [0.1, 0.2, 0.3]
point, normal = [4, 3, 1], [-0.11, 0.31, -0.17]
S = cg.Shear.from_angle_direction_plane(angle, direction, (point, normal))
print("Shear:\n", S)
