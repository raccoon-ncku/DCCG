"""Property tests for every algorithm in ../tutorials.

    uv run pytest Lecture/Algorithms/geometric/tests -v

Geometry is tested here the way Week 10 teaches: by PROPERTIES that must hold
whatever the exact numbers are -- counts, invariants, theorems, inequalities
-- never by comparing against a picture. Several of these are famous results
(Gauss-Bonnet, the Delaunay empty-circle property) used as free, exact
checks on code that would otherwise only be checked by eye.
"""

import math
import random

import pytest
from compas.datastructures import Mesh
from compas.geometry import Box, Sphere, Torus

import contouring
import curvature
import geodesics
import planarity
import smoothing
import subdivision
import voronoi


def grid(n=8, size=8.0):
    return Mesh.from_meshgrid(dx=size, nx=n)


def ball(u=24, v=16, r=1.0):
    return Mesh.from_shape(Sphere(radius=r), u=u, v=v)


def noisy(mesh, amount=0.05, seed=0):
    rnd = random.Random(seed)
    result = mesh.copy()
    for v in result.vertices():
        x, y, z = result.vertex_coordinates(v)
        result.vertex_attributes(v, "xyz", [x + rnd.uniform(-amount, amount),
                                            y + rnd.uniform(-amount, amount),
                                            z + rnd.uniform(-amount, amount)])
    return result


def mean_radius(mesh):
    return sum(math.dist(mesh.vertex_coordinates(v), (0, 0, 0)) for v in mesh.vertices()) / mesh.number_of_vertices()


# --- smoothing --------------------------------------------------------------

def test_smoothing_reduces_roughness():
    rough = noisy(ball())
    assert smoothing.roughness(smoothing.laplacian_smooth(rough, rounds=5)) < smoothing.roughness(rough)


def test_smoothing_keeps_fixed_vertices_and_topology():
    mesh = noisy(grid())
    fixed = [v for v in mesh.vertices() if mesh.is_vertex_on_boundary(v)]
    out = smoothing.laplacian_smooth(mesh, fixed=fixed, rounds=10)
    for v in fixed:
        assert out.vertex_coordinates(v) == pytest.approx(mesh.vertex_coordinates(v))
    assert out.euler() == mesh.euler()
    assert {f: out.face_vertices(f) for f in out.faces()} == {f: mesh.face_vertices(f) for f in mesh.faces()}


def test_smoothing_returns_a_copy():
    mesh = noisy(grid())
    before = [mesh.vertex_coordinates(v) for v in mesh.vertices()]
    smoothing.laplacian_smooth(mesh)
    assert [mesh.vertex_coordinates(v) for v in mesh.vertices()] == before


def test_laplacian_shrinks_and_taubin_does_not():
    rough = noisy(ball())
    r0 = mean_radius(rough)
    lap = mean_radius(smoothing.laplacian_smooth(rough, rounds=30))
    tau = mean_radius(smoothing.taubin_smooth(rough, rounds=30))
    assert lap < 0.95 * r0                      # Laplacian visibly shrinks
    assert abs(tau - r0) < abs(lap - r0) / 3    # Taubin stays much closer


def test_taubin_rejects_bad_parameters():
    with pytest.raises(ValueError):
        smoothing.taubin_smooth(grid(), lam=0.5, mu=-0.4)


# --- curvature --------------------------------------------------------------

@pytest.mark.parametrize("mesh, euler", [
    (Mesh.from_shape(Box(1, 2, 3)), 2),
    (ball(), 2),
    (Mesh.from_shape(Torus(radius_axis=2.0, radius_pipe=0.7), u=24, v=12), 0),
])
def test_gauss_bonnet_on_closed_meshes(mesh, euler):
    """sum of angle defects == 2 pi * euler, for any closed mesh"""
    assert mesh.euler() == euler
    assert curvature.total_curvature(mesh) == pytest.approx(2 * math.pi * euler, abs=1e-6)


def test_gauss_bonnet_on_an_open_mesh():
    """with boundary terms included, the theorem holds for a disc too"""
    mesh = hypar()
    mesh.quads_to_triangles()
    assert curvature.total_curvature(mesh) == pytest.approx(2 * math.pi * mesh.euler(), abs=1e-6)


def test_flat_interior_has_zero_curvature():
    mesh = grid()
    for v in mesh.vertices():
        if not mesh.is_vertex_on_boundary(v):
            assert curvature.angle_defect(mesh, v) == pytest.approx(0.0, abs=1e-9)


def hypar(n=8, size=8.0):
    """A hyperbolic paraboloid, meshed along its straight rulings."""
    mesh = grid(n, size)
    for v in mesh.vertices():
        x, y, _ = mesh.vertex_coordinates(v)
        mesh.vertex_attribute(v, "z", 0.1 * (x - size / 2) * (y - size / 2))
    return mesh


def test_sphere_curvature_is_positive():
    assert all(k > 0 for k in curvature.gaussian_curvature(ball()).values())


def test_saddle_curvature_is_negative_once_triangulated():
    """non-planar quads hide curvature from the angle defect -- triangles do not"""
    # A hypar meshed along its rulings: every quad is twisted, yet the face
    # angles around each vertex still add up to exactly 2 pi. The angle
    # defect is only meaningful for PLANAR faces. Triangulate, and the
    # negative curvature appears at every interior vertex.
    quads = hypar()
    interior = [v for v in quads.vertices() if not quads.is_vertex_on_boundary(v)]
    assert all(curvature.angle_defect(quads, v) == pytest.approx(0.0, abs=1e-9) for v in interior)
    tris = hypar()
    tris.quads_to_triangles()
    assert all(curvature.angle_defect(tris, v) < 0 for v in interior)


def test_sphere_curvature_is_about_one_over_r_squared():
    r = 2.0
    ks = list(curvature.gaussian_curvature(ball(48, 32, r)).values())
    assert sum(ks) / len(ks) == pytest.approx(1 / r ** 2, rel=0.05)


# --- geodesics --------------------------------------------------------------

def test_edge_distance_is_never_shorter_than_a_straight_line():
    mesh = grid()
    src = 0
    for v, d in geodesics.edge_distances(mesh, src).items():
        assert d >= math.dist(mesh.vertex_coordinates(src), mesh.vertex_coordinates(v)) - 1e-9


def test_edge_distance_on_a_grid_is_taxicab():
    """on a quad grid, Dijkstra on edges reports |dx| + |dy| -- not Euclidean"""
    mesh = grid()
    d = geodesics.edge_distances(mesh, 0)
    x0, y0, _ = mesh.vertex_coordinates(0)
    for v, dv in d.items():
        x, y, _ = mesh.vertex_coordinates(v)
        assert dv == pytest.approx(abs(x - x0) + abs(y - y0))


def test_heat_method_is_closer_to_the_truth_on_a_flat_mesh():
    mesh = grid(16, 8.0)
    mesh.quads_to_triangles()
    src = next(v for v in mesh.vertices() if mesh.vertex_coordinates(v)[:2] == pytest.approx([4.0, 4.0]))
    true = {v: math.dist(mesh.vertex_coordinates(src), mesh.vertex_coordinates(v)) for v in mesh.vertices()}
    edge = geodesics.edge_distances(mesh, src)
    heat = geodesics.heat_distances(mesh, src)
    err_edge = sum(abs(edge[v] - true[v]) for v in true) / len(true)
    err_heat = sum(abs(heat[v] - true[v]) for v in true) / len(true)
    assert err_heat < err_edge


def test_edge_distance_rejects_unknown_source():
    with pytest.raises(ValueError):
        geodesics.edge_distances(grid(), 10_000)


# --- subdivision ------------------------------------------------------------

@pytest.mark.parametrize("mesh", [Mesh.from_polyhedron(6), grid(3), Mesh.from_polyhedron(20)])
def test_catmull_clark_counts_and_topology(mesh):
    out = subdivision.catmull_clark(mesh)
    V, E, F = mesh.number_of_vertices(), mesh.number_of_edges(), mesh.number_of_faces()
    assert out.number_of_vertices() == V + E + F
    assert out.number_of_faces() == sum(len(mesh.face_vertices(f)) for f in mesh.faces())
    assert all(len(out.face_vertices(f)) == 4 for f in out.faces())
    assert out.euler() == mesh.euler()


def test_catmull_clark_agrees_with_compas_on_a_closed_mesh():
    cube = Mesh.from_polyhedron(6)
    ours = sorted(tuple(round(c, 9) for c in subdivision.catmull_clark(cube).vertex_coordinates(v))
                  for v in subdivision.catmull_clark(cube).vertices())
    ref = cube.subdivided("catmullclark", k=1)
    theirs = sorted(tuple(round(c, 9) for c in ref.vertex_coordinates(v)) for v in ref.vertices())
    assert ours == theirs


def test_catmull_clark_shrinks_into_the_hull():
    cube = Mesh.from_polyhedron(6)
    r = max(abs(c) for v in cube.vertices() for c in cube.vertex_coordinates(v))
    out = subdivision.catmull_clark(subdivision.catmull_clark(cube))
    assert max(abs(c) for v in out.vertices() for c in out.vertex_coordinates(v)) <= r + 1e-9


# --- planarity --------------------------------------------------------------

def dome(n=8, size=8.0, radius=7.0):
    mesh = grid(n, size)
    for v in mesh.vertices():
        x, y, _ = mesh.vertex_coordinates(v)
        r2 = (x - size / 2) ** 2 + (y - size / 2) ** 2
        mesh.vertex_attribute(v, "z", math.sqrt(radius ** 2 - r2) - math.sqrt(radius ** 2 - 2 * (size / 2) ** 2))
    return mesh


def test_flatness_is_zero_for_flat_quads_and_triangles():
    mesh = grid()
    assert all(planarity.flatness(mesh, f) == pytest.approx(0.0, abs=1e-12) for f in mesh.faces())
    mesh.quads_to_triangles()
    assert all(planarity.flatness(mesh, f) == 0.0 for f in mesh.faces())


def test_a_curved_dome_has_twisted_panels():
    """the reason planarize() exists: a dome on a square grid is not flat-panelled"""
    mesh = dome()
    assert all(planarity.flatness(mesh, f) >= 0 for f in mesh.faces())
    assert max(planarity.flatness(mesh, f) for f in mesh.faces()) > 0.01


def test_planarize_makes_panels_flatter():
    mesh = dome()
    before = max(planarity.flatness(mesh, f) for f in mesh.faces())
    after_mesh = planarity.planarize(mesh, rounds=100)
    after = max(planarity.flatness(after_mesh, f) for f in after_mesh.faces())
    assert after < before / 10
    assert after_mesh.euler() == mesh.euler()


def test_planarize_respects_fixed_vertices():
    mesh = dome()
    fixed = [v for v in mesh.vertices() if mesh.is_vertex_on_boundary(v)]
    out = planarity.planarize(mesh, fixed=fixed, rounds=20)
    for v in fixed:
        assert out.vertex_coordinates(v) == pytest.approx(mesh.vertex_coordinates(v))


def test_flatness_rejects_pentagons():
    mesh = Mesh.from_polyhedron(12)
    with pytest.raises(ValueError):
        planarity.flatness(mesh, next(iter(mesh.faces())))


# --- contouring -------------------------------------------------------------

def test_contour_points_lie_at_the_height():
    mesh = ball()
    mesh.quads_to_triangles()
    for h in (-0.5, 0.013, 0.7):
        for line in contouring.contours(mesh, h):
            assert all(p[2] == pytest.approx(h) for p in line)


def test_a_sphere_cut_through_the_middle_gives_one_closed_loop():
    mesh = ball()
    mesh.quads_to_triangles()
    lines = contouring.contours(mesh, 0.013)
    assert len(lines) == 1
    assert lines[0][0] == pytest.approx(lines[0][-1])          # closed
    length = sum(math.dist(a, b) for a, b in zip(lines[0], lines[0][1:]))
    assert length == pytest.approx(2 * math.pi, rel=0.02)      # about the circumference


def test_an_open_surface_gives_open_contours():
    mesh = grid()
    for v in mesh.vertices():
        x, y, _ = mesh.vertex_coordinates(v)
        mesh.vertex_attribute(v, "z", 0.3 * x)
    mesh.quads_to_triangles()
    lines = contouring.contours(mesh, 1.05)
    assert len(lines) == 1
    assert lines[0][0] != pytest.approx(lines[0][-1])
    assert all(p[0] == pytest.approx(3.5) for p in lines[0])   # z = 0.3 x = 1.05


def test_two_bumps_give_two_loops():
    mesh = grid(24, 12.0)
    for v in mesh.vertices():
        x, y, _ = mesh.vertex_coordinates(v)
        z = math.exp(-((x - 3.5) ** 2 + (y - 6) ** 2)) + math.exp(-((x - 8.5) ** 2 + (y - 6) ** 2))
        mesh.vertex_attribute(v, "z", z)
    mesh.quads_to_triangles()
    assert len(contouring.contours(mesh, 0.5)) == 2


def test_contours_require_triangles():
    with pytest.raises(ValueError):
        contouring.contours(grid(), 0.5)


# --- Delaunay / Voronoi -----------------------------------------------------

def scatter(n=60, seed=3):
    rnd = random.Random(seed)
    return [[rnd.uniform(0, 10), rnd.uniform(0, 6), 0] for _ in range(n)]


def test_delaunay_has_the_empty_circle_property():
    pts = scatter()
    mesh = voronoi.delaunay(pts)
    for f in mesh.faces():
        tri = [mesh.vertex_coordinates(v) for v in mesh.face_vertices(f)]
        c = voronoi.circumcentre(*tri)
        r = math.dist(c, tri[0])
        for p in pts:
            assert math.dist(c, [p[0], p[1], 0]) >= r - 1e-9


def test_circumcentre_is_equidistant():
    a, b, c = [0, 0, 0], [4, 0, 0], [1, 3, 0]
    o = voronoi.circumcentre(a, b, c)
    assert math.dist(o, a) == pytest.approx(math.dist(o, b))
    assert math.dist(o, a) == pytest.approx(math.dist(o, c))


def test_voronoi_cell_points_are_closer_to_their_site():
    """every corner of a cell is at least as close to its site as to any other point"""
    pts = scatter()
    mesh = voronoi.delaunay(pts)
    for v, cell in voronoi.voronoi_cells(mesh).items():
        site = mesh.vertex_coordinates(v)
        for corner in cell:
            mine = math.dist(corner, site)
            assert all(mine <= math.dist(corner, [p[0], p[1], 0]) + 1e-9 for p in pts)


def test_voronoi_has_a_cell_per_interior_point():
    mesh = voronoi.delaunay(scatter())
    cells = voronoi.voronoi_cells(mesh)
    assert len(cells) == sum(not mesh.is_vertex_on_boundary(v) for v in mesh.vertices())


def test_collinear_points_have_no_circumcentre():
    with pytest.raises(ValueError):
        voronoi.circumcentre([0, 0, 0], [1, 1, 0], [2, 2, 0])


# --- convex hull ------------------------------------------------------------

import convex_hull  # noqa: E402
import lloyd  # noqa: E402
import nearest  # noqa: E402


def test_hull_contains_every_point():
    pts = scatter(200, seed=5)
    hull = convex_hull.convex_hull(pts)
    for p in pts:                                    # left of (or on) every hull edge
        for a, b in zip(hull, hull[1:] + hull[:1]):
            assert convex_hull.cross(a, b, p) >= -1e-9


def test_hull_is_counter_clockwise_and_convex():
    hull = convex_hull.convex_hull(scatter(80, seed=2))
    assert convex_hull.area(hull) > 0
    n = len(hull)
    assert all(convex_hull.cross(hull[i], hull[(i + 1) % n], hull[(i + 2) % n]) > 0 for i in range(n))


def test_hull_of_a_square_with_points_inside_is_the_square():
    pts = [[0, 0, 0], [4, 0, 0], [4, 4, 0], [0, 4, 0], [2, 2, 0], [1, 3, 0], [2, 0, 0]]
    hull = convex_hull.convex_hull(pts)
    assert sorted(map(tuple, hull)) == sorted([(0, 0, 0), (4, 0, 0), (4, 4, 0), (0, 4, 0)])
    assert convex_hull.area(hull) == pytest.approx(16.0)


def test_hull_agrees_with_compas():
    from compas.geometry import convex_hull_xy
    pts = scatter(150, seed=9)
    assert len(convex_hull.convex_hull(pts)) == len(convex_hull_xy(pts))


def test_hull_rejects_collinear_points():
    with pytest.raises(ValueError):
        convex_hull.convex_hull([[0, 0, 0], [1, 1, 0], [2, 2, 0]])


# --- nearest neighbours -----------------------------------------------------

def test_spatial_hash_gives_the_brute_force_answer():
    pts = scatter(300, seed=4)
    assert nearest.all_pairs_hashed(pts, 0.8) == nearest.all_pairs_brute(pts, 0.8)


def test_spatial_hash_handles_negative_coordinates_and_cell_edges():
    pts = [[-1.0, -1.0, 0], [-0.5, -1.0, 0], [0.0, 0.0, 0], [0.5, 0.0, 0], [1.0, 0.0, 0]]
    for r in (0.5, 0.75, 1.0):
        assert nearest.all_pairs_hashed(pts, r) == nearest.all_pairs_brute(pts, r)


def test_spatial_hash_refuses_a_radius_it_cannot_answer():
    grid = nearest.SpatialHash(scatter(20), 0.5)
    with pytest.raises(ValueError):
        grid.within(0, 1.0)


# --- Lloyd relaxation -------------------------------------------------------

def test_lloyd_energy_never_increases():
    rnd = random.Random(1)
    sites = [(rnd.uniform(0, 10), rnd.uniform(0, 6)) for _ in range(25)]
    _, history = lloyd.lloyd(sites, lloyd.samples(10, 6, 40), rounds=15)
    assert all(b <= a + 1e-9 for a, b in zip(history, history[1:]))
    assert history[-1] < history[0]


def test_lloyd_evens_out_spacing():
    rnd = random.Random(3)
    sites = [(rnd.uniform(0, 10), rnd.uniform(0, 6)) for _ in range(30)]
    after, _ = lloyd.lloyd(sites, lloyd.samples(10, 6, 40), rounds=25)
    sb, sa = lloyd.nearest_spacing(sites), lloyd.nearest_spacing(after)
    assert min(sa) > min(sb)                                   # no more near-collisions
    spread = lambda xs: (sum((x - sum(xs) / len(xs)) ** 2 for x in xs) / len(xs)) ** 0.5  # noqa: E731
    assert spread(sa) < spread(sb)


def test_lloyd_keeps_sites_on_the_site():
    rnd = random.Random(8)
    sites = [(rnd.uniform(0, 10), rnd.uniform(0, 6)) for _ in range(12)]
    after, _ = lloyd.lloyd(sites, lloyd.samples(10, 6, 30), rounds=10)
    assert all(0 <= x <= 10 and 0 <= y <= 6 for x, y in after)
