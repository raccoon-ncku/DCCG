"""Tests for the from-scratch learning tutorials.

    uv run pytest Lecture/Algorithms/learning/tests -v

The strongest test of a learning method is a case where you already know the
answer: clusters you planted, a physical law you can write down. If the
method cannot find those, it will not find anything you do not know either.
"""

import numpy as np
import pytest

import kmeans as km
import regression as rg


# --- k-means ----------------------------------------------------------------

def blobs(seed=0):
    rng = np.random.default_rng(seed)
    centres = np.array([[0, 0], [10, 0], [5, 9]])
    return np.vstack([c + rng.normal(0, 0.8, (40, 2)) for c in centres]), centres


def test_kmeans_finds_planted_clusters():
    X, true = blobs()
    labels, centres, _, _ = km.kmeans(X, 3)
    for c in true:                                   # every planted centre is recovered
        assert np.min(np.linalg.norm(centres - c, axis=1)) < 0.5
    assert sorted(np.bincount(labels)) == [40, 40, 40]


def test_inertia_never_increases_within_a_run():
    X, _ = blobs(1)
    _, _, _, history = km.kmeans(X, 5, n_init=1, seed=3)
    assert all(b <= a + 1e-9 for a, b in zip(history, history[1:]))


def test_more_clusters_never_fit_worse():
    X = km.roof_panels()
    inertias = [km.kmeans(X, k, seed=0)[2] for k in range(1, 7)]
    assert all(b <= a + 1e-6 for a, b in zip(inertias, inertias[1:]))


def test_kmeans_is_reproducible_and_validates_k():
    X, _ = blobs()
    assert (km.kmeans(X, 3, seed=7)[0] == km.kmeans(X, 3, seed=7)[0]).all()
    with pytest.raises(ValueError):
        km.kmeans(X, 0)


def test_roof_panels_vary_and_fewer_families_suffice():
    X = km.roof_panels()
    assert X.shape == (196, 2)
    assert X.max() - X.min() > 30                    # the panels really differ (mm)
    k10, (labels, centres, _, _) = km.families_needed(X, tolerance=10.0)
    assert km.worst_deviation(X, labels, centres) <= 10.0
    assert 1 < k10 < len(np.unique(X.round(1), axis=0))   # fewer families than distinct sizes


def test_a_looser_tolerance_needs_fewer_families():
    X = km.roof_panels()
    k5, _ = km.families_needed(X, tolerance=5.0, k_max=60)
    k20, _ = km.families_needed(X, tolerance=20.0, k_max=60)
    assert k20 < k5


# --- regression -------------------------------------------------------------

def test_linear_fit_recovers_known_coefficients():
    rng = np.random.default_rng(0)
    X = rng.uniform(-5, 5, (50, 2))
    y = 3.0 + 2.0 * X[:, 0] - 1.5 * X[:, 1]
    assert rg.fit_linear(X, y) == pytest.approx([3.0, 2.0, -1.5])


def test_regression_rediscovers_the_beam_law():
    """deflection ~ L^4 h^-3: the fit should find the exponents from noisy data alone"""
    L, h, d = rg.beam_experiments(n=60, noise=0.05)
    _, a, e = rg.fit_power_law(L, h, d)
    assert a == pytest.approx(4.0, abs=0.15)
    assert e == pytest.approx(-3.0, abs=0.15)


def test_surrogate_predicts_beams_it_has_not_seen():
    L, h, d = rg.beam_experiments(n=80, seed=2)
    train, test = rg.split(len(L))
    c, a, e = rg.fit_power_law(L[train], h[train], d[train])
    pred = np.exp(c + a * np.log(L[test]) + e * np.log(h[test]))
    assert rg.r2(np.log(d[test]), np.log(pred)) > 0.97


def test_train_error_falls_but_test_error_does_not():
    """the overfitting signature: a degree-12 fit beats degree 2 on training data, loses on test data"""
    x, y = rg.daylight_samples()
    train, test = rg.split(len(x), seed=4)
    errs = rg.polynomial_errors(x, y, [2, 12], train, test)
    assert errs[12][0] < errs[2][0]
    assert errs[12][1] > errs[2][1]


def test_split_is_a_partition():
    train, test = rg.split(20, 0.25)
    assert sorted(np.concatenate([train, test]).tolist()) == list(range(20))
    assert len(test) == 5
