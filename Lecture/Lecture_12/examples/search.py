"""Four searches on one problem: place K columns in an L-shaped plan so that no
floor point is far from a column (minimise the worst distance).

Random search, hill climbing, simulated annealing and a genetic algorithm,
compared fairly: the same evaluation Budget for each, over several seeds.
W12 optimization README §3.
"""

import math
import random

import numpy as np

# an L-shaped plan, metres: a 24 x 8 bar plus a 8 x 10 wing
PLAN = [(0, 0), (24, 0), (24, 8), (8, 8), (8, 18), (0, 18)]


def inside(p, poly=PLAN):
    """Ray casting: is point p inside the polygon?"""
    x, y = p
    hit = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            hit = not hit
    return hit


def floor_samples(step=0.5, poly=PLAN):
    xs = [x for x, _ in poly]
    ys = [y for _, y in poly]
    pts = [(x, y) for x in np.arange(min(xs) + step / 2, max(xs), step)
           for y in np.arange(min(ys) + step / 2, max(ys), step) if inside((x, y), poly)]
    return np.array(pts)


SAMPLES = floor_samples()


def objective(layout, samples=SAMPLES):
    """Largest distance from any floor sample to its nearest column (m). Lower is better."""
    cols = np.asarray(layout, dtype=float).reshape(-1, 2)
    d = np.linalg.norm(samples[:, None, :] - cols[None, :, :], axis=2)
    return float(d.min(axis=1).max())


class BudgetExceeded(Exception):
    pass


class Budget:
    """Counts objective evaluations; raises once the budget is spent."""

    def __init__(self, evaluations):
        self.left = evaluations
        self.used = 0

    def __call__(self, layout):
        if self.left <= 0:
            raise BudgetExceeded
        self.left -= 1
        self.used += 1
        return objective(layout)


def random_layout(k, rnd):
    cols = []
    while len(cols) < k:
        p = (rnd.uniform(0, 24), rnd.uniform(0, 18))
        if inside(p):
            cols.append(p)
    return cols


def nudge(layout, rnd, size):
    """Move one random column by a random step, staying inside the plan."""
    new = list(layout)
    i = rnd.randrange(len(new))
    for _ in range(50):
        p = (new[i][0] + rnd.gauss(0, size), new[i][1] + rnd.gauss(0, size))
        if inside(p):
            new[i] = p
            return new
    return new


def random_search(k=6, budget=3000, seed=0):
    rnd, f = random.Random(seed), Budget(budget)
    best, best_val, history = None, math.inf, []
    try:
        while True:
            cand = random_layout(k, rnd)
            val = f(cand)
            if val < best_val:
                best, best_val = cand, val
            history.append(best_val)
    except BudgetExceeded:
        return best, best_val, history


def hill_climb(k=6, budget=3000, seed=0, step=1.5):
    rnd, f = random.Random(seed), Budget(budget)
    cur = random_layout(k, rnd)
    cur_val = f(cur)
    history = [cur_val]
    try:
        while True:
            cand = nudge(cur, rnd, step)
            val = f(cand)
            if val < cur_val:                       # only ever downhill
                cur, cur_val = cand, val
            history.append(cur_val)
    except BudgetExceeded:
        return cur, cur_val, history


def simulated_annealing(k=6, budget=3000, seed=0, step=1.5, t_start=1.0, t_end=0.005):
    rnd, f = random.Random(seed), Budget(budget)
    cur = random_layout(k, rnd)
    cur_val = f(cur)
    best, best_val, history = cur, cur_val, [cur_val]
    n = 1
    try:
        while True:
            t = t_start * (t_end / t_start) ** (n / budget)    # geometric cooling
            cand = nudge(cur, rnd, step * (0.3 + 0.7 * t / t_start))
            val = f(cand)
            n += 1
            # better: always accept. worse: accept with probability exp(-delta / T)
            if val < cur_val or rnd.random() < math.exp(-(val - cur_val) / t):
                cur, cur_val = cand, val
                if val < best_val:
                    best, best_val = cand, val
            history.append(best_val)
    except BudgetExceeded:
        return best, best_val, history


def genetic(k=6, budget=3000, seed=0, population=30, mutation=1.2, elite=2):
    rnd, f = random.Random(seed), Budget(budget)
    history = []
    try:
        pop = [random_layout(k, rnd) for _ in range(population)]
        scored = sorted(((f(ind), ind) for ind in pop), key=lambda s: s[0])
        history.append(scored[0][0])
        while True:
            def pick():                                  # tournament of three
                return min(rnd.sample(scored, 3), key=lambda s: s[0])[1]
            children = [ind for _, ind in scored[:elite]]          # elitism: the best survive
            while len(children) < population:
                a, b = pick(), pick()
                child = [a[i] if rnd.random() < 0.5 else b[i] for i in range(k)]   # crossover
                if rnd.random() < 0.8:
                    child = nudge(child, rnd, mutation)                            # mutation
                children.append(child)
            new_scored = list(scored[:elite])
            for child in children[elite:]:
                new_scored.append((f(child), child))
            scored = sorted(new_scored, key=lambda s: s[0])
            history.append(scored[0][0])
    except BudgetExceeded:
        return scored[0][1], scored[0][0], history


METHODS = {
    "random search": random_search,
    "hill climbing": hill_climb,
    "simulated annealing": simulated_annealing,
    "genetic algorithm": genetic,
}


def compare(seeds=range(8), budget=3000, k=6):
    """{method: [best value for each seed]} -- the fair comparison."""
    return {name: [fn(k=k, budget=budget, seed=s)[1] for s in seeds] for name, fn in METHODS.items()}


if __name__ == "__main__":
    results = compare()
    for name, vals in results.items():
        print(f"{name:20s} mean {np.mean(vals):5.2f} m   best {min(vals):5.2f}   worst {max(vals):5.2f}")
