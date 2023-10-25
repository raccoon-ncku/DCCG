"""
Dictionaries are used to store data values in key:value pairs.
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