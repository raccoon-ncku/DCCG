import time
import matplotlib.pyplot as plt
import numpy as np

ITERATION = 500

d = {1: 80, 2: 270, 3: 250, 4: 160, 5: 180}  # customer demand
M = {1: 500, 2: 500, 3: 500}                 # factory capacity
I = [1, 2, 3, 4, 5]     # Customers
J = [1, 2, 3]         # Factories
cost = {(1, 1): 4,    (1, 2): 6,    (1, 3): 9,
        (2, 1): 5,    (2, 2): 4,    (2, 3): 7,
        (3, 1): 6,    (3, 2): 3,    (3, 3): 3,
        (4, 1): 8,    (4, 2): 5,    (4, 3): 3,
        (5, 1): 10,   (5, 2): 8,    (5, 3): 4
        }              # transportation cost
# Transform cost dictionary into 2D array
cost2d = np.empty([len(I), len(J)])
for i in range(len(I)):
    for j in range(len(J)):
        cost2d[i, j] = cost[i+1, j+1]
# Variables bounds
n_vars = cost2d.size    # number of variables
bounds = 3*[(0, 80), (0, 270), (0, 250), (0, 160), (0, 180)]


def objective_function(x):
    obj_func = sum(x[idx]*cost2d[idx//len(J), idx % len(J)]
                   for idx in range(cost2d.size))

    # Penalty: sum of all factories outputs == customer_i demand
    pen_cust_demand = 0
    for idx in range(0, cost2d.size, len(J)):
        pen_cust_demand += (max(0,
                            abs(sum(x[idx: idx + len(J)]) - d[idx//len(J) + 1])))**2

    obj_func += pen_cust_demand

    # Penalty: sum of all customers demands <= factory_j capacity
    pen_fact_capacity = 0
    for idx in range(0, cost2d.size, len(I)):
        pen_fact_capacity += (max(0,
                              (sum(x[idx: idx + len(I)]) - M[idx//len(I) + 1])))**3

    obj_func += pen_fact_capacity

    return obj_func


def de(fobj, bounds, mut=0.8, crossp=0.7, popsize=200, its=500):
    dimensions = len(bounds)
    # random (0-1) positions for all particles
    pop = np.random.rand(popsize, dimensions)
    min_b, max_b = np.asarray(bounds).T
    diff = np.fabs(min_b - max_b)
    # scale particle positions according to bounds
    pop_denorm = min_b + pop * diff
    # initial objective function value
    fitness = np.asarray([fobj(ind) for ind in pop_denorm])
    # global best particle position
    best_idx = np.argmin(fitness)
    best = pop_denorm[best_idx]
    for i in range(its):
        for j in range(popsize):
            # get indices of all particles except current
            idxs = [idx for idx in range(popsize) if idx != j]
            # randomly select 3 particles
            a, b, c = pop[np.random.choice(idxs, 3, replace=False)]
            # mix them into new mutant particle
            mutant = np.clip(a + mut * (b - c), 0, 1)
            # exchange some coordinates between mutant and current particle
            cross_points = np.random.rand(dimensions) < crossp
            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True
            trial = np.where(cross_points, mutant, pop[j])
            # scale new trial particle to bounds
            trial_denorm = min_b + trial * diff
            f = fobj(trial_denorm)
            if f < fitness[j]:
                fitness[j] = f
                pop[j] = trial
                if f < fitness[best_idx]:
                    best_idx = j
                    best = trial_denorm
        yield best, fitness[best_idx]


bounds = 3*[(0, 80), (0, 270), (0, 250), (0, 160), (0, 180)]
# Run Differential Evolution optimization
DE = list(de(objective_function, bounds, mut=0.8,
          crossp=0.7, popsize=200, its=ITERATION))
x = DE[-1][0]
ofunc_value = DE[-1][-1]
pen_cust_demand = \
    sum((max(0, abs(sum(x[idx: idx + len(J)]) - d[idx//len(J) + 1])))
        ** 2 for idx in range(0, cost2d.size, len(J)))
pen_fact_capacity = \
    sum((max(0, (sum(x[idx: idx + len(I)]) - M[idx//len(I) + 1])))
        ** 3 for idx in range(0, cost2d.size, len(I)))
print('RESULT:')
print('Objective function value:', ofunc_value)
print('Penalty customer demand:', pen_cust_demand)
print('Penalty factory capacity:', pen_fact_capacity)
print('Objective function value clean:', ofunc_value -
      pen_cust_demand - pen_fact_capacity)
EPS = 1.e-0
for idx, _ in enumerate(x):
    if x[idx] > EPS:
        print("sending quantity %10s from factory %3s to customer %3s" %
              (round(x[idx]), idx % len(J) + 1, idx//len(J) + 1))

# Visualization
fig, ax = plt.subplots()

plt.title('Evolutionary process of the objective function value')
plt.xlabel("Iteration")
plt.ylabel("Objective function")

A = []
for item in DE:
    A.append(item[-1])

# Visualization
ax.plot(A, color='r')
ax.set_ylim(3400, 6000)
fig.canvas.draw()
ax.set_xlim(left=0, right=ITERATION)


plt.ioff()
plt.show()
