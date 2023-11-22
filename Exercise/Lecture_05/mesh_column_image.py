# create a mesh column using math functions
import math
import compas.datastructures as cd
import compas.geometry as cg
from compas.utilities import remap_values
from compas.colors import Color
from compas_view2.app import App
from PIL import Image
import pathlib

# load the image
image_path = pathlib.Path(__file__).parent / "data" / "map.png"
image = Image.open(image_path)

IMAGE_HEIGHT = image.height
IMAGE_WIDTH = image.width


# Create an empty mesh
mesh = cd.Mesh()

COLUMN_HEIGHT = 100
COLUMN_RADIUS = 5
MESH_EDGE_LENGTH = 1

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
        # remap the z value to the range of the image height
        image_x = remap_values([j], target_min=0, target_max=IMAGE_WIDTH-1, original_min=0, original_max=COLUMN_CIRCLE_DIVISION-1)[0]
        image_y = remap_values([i], target_min=0, target_max=IMAGE_HEIGHT-1, original_min=0, original_max=COLUMN_Z_COUNT-1)[0]
        image_color = image.getpixel((image_x, image_y))

        vector = cg.Vector(
            math.cos(angle),
            math.sin(angle),
            0
        )
        # Use the average of the RGB values as the height
        push_distance = (image_color[0] + image_color[1] + image_color[2]) / 3
        vector.scale( push_distance / 255 * 10)
        translation = cg.Translation.from_vector(vector)

        # Apply the transformation
        point.transform(translation)

        # Add the point to the mesh
        vertex = mesh.add_vertex(x=point.x, y=point.y, z=point.z)
        color = Color.from_rgb255(*image_color[:3])
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
