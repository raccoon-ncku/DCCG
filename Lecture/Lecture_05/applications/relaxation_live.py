"""Surface relaxation animation using COMPAS and ``compas_viewer``.

The clip highlights the core idea of mesh form-finding: keep the boundary of a
surface fixed, move the interior vertices to the average of their neighbours,
and inject a small vertical load so the sheet settles into a smooth shape. A
noisy starting mesh is shown to the left, while the copy on the right relaxes
live inside the viewer.
"""

import random

from compas.datastructures import Mesh
from compas.geometry import Translation
from compas_viewer import Viewer


def make_noisy_grid(rows=12, cols=18, spacing=1.0, amplitude=0.6):
    """Create a quad mesh grid and add random interior noise for variation."""

    vertices = []
    faces = []

    for i in range(rows):
        for j in range(cols):
            x = j * spacing
            y = i * spacing
            on_boundary = i in (0, rows - 1) or j in (0, cols - 1)

            # Keep the boundary vertices flat so they can act as anchors.
            if on_boundary:
                z = 0.0
            else:
                z = random.uniform(-amplitude, amplitude)

            vertices.append([x, y, z])

            if i < rows - 1 and j < cols - 1:
                a = i * cols + j
                b = a + 1
                c = a + cols + 1
                d = a + cols
                faces.append([a, b, c, d])

    return Mesh.from_vertices_and_faces(vertices, faces)


def relax_iteration(mesh, fixed, *, smoothing=0.6, load=-0.015):
    """Apply one Laplacian smoothing step with a constant downward load."""

    updates = {}

    for vertex in mesh.vertices():
        if vertex in fixed:
            continue

        nbrs = list(mesh.vertex_neighbors(vertex))
        if not nbrs:
            continue

        cx = cy = cz = 0.0
        for nbr in nbrs:
            nx, ny, nz = mesh.vertex_coordinates(nbr)
            cx += nx
            cy += ny
            cz += nz

        count = float(len(nbrs))
        ax = cx / count
        ay = cy / count
        az = cz / count

        px, py, pz = mesh.vertex_coordinates(vertex)
        updates[vertex] = (
            px + smoothing * (ax - px),
            py + smoothing * (ay - py),
            pz + smoothing * (az - pz) + load,
        )

    for vertex, xyz in updates.items():
        mesh.vertex_attributes(vertex, "xyz", xyz)


# --- Mesh setup -----------------------------------------------------------

random.seed(7)

base_mesh = make_noisy_grid()
relaxing_mesh = base_mesh.copy()
fixed_vertices = set(relaxing_mesh.vertices_on_boundary())

original_mesh = base_mesh.copy()
original_mesh.transform(Translation.from_vector([-25, 0, 0]))


# --- Viewer & scene objects -----------------------------------------------

viewer = Viewer()
viewer.scene.add(original_mesh, name="start", color=(0.5, 0.7, 1.0), opacity=0.5)
relaxing_obj = viewer.scene.add(relaxing_mesh, name="relaxing", color=(1.0, 0.2, 0.2))


# --- Animation loop -------------------------------------------------------

max_frames = 160
frame_state = {"count": 0}


@viewer.on(interval=50)
def animate(frame):
    if frame_state["count"] >= max_frames:
        return

    relax_iteration(relaxing_mesh, fixed_vertices)
    relaxing_obj.update(update_data=True)
    frame_state["count"] += 1


viewer.show()

