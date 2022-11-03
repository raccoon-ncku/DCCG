import os
import numpy as np
import compas.geometry as cg
import compas.datastructures as cd
import compas_vol.primitives as cvol_p
import compas_vol.combinations as cvol_c
import compas_vol.modifications as cvol_m
import compas_vol.microstructures as cvol_ms
from compas_view2.app import App
from skimage.measure import marching_cubes
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# Modeling
# CSG tree
# VM object
s = cg.Sphere(cg.Point(5, 6, 0), 9)
b = cg.Box(cg.Frame.worldXY(), 20, 15, 10)
vs = cvol_p.VolSphere(s)
vb = cvol_p.VolBox(b, 0)
vm = cvol_c.SmoothUnion(vs, vb, 4.0)


# lower and upper bounds
LBX, UBX = -20.0, 20.0
LBY, UBY = -20.0, 20.0
LBZ, UBZ = -20.0, 20.0
# resolution(s)
NX, NY, NZ = 160, 160, 160

# workspace initialization
x, y, z = np.ogrid[LBX:UBX:NX*1j, LBY:UBY:NY*1j, LBZ:UBZ:NZ*1j]
# voxel dimensions
GX = (UBX-LBX)/NX
GY = (UBY-LBY)/NY
GZ = (UBZ-LBZ)/NZ

# sampling
sdf = vm.get_distance_numpy(x, y, z)
print(type(sdf), sdf.shape)

# generate isosurface
v, f, n, l = marching_cubes(sdf, 0, spacing=(GX, GY, GZ))

mesh = cd.Mesh.from_vertices_and_faces(v, f)
T = cg.Translation.from_vector(-cg.Vector(*mesh.centroid()))
mesh.transform(T)

fp = os.path.join(os.path.dirname(__file__), "output.stl")
with open(fp, "wb") as f:
    mesh.to_stl(f, binary=True)

viewer = App()
viewer.add(mesh)
viewer.run()

# Define initial parameters
INIT_Z = 0

# Create the figure and the image that we will manipulate
fig, ax = plt.subplots()
img = ax.imshow(sdf[:, :, INIT_Z].T, cmap='RdBu',
                vmin=-1, vmax=1, origin='lower')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')

# adjust the main plot to make room for the sliders
fig.subplots_adjust(left=0.25, bottom=0.25)

# Make a vertically oriented slider to control the Z value
z_ax = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
z_slider = Slider(
    ax=z_ax,
    label="Z value",
    valmin=0,
    valmax=z.shape[2] - 1,
    valfmt='%0.0f',
    valinit=INIT_Z,
    orientation="vertical"
)


# The function to be called anytime a slider's value changes
def update(val):
    img.set_data(sdf[:, :, int(val)].T)
    fig.canvas.draw_idle()


# register the update function with each slider
z_slider.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
reset_ax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
reset_button = Button(reset_ax, 'Reset', hovercolor='0.975')


def reset(event):
    z_slider.reset()


reset_button.on_clicked(reset)
plt.colorbar(img, ax=ax)
plt.show()
