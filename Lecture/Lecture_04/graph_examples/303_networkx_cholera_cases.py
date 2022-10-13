import compas.datastructures as cd
from compas_view2.app import App
from libpysal import weights
from contextily import add_basemap
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import geopandas
import os

# read in example data from a geopackage file. Geopackages
# are a format for storing geographic data that is backed
# by sqlite. geopandas reads data relying on the fiona package,
# providing a high-level pandas-style interface to geographic data.
fp = os.path.join(os.path.dirname(__file__), "cholera_cases.gpkg")
cases = geopandas.read_file(fp)

# construct the array of coordinates for the centroid
coordinates = np.column_stack((cases.geometry.x, cases.geometry.y))

# construct two different kinds of graphs:

# 3-nearest neighbor graph, meaning that points are connected
# to the three closest other points. This means every point
# will have exactly three neighbors.
knn3 = weights.KNN.from_dataframe(cases, k=3)

# The 50-meter distance band graph will connect all pairs of points
# that are within 50 meters from one another. This means that points
# may have different numbers of neighbors.
dist = weights.DistanceBand.from_array(coordinates, threshold=50)

# Then, we can convert the graph to networkx object using the
# .to_networkx() method.
knn_graph = knn3.to_networkx()
dist_graph = dist.to_networkx()

# To plot with networkx, we need to merge the nodes back to
# their positions in order to plot in networkx
positions = dict(zip(knn_graph.nodes, coordinates))

# plot with a nice basemap
f, ax = plt.subplots(1, 2, figsize=(8, 4))
for i, facet in enumerate(ax):
    cases.plot(marker=".", color="orangered", ax=facet)
    add_basemap(facet)
    facet.set_title(("KNN-3", "50-meter Distance Band")[i])
    facet.axis("off")
nx.draw(knn_graph, positions, ax=ax[0], node_size=5, node_color="b")
nx.draw(dist_graph, positions, ax=ax[1], node_size=5, node_color="b")
plt.show()


network = cd.Network.from_networkx(knn_graph)
for node_id in network.nodes():
    coordinate = (positions[node_id][0]+15000, positions[node_id][1]-6712110)
    network.node_attributes(node_id, "xy", coordinate)
viewer = App()
viewer.add(network)
viewer.run()
