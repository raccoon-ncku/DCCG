# ──────────────────────────────────────────────────────────────────────────────
#  READ ONLY  ·  this file is the SPEC, not the answers.
#
#  Your work goes in  ../answers.py  (or ../answers_core.py + ../answers_runner.py
#  in Week 09). That file is auto-created from the shipped starter on first run
#  and is gitignored, so `git pull` never conflicts with it. Read the
#  assertions below to understand what each checkpoint is checking; do not
#  change them.
# ──────────────────────────────────────────────────────────────────────────────
"""
The SPECIFICATION for Week 05.

`test_grid_satisfies_eulers_formula` is the one worth stealing for your own
projects. It is a single integer comparison, it costs nothing, and it catches
duplicated vertices, missing faces and accidental holes -- all of which look
completely normal in a viewer.
"""

import math

import pytest
from compas.datastructures import Mesh

from answers import (
    colour_by_height,
    deform_by_wave,
    grid_mesh,
    mesh_stats,
    tag_supports,
    vertex_ring,
)

TOL = 1e-9


def approx(a, b, tol=TOL):
    return abs(a - b) < tol


# --- 1. grid_mesh -----------------------------------------------------------

def test_grid_has_the_right_counts():
    """grid_mesh(nx, ny) has (nx+1)*(ny+1) vertices and nx*ny faces"""
    mesh = grid_mesh(2, 3)
    assert mesh.number_of_vertices() == 12
    assert mesh.number_of_faces() == 6


def test_grid_faces_are_all_quads():
    """every face has exactly four vertices"""
    mesh = grid_mesh(3, 2)
    for fkey in mesh.faces():
        assert len(mesh.face_vertices(fkey)) == 4


def test_grid_satisfies_eulers_formula():
    """V - E + F == 1 for a flat disc-like grid"""
    # If this is not 1, the topology is wrong: duplicated vertices (each corner
    # added separately instead of shared), or a missing face. Neither is
    # visible on screen -- this integer is the only thing that tells you.
    for nx, ny in ((1, 1), (2, 3), (4, 4)):
        mesh = grid_mesh(nx, ny)
        assert mesh.euler() == 1, (
            f"grid_mesh({nx}, {ny}) has euler={mesh.euler()}, expected 1. "
            "The most likely cause is that neighbouring faces do not SHARE "
            "vertices -- reuse the keys instead of adding new ones."
        )


def test_grid_spacing_and_extent():
    """the grid spans from the origin to (nx*spacing, ny*spacing)"""
    mesh = grid_mesh(2, 3, spacing=0.5)
    xs = [mesh.vertex_coordinates(k)[0] for k in mesh.vertices()]
    ys = [mesh.vertex_coordinates(k)[1] for k in mesh.vertices()]
    assert approx(min(xs), 0) and approx(max(xs), 1.0)
    assert approx(min(ys), 0) and approx(max(ys), 1.5)


def test_grid_is_flat():
    """every vertex of the grid is at z = 0"""
    mesh = grid_mesh(2, 2)
    assert all(approx(mesh.vertex_coordinates(k)[2], 0) for k in mesh.vertices())


def test_grid_normals_all_point_up():
    """faces are wound consistently, so every normal points along +Z"""
    mesh = grid_mesh(3, 3)
    for fkey in mesh.faces():
        assert mesh.face_normal(fkey)[2] > 0, (
            f"face {fkey} points downward. Face vertex order decides the "
            "normal -- wind every face counter-clockwise seen from above."
        )


def test_grid_total_area_is_correct():
    """the grid's area is nx * ny * spacing^2"""
    mesh = grid_mesh(3, 4, spacing=2.0)
    total = sum(mesh.face_area(f) for f in mesh.faces())
    assert approx(total, 3 * 4 * 4.0)


def test_grid_rejects_nonsense_input():
    """a grid needs at least one face in each direction"""
    with pytest.raises(ValueError):
        grid_mesh(0, 3)
    with pytest.raises(ValueError):
        grid_mesh(2, -1)


# --- 2. mesh_stats ----------------------------------------------------------

def test_mesh_stats_reports_the_counts():
    """mesh_stats() reports vertices, edges and faces"""
    stats = mesh_stats(grid_mesh(2, 3))
    assert stats["vertices"] == 12
    assert stats["faces"] == 6
    assert stats["edges"] == 17


def test_mesh_stats_euler_is_consistent():
    """the reported euler equals V - E + F"""
    stats = mesh_stats(grid_mesh(3, 3))
    assert stats["euler"] == stats["vertices"] - stats["edges"] + stats["faces"]


def test_mesh_stats_counts_boundary_vertices():
    """a 2x2 grid has 8 DISTINCT boundary vertices and one in the middle"""
    # If you got 9, you used len(mesh.vertices_on_boundary()). That method
    # returns the boundary as a closed cycle -- the first vertex appears again
    # at the end. Reading the docstring of a library function you are about to
    # trust is not optional; this is what it costs when you skip it.
    stats = mesh_stats(grid_mesh(2, 2))
    assert stats["vertices"] == 9
    assert stats["boundary"] == 8


def test_mesh_stats_reports_area():
    """mesh_stats() totals the face areas"""
    assert approx(mesh_stats(grid_mesh(2, 2, spacing=3.0))["area"], 4 * 9.0)


# --- 3. colour_by_height ----------------------------------------------------

def test_colour_sets_an_attribute_on_every_vertex():
    """every vertex ends up with a "color" attribute"""
    mesh = deform_by_wave(grid_mesh(3, 3), amplitude=1.0)
    colour_by_height(mesh)
    for key in mesh.vertices():
        assert mesh.vertex_attribute(key, "color") is not None


def test_colour_extremes_match_the_endpoints():
    """the lowest vertex gets `low` and the highest gets `high`"""
    mesh = deform_by_wave(grid_mesh(4, 1), amplitude=2.0)
    colour_by_height(mesh, low=(0, 0, 255), high=(255, 0, 0))
    heights = {k: mesh.vertex_coordinates(k)[2] for k in mesh.vertices()}
    lowest = min(heights, key=heights.get)
    highest = max(heights, key=heights.get)
    assert tuple(mesh.vertex_attribute(lowest, "color")) == (0, 0, 255)
    assert tuple(mesh.vertex_attribute(highest, "color")) == (255, 0, 0)


def test_colour_handles_a_completely_flat_mesh():
    """a flat mesh does not crash with a division by zero"""
    # Every z is identical, so the range is 0. Dividing by it is the obvious
    # implementation and the wrong one. The spec says: everyone gets `low`.
    mesh = grid_mesh(2, 2)
    colour_by_height(mesh, low=(1, 2, 3), high=(9, 9, 9))
    for key in mesh.vertices():
        assert tuple(mesh.vertex_attribute(key, "color")) == (1, 2, 3)


def test_colour_returns_the_same_mesh():
    """colour_by_height() modifies in place and returns the same object"""
    mesh = grid_mesh(2, 2)
    assert colour_by_height(mesh) is mesh


# --- 4. deform_by_wave ------------------------------------------------------

def test_deform_moves_vertices_by_the_wave():
    """each vertex moves by amplitude * sin(2*pi*x / wavelength)"""
    mesh = grid_mesh(4, 1, spacing=1.0)
    before = {k: mesh.vertex_coordinates(k) for k in mesh.vertices()}
    deform_by_wave(mesh, amplitude=2.0, wavelength=4.0)
    for key, (x, y, z) in before.items():
        expected = z + 2.0 * math.sin(2 * math.pi * x / 4.0)
        assert approx(mesh.vertex_coordinates(key)[2], expected)


def test_deform_leaves_x_and_y_alone():
    """only z changes"""
    mesh = grid_mesh(3, 3)
    before = {k: mesh.vertex_coordinates(k)[:2] for k in mesh.vertices()}
    deform_by_wave(mesh, amplitude=1.0)
    for key, (x, y) in before.items():
        assert approx(mesh.vertex_coordinates(key)[0], x)
        assert approx(mesh.vertex_coordinates(key)[1], y)


def test_deform_does_not_change_the_topology():
    """same vertices, same edges, same faces -- only coordinates move"""
    # This is the whole reason a mesh is a mesh. You just moved every point in
    # the model and did not have to rebuild a single face.
    mesh = grid_mesh(4, 4)
    before = mesh_stats(mesh)
    faces_before = {f: tuple(mesh.face_vertices(f)) for f in mesh.faces()}
    deform_by_wave(mesh, amplitude=3.0)
    after = mesh_stats(mesh)
    for key in ("vertices", "edges", "faces", "euler", "boundary"):
        assert before[key] == after[key], f"deforming changed {key}"
    assert {f: tuple(mesh.face_vertices(f)) for f in mesh.faces()} == faces_before


def test_deform_returns_the_same_mesh():
    """deform_by_wave() modifies in place and returns the same object"""
    mesh = grid_mesh(2, 2)
    assert deform_by_wave(mesh) is mesh


# --- 5. tag_supports --------------------------------------------------------

def test_supports_are_exactly_the_boundary():
    """the returned keys are the boundary vertices, sorted, each once"""
    mesh = grid_mesh(4, 3)
    supports = tag_supports(mesh)
    expected = sorted(k for k in mesh.vertices() if mesh.is_vertex_on_boundary(k))
    assert len(supports) == len(set(supports)), (
        "a key appears twice -- vertices_on_boundary() is a closed cycle, "
        "so its first vertex repeats at the end"
    )
    assert supports == sorted(supports), "return the keys SORTED"
    assert supports == expected
    assert len(supports) == 2 * (4 + 3)


def test_supports_attribute_is_on_every_vertex():
    """every vertex has is_support set explicitly, True or False"""
    # Leaving it unset on interior vertices "works" because the default is
    # None and None is falsy -- until someone queries is_support=False and
    # gets nothing back. Set it everywhere.
    mesh = grid_mesh(3, 3)
    tag_supports(mesh)
    for key in mesh.vertices():
        value = mesh.vertex_attribute(key, "is_support")
        assert value is True or value is False, f"vertex {key}: is_support is {value!r}"
    assert len(list(mesh.vertices_where(is_support=False))) == 4


def test_supports_survive_deformation():
    """attributes stay with their vertices when the geometry moves"""
    mesh = grid_mesh(4, 2)
    before = tag_supports(mesh)
    deform_by_wave(mesh, amplitude=2.0)
    assert sorted(mesh.vertices_where(is_support=True)) == before


# --- 6. vertex_ring ---------------------------------------------------------

def _middle(mesh):
    xs = [mesh.vertex_coordinates(k)[0] for k in mesh.vertices()]
    ys = [mesh.vertex_coordinates(k)[1] for k in mesh.vertices()]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    return min(
        mesh.vertices(),
        key=lambda k: (mesh.vertex_coordinates(k)[0] - cx) ** 2
        + (mesh.vertex_coordinates(k)[1] - cy) ** 2,
    )


def test_ring_zero_is_just_the_vertex():
    """vertex_ring(mesh, key, 0) == {key}"""
    mesh = grid_mesh(4, 4)
    key = _middle(mesh)
    assert vertex_ring(mesh, key, 0) == {key}


def test_ring_one_is_the_vertex_and_its_neighbours():
    """k = 1 adds exactly the direct neighbours"""
    mesh = grid_mesh(4, 4)
    key = _middle(mesh)
    assert vertex_ring(mesh, key, 1) == {key} | set(mesh.vertex_neighbors(key))


def test_ring_grows_like_a_diamond():
    """on a grid, the middle vertex reaches 1, 5, 13, 25 vertices"""
    # On a quad grid, "k edges away" is the Manhattan distance -- so the ring
    # is a diamond, not a square. If you got 9 for k=1 you counted the
    # diagonal corners, which are two edges away, not one.
    mesh = grid_mesh(6, 6)
    key = _middle(mesh)
    assert [len(vertex_ring(mesh, key, k)) for k in range(4)] == [1, 5, 13, 25]


def test_ring_stops_at_the_boundary():
    """a corner vertex has fewer vertices to reach, and k too large is fine"""
    mesh = grid_mesh(3, 3)
    corner = next(k for k in mesh.vertices() if mesh.vertex_degree(k) == 2)
    assert len(vertex_ring(mesh, corner, 1)) == 3
    assert vertex_ring(mesh, corner, 50) == set(mesh.vertices())


def test_ring_rejects_negative_k():
    """a negative ring size is a mistake, not an empty set"""
    with pytest.raises(ValueError):
        vertex_ring(grid_mesh(2, 2), 0, -1)
