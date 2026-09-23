"""
Week 09 checkpoints — the Mesh data structure.

Edit ONLY this file. Run from the repository root:

    uv run check.py 09

Still the core layer: no viewer, no files, no print.
"""

import math

from compas.datastructures import Mesh


def grid_mesh(nx, ny, spacing=1.0):
    """Build a flat rectangular grid mesh in the XY plane, from scratch.

    - `nx` and `ny` are the number of FACES along x and y
    - so there are (nx+1) * (ny+1) vertices
    - vertex (i, j) sits at (i*spacing, j*spacing, 0)
    - every face is a quad, wound counter-clockwise seen from +Z, so all the
      normals point up

    grid_mesh(2, 3) -> a mesh with 12 vertices and 6 faces

    Parameters
    ----------
    nx, ny : int   -- at least 1 each; otherwise raise ValueError
    spacing : float

    Returns
    -------
    compas.datastructures.Mesh

    Hints
    -----
    - Do NOT use Mesh.from_meshgrid. The point is to work out the vertex keys
      yourself -- that is the part that transfers to every other mesh you build.
    - Keep a dictionary mapping (i, j) -> vertex key as you add vertices, then
      look up the four corners of each face. Much easier than doing the
      index arithmetic in your head.
    - Counter-clockwise from above means, for the face whose lower-left corner
      is (i, j):  (i,j) -> (i+1,j) -> (i+1,j+1) -> (i,j+1)
    - Neighbouring faces must SHARE vertices, not each add their own. If they
      do not, the mesh looks perfect and its Euler characteristic is wrong.
    """
    raise NotImplementedError("grid_mesh")


def mesh_stats(mesh):
    """Return a summary dictionary describing a mesh.

    Keys, exactly these:
        "vertices"  : int   -- number of vertices
        "edges"     : int   -- number of edges
        "faces"     : int   -- number of faces
        "euler"     : int   -- V - E + F
        "boundary"  : int   -- number of DISTINCT vertices on the boundary
        "area"      : float -- total area of all faces

    A summary like this is the cheapest possible regression test: one call
    tells you whether a change to your generator altered the topology.

    Returns
    -------
    dict

    Watch out
    ---------
    `mesh.vertices_on_boundary()` returns the boundary as an ordered CYCLE,
    with the first vertex repeated at the end -- so `len()` of it is one more
    than the number of distinct vertices. Count with

        sum(mesh.is_vertex_on_boundary(k) for k in mesh.vertices())

    or take `len(set(...))`. This is a genuine trap in a real library, and it
    is exactly the kind of thing that "looks right" until something counts it.
    """
    raise NotImplementedError("mesh_stats")


def colour_by_height(mesh, low=(0, 0, 255), high=(255, 0, 0)):
    """Give every vertex a "color" attribute interpolated by its height.

    - the LOWEST vertex in the mesh gets exactly `low`
    - the HIGHEST gets exactly `high`
    - everything between is linearly interpolated on z
    - if the mesh is completely flat (all z equal), every vertex gets `low`
      -- there is no gradient to compute, and dividing by the zero range would
      crash

    Each colour is a tuple/list of three ints, 0-255.

    The mesh is modified IN PLACE (that is what a mesh is for) and also
    returned, so callers can chain.

    Returns
    -------
    compas.datastructures.Mesh -- the same object

    Hint: mesh.vertex_attribute(key, "color", value) sets it.
    """
    raise NotImplementedError("colour_by_height")


def deform_by_wave(mesh, amplitude=1.0, wavelength=4.0):
    """Push every vertex up or down by a sine wave along x, IN PLACE.

    New z for a vertex = its old z + amplitude * sin(2*pi*x / wavelength)

    The topology must be completely untouched: same vertex keys, same faces,
    same edges. Only the coordinates change. Demonstrating that to yourself is
    the point of this checkpoint.

    Returns
    -------
    compas.datastructures.Mesh -- the same object

    Hint: mesh.vertex_attribute(key, "z", new_value) moves a vertex. You do not
    need to touch a single face.
    """
    raise NotImplementedError("deform_by_wave")
