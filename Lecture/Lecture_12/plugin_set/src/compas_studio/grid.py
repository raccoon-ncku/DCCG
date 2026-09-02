"""A flat quad grid mesh, as a pure geometry function."""

from compas.datastructures import Mesh


def grid_mesh(nx, ny, spacing=1.0):
    """Build a flat rectangular quad-mesh in the XY plane.

    Parameters
    ----------
    nx, ny : int    -- number of faces along x and y (at least 1 each)
    spacing : float -- distance between vertices, m

    Returns
    -------
    compas.datastructures.Mesh -- (nx+1)*(ny+1) vertices, nx*ny quad faces,
    every face wound counter-clockwise so all normals point up

    Raises
    ------
    ValueError -- if nx < 1, ny < 1, or spacing <= 0
    """
    if nx < 1 or ny < 1:
        raise ValueError("a grid needs at least one face in each direction")
    if spacing <= 0:
        raise ValueError("spacing must be positive")

    mesh = Mesh()
    keys = {}
    for j in range(ny + 1):
        for i in range(nx + 1):
            keys[(i, j)] = mesh.add_vertex(x=i * spacing, y=j * spacing, z=0)
    for j in range(ny):
        for i in range(nx):
            mesh.add_face(
                [keys[(i, j)], keys[(i + 1, j)], keys[(i + 1, j + 1)], keys[(i, j + 1)]]
            )
    return mesh
