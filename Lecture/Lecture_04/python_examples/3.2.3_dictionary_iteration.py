dict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}
print(dict)
# Iterate through a dictionary

# To get keys
print("\n---To get Keys---")
for key in dict:
    print(key, end=' ')
print()

for key in dict.keys():
    print(key, end=' ')
print()

print("\n---To get values---")
# To get values
for key in dict:
    print(dict[key], end=' ')
print()

for value in dict.values():
    print(value, end=' ')
print()

print("\n---To get key and values---")
for key, value in dict.items():
    print(key, value, end=', ')
print()