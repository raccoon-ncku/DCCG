"""
Lecture 09: Architectural Optimization
Example 02: Multi-Objective Optimization of a Cantilever Beam using Pymoo

Problem Statement:
    Explore the trade-off between minimizing the weight of the beam 
    and minimizing the deflection.
    
    We are not setting a hard limit on deflection, but rather asking:
    "What is the lightest beam for a given deflection?" and vice versa.

Objectives:
    1. Minimize Area (b * h)
    2. Minimize Deflection

Variables:
    b (width): 0.01m to 0.5m
    h (height): 0.01m to 0.5m
"""

import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

class BeamProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=2, 
                         n_obj=2, 
                         n_ieq_constr=0, # No hard constraints for this exploration
                         xl=np.array([0.01, 0.01]), 
                         xu=np.array([0.5, 0.5]))
        
        # Constants
        self.L = 2.0
        self.F = 5000.0
        self.E = 210e9

    def _evaluate(self, x, out, *args, **kwargs):
        b, h = x
        
        # Objective 1: Area (Minimize Weight)
        f1 = b * h
        
        # Objective 2: Deflection (Maximize Stiffness)
        I = (b * h**3) / 12
        f2 = (self.F * self.L**3) / (3 * self.E * I)
        
        out["F"] = [f1, f2]

def run_optimization():
    print("--- Multi-Objective Beam Optimization (NSGA-II) ---")
    
    problem = BeamProblem()

    # NSGA-II is a popular genetic algorithm for multi-objective problems
    algorithm = NSGA2(pop_size=100)

    print("Running Genetic Algorithm...")
    res = minimize(problem,
                   algorithm,
                   ('n_gen', 100),
                   seed=1,
                   verbose=True)

    print("\nOptimization Complete!")
    print(f"Found {len(res.F)} solutions on the Pareto Front.")
    
    # Sort results by Area (Objective 1)
    sorted_indices = np.argsort(res.F[:, 0])
    sorted_F = res.F[sorted_indices]
    sorted_X = res.X[sorted_indices]

    print("\n--- Selected Solutions from Pareto Front ---")
    print(f"{'Width (mm)':<15} {'Height (mm)':<15} {'Area (m2)':<15} {'Deflection (mm)':<15}")
    print("-" * 65)
    
    # Print 5 evenly spaced solutions
    indices = np.linspace(0, len(sorted_F)-1, 5, dtype=int)
    for i in indices:
        b, h = sorted_X[i]
        area = sorted_F[i, 0]
        defl = sorted_F[i, 1]
        print(f"{b*1000:<15.2f} {h*1000:<15.2f} {area:<15.4f} {defl*1000:<15.2f}")

    # Visualization
    try:
        plot = Scatter(title="Pareto Front: Weight vs Deflection")
        plot.add(res.F, color="red")
        plot.show()
        print("\nPlot displayed. Close window to exit.")
    except Exception as e:
        print(f"\nCould not display plot: {e}")

if __name__ == "__main__":
    run_optimization()
