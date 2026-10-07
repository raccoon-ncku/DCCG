import random

from compas.geometry import Pointcloud, KDTree, Line
from compas.datastructures import Graph
from compas.itertools import pairwise
from compas.colors import Color

from compas_viewer import Viewer

# ==============================================================================
# Pointcloud and Tree for NNBRS lookup
# ==============================================================================

cloud = Pointcloud.from_bounds(10, 5, 3, 200)
tree = KDTree(cloud)

# ==============================================================================
# Graph connecting points to their NNBRS
# ==============================================================================

network = Graph()

for point in cloud:
    network.add_node(x=point[0], y=point[1], z=point[2])

for node in network.nodes():
    point = network.node_coordinates(node)
    for nbr in tree.nearest_neighbors(point, 4, distance_sort=True):
        if nbr[2] < 1e-6:
            continue
        if not network.has_edge((node, nbr[1]), directed=False):
            network.add_edge(node, nbr[1])

# ==============================================================================
# Shortest path between any two nodes of network
# ==============================================================================

start, goal = random.sample(list(network.nodes()), 2)
path = network.shortest_path(start, goal) or [start]   # None if not connected

# ==============================================================================
# Viz
# ==============================================================================

viewer = Viewer()

viewer.scene.add(network)

for u, v in pairwise(path):
    a = network.node_coordinates(u)
    b = network.node_coordinates(v)
    viewer.scene.add(Line(a, b), linewidth=10, linecolor=Color(1.0, 0.4, 0.0))
viewer.show()
