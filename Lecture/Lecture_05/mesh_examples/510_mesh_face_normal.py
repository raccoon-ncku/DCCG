import compas
import compas.geometry as cg
import compas.datastructures as cd
from compas_view2.app import App


mesh = cd.Mesh.from_obj(compas.get('hypar.obj'))

viewer = App()
for fkey in mesh.faces():
    cen = mesh.face_centroid(fkey)
    frame = cg.Frame.from_plane(mesh.face_plane(fkey))
    box = cg.Box(frame, 0.5, 0.5, 0.5)
    viewer.add(box)
viewer.run()
