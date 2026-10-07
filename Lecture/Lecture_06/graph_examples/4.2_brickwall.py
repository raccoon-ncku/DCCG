import random
import compas
import compas.datastructures as cd
from compas.geometry import Box, Frame
from compas_viewer import Viewer
from compas.colors import Color

# Define wall parameters
brick_length = 6
brick_height = 2
brick_depth = 3
rows = 5  # number of rows
cols = 10  # bricks per row

# Create a graph to store the wall's connections
wall_graph = cd.Graph()

# Generate bricks and add nodes and edges to the graph
bricks = {}
for row in range(rows):
    offset = 0 if row % 2 == 0 else brick_length / 2  # alternate bonding pattern
    for col in range(cols):
        x = col * brick_length + offset
        y = 0
        z = row * brick_height
        brick_id = row * cols + col
        bricks[brick_id] = Box(brick_length, brick_depth, brick_height, Frame([x, y, z], [1, 0, 0], [0, 1, 0]))
        
        # Add node to the graph
        wall_graph.add_node(brick_id)
        wall_graph.node_attributes(brick_id, 'xyz', [x, y, z])
        
        # Connect bricks in even rows to the two above (offset bonding pattern)
        if row > 0:
            if row % 2 == 0:  # Even row (offset)
                # Connect to the two bricks in the previous row
                previous_row_left = (row - 1) * cols + col
                previous_row_right = (row - 1) * cols + col + 1
                if previous_row_left in wall_graph.nodes():
                    wall_graph.add_edge(brick_id, previous_row_left)
                if previous_row_right in wall_graph.nodes() and col < cols - 1:
                    wall_graph.add_edge(brick_id, previous_row_right)
            else:  # Odd row
                # Connect to the one centered brick in the previous row
                previous_row_center = (row - 1) * cols + col
                if previous_row_center in wall_graph.nodes():
                    wall_graph.add_edge(brick_id, previous_row_center)
                
        # Add horizontal connections within the same row
        if col > 0:
            wall_graph.add_edge(brick_id, brick_id - 1)

# Randomly pick a brick and highlight it along with its neighbors
random_brick = random.choice(list(wall_graph.nodes()))
neighbors = wall_graph.neighbors(random_brick)

# Set up viewer
viewer = Viewer()
viewer.scene.add(wall_graph)
for brick_id, brick in bricks.items():
    if brick_id == random_brick:
        viewer.scene.add(brick, facecolor=Color(0.8, 0, 0), opacity=0.3)
    elif brick_id in neighbors:
        viewer.scene.add(brick, facecolor=Color(0, 0, 1), opacity=0.3)
    else:
        viewer.scene.add(brick, facecolor=Color(0.8, 0.8, 0.8), opacity=0.3)

viewer.show()
