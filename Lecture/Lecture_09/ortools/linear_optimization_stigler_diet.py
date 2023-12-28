"""The Stigler diet problem.

A description of the problem can be found here:
https://en.wikipedia.org/wiki/Stigler_diet.
"""
from ortools.linear_solver import pywraplp
import pathlib
import pandas as pd

# Read the data from the CSV files.
PWD = pathlib.Path(__file__).parent.absolute()
GOAL_FILE = PWD / "stigler_diet_nutrient_goal.csv"
DATA_FILE = PWD / "stigler_diet_data.csv"

with open(GOAL_FILE, "r") as f:
    df = pd.read_csv(f, header=0)
    nutrients = df.values.tolist()

with open(DATA_FILE, "r") as f:
    df = pd.read_csv(f, header=0)
    data = df.values.tolist()

# Instantiate a Glop solver and naming it.
solver = pywraplp.Solver.CreateSolver("GLOP")

# Declare an array to hold our variables.
foods = [solver.NumVar(0.0, solver.infinity(), item[0]) for item in data]

print("Number of variables =", solver.NumVariables())

# Create the constraints, one per nutrient.
constraints = []
for i, nutrient in enumerate(nutrients):
    constraints.append(solver.Constraint(nutrient[1], solver.infinity()))
    for j, item in enumerate(data):
        constraints[i].SetCoefficient(foods[j], item[i + 3])

print("Number of constraints =", solver.NumConstraints())

# Objective function: Minimize the sum of (price-normalized) foods.
objective = solver.Objective()
for food in foods:
    objective.SetCoefficient(food, 1)
objective.SetMinimization()

print(f"Solving with {solver.SolverVersion()}")
status = solver.Solve()

# Check that the problem has an optimal solution.
if status != solver.OPTIMAL:
    print("The problem does not have an optimal solution!")
    if status == solver.FEASIBLE:
        print("A potentially suboptimal solution was found.")
    else:
        print("The solver could not solve the problem.")


# Display the amounts (in dollars) to purchase of each food.
nutrients_result = [0] * len(nutrients)
print("\nAnnual Foods:")
for i, food in enumerate(foods):
    if food.solution_value() > 0.0:
        print("{}: ${}".format(data[i][0], 365.0 * food.solution_value()))
        for j, _ in enumerate(nutrients):
            nutrients_result[j] += data[i][j + 3] * food.solution_value()
print("\nOptimal annual price: ${:.4f}".format(365.0 * objective.Value()))

print("\nNutrients per day:")
for i, nutrient in enumerate(nutrients):
    print(
        "{}: {:.2f} (min {})".format(nutrient[0], nutrients_result[i], nutrient[1])
    )

print("\nAdvanced usage:")
print(f"Problem solved in {solver.wall_time():d} milliseconds")
print(f"Problem solved in {solver.iterations():d} iterations")
