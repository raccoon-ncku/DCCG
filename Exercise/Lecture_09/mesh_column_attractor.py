# create a mesh column using math functions
import math
import compas.datastructures as cd
import compas.geometry as cg
from compas.itertools import remap_values
from compas.colors import Color
from compas_viewer import Viewer

# Create an empty mesh
mesh = cd.Mesh()

COLUMN_HEIGHT = 100
COLUMN_RADIUS = 5
MESH_EDGE_LENGTH = 1

COLUMN_Z_COUNT = int(round(COLUMN_HEIGHT / MESH_EDGE_LENGTH))
COLUMN_CIRCLE_DIVISION = int(round(COLUMN_RADIUS * 2 * math.pi/ MESH_EDGE_LENGTH))

# Create a bezier curve
points = [
    [15, 0, 0], [0, 12, 20], [-12, 0, 60], [0, -15, 100]
]
curve = cg.Bezier(points)
# Convert the curve into a polyline, as the former has less methods available
curve = cg.Polyline(curve.points)

# Create a column using math functions
for i in range(COLUMN_Z_COUNT):
    z = i * MESH_EDGE_LENGTH
    for j in range(COLUMN_CIRCLE_DIVISION):
        # Create a base point
        angle = j * math.pi * 2 / COLUMN_CIRCLE_DIVISION
        x = math.cos(angle) * COLUMN_RADIUS
        y = math.sin(angle) * COLUMN_RADIUS
        point = cg.Point(x, y, z)

        # Transform the base point
        # find the closest point on the curve
        closest_pt = cg.closest_point_on_polyline(point, curve)
        distance = cg.distance_point_point(point, closest_pt)
        distance = max([distance, 0.1]) # avoid division by zero
        vector = cg.Vector(
            math.cos(angle),
            math.sin(angle),
            0
        )
        vector.scale(
            1000 / (10 * distance ** 2 )
            )
        
        translation = cg.Translation.from_vector(vector)

        # Apply the transformation
        point.transform(translation)

        # Add the point to the mesh
        mesh.add_vertex(x=point.x, y=point.y, z=point.z)

# Create faces
for i in range(COLUMN_Z_COUNT - 1):
    for j in range(COLUMN_CIRCLE_DIVISION):
        mesh.add_face([i * COLUMN_CIRCLE_DIVISION + j,
                       i * COLUMN_CIRCLE_DIVISION + (j + 1) % COLUMN_CIRCLE_DIVISION,
                       (i + 1) * COLUMN_CIRCLE_DIVISION + (j + 1) % COLUMN_CIRCLE_DIVISION,
                       (i + 1) * COLUMN_CIRCLE_DIVISION + j])

        
# Create a viewer
viewer = Viewer(show_grid=False, viewmode='lighted')
for pt in points:
    viewer.scene.add(cg.Point(* pt), pointsize=10, pointcolor=(0.8, 0.2, 0.2))
viewer.scene.add(curve)
viewer.scene.add(mesh)
viewer.show()
