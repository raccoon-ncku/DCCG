import compas.datastructures as cd
import pathlib

HERE = pathlib.Path(__file__).parent

# Read a mesh file
filepath = HERE.parent / "data" / "bunny.ply"
mesh = cd.Mesh.from_ply(filepath)

# Write as another file format (output/ is git-ignored)
output_path = HERE.parent / "output" / "bunny.stl"
output_path.parent.mkdir(exist_ok=True)
mesh.to_stl(output_path)
