import json

dict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

with open('result.json', 'w') as fp:
    json.dump(dict, fp)
