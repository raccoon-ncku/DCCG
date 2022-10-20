import compas
import compas.geometry as cg
import compas.datastructures as cd


mesh = cd.Mesh.from_obj(compas.get('hypar.obj'))

# Tags
tags = []
for vertex_key in mesh.vertices():
    tags.append(
        str(mesh.vertex_degree(vertex_key))
    )
# Or a one-line code
# tags = [str(mesh.vertex_degree(vertex_key)) for vertex_key in mesh.vertices()]

# Vertex coordinates
coordinates = [cg.Point(*mesh.vertex_coordinates(vertex_key))
               for vertex_key in mesh.vertices()]

if compas.is_grasshopper():
    a = mesh
    b = tags
    c = coordinates
else:
    from compas_view2.app import App
    from compas_view2.shapes import Text
    viewer = App()

    viewer.add(mesh)
    for i, tag in enumerate(tags):
        viewer.add(
            Text(tag, coordinates[i])
        )
    viewer.run()
