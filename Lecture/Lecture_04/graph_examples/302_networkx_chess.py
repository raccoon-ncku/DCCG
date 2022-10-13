from compas_view2.app import App
from compas_view2.shapes import Text
import compas.datastructures as cd
import compas.geometry as cg
import matplotlib.pyplot as plt
import networkx as nx
import os

# tag names specifying what game info should be
# stored in the dict on each digraph edge
game_details = ["Event", "Date", "Result", "ECO", "Site"]

fp = os.path.join(os.path.dirname(__file__), "WCC.pgn")


def chess_pgn_graph(pgn_file):
    """Read chess games in pgn format in pgn_file.

    Filenames ending in .bz2 will be uncompressed.

    Return the MultiDiGraph of players connected by a chess game.
    Edges contain game data in a dict.

    """

    G = nx.MultiDiGraph()
    game = {}
    with open(pgn_file, 'r') as fo:
        lines = [line.rstrip("\r\n") for line in fo.readlines()]
    for line in lines:
        if line.startswith("["):
            tag, value = line[1:-1].split(" ", 1)
            game[str(tag)] = value.strip('"')
        else:
            # empty line after tag set indicates
            # we finished reading game info
            if game:
                white = game.pop("White")
                black = game.pop("Black")
                G.add_edge(white, black, **game)
                game = {}
    return G


G = chess_pgn_graph(fp)

print(
    f"Loaded {G.number_of_edges()} chess games between {G.number_of_nodes()} players\n"
)

# identify connected components of the undirected version
H = G.to_undirected()
Gcc = [H.subgraph(c) for c in nx.connected_components(H)]

# make new undirected graph H without multi-edges
H = nx.Graph(G)

# edge width is proportional number of games played
edgewidth = []
for u, v in H.edges():
    temp = G.get_edge_data(u, v)
    if temp is None:
        edgewidth.append(1)
    else:
        edgewidth.append(len(temp))


# node size is proportional to number of games won
wins = dict.fromkeys(G.nodes(), 0.0)
for (u, v, d) in G.edges(data=True):
    r = d["Result"].split("-")
    if r[0] == "1":
        wins[u] += 1.0
    elif r[0] == "1/2":
        wins[u] += 0.5
        wins[v] += 0.5
    else:
        wins[v] += 1.0
nodesize = [wins[v] * 50 for v in H]

# Generate layout for visualization
pos = nx.kamada_kawai_layout(H)

fig, ax = plt.subplots(figsize=(12, 12))
# Visualize graph components
nx.draw_networkx_edges(H, pos, alpha=0.3, width=edgewidth, edge_color="m")
nx.draw_networkx_nodes(H, pos, node_size=nodesize,
                       node_color="#210070", alpha=0.9)
label_options = {"ec": "k", "fc": "white", "alpha": 0.7}
nx.draw_networkx_labels(H, pos, font_size=14, bbox=label_options)

# Resize figure for label readibility
ax.margins(0.1, 0.05)
fig.tight_layout()
plt.show()

# Convert to COMPAS Network
network = cd.Network.from_networkx(H)
for i, node_id in enumerate(network.nodes()):
    coordinate = pos[node_id]
    nodesize_attr = nodesize[i]
    network.node_attributes(node_id, "xy", coordinate)
    network.node_attribute(node_id, "z", 0)
    network.node_attribute(node_id, "nodesize", nodesize_attr)

# visualize COMPAS Network
viewer = App()
viewer.add(network)
for node_id in network.nodes():
    coordinate = network.node_coordinates(node_id)

    # Add tag
    t = Text(node_id, coordinate, height=10)
    viewer.add(t)

    # Add node
    radius = network.node_attribute(node_id, "nodesize") ** 0.5 / 1000
    sphere = cg.Sphere(coordinate, radius)
    viewer.add(sphere)

viewer.run()
