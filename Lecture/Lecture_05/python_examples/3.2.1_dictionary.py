"""
Dictionaries — indexed by a key you choose, not by position.
"""

# Curly brackets, `key: value` pairs. Keys are usually strings; values are anything.
room = {
    "name":  "studio",
    "area":  45.0,
    "floor": 2,
}


# --- read a value --------------------------------------------------------

print(room["name"])              # 'studio' — crashes with KeyError if missing


# --- change / add / remove -----------------------------------------------

room["area"] = 47.5              # change an existing value
room["height"] = 3.2             # add a new key
del room["floor"]                # remove a key
print(room)


# --- safe reads: .get() and `in` -----------------------------------------

# .get() returns None (or a default you supply) instead of crashing.
# Use `[…]` when a missing key means the program is broken.
# Use .get() when a missing key is a normal, expected situation.
print(room.get("colour"))              # None
print(room.get("colour", "grey"))      # 'grey' -- default
print("area" in room)                  # True
print("colour" in room)                # False


# --- update ---------------------------------------------------------------

# .update() merges another dict in; existing keys are overwritten.
extras = {"orientation": "south", "area": 50.0}
room.update(extras)
print(room)
