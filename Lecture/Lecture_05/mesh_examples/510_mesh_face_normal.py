import compas
import compas.geometry as cg
import compas.datastructures as cd
from compas_viewer import Viewer


mesh = cd.Mesh.from_obj(compas.get('hypar.obj'))

viewer = Viewer()
for fkey in mesh.faces():
    cen = mesh.face_centroid(fkey)
    frame = cg.Frame.from_plane(mesh.face_plane(fkey))
    box = cg.Box(0.5, 0.5, 0.5, frame)
    viewer.scene.add(box)
viewer.show()
