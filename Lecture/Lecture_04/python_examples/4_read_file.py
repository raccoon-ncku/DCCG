import json
import os

DIR_NAME = "data"
FILE_NAME = "output.json"


data_path = os.path.join(
    os.path.dirname(__file__),
    DIR_NAME,
    FILE_NAME
)

# Opening JSON file
with open(data_path, 'r') as fp:
    data = json.load(fp)

    # Print the type of data variable
    print("Type:", type(data))

    # Print the data of dictionary
    print("Brand:", data['brand'])
