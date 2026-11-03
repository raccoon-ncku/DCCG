"""A stud wall, as a class: a design you can ask questions, then ask for geometry."""

from compas.datastructures import Graph
from compas.geometry import Line


class StudWall:
    """A timber stud wall in the XZ plane: two plates and a stud every `spacing`.

    Parameters
    ----------
    length, height : float -- metres
    spacing : float        -- metres between studs. A stud always closes the
                              far end, so the last bay may be shorter.

    Raises
    ------
    ValueError -- if any of the three is not positive
    """

    def __init__(self, length, height, spacing=0.6):
        if length <= 0 or height <= 0 or spacing <= 0:
            raise ValueError(f"need positive dimensions, got {length}, {height}, {spacing}")
        self.length = length
        self.height = height
        self.spacing = spacing

    def __repr__(self):
        return f"StudWall({self.length} x {self.height} m, {self.n_studs} studs)"

    @property
    def stud_positions(self):
        """x of every stud, from 0 to `length`."""
        full_bays = int(self.length / self.spacing + 1e-9)
        xs = [i * self.spacing for i in range(full_bays + 1)]
        if self.length - xs[-1] > 1e-9:
            xs.append(self.length)
        return xs

    @property
    def n_studs(self):
        return len(self.stud_positions)

    def lines(self):
        """{name: Line}: `bottom_plate`, `top_plate`, `stud_0`, `stud_1`, ..."""
        lines = {
            "bottom_plate": Line([0, 0, 0], [self.length, 0, 0]),
            "top_plate": Line([0, 0, self.height], [self.length, 0, self.height]),
        }
        for i, x in enumerate(self.stud_positions):
            lines[f"stud_{i}"] = Line([x, 0, 0], [x, 0, self.height])
        return lines

    def graph(self):
        """The element graph: a node per member, an edge per joint (each stud to both plates)."""
        graph = Graph()
        for name, line in self.lines().items():
            x, y, z = line.midpoint
            graph.add_node(name, x=x, y=y, z=z)
        for i in range(self.n_studs):
            graph.add_edge(f"stud_{i}", "bottom_plate")
            graph.add_edge(f"stud_{i}", "top_plate")
        return graph
