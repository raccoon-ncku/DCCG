import random
import compas
import compas.datastructures as cd

# Create a (empty) network
network = cd.Network()

# Add edges, and nodes will be created automatically
network.add_edge(1, 2)
network.add_edge(2, 3)
network.add_edge(1, 4)
network.add_edge(4, 5)
network.add_edge(4, 6)

# Add randomly chosen coordinates to each node
for node in network.nodes():
    x = random.randint(0, 50)
    y = random.randint(0, 50)
    z = random.randint(0, 50)
    network.node_attributes(node, 'xyz', [x, y, z])


print(network.summary())

geometries = [network]

if compas.is_grasshopper():
    a = geometries
else:
    from compas_viewer import Viewer
    from compas_view2.shapes import Text
    viewer = Viewer()
    for geometry in geometries:
        viewer.scene.add(geometry)
    for node in network.nodes():
        node_coordinate = network.node_coordinates(node)
        node_weight_tag = str(node)
        t = Text(node_weight_tag, node_coordinate, height=50)
        viewer.scene.add(t)
    viewer.show()
