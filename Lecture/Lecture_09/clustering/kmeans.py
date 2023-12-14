import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

# Number of clusters
K = 4

# Generate pseudo-random isotropic Gaussian blobs for clustering.
X, y_true = make_blobs(n_samples=300, centers=4,
                       cluster_std=0.60, random_state=0)
plt.scatter(X[:, 0], X[:, 1], s=50)
plt.show()

# K-means clustering
kmeans = KMeans(n_clusters=K)
kmeans.fit(X)

# Predict the closest cluster each sample in X belongs to.
y_kmeans = kmeans.predict(X)

# Coordinates of cluster centers.
centers = kmeans.cluster_centers_

# Plot the clusters
plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
plt.show()