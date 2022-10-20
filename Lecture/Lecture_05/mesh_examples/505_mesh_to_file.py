import compas.datastructures as cd
import pathlib

# Read a mesh file
filepath = pathlib.Path(__file__).parent / "data" / "Bunny.ply"
mesh = cd.Mesh.from_ply(filepath)

# Write as another file format
output_path = pathlib.Path(__file__).parent / "data" / "Bunny.stl"
mesh.to_stl(output_path)
