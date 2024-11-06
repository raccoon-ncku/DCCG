import os
import random

import compas
from compas.datastructures import Graph

graph = Graph.from_obj(compas.get('grid_irregular.obj'))

for node in graph.nodes():
    graph.node_attribute(node, 'weight', random.choice(range(20)))

print(graph.summary())

# Serialize graph to JSON and back
filename = os.path.join(os.path.dirname(__file__), 'data',
                        '033_graph_serialization.json')

if not os.path.exists(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

graph.to_json(filename, pretty=True)
print(graph.summary())
print(f'Saved to {filename}')

graph2 = Graph.from_json(filename)
print(graph2.summary())
