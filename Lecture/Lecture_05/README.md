# Week 09 — Mesh: a real geometric data structure

> In person again. We open with a **debrief and peer code review** of Weeks 07
> and 08 — bring your checkpoints, working or not. A stuck checkpoint you can
> describe precisely is more useful to the class than a green one you rushed.
>
> Then: `uv run check.py 09`.

## 1. Why a mesh is not a list of triangles

You could store a surface as a list of triangles, each with three points. It
would draw correctly and be useless for everything else, because it does not
know **which triangles touch**. Ask "what is next to this face?" or "is this
edge on the boundary?" and you would have to compare floating-point
coordinates — the one thing Week 02 told you never to do.

A **mesh** stores topology explicitly:

- **vertices** — points, each with an integer key
- **faces** — ordered lists of vertex keys
- **edges** — pairs of vertex keys, derived from the faces

Because faces refer to vertices *by key*, neighbours are found by looking up
keys, not by comparing positions. Move a vertex and every face using it follows
automatically. That single property is what makes subdivision, smoothing,
relaxation, and offsetting possible at all.

**And every vertex, edge and face carries a dictionary of attributes.** This is
where Week 04 pays off: a vertex is not just a point, it is a point with a
colour, a load, a material, a fabrication ID — whatever your problem needs.

## 2. Making a mesh

```python
from compas.datastructures import Mesh

mesh = Mesh()
a = mesh.add_vertex(x=0, y=0, z=0)     # returns an integer key
b = mesh.add_vertex(x=1, y=0, z=0)
c = mesh.add_vertex(x=1, y=1, z=0)
d = mesh.add_vertex(x=0, y=1, z=0)

f = mesh.add_face([a, b, c, d])        # vertex keys, in order around the face
```

> ⚠️ **Face vertex order defines the normal.** Counter-clockwise seen from the
> front gives an outward normal; reverse it and the face points the other way.
> Inconsistent ordering across a mesh causes normals that flip randomly, which
> breaks shading, offsetting, boolean operations and 3D printing — while
> looking almost fine on screen.

Ready-made constructors:

```python
Mesh.from_meshgrid(dx=10, nx=10, dy=5, ny=5)   # a flat grid
Mesh.from_polyhedron(6)                         # a cube
Mesh.from_obj(path)                             # from file
Mesh.from_shape(Box(1, 2, 3))
```

📄 `mesh_examples/501_mesh.py`, `502_mesh_from_scratch.py`, `503_mesh_constructor.py`

## 3. Getting around

```python
mesh.number_of_vertices()
mesh.number_of_edges()
mesh.number_of_faces()

for key in mesh.vertices():
    x, y, z = mesh.vertex_coordinates(key)

for fkey in mesh.faces():
    mesh.face_vertices(fkey)
    mesh.face_area(fkey)
    mesh.face_normal(fkey)
    mesh.face_centroid(fkey)

for u, v in mesh.edges():
    mesh.edge_length((u, v))
```

Topology queries — the part a list of triangles cannot do:

```python
mesh.vertex_neighbors(key)       # vertices connected to this one
mesh.vertex_faces(key)           # faces touching this vertex
mesh.face_neighbors(fkey)        # faces sharing an edge with this one
mesh.vertices_on_boundary()      # the open edge of the mesh
mesh.is_vertex_on_boundary(key)
```

📄 `mesh_examples/506_access_mesh_v_f_e.py`, `507_mesh_topology.py`,
`509_mesh_info_vertices_on_boundary.py`, `510_mesh_face_normal.py`

## 4. Attributes

```python
mesh.vertex_attribute(key, "color", [255, 0, 0])    # set one
mesh.vertex_attribute(key, "color")                  # read it back
mesh.vertex_attributes(key)                          # all of them, as a dict

mesh.update_default_vertex_attributes({"load": 0.0}) # a default for every vertex
mesh.face_attribute(fkey, "material", "timber")
```

This is how a geometric model becomes a *design* model. Colour by height,
store a panel ID per face, tag which vertices are supports — the mesh carries
your data alongside the geometry, and `compas.json_dump` saves both together.

📄 `mesh_examples/506-1_mesh_color.py`, `511_mesh_face_normal_pattern.py`

## 5. Euler's formula — a free correctness check

For any single connected surface:

```
V - E + F = 2 - 2g        (g = number of holes/handles)
```

A closed sphere-like mesh gives 2. A flat disc-like grid gives 1. **A mesh
whose Euler characteristic is unexpected has a topology bug** — a duplicated
vertex, a missing face, a hole you did not intend.

This is an unusually good test: it is one integer, it costs nothing, and it
catches a whole class of errors that look perfectly fine on screen.

```python
mesh.euler()
```

## 6. Operations

```python
mesh.subdivide(scheme="catmullclark", k=2)
mesh.smooth_area(fixed=mesh.vertices_on_boundary(), kmax=50)
mesh.flip_cycles()
mesh.unify_cycles()      # make all face normals consistent -- run it when unsure
```

📄 `mesh_examples/562_mesh_subdivision_scheme.py`, `557_conway_1.py` …
`559_conway_3.py`, `554_mesh_booleans.py`

Advanced material — remeshing, Delaunay triangulation, CGAL slicing, Catmull-
Clark — is in `mesh_examples_advanced/`. Not examined; very useful for final
projects, especially `556_compas_cgal_slicer.py` if you are heading toward
fabrication.

`mesh_applications/mesh_relaxation.py` and `mesh_pavilion.ipynb` are worked
examples of form-finding, and a strong starting point for a project.

## 7. Saving

```python
import compas
compas.json_dump(mesh, "output/mesh.json")   # geometry AND attributes
mesh = compas.json_load("output/mesh.json")

mesh.to_obj("mesh.obj")        # for other software
mesh.to_stl("mesh.stl")        # for 3D printing
```

The JSON artifact is the one that keeps your attributes. OBJ and STL throw them
away — they are export formats, not save formats.

---

## Checkpoints

```bash
uv run check.py 09
```

| # | Task | Exercises |
| - | ---- | --------- |
| 1 | `grid_mesh(nx, ny, spacing)` | building a mesh from scratch, vertex keys |
| 2 | `mesh_stats(mesh)` | topology queries, and Euler as a sanity check |
| 3 | `colour_by_height(mesh)` | attributes — data living on geometry |
| 4 | `deform_by_wave(mesh, ...)` | moving vertices while keeping topology intact |

Checkpoint 1 asks you to build the grid yourself rather than call
`Mesh.from_meshgrid`, precisely so you have to think about which vertex keys
form each face. Checkpoint 4 is the payoff: you change every coordinate in the
mesh and the topology is completely unaffected — which is the whole reason this
data structure exists.

## Exercise

📝 [Mesh colouring and deformation](/Exercise/Lecture_05/README.md)

## Due this week

📝 [A3 — Recursion](/Assignment/4_recursion/README.md)

## Self-test

1. Why can a mesh answer "which faces touch this one?" when a list of triangles cannot?
2. What does the order of vertices in a face determine?
3. A flat grid has `V - E + F == 1`. Yours gives 0. What kind of mistake is that?
4. Which file format keeps your vertex attributes: OBJ, STL, or COMPAS JSON?
5. You move every vertex of a mesh. How many faces do you have to rebuild?
