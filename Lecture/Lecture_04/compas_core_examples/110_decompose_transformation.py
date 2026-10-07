"""Example: Decompose transformations
"""
from compas.geometry import *

A = Scale.from_factors([0.1, 0.3, 0.4])  # create Scale
B = Rotation.from_axis_and_angle([-0.8, 0.35, 0.5], 2.2)  # create Rotation
C = Translation.from_vector([1, 2, 3])  # create Translation

# Concatenate transformations
M = C * B * A

# A matrix can also be decomposed into its components of Scale,
# Shear, Rotation, Translation and Perspective
Sc, Sh, R, T, P = M.decomposed()
# Check, must be all `True`
print(A == Sc)
print(B == R)
print(C == T)
print(P * T * R * Sh * Sc == M)
