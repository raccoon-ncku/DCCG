# notebook currently having performance issues due to boolean operations
# So this code is better run as a script

import compas.geometry as cg
from compas_viewer.viewer import Viewer
import compas.datastructures as cd
import math
# Create a viewer
viewer = Viewer()

network = cd.Network()

BRICK_DIM = [0.230, 0.110, 0.050]
MORTAR_THICKNESS = 0.010
LAYER_HEIGHT = BRICK_DIM[2] + MORTAR_THICKNESS
MAXIMUM_INTERSECTION_DISTANCE = (BRICK_DIM[0]**2 + BRICK_DIM[1]**2 + BRICK_DIM[2]**2) ** 0.5 - 0.01

LAYERS = 6
BRICKS_PER_LAYER = 8

def compute_mortar(brick_1, brick_2):
    """
    Compute the mortar between two brickes and return as a mesh.
    """

    # instersection is computational expensive, so we comute it only when brickes are close enough
    distance = brick_1.frame.point.distance_to_point(brick_2.frame.point)
    if distance > MAXIMUM_INTERSECTION_DISTANCE:
        return None


    # generate larger brick for boolean intersection
    brick_1_large = cg.Box(
        BRICK_DIM[0],
        BRICK_DIM[1],
        BRICK_DIM[2] + MORTAR_THICKNESS*2,
        brick_1.frame
    )
    brick_2_large = cg.Box(
        BRICK_DIM[0],
        BRICK_DIM[1],
        BRICK_DIM[2] + MORTAR_THICKNESS*2,
        brick_2.frame
    )

    # boolean intersection takes vertices and faces as input
    brick_1_vf = brick_1_large.to_mesh(True, 10, 10).to_vertices_and_faces()
    brick_2_vf = brick_2_large.to_mesh(True, 10, 10).to_vertices_and_faces()

    # perform boolean intersection
    intersection = cg.boolean_intersection_mesh_mesh(brick_1_vf, brick_2_vf)

    # convert result to mesh
    intersection_mesh = cd.Mesh.from_vertices_and_faces(*intersection)

    # only return the intersection if it is not empty
    if len(list(intersection_mesh.vertices())) == 0:
        return None

    return intersection_mesh
    

for layer in range(LAYERS):
    for i in range(BRICKS_PER_LAYER):
        x = i * (BRICK_DIM[0]*1.2 + MORTAR_THICKNESS)
        if layer % 2 == 1:
            x += (BRICK_DIM[0] + MORTAR_THICKNESS) / 2
        y = 0
        z = layer * LAYER_HEIGHT

        frame = cg.Frame.worldXY()
        rotate_angle = math.radians(15*(i + layer) / BRICKS_PER_LAYER)
        rotation = cg.Rotation.from_axis_and_angle(cg.Vector(0, 0, 1), rotate_angle)
        translation = cg.Translation.from_vector(cg.Vector(x, y, z))
        frame.transform(rotation)
        frame.transform(translation)

        brick = cg.Box(BRICK_DIM[0], BRICK_DIM[1], BRICK_DIM[2], frame)
        brick_id = network.add_node(
            attr_dict={
                "x": x,
                "y": y,
                "z": z,
                "layer": layer,
                "index_in_layer": i,
                'geometry': brick})

for node in network.nodes():
    for node2 in network.nodes():
        if node >= node2:
            continue
        brick_1 = network.node_attribute(node, 'geometry')
        brick_2 = network.node_attribute(node2, 'geometry')
        mortar = compute_mortar(brick_1, brick_2)
        if mortar:
            network.add_edge(node, node2)
            network.edge_attribute((node, node2), 'geometry', mortar)
            viewer.scene.add(mortar, color=(0.9, 0.9, 0.9))


# Visualize the bricks

for node in network.nodes():
    viewer.scene.add(network.node_attribute(node, 'geometry'), facecolor=(0.8, 0.3, 0.3), opacity=0.4)

for edge in network.edges():
    mortar = network.edge_attribute(edge, 'geometry')
    viewer.scene.add(mortar, color=(0.9, 0.9, 0.9), opacity=0.3)

viewer.scene.add(network)

# Visualize one brick and its mortar
node = network.node_sample()[0]
brick = network.node_attribute(node, 'geometry')
viewer.scene.add(brick, facecolor=(0.2, 0.7, 0.3), opacity=0.4)
for neighbor in network.neighbors(node):
    if network.has_edge((node, neighbor)):
        mortar = network.edge_attribute((node, neighbor), 'geometry')
    else:
        mortar = network.edge_attribute((neighbor, node), 'geometry')
    viewer.scene.add(mortar, color=(0.3, 0.5, 0.9), opacity=0.6)

    

viewer.show()

# Save the network to a JSON file
import pathlib
current_dir = pathlib.Path(__file__).parent
network.to_json(current_dir / 'brickwall_network.json')