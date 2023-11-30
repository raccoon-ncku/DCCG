import numpy as np

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter


class MyProblem(Problem):
    def __init__(self):
        """
        max f1 = X1
        min f2 = X1 ^ 5 / X2 ^ 2
        st  1 <= X1 <= 20
            1 <= X2 <= 40
            X1 * X2 <= 200
        """

        super().__init__(n_var=2,
                         n_obj=2,
                         n_constr=1,
                         xl=np.array([1, 1]),
                         xu=np.array([20, 40]))

    def _evaluate(self, x, out, *args, **kwargs):
        # define both objectives
        f1 = x[:, 0]
        f2 = x[:, 0] ** 5 / x[:, 1] ** 2

        # we have to negate the objectives because by default we assume minimization
        f1, f2 = -f1, f2

        # define the constraint as a less or equal to zero constraint
        g1 = x[:, 0] * x[:, 1] - 200

        out["F"] = np.column_stack([f1, f2])
        out["G"] = g1


problem = MyProblem()

algorithm = NSGA2()

res = minimize(problem,
               algorithm,
               ('n_gen', 200),
               seed=1,
               verbose=True)

print(res.X)
print(res.F)

Scatter(title="Design Space").add(res.X, color="blue").show()
Scatter(title="Objective Space").add(
    res.F, color="red").show()
