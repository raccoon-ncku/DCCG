import numpy as np
from scipy.optimize import minimize

# prepare all data structures
CUSTOMER_DEMAND = {1: 80, 2: 270, 3: 250, 4: 160, 5: 180}
FACTORY_CAPACITY = {1: 500, 2: 500, 3: 500}
CUSTOMERS = (1, 2, 3, 4, 5)
FACTORIES = (1, 2, 3)
TRANSPORTATION_COST = {
    (1, 1): 4,    (1, 2): 6,    (1, 3): 9,
    (2, 1): 5,    (2, 2): 4,    (2, 3): 7,
    (3, 1): 6,    (3, 2): 3,    (3, 3): 3,
    (4, 1): 8,    (4, 2): 5,    (4, 3): 3,
    (5, 1): 10,   (5, 2): 8,    (5, 3): 4
}


# to be used in SciPy we must transform cost dictionary into 2D array
cost2d = np.empty([len(CUSTOMERS), len(FACTORIES)])
for i in range(len(CUSTOMERS)):
    for j in range(len(FACTORIES)):
        cost2d[i, j] = TRANSPORTATION_COST[i+1, j+1]


# Initialize decision variables
x0 = np.ones(len(TRANSPORTATION_COST))*10

# bounds = list((0, max(CUSTOMER_DEMAND.values())) for _ in range(cost2d.size))
bounds = []
for i in range(len(CUSTOMERS)):
    for j in range(len(FACTORIES)):
        bounds.append((0, min([CUSTOMER_DEMAND[i+1], FACTORY_CAPACITY[j+1]])))


def objective(x):
    # objective function
    obj_func = sum(x[i]*cost2d[i//len(FACTORIES), i % len(FACTORIES)]
                   for i in range(cost2d.size))
    return obj_func


def const1():
    # Constraints: sum of goods == customer demand
    tmp = []
    for i in range(0, cost2d.size, len(FACTORIES)):
        tmp_constr = {
            'type': 'eq',
            'fun': lambda x, i=i: CUSTOMER_DEMAND[i//len(FACTORIES) + 1] - np.sum(x[i: i + len(FACTORIES)]),
        }
        tmp.append(tmp_constr)
    return tmp


def const2():
    # Constraints: sum of goods <= factory capacity
    tmp = []
    for i in range(len(FACTORIES)):
        tmp_constr = {
            'type': 'ineq',
            'fun': lambda x, i=i: FACTORY_CAPACITY[i + 1] - np.sum([x[i+j*len(FACTORIES)] for j in range(len(CUSTOMERS))])
        }
        tmp.append(tmp_constr)
    return tmp


constraints = [*const1(), *const2()]

solution = minimize(fun=objective,
                    x0=x0,
                    bounds=bounds,
                    method='SLSQP',
                    constraints=constraints,
                    )

if solution.success and solution.status == 0:
    print("Solution is feasible and optimal")
    print("Objective function value = ", solution.fun)
elif solution.status != 0:
    print("Failed to find solution. Exit code", solution.status)
else:
    # something else is wrong
    print(solution.message)
if solution.success:
    EPS = 1.e-6
    for i, _ in enumerate(solution.x):
        if solution.x[i] > EPS:
            print("sending quantity %10s from factory %3s to customer %3s" %
                  (round(solution.x[i]), i % len(FACTORIES) + 1, i//len(FACTORIES) + 1))
