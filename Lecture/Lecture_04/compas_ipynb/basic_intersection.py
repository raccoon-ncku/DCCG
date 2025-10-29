import compas.geometry as cg
from compas_viewer import Viewer
from compas.datastructures import Mesh
# Create a viewer
viewer = Viewer()

BRICK_DIM = [230, 110, 50.01] # We set a small overlap in height to ensure intersection fall within tolerance
LAYER_HEIGHT = 50
MAXIMUM_INTERSECTION_DISTANCE = (BRICK_DIM[0]**2 + BRICK_DIM[1]**2 + BRICK_DIM[2]**2) ** 0.5 - 0.01

def compute_intersection(box1, box2):
    """
    Compute the intersection of two boxes and return as a mesh.
    """

    # instersection is computational expensive, so we comute it only when boxes are close enough
    distance = box1.frame.point.distance_to_point(box2.frame.point)
    if distance > MAXIMUM_INTERSECTION_DISTANCE:
        return None

    box_1_vf = box1.to_mesh(True, 10, 10).to_vertices_and_faces()
    box_2_vf = box2.to_mesh(True, 10, 10).to_vertices_and_faces()
    intersection = cg.boolean_intersection_mesh_mesh(box_1_vf, box_2_vf)
    intersection_mesh = Mesh.from_vertices_and_faces(*intersection)
    return intersection_mesh


# Define two stacked boxes
frame1 = cg.Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
frame2 = cg.Frame([0, 15, LAYER_HEIGHT], [1, 1, 0], [0, 1, 0])

box_1 = cg.Box(BRICK_DIM[0], BRICK_DIM[1], BRICK_DIM[2], frame1)
box_2 = cg.Box(BRICK_DIM[0], BRICK_DIM[1], BRICK_DIM[2], frame2)

# Compute intersection
intersection_mesh = compute_intersection(box_1, box_2)
# Add boxes and intersection to viewer
viewer.scene.add(box_1.to_mesh(), color=(200, 0, 0), opacity=0.3)
viewer.scene.add(box_2.to_mesh(), color=(0, 0, 200), opacity=0.3)
if intersection_mesh:
    viewer.scene.add(intersection_mesh, color=(0, 200, 0), opacity=0.6)

viewer.show()