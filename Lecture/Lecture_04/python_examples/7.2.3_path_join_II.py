import json
import os

DIR1_NAME = "data"
DIR2_NAME = "output"
FILE_NAME = "output.json"

dict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

output_dir = os.path.join(
    os.path.dirname(__file__),
    DIR1_NAME,
    DIR2_NAME
)

# Create the directory if it is not currently existed
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

output_path = os.path.join(
    output_dir,
    FILE_NAME
)

with open(output_path, 'w') as fp:
    json.dump(dict, fp)
