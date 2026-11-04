import random
import compas
from compas.datastructures import Graph

graph = Graph.from_obj(compas.get('grid_irregular.obj'))

for node in graph.nodes():
    graph.node_attribute(node, 'weight', random.choice(range(20)))

print(graph.summary())

text = {node: graph.node_attribute(node, 'weight') for node in graph.nodes()}


if compas.is_grasshopper():
    a = graph
else:
    from compas_viewer import Viewer
    from compas_viewer.scene import Tag
    viewer = Viewer()
    viewer.scene.add(graph)
    for node in graph.nodes():
        node_coordinate = graph.node_coordinates(node)
        node_weight_tag = str(graph.node_attribute(node, "weight"))
        t = Tag(node_weight_tag, node_coordinate, height=50)
        viewer.scene.add(t)
    viewer.show()
