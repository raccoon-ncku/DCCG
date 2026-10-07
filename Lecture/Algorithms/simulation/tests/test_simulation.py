"""Property tests for the simulation tutorials.

    uv run pytest Lecture/Algorithms/simulation/tests -v

Simulations are tested the way experiments are run: known cases with known
outcomes (a blinker blinks, a glider glides), invariants that must hold at
every step (speed limits, connectivity), and a measured trend in the right
direction (alignment raises polarization). Never "the picture looks right".
"""

import math

import numpy as np
import pytest

import boids
import cellular_automata as ca
import dla


# --- cellular automata ------------------------------------------------------

def test_empty_stays_empty():
    assert not ca.step(np.zeros((8, 8), bool)).any()


def test_block_is_a_still_life():
    block = ca.pattern(["....", ".##.", ".##.", "...."])
    assert (ca.step(block) == block).all()


def test_blinker_has_period_two():
    blinker = ca.pattern([".....", ".....", ".###.", ".....", "....."])
    once, twice = ca.step(blinker), ca.step(ca.step(blinker))
    assert not (once == blinker).all()
    assert (twice == blinker).all()


def test_glider_moves_one_cell_diagonally_every_four_generations():
    g = np.zeros((12, 12), bool)
    g[1:4, 1:4] = ca.pattern([".#.", "..#", "###"])
    after = ca.run(g, 4)[-1]
    assert (np.roll(np.roll(g, 1, axis=0), 1, axis=1) == after).all()


def test_the_border_is_dead_not_wrapped():
    # a blinker against the edge loses the cells that would lie outside
    g = ca.pattern(["#..", "#..", "#.."])
    assert ca.step(g).sum() == 2          # wrapped, it would keep 3


def test_step_does_not_modify_its_input():
    g = ca.pattern([".....", ".###.", "....."])
    copy = g.copy()
    ca.step(g)
    assert (g == copy).all()


def test_voxels_put_generation_t_on_floor_t():
    hist = ca.run(ca.pattern([".....", ".....", ".###.", ".....", "....."]), 3)
    vox = ca.voxels(hist)
    assert len(vox) == sum(int(h.sum()) for h in hist)
    assert {z for _, _, z in vox} == {0, 1, 2, 3}


# --- boids ------------------------------------------------------------------

def test_speed_limits_always_hold():
    pos, vel = boids.init(120, seed=1)
    for _ in range(30):
        pos, vel = boids.step(pos, vel)
        s = np.linalg.norm(vel, axis=1)
        assert s.min() >= 0.5 - 1e-9 and s.max() <= 2.0 + 1e-9
        assert np.isfinite(pos).all()


def test_boids_stay_in_the_world():
    pos, vel = boids.init(80, seed=2)
    trail, _ = boids.run(pos, vel, 40)
    assert all(((p >= 0) & (p < 100.0)).all() for p in trail)


def test_alignment_makes_the_flock_polarized():
    """averaged over seeds: one run of a random simulation is an anecdote"""
    # Single runs vary a lot (0.17 to 0.91 for seeds 0-5): local alignment
    # forms aligned GROUPS, and whether they merge into one flock in 120 steps
    # depends on the start. So: every run must increase, and the average
    # must increase a lot. Testing one lucky seed would be testing the seed.
    before, after = [], []
    for seed in range(4):
        pos, vel = boids.init(150, seed=seed)
        _, vel_after = boids.run(pos, vel, 120, w_sep=0.0, w_coh=0.0, w_ali=1.0, radius=12.0)
        before.append(boids.polarization(vel))
        after.append(boids.polarization(vel_after))
    assert all(a > b for a, b in zip(after, before))
    assert sum(after) / 4 > sum(before) / 4 + 0.2


def test_without_rules_headings_do_not_change():
    pos, vel = boids.init(150, seed=3)
    _, vel_after = boids.run(pos, vel, 60, w_sep=0.0, w_coh=0.0, w_ali=0.0)
    assert boids.polarization(vel_after) == pytest.approx(boids.polarization(vel))


def test_step_returns_new_arrays():
    pos, vel = boids.init(20, seed=0)
    p0, v0 = pos.copy(), vel.copy()
    boids.step(pos, vel)
    assert (pos == p0).all() and (vel == v0).all()


def test_neighbour_lists_match_brute_force():
    pos, _ = boids.init(200, seed=5)
    fast = boids._neighbour_lists(pos, 8.0, 100.0)
    for i in range(0, 200, 17):
        d = np.linalg.norm(boids._wrap_delta(pos - pos[i], 100.0), axis=1)
        brute = sorted(j for j in np.nonzero(d < 8.0)[0] if j != i)
        assert sorted(fast[i].tolist()) == brute


# --- DLA --------------------------------------------------------------------

def test_dla_grows_the_requested_number_of_cells():
    assert len(dla.grow(300, seed=1)) == 300


def test_every_cell_touches_an_earlier_one():
    cells = dla.grow(400, seed=2)
    seen = {cells[0]}
    for c in cells[1:]:
        assert any((c[0] + dx, c[1] + dy) in seen for dx, dy in dla.NEIGHBOURS)
        assert c not in seen
        seen.add(c)


def test_dla_is_reproducible_from_its_seed():
    assert dla.grow(200, seed=7) == dla.grow(200, seed=7)
    assert dla.grow(200, seed=7) != dla.grow(200, seed=8)


def test_dla_is_branchy_not_solid():
    """fractal dimension clearly below 2 (a filled disc), around 1.7"""
    d = dla.fractal_dimension(dla.grow(800, seed=4))
    assert 1.4 < d < 1.95
