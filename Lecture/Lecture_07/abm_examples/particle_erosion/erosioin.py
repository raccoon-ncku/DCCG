import random
from compas_view2.app import App
from compas_cgal.subdivision import catmull_clark
import compas.geometry as cg
import compas.datastructures as cd
from particle import Particle
import pathlib

ITERATION = 10
FRAMERATE = 5
MAX_FRAME = 120
PARTICLE_COUNT = 30

input_path = pathlib.Path(__file__).parent / "mesh.stl"
mesh = cd.Mesh.from_stl(input_path)


mesh_vertex_coordinates = []
mesh_vertex_keys = []
mesh_vertex_coordinates, mesh_faces = mesh.to_vertices_and_faces()
mesh_vertex_keys = list(mesh.vertices())

bbox = cg.bounding_box(mesh_vertex_coordinates)
bbox = cg.Box.from_bounding_box(bbox)

for i in range(ITERATION):
    particles = []
    for _ in range(PARTICLE_COUNT):
        init_position = (
            bbox.xmin + random.random() * bbox.width,
            bbox.ymin + random.random() * bbox.depth,
            bbox.zmax + bbox.height * 0.01
        )
        particles.append(Particle(init_position, init_velocity=(0, 0, -1)))

    for i in range(MAX_FRAME):
        for particle in particles:
            particle.glide_on_mesh(
                mesh, mesh_vertex_coordinates, mesh_vertex_keys)
            particle.update()

VF = catmull_clark((mesh_vertex_coordinates, mesh_faces), 2)
new_mesh = cd.Mesh.from_vertices_and_faces(*VF)
viewer = App()
viewer.add(new_mesh)
viewer.show()


path = pathlib.Path(__file__).parent / "erosion.stl"
new_mesh.quads_to_triangles()
new_mesh.to_stl(path)
