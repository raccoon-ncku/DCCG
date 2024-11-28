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
MESH_EDGE_LENGTH = 5

COLUMN_Z_COUNT = int(round(COLUMN_HEIGHT / MESH_EDGE_LENGTH))
COLUMN_CIRCLE_DIVISION = int(round(COLUMN_RADIUS * 2 * math.pi/ MESH_EDGE_LENGTH))

def create_face_window(mesh, face, frame_width):
    """
    offset the face to create a window

    Parameters
    ----------
    mesh: Mesh
        mesh to be modified
    face: Face
        face to be modified
    frame_width: float
        width of the window frame
    """

    vertex_pts = []
    vertex_keys = []
    # Iterate through the vertices
    for vertex_key in mesh.face_vertices(face):
        # Get the vertex
        vertex_coor = mesh.vertex_coordinates(vertex_key)
        vertex_pts.append(cg.Point(*vertex_coor))
        vertex_keys.append(vertex_key)

    offset_polygon = cg.offset_polygon(vertex_pts, frame_width)

    new_vertex_keys = []
    for pt in offset_polygon:
        vertex = mesh.add_vertex(x=pt[0], y=pt[1], z=pt[2])
        new_vertex_keys.append(vertex)
        
    for vertex_key in range(len(vertex_keys)):
        new_face = mesh.add_face([vertex_keys[vertex_key],
                       new_vertex_keys[vertex_key],
                       new_vertex_keys[(vertex_key+1)%len(vertex_keys)],
                       vertex_keys[(vertex_key+1)%len(vertex_keys)]])
        
    # delete the original face
    mesh.delete_face(face)


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


# Create faces
for i in range(COLUMN_Z_COUNT - 1):
    for j in range(COLUMN_CIRCLE_DIVISION):
        mesh.add_face([i * COLUMN_CIRCLE_DIVISION + j,
                       i * COLUMN_CIRCLE_DIVISION + (j + 1) % COLUMN_CIRCLE_DIVISION,
                       (i + 1) * COLUMN_CIRCLE_DIVISION + (j + 1) % COLUMN_CIRCLE_DIVISION,
                       (i + 1) * COLUMN_CIRCLE_DIVISION + j])
mesh = mesh.subdivided(k=1, scheme="tri")        

# Freeze the mesh keys
facekeys = list(mesh.faces())

for i, face in enumerate(facekeys):
    width = math.sin(10 * i / len(facekeys) * math.pi)*0.3 + 0.5
    create_face_window(mesh, face, width)

mesh = mesh.thickened(thickness=0.2)
        
# Create a viewer
viewer = Viewer(show_grid=False)
viewer.scene.add(mesh)
viewer.show()
