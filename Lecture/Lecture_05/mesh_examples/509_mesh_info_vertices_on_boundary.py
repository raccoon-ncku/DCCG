import compas
import compas.geometry as cg
import compas.datastructures as cd


mesh = cd.Mesh.from_obj(compas.get('hypar.obj'))

geometries = [mesh]

for vertex_key in mesh.vertices_on_boundary():
    geometries.append(cg.Point(*mesh.vertex_coordinates(vertex_key)))

if compas.is_grasshopper():
    a = mesh
else:
    from compas_view2.app import App
    viewer = App()
    for geometry in geometries:
        viewer.add(geometry)
    viewer.run()
