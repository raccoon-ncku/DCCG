import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# read in the facebook data
facebook = pd.read_csv(
    os.path.join(
        os.path.dirname(__file__),
        "facebook_combined.txt.gz"
        ),
    compression="gzip",
    sep=" ",
    names=["start_node", "end_node"],
)

# create a graph from the edgelist
G = nx.from_pandas_edgelist(facebook, "start_node", "end_node")

# compute the layout
# Graph don't have geometrical information, 
# so we need to compute the layout to visualize it
pos = nx.spring_layout(G, iterations=15, seed=1721)

# visualize the graph
fig, ax = plt.subplots(figsize=(15, 9))
ax.axis("off")
plot_options = {"node_size": 10, "with_labels": False, "width": 0.15}
nx.draw_networkx(G, pos=pos, ax=ax, **plot_options)
plt.show()