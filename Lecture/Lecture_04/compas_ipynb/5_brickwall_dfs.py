# deserialize a brick wall from a file

import pathlib
import compas.datastructures as cd
from compas_viewer.viewer import Viewer

# Load the network from a JSON file
current_dir = pathlib.Path(__file__).parent
network = cd.Network.from_json(current_dir / 'brickwall_network.json')

networkx = network.to_networkx()

# Visualize the bricks
viewer = Viewer()
for node in network.nodes():
    viewer.scene.add(network.node_attribute(node, 'geometry'), facecolor=(0.8, 0.3, 0.3), opacity=0.4)

for edge in network.edges():
    mortar = network.edge_attribute(edge, 'geometry')
    viewer.scene.add(mortar, color=(0.9, 0.9, 0.9), opacity=0.3)

def depth_first_search_to_layer_zero(network, start_node):
    """
    Perform depth-first search to find a brick with layer = 0.
    Returns the path from start_node to the target node, or None if not found.
    """
    visited = set()
    parent = {}  # To reconstruct the path
    
    def dfs(current_node):
        visited.add(current_node)
        
        # Check if current node has layer = 0
        layer = network.node_attribute(current_node, 'layer')
        if layer == 0:
            return current_node  # Found target
        
        # Explore neighbors
        for neighbor in network.neighbors(current_node):
            if neighbor not in visited:
                parent[neighbor] = current_node
                result = dfs(neighbor)
                if result is not None:
                    return result  # Found target in this branch
        
        return None  # Target not found in this branch
    
    target_node = dfs(start_node)
    
    if target_node is None:
        return None  # No path found
    
    # Reconstruct path from start to target
    path = []
    current = target_node
    while current is not None:
        path.append(current)
        current = parent.get(current)
    
    path.reverse()  # Reverse to get path from start to target
    return path

# Start DFS from a random node (preferably higher layer)
start_node = network.node_sample()[0]
max_layer = -1


print(f"Starting DFS from node {start_node} (layer {max_layer})")

# Perform depth-first search to find layer 0
path_to_layer_zero = depth_first_search_to_layer_zero(network, start_node)

if path_to_layer_zero:
    print(f"Found path to layer 0. Path length: {len(path_to_layer_zero)}")
    print(f"Path: {' -> '.join(map(str, path_to_layer_zero))}")
    
    # Highlight the path nodes and edges
    for i, node in enumerate(path_to_layer_zero):
        brick = network.node_attribute(node, 'geometry')
        layer = network.node_attribute(node, 'layer')
        
        if i == 0:
            # Start node - green
            viewer.scene.add(brick, facecolor=(0.2, 0.8, 0.2), opacity=0.8)
        elif i == len(path_to_layer_zero) - 1:
            # Target node (layer 0) - blue
            viewer.scene.add(brick, facecolor=(0.2, 0.2, 0.8), opacity=0.8)
        else:
            # Path nodes - orange
            viewer.scene.add(brick, facecolor=(0.9, 0.5, 0.1), opacity=0.8)
    
    # Highlight the edges in the path
    for i in range(len(path_to_layer_zero) - 1):
        node1 = path_to_layer_zero[i]
        node2 = path_to_layer_zero[i + 1]
        
        # Find the mortar edge between consecutive nodes in path
        if network.has_edge((node1, node2)):
            mortar = network.edge_attribute((node1, node2), 'geometry')
        elif network.has_edge((node2, node1)):
            mortar = network.edge_attribute((node2, node1), 'geometry')
        else:
            continue  # No edge found
        
        # Highlight path edges in bright yellow
        viewer.scene.add(mortar, color=(1.0, 1.0, 0.0), opacity=0.9)

else:
    print("No path to layer 0 found")
    # Still visualize a random brick if no path found
    node = network.node_sample()[0]
    brick = network.node_attribute(node, 'geometry')
    viewer.scene.add(brick, facecolor=(0.8, 0.2, 0.2), opacity=0.8)

print("\nVisualization Legend:")
print("Green = Start node (highest layer)")
print("Orange = Path nodes (intermediate layers)")
print("Blue = Target node (layer 0)")
print("Yellow = Path edges (connections)")
print("Light red = All other bricks")
print("Light gray = All other mortar")

viewer.show()