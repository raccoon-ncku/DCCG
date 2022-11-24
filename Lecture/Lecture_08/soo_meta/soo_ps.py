import time
import matplotlib.pyplot as plt
import numpy as np

ITERATION = 500
POPULATION = 100

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


# Parameters of PS algorithm
problem = 'minimize'
n_particles = POPULATION
n_iterations = ITERATION
inertia_coeff = 0.9     # inertia constant
c1 = 1                  # cognitive constant
c2 = 2                  # social constant

# Visualization
fig, ax = plt.subplots()

plt.title('Evolutionary process of the objective function value')
plt.xlabel("Iteration")
plt.ylabel("Objective function")


class Particle:
    def __init__(self, bounds):
        self.particle_position = []
        self.particle_velocity = []
        self.local_best_particle_position = []
        # objective function value of the best particle position
        self.fitness_local_best_particle_position = initial_fitness
        # objective function value of the particle position
        self.fitness_particle_position = initial_fitness

        for i in range(n_vars):
            self.particle_position.append(
                np.random.uniform(bounds[i][0], bounds[i][1]))  # generate random initial position
            # generate random initial velocity
            self.particle_velocity.append(np.random.uniform(-1, 1))

    def evaluate(self, objective_function):
        self.fitness_particle_position = objective_function(
            self.particle_position)
        if problem == 'minimize':
            if self.fitness_particle_position < self.fitness_local_best_particle_position:
                # update particle's local best poition
                self.local_best_particle_position = self.particle_position
                # update fitness at particle's local best position
                self.fitness_local_best_particle_position = self.fitness_particle_position
        if problem == 'maximize':
            if self.fitness_particle_position > self.fitness_local_best_particle_position:
                # update particle's local best position
                self.local_best_particle_position = self.particle_position
                # update fitness at particle's local best position
                self.fitness_local_best_particle_position = self.fitness_particle_position

    def update_velocity(self, global_best_particle_position):
        for i in range(n_vars):
            r1 = np.random.rand()
            r2 = np.random.rand()

            # local explorative position displacement component
            cognitive_velocity = c1*r1 * \
                (self.local_best_particle_position[i] -
                 self.particle_position[i])

            # position displacement component towards global best
            social_velocity = c2*r2 * \
                (global_best_particle_position[i] - self.particle_position[i])

            self.particle_velocity[i] = inertia_coeff * \
                self.particle_velocity[i] + \
                cognitive_velocity + social_velocity

    def update_position(self, bounds):
        for i in range(n_vars):
            self.particle_position[i] = self.particle_position[i] + \
                self.particle_velocity[i]

            # check and repair to satisfy the upper bounds
            if self.particle_position[i] > bounds[i][1]:
                self.particle_position[i] = bounds[i][1]
            # check and repair to satisfy the lower bounds
            if self.particle_position[i] < bounds[i][0]:
                self.particle_position[i] = bounds[i][0]


class PSO:
    def __init__(self, objective_function, bounds, n_particles, n_iterations):
        fitness_global_best_particle_position = initial_fitness
        global_best_particle_position = []
        swarm_particle = []
        for i in range(n_particles):
            swarm_particle.append(Particle(bounds))
        A = []

        for i in range(n_iterations):
            for j in range(n_particles):
                swarm_particle[j].evaluate(objective_function)

                if problem == 'minimize':
                    if swarm_particle[j].fitness_particle_position < fitness_global_best_particle_position:
                        global_best_particle_position = list(
                            swarm_particle[j].particle_position)
                        fitness_global_best_particle_position = float(
                            swarm_particle[j].fitness_particle_position)
                if problem == 'maximize':
                    if swarm_particle[j].fitness_particle_position > fitness_global_best_particle_position:
                        global_best_particle_position = list(
                            swarm_particle[j].particle_position)
                        fitness_global_best_particle_position = float(
                            swarm_particle[j].fitness_particle_position)

            for j in range(n_particles):
                swarm_particle[j].update_velocity(
                    global_best_particle_position)
                swarm_particle[j].update_position(bounds)

            # record the best fitness
            A.append(fitness_global_best_particle_position)

            x = global_best_particle_position
            ofunc_clean = sum(x[idx]*cost2d[idx//len(J), idx % len(J)]
                              for idx in range(cost2d.size))

            # if i% 100 == 0:
            #     print(i, fitness_global_best_particle_position, ofunc_clean, global_best_particle_position)

            # Visualization
            ax.plot(A, color='r')
            ax.set_ylim(3400, 6000)
            fig.canvas.draw()
            ax.set_xlim(left=max(0, i - n_iterations), right=i + 3)
            time.sleep(0.001)

        pen_cust_demand = \
            sum((max(0, abs(sum(x[idx: idx + len(J)]) - d[idx//len(J) + 1])))
                ** 2 for idx in range(0, cost2d.size, len(J)))
        pen_fact_capacity = \
            sum((max(0, (sum(x[idx: idx + len(I)]) - M[idx//len(I) + 1])))
                ** 3 for idx in range(0, cost2d.size, len(I)))

        print('RESULT:')
        print('Objective function value:',
              fitness_global_best_particle_position)
        print('Penalty customer demand:', pen_cust_demand)
        print('Penalty factory capacity:', pen_fact_capacity)
        print('Objective function value clean:', ofunc_clean)

        EPS = 1.e-1
        x = global_best_particle_position
        for idx, _ in enumerate(x):
            if x[idx] > EPS:
                print("sending quantity %10s from factory %3s to customer %3s" % (
                    round(x[idx]), idx % len(J) + 1, idx//len(J) + 1))


if problem == 'minimize':
    initial_fitness = float("inf")
if problem == 'maximize':
    initial_fitness = -float("inf")
# Run Particle Swarm optimization
PSO(objective_function, bounds, n_particles, n_iterations)

plt.ioff()
plt.show()
