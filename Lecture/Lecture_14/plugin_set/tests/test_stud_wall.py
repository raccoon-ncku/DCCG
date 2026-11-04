"""Executable spec for StudWall. Each test is one sentence of the brief."""

import pytest

from compas_studio import StudWall


def test_a_stud_closes_both_ends():
    xs = StudWall(3.0, 2.4, spacing=0.7).stud_positions
    assert xs[0] == pytest.approx(0.0)
    assert xs[-1] == pytest.approx(3.0)


def test_no_bay_is_wider_than_the_spacing():
    xs = StudWall(3.0, 2.4, spacing=0.7).stud_positions
    assert all(b - a <= 0.7 + 1e-9 for a, b in zip(xs, xs[1:]))


def test_an_exact_fit_adds_no_extra_stud():
    assert StudWall(3.6, 2.4, spacing=0.6).n_studs == 7


def test_every_stud_runs_from_floor_to_top_plate():
    for name, line in StudWall(3.0, 2.4).lines().items():
        if name.startswith("stud"):
            assert line.start.z == pytest.approx(0.0)
            assert line.end.z == pytest.approx(2.4)


def test_the_plates_span_the_whole_wall():
    lines = StudWall(3.0, 2.4).lines()
    assert lines["bottom_plate"].length == pytest.approx(3.0)
    assert lines["top_plate"].length == pytest.approx(3.0)


def test_derived_values_follow_a_change():
    wall = StudWall(3.6, 2.4, spacing=0.6)
    wall.spacing = 1.2
    assert wall.n_studs == 4


def test_the_graph_has_a_node_per_member_and_two_edges_per_stud():
    wall = StudWall(3.6, 2.4, spacing=0.6)
    graph = wall.graph()
    assert graph.number_of_nodes() == wall.n_studs + 2
    assert graph.number_of_edges() == 2 * wall.n_studs


def test_the_graph_is_one_piece_with_the_plates_as_hubs():
    wall = StudWall(3.6, 2.4, spacing=0.6)
    graph = wall.graph()
    assert graph.is_connected()
    assert graph.degree("top_plate") == wall.n_studs
    assert graph.degree("stud_0") == 2


def test_repr_says_what_it_is():
    assert repr(StudWall(3.6, 2.4)) == "StudWall(3.6 x 2.4 m, 7 studs)"


@pytest.mark.parametrize("length, height, spacing", [(0, 2.4, 0.6), (3, 0, 0.6), (3, 2.4, 0), (-1, 2.4, 0.6)])
def test_rejects_nonsense_input(length, height, spacing):
    with pytest.raises(ValueError):
        StudWall(length, height, spacing)
