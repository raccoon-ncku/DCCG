"""Boids (Reynolds, 1987): separation, alignment and cohesion on a torus.

State is two numpy arrays (positions, velocities). Neighbours come from a
spatial hash, not O(n^2) search; polarization() measures how aligned the
flock is. W11 simulation README §2.
"""

import math
from collections import defaultdict

import numpy as np


def init(n=150, size=100.0, speed=1.0, seed=0):
    rng = np.random.default_rng(seed)
    pos = rng.uniform(0, size, (n, 2))
    angle = rng.uniform(0, 2 * math.pi, n)
    vel = speed * np.column_stack([np.cos(angle), np.sin(angle)])
    return pos, vel


def _wrap_delta(d, size):
    """Shortest offset on a torus."""
    return (d + size / 2) % size - size / 2


def _neighbour_lists(pos, radius, size):
    cells = defaultdict(list)
    keys = np.floor(pos / radius).astype(int)
    ncell = max(1, int(size // radius))
    for i, (cx, cy) in enumerate(keys):
        cells[(cx % ncell, cy % ncell)].append(i)
    result = []
    for i, (cx, cy) in enumerate(keys):
        cand = [j for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                for j in cells.get(((cx + dx) % ncell, (cy + dy) % ncell), ()) if j != i]
        cand = np.unique(np.array(cand, dtype=int)) if cand else np.array([], dtype=int)
        if len(cand):
            d = np.linalg.norm(_wrap_delta(pos[cand] - pos[i], size), axis=1)
            cand = cand[d < radius]
        result.append(cand)
    return result


def step(pos, vel, size=100.0, radius=8.0, too_close=3.0,
         w_sep=1.5, w_ali=1.0, w_coh=1.0, min_speed=0.5, max_speed=2.0):
    """One time step. Returns NEW (pos, vel); the inputs are not modified."""
    steer = np.zeros_like(vel)
    for i, nb in enumerate(_neighbour_lists(pos, radius, size)):
        if not len(nb):
            continue
        offsets = _wrap_delta(pos[nb] - pos[i], size)
        if w_coh:
            steer[i] += w_coh * offsets.mean(axis=0) / radius
        if w_ali:
            steer[i] += w_ali * (vel[nb].mean(axis=0) - vel[i]) / max_speed
        if w_sep:
            d = np.linalg.norm(offsets, axis=1)
            close = d < too_close
            if close.any():
                steer[i] -= w_sep * (offsets[close] / d[close, None] ** 2).sum(axis=0)
    new_vel = vel + 0.1 * steer
    speed = np.linalg.norm(new_vel, axis=1)
    speed_safe = np.where(speed == 0, 1.0, speed)
    clamped = np.clip(speed, min_speed, max_speed)
    new_vel = new_vel / speed_safe[:, None] * clamped[:, None]
    return (pos + new_vel) % size, new_vel


def run(pos, vel, steps, **params):
    """Returns the list of position arrays (steps + 1 of them) and the final velocity."""
    trail = [pos]
    for _ in range(steps):
        pos, vel = step(pos, vel, **params)
        trail.append(pos)
    return trail, vel


def polarization(vel):
    """|mean of unit headings|: 0 = every direction, 1 = all parallel."""
    unit = vel / np.linalg.norm(vel, axis=1)[:, None]
    return float(np.linalg.norm(unit.mean(axis=0)))
