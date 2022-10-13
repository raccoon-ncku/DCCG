from compas.geometry import Pointcloud, KDTree, Line
from compas.datastructures import Network
from compas.utilities import pairwise

from compas_view2.app import App
from compas_view2.collections import Collection

# ==============================================================================
# Pointcloud and Tree for NNBRS lookup
# ==============================================================================

cloud = Pointcloud.from_bounds(10, 5, 3, 200)
tree = KDTree(cloud)

# ==============================================================================
# Network connecting points to their NNBRS
# ==============================================================================

network = Network()

for point in cloud:
    network.add_node(x=point[0], y=point[1], z=point[2])

for node in network.nodes():
    point = network.node_coordinates(node)
    for nbr in tree.nearest_neighbors(point, 4, distance_sort=True):
        if nbr[2] < 1e-6:
            continue
        if not network.has_edge(node, nbr[1], directed=False):
            network.add_edge(node, nbr[1])

# ==============================================================================
# Shortest path between any two nodes of network
# ==============================================================================

start = network.get_any_node()
goal = network.get_any_node()
path = network.shortest_path(start, goal)

# ==============================================================================
# Viz
# ==============================================================================

viewer = App()

viewer.add(network)

lines = []
for u, v in pairwise(path):
    a = network.node_coordinates(u)
    b = network.node_coordinates(v)
    line = Line(a, b)
    lines.append(line)

viewer.add(Collection(lines), linewidth=10, color=(1, 0, 0))
viewer.run()
