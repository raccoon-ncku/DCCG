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