"""Tests for the from-scratch optimizers.

    uv run pytest Lecture/Algorithms/optimization/tests -v

An optimizer can be wrong in ways a single run never shows: cheating on its
budget, wandering outside the constraints, forgetting its best answer. These
tests check each of those directly, and compare methods the only fair way --
same budget, several seeds, averages.
"""

import numpy as np
import pytest

import search

BUDGET = 600
FAST = dict(k=6, budget=BUDGET)


def test_inside_knows_the_l_shape():
    assert search.inside((4, 14))          # in the wing
    assert search.inside((20, 4))          # in the bar
    assert not search.inside((16, 14))     # in the notch of the L
    assert not search.inside((-1, 4))


def test_more_columns_are_never_worse():
    layout = [(4, 4), (12, 4), (20, 4)]
    assert search.objective(layout + [(4, 14)]) <= search.objective(layout)


def test_a_column_everywhere_means_no_distance():
    assert search.objective(search.SAMPLES) == pytest.approx(0.0)


@pytest.mark.parametrize("name", list(search.METHODS))
def test_methods_respect_the_budget(name, monkeypatch):
    calls = []
    real = search.objective
    monkeypatch.setattr(search, "objective", lambda layout, samples=search.SAMPLES: calls.append(1) or real(layout, samples))
    search.METHODS[name](**FAST, seed=1)
    assert len(calls) <= BUDGET


@pytest.mark.parametrize("name", list(search.METHODS))
def test_methods_keep_columns_inside_the_plan(name):
    layout, value, _ = search.METHODS[name](**FAST, seed=2)
    assert len(layout) == 6
    assert all(search.inside(p) for p in layout)
    assert value == pytest.approx(search.objective(layout))     # the reported value is real


@pytest.mark.parametrize("name", list(search.METHODS))
def test_best_so_far_never_gets_worse(name):
    _, _, history = search.METHODS[name](**FAST, seed=3)
    assert all(b <= a + 1e-12 for a, b in zip(history, history[1:]))


@pytest.mark.parametrize("name", list(search.METHODS))
def test_methods_are_reproducible(name):
    a = search.METHODS[name](**FAST, seed=4)[1]
    b = search.METHODS[name](**FAST, seed=4)[1]
    assert a == b


def test_guided_search_beats_random_search_on_average():
    """averaged over seeds, with equal budgets -- the only fair comparison"""
    results = search.compare(seeds=range(4), budget=BUDGET)
    rand = np.mean(results["random search"])
    for name in ("hill climbing", "simulated annealing", "genetic algorithm"):
        assert np.mean(results[name]) < rand, name
