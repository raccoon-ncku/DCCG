import compas
import compas.datastructures as cd

mesh = cd.Mesh.from_obj(compas.get('hypar.obj'))

# Visualization
if compas.is_grasshopper():
    a = mesh
else:
    from compas_view2.app import App
    viewer = App()
    viewer.add(mesh)
    viewer.run()
