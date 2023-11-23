# create a mesh column using math functions
import math
import compas.datastructures as cd
import compas.geometry as cg
from compas.utilities import remap_values
from compas.colors import Color
from compas_view2.app import App

# Create an empty mesh
mesh = cd.Mesh()

COLUMN_HEIGHT = 100
COLUMN_RADIUS = 5
MESH_EDGE_LENGTH = 0.3

COLUMN_Z_COUNT = int(round(COLUMN_HEIGHT / MESH_EDGE_LENGTH))
COLUMN_CIRCLE_DIVISION = int(round(COLUMN_RADIUS * 2 * math.pi/ MESH_EDGE_LENGTH))

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
        vector = cg.Vector(
            math.cos(angle),
            math.sin(angle),
            0
        )
        vector.scale(
            math.sin(z / COLUMN_HEIGHT * math.pi + math.pi / 16) * 5 +
            math.sin(angle * 5 + z / COLUMN_HEIGHT * math.pi * 2) * 1 +
            math.cos(-angle * 3 + z / COLUMN_HEIGHT * math.pi * 4) * 1
            )
        translation = cg.Translation.from_vector(vector)

        # Apply the transformation
        point.transform(translation)

        # Add the point to the mesh
        vertex = mesh.add_vertex(x=point.x, y=point.y, z=point.z)

        # Color the mesh
        red_value = 1 - remap_values(
            [z],
            original_min=0,
            original_max=COLUMN_HEIGHT)[0]
        green_value = (math.cos(angle+z*0.1)+1)/2
        color = Color(red_value*0.7,
                      0.6-red_value*0.3-green_value*0.3,
                      1-red_value*0.6)
        mesh.vertex_attribute(vertex, 'color', color)

# Create faces
for i in range(COLUMN_Z_COUNT - 1):
    for j in range(COLUMN_CIRCLE_DIVISION):
        mesh.add_face([i * COLUMN_CIRCLE_DIVISION + j,
                       i * COLUMN_CIRCLE_DIVISION + (j + 1) % COLUMN_CIRCLE_DIVISION,
                       (i + 1) * COLUMN_CIRCLE_DIVISION + (j + 1) % COLUMN_CIRCLE_DIVISION,
                       (i + 1) * COLUMN_CIRCLE_DIVISION + j])

        
# Create a viewer
viewer = App(show_grid=False, viewmode='lighted')
viewer.add(mesh, use_vertex_color=True, show_lines=False)
viewer.run()
