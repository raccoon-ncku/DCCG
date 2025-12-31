# Lecture 09: Architectural Optimization

This lecture focuses on **Optimization** in the context of architectural design. We move beyond simply generating geometry to finding the "best" geometry based on performance criteria.

👉[Slides: Optimization](https://app.rccn.dev/slidev/DCCG-09)

## 1. Concepts

Optimization is the process of finding the best solution from all feasible solutions. In architecture, this often involves:
*   **Variables**: Parameters we can change (e.g., beam width, column spacing).
*   **Objectives**: Goals we want to achieve (e.g., minimize weight, maximize daylight).
*   **Constraints**: Rules we must follow (e.g., max deflection < 5mm, total cost < $1M).

## 2. Examples

### Example 01: The Optimal Beam (Single Objective)
**File:** `01_beam_optimization_scipy.py`

A classic structural engineering problem. We use `scipy.optimize` to find the lightest possible rectangular beam that can support a 500kg load without deflecting more than 5mm.

*   **Library**: `scipy` (Standard scientific computing library)
*   **Method**: SLSQP (Sequential Least SQuares Programming)

### Example 02: Design Trade-offs (Multi-Objective)
**File:** `02_beam_optimization_pymoo.py`

Real design problems often have conflicting goals. Here, we explore the trade-off between a **light beam** (cheap) and a **stiff beam** (performant). The result is not one single answer, but a **Pareto Front** of optimal compromises.

*   **Library**: `pymoo` (Multi-objective Optimization in Python)
*   **Method**: NSGA-II (Non-dominated Sorting Genetic Algorithm II)

## 3. Legacy Examples
Older examples covering generic mathematical optimization (Knapsack, TSP, etc.) using `ortools` and `deap` can be found in the `legacy_examples/` folder.

## 4. Installation

For the easiest setup, create the dedicated AI environment from the root of the repository:

```bash
conda env create -f environment_ml.yml
conda activate DCCG_ML
```

Alternatively, you can install the required libraries manually in your existing environment:

```bash
pip install scipy pymoo matplotlib
```
