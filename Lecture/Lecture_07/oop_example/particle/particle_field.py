import random
from compas_view2.app import App
import compas
import compas.geometry as cg
import compas.datastructures as cd
import pathlib
from particle import Particle

FRAMERATE = 5
MAX_FRAME = 60
PARTICLE_COUNT = 40

viewer = App()

input_path = pathlib.Path(__file__).parent / "mesh.stl"
mesh = cd.Mesh.from_stl(input_path)

mesh_vertex_coordinates = []
mesh_vertex_keys = []

for vk in mesh.vertices():
    mesh_vertex_keys.append(vk)
    mesh_vertex_coordinates.append(mesh.vertex_attributes(vk, 'xyz'))

bbox = cg.bounding_box(mesh_vertex_coordinates)
bbox = cg.Box.from_bounding_box(bbox)

model_objs = []
for _ in range(PARTICLE_COUNT):
    init_position = (
        bbox.xmin + random.random() * bbox.width,
        bbox.ymin + random.random() * bbox.depth,
        bbox.zmax + bbox.height * 0.2
    )
    particle = Particle(init_position, init_velocity=(0, 0, -1))
    viewer_obj = viewer.add(particle.get_body())
    model_objs.append(
        {
            "obj": particle,
            "viewer_obj": viewer_obj
        }
    )


@viewer.on(interval=1000 / FRAMERATE, frames=MAX_FRAME)
def update(f):
    for obj in model_objs:
        obj["obj"].glide_on_mesh(
            mesh, mesh_vertex_coordinates, mesh_vertex_keys)
        obj["obj"].update()
        obj["viewer_obj"]._data = obj["obj"].get_body()
        obj["viewer_obj"].update()

        # Draw Path
        viewer.add(cg.Line(obj["obj"].position_history[-1],
                   obj["obj"].position_history[-2]))


viewer.add(mesh)
viewer.show()
