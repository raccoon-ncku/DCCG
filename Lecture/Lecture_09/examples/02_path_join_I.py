# .json is a file format that is used to store
# data in a dictionary-like format.
# It is a text-based file format, 
# and it is the most common data format used for client/server communication.
# JSON is a language-independent data format.


import json
import os

dict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

# use os.path.join() to join the path
# This will work on any operating system
# E.g., Windows, Mac, Linux
output_path = os.path.join(
    os.path.dirname(__file__),
    'result.json'
)

# if not using os.path.join(), the path needs to be coded manually
# Windows: output_path = os.path.dirname(__file__) + '\\result.json'
# macOS/Linux Distributions: output_path = os.path.dirname(__file__) + '/result.json'

with open(output_path, 'w') as fp:
    # save the dictionary to the json file
    json.dump(dict, fp)
