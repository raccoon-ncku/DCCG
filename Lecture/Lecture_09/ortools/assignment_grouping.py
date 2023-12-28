from ortools.linear_solver import pywraplp


costs = [
    [0, 10, 100],
    [0, 100, 10],
    [10, 100, 0],
    [0, 100, 10],
    [10, 0, 100],
    [0, 10, 100],
    [10, 100, 10],
    [100, 0, 10],
    [0, 100, 10],
    [10, 100, 0]
]
num_workers = len(costs)
num_tasks = len(costs[0])

# Solver
# Create the mip solver with the SCIP backend.
solver = pywraplp.Solver.CreateSolver("SCIP")

# Variables
# x[i, j] is an array of 0-1 variables, which will be 1
# if student i is assigned to group j.
x = {}
for i in range(num_workers):
    for j in range(num_tasks):
        x[i, j] = solver.IntVar(0, 1, "")

# Constraints
# Each student is assigned to exactly one 1 group.
for i in range(num_workers):
    solver.Add(solver.Sum([x[i, j] for j in range(num_tasks)]) == 1)

# Each group is assigned to at least 3 student.
for j in range(num_tasks):
    solver.Add(solver.Sum([x[i, j] for i in range(num_workers)]) >= 3)

# Objective
objective_terms = []
for i in range(num_workers):
    for j in range(num_tasks):
        objective_terms.append(costs[i][j] * x[i, j])
solver.Minimize(solver.Sum(objective_terms))

# Solve
print(f"Solving with {solver.SolverVersion()}")
status = solver.Solve()

# Print solution.
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print(f"Total cost = {solver.Objective().Value()}\n")
    for i in range(num_workers):
        for j in range(num_tasks):
            # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
            if x[i, j].solution_value() > 0.5:
                print(f"Student {i} assigned to studio {j}." + f" Cost: {costs[i][j]}")
else:
    print("No solution found.")
