# Excercise 05

## 1. Mesh Coloring
Create a mesh and color it according to its normal direction.

### Hints
- load a mesh, e.g. the stanford bunny
- iterate over the vertices of the mesh, and get the normal direction of the vertex using the `mesh.vertex_normal` method
- use `try` and `except` to catch the `ValueError` exception when the vertex has no valid normal direction 

![](https://app.rccn.dev/assets/dccg/imgs/exercise_normal_color.png)
## 2. Mesh Modeling
Create a mesh and deform it using attractors. Color the mesh according to the distance to the attractors.

### Hints
- start with a sphere
- create a few points in space
- iterate over the vertices of the mesh, and move them according to the distance to the attractor points


![](https://app.rccn.dev/assets/dccg/imgs/exercise_deform_mesh.png)