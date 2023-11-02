import compas.geometry as cg
from compas.colors import Color
from compas_view2.app import App

axis, angle = [0.2, 0.4, 0.1], 0.3
R = cg.Rotation.from_axis_and_angle(axis, angle)

translation_vector = [5, 3, 1]
T = cg.Translation.from_vector(translation_vector)

scale_factors = [0.1, 0.3, 0.4]
S = cg.Scale.from_factors(scale_factors)

point, normal = [0.3, 0.2, 1], [0.3, 0.1, 1]
RL = cg.Reflection.from_plane((point, normal))

angle, direction = 0.1, [0.1, 0.2, 0.3]
point, normal = [4, 3, 1], [-0.11, 0.31, -0.17]
SH = cg.Shear.from_angle_direction_plane(angle, direction, (point, normal))

viewer = App()
box = cg.Box.from_width_height_depth(1, 2, 3)
viewer.add(box, facecolor=Color(1, 1, 1, 0.0), opacity=0.6)

# Change the following line to see the effect of different transformations
# T, R, S, RL, SH
box2 = box.transformed(RL)

viewer.add(box2, facecolor=Color(0.7, 0.5, 0.7), opacity=1)
viewer.run()