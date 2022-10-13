import json
import os

dict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

output_path = os.path.join(
    os.path.dirname(__file__),
    'result.json'
)

with open(output_path, 'w') as fp:
    json.dump(dict, fp)
