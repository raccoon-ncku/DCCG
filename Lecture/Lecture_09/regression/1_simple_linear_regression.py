# Code rewrited based on Jaques Grobler's tutorial

import matplotlib.pyplot as plt
import numpy as np

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

# Load the diabetes dataset
diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y=True)

# Use only one feature
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
features = datasets.load_diabetes()['feature_names']
idx = features.index('s2')
diabetes_X = diabetes_X[:, np.newaxis, idx]

# Split the data into training/testing sets
diabetes_X_train = diabetes_X[:-20]
diabetes_X_test = diabetes_X[-20:]

# Split the targets into training/testing sets
diabetes_y_train = diabetes_y[:-20]
diabetes_y_test = diabetes_y[-20:]

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(diabetes_X_train, diabetes_y_train)

# Make predictions using the testing set
diabetes_y_pred = regr.predict(diabetes_X_test)

# The coefficients
print("Coefficients: \n", regr.coef_)
# The mean squared error
print("Mean squared error: %.2f" % mean_squared_error(diabetes_y_test, diabetes_y_pred))
# The coefficient of determination: 1 is perfect prediction
print("Coefficient of determination: %.2f" % r2_score(diabetes_y_test, diabetes_y_pred))

# Plot outputs
plt.scatter(diabetes_X_train, diabetes_y_train, color="black")
plt.plot(diabetes_X_test, diabetes_y_pred, color="blue", linewidth=3)
plt.xlabel(features[idx])
plt.xticks(())
plt.yticks(())

plt.show()