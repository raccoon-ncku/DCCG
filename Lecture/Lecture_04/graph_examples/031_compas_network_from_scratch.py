import random
import compas
import compas.datastructures as cd

# Create a (empty) graph
graph = cd.Graph()

# Add edges, and nodes will be created automatically
graph.add_edge(1, 2)
graph.add_edge(2, 3)
graph.add_edge(1, 4)
graph.add_edge(4, 5)
graph.add_edge(4, 6)

# Add randomly chosen coordinates to each node
for node in graph.nodes():
    x = random.randint(0, 50)
    y = random.randint(0, 50)
    z = random.randint(0, 50)
    graph.node_attributes(node, 'xyz', [x, y, z])


print(graph.summary())

geometries = [graph]

if compas.is_grasshopper():
    a = geometries
else:
    from compas_viewer import Viewer

    viewer = Viewer()
    for geometry in geometries:
        viewer.scene.add(geometry)
    # for node in graph.nodes():
    #     node_coordinate = graph.node_coordinates(node)
    #     node_weight_tag = str(node)
    #     t = Text(node_weight_tag, node_coordinate, height=50)
    #     viewer.scene.add(t)
    viewer.show()
