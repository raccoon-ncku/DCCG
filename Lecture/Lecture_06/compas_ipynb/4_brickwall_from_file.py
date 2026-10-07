# deserialize a brick wall from a file

import pathlib
import compas.datastructures as cd
from compas_viewer.viewer import Viewer

# Load the network from a JSON file
current_dir = pathlib.Path(__file__).parent
network = cd.Network.from_json(current_dir / 'brickwall_network.json')


# Visualize the bricks
viewer = Viewer()
for node in network.nodes():
    viewer.scene.add(network.node_attribute(node, 'geometry'), facecolor=(0.8, 0.3, 0.3), opacity=0.4)

for edge in network.edges():
    mortar = network.edge_attribute(edge, 'geometry')
    viewer.scene.add(mortar, color=(0.9, 0.9, 0.9), opacity=0.3)

viewer.show()