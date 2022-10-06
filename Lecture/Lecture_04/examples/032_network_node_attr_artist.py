import random
import compas
from compas.datastructures import Network

network = Network.from_obj(compas.get('grid_irregular.obj'))

for node in network.nodes():
    network.node_attribute(node, 'weight', random.choice(range(20)))

print(network.summary())

text = {node: network.node_attribute(node, 'weight') for node in network.nodes()}


if compas.is_grasshopper():
    a = network
else:
    from compas_view2.app import App
    from compas_view2.shapes import Text
    viewer = App()
    viewer.add(network)
    for node in network.nodes():
        node_coordinate = network.node_coordinates(node)
        node_weight_tag = str(network.node_attribute(node, "weight"))
        t = Text(node_weight_tag, node_coordinate, height=50)
        viewer.add(t)
    viewer.run()
