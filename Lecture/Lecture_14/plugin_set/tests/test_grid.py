"""Executable spec for grid_mesh."""

import pytest

from compas_studio import grid_mesh

TOL = 1e-9


def test_counts():
    """(nx+1)*(ny+1) vertices, nx*ny faces"""
    mesh = grid_mesh(2, 3)
    assert mesh.number_of_vertices() == 12
    assert mesh.number_of_faces() == 6


def test_euler_characteristic_is_a_disc():
    """V - E + F == 1 for a flat grid (catches topology bugs)"""
    for nx, ny in ((1, 1), (3, 2), (4, 4)):
        assert grid_mesh(nx, ny).euler() == 1


def test_all_faces_are_quads():
    """every face has four vertices"""
    mesh = grid_mesh(3, 3)
    assert all(len(mesh.face_vertices(f)) == 4 for f in mesh.faces())


def test_normals_point_up():
    """consistent winding -> every normal has positive z"""
    mesh = grid_mesh(3, 3)
    assert all(mesh.face_normal(f)[2] > 0 for f in mesh.faces())


def test_rejects_nonsense_input():
    """no faces, or non-positive spacing, raises"""
    with pytest.raises(ValueError):
        grid_mesh(0, 3)
    with pytest.raises(ValueError):
        grid_mesh(2, 2, spacing=0)
