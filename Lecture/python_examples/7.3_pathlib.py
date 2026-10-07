import pathlib

# pathlib provides an object-oriented interface for working with file system paths.

# Get the path of the current file
current_file = pathlib.Path(__file__)

# .parent gives the directory containing the file
current_dir = current_file.parent

# Simple path joining using the / operator
data_dir = current_dir / 'data' / 'output'
data_dir.mkdir(parents=True, exist_ok=True)

# Define the output file path
output_path = data_dir / 'result.json'
print(f"Output path: {output_path}")

# Write a sample dictionary to the JSON file
import json
sample_dict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

with open(output_path, 'w') as fp:
    json.dump(sample_dict, fp)

# Read back the JSON file to verify
with open(output_path, 'r') as fp:
    data = json.load(fp)
print(f"Read data: {data}")