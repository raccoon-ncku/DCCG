import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn import datasets

#   - age     age in years
#   - sex
#   - bmi     body mass index
#   - bp      average blood pressure
#   - s1      tc, total serum cholesterol
#   - s2      ldl, low-density lipoproteins
#   - s3      hdl, high-density lipoproteins
#   - s4      tch, total cholesterol / HDL
#   - s5      ltg, possibly log of serum triglycerides level
#   - s6      glu, blood sugar level

FEATURE_1 = 's2'
FEATURE_2 = 's5'

# Load the diabetes dataset
X, y = datasets.load_diabetes(return_X_y=True)
features = datasets.load_diabetes()['feature_names']

# Use only two features
indices = (
    features.index(FEATURE_1),
    features.index(FEATURE_2),
)

# Split the data into training/testing sets
diabetes_X_train = X[:-20, indices]
diabetes_X_test = X[-20:, indices]
diabetes_y_train = y[:-20]
diabetes_y_test = y[-20:]

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(diabetes_X_train, diabetes_y_train)


def plot_figs(fig_num, X_train, clf, elev=-0.5, azim=90):
    """
    Plot 3D figures of linear regressions

    Parameters
    ----------
    fig_num: int, figure number
    X_train: numpy array of shape [n_samples, 2]
        Training data
    clf: regressor
    elev: elevation angle for 3D plot
    azim: azimuth angle for 3D plot
    """
    
    fig = plt.figure(fig_num, figsize=(10, 10))
    plt.clf()
    ax = fig.add_subplot(111, projection="3d", elev=elev, azim=azim)

    ax.scatter(X_train[:, 0], X_train[:, 1], diabetes_y_train, c="k", marker="+")
    ax.plot_surface(
        np.array([[-0.1, -0.1], [0.15, 0.15]]),
        np.array([[-0.1, 0.15], [-0.1, 0.15]]),
        clf.predict(
            np.array([[-0.1, -0.1, 0.15, 0.15], [-0.1, 0.15, -0.1, 0.15]]).T
        ).reshape((2, 2)),
        alpha=0.5,
    )
    ax.set_xlabel(FEATURE_1)
    ax.set_ylabel(FEATURE_2)
    ax.set_zlabel("Y (diabetes progression)")
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    ax.zaxis.set_ticklabels([])


# Plot the figures
plot_figs(1, diabetes_X_train, regr)
plt.show()