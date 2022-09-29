"""
Dictionaries are used to store data values in key:value pairs.

A dictionary is a collection which is ordered*, changeable and do not allow duplicates.
"""
# Dictionaries are written with curly brackets, and have keys and values:
dict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

# Access an item's value
print(dict["brand"])

# Change an item value
dict["year"] = 2018
print(dict)

# Add an item
dict["aka"] = "Ford T5"
print(dict)

# Update a dictionary
more_info = {
    "layout": "FR",
    "year": 2022
}
dict.update(more_info)
print(dict)

# Iterate through a dictionary
for key in dict:
    print(key)

for key in dict.keys():
    print(key)

for key in dict:
    print(dict[key])

for value in dict.values():
    print(value)

for key, value in dict.items():
    print(key, value)