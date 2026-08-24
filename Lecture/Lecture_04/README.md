# Week 04 — Python III: dictionaries, files, JSON — and reading AI code

> Self-contained. `uv run check.py 04` when you are ready.

Two halves this week.

**First**, the last pieces of core Python you need: dictionaries (how you
attach *meaning* to data), files, and JSON (how data survives past the end of
your program). JSON matters more than it looks — from Week 06 onward, the
verified output of your work is a JSON file.

**Second**, the skill this course is actually about: **reading code you did not
write and finding what is wrong with it.** The last checkpoint is an
AI-generated module that looks completely reasonable and is not.

---

## 1. Dictionaries

A list is indexed by position. A dictionary is indexed by a **key** you choose.

```python
room = {
    "name": "studio",
    "area": 45.0,
    "floor": 2,
}

room["name"]              # 'studio'
room["area"] = 47.5       # change a value
room["height"] = 3.2      # add a new key
del room["floor"]         # remove one
```

Keys are usually strings. Values can be anything, including lists and other
dictionaries.

### Reading safely

```python
room["colour"]              # KeyError -- crashes
room.get("colour")          # None -- no crash
room.get("colour", "grey")  # 'grey' -- a default
"area" in room              # True
```

Use `[...]` when a missing key means your program is broken and should stop.
Use `.get(...)` when a missing key is a normal, expected situation. Choosing
deliberately between those two is a small piece of engineering judgment.

### Looping

```python
for key in room:                     # keys
    print(key)

for key, value in room.items():      # keys AND values -- the common one
    print(key, "=", value)

for value in room.values():
    print(value)
```

📄 `../Lecture_03/python_examples/3.2.1_dictionary.py`, `3.2.2_update_dictionary.py`,
`3.2.3_dictionary_iteration.py`

### The counting pattern

Worth memorising — it turns up constantly:

```python
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
```

### Dictionaries in geometry

This is why we care. A mesh vertex is not just a point; it is a point *with
attributes* — a colour, a load, a material, a fabrication ID. COMPAS stores
exactly that, as dictionaries, on every vertex and face. Week 09 builds on this.

### Tuples, briefly

A tuple is an unchangeable list, written with parentheses:

```python
point = (3.0, 4.0, 0.0)
x, y, z = point            # unpacking
```

Use a tuple when the collection is a fixed record (a coordinate, an RGB
colour) rather than a growing sequence. Tuples can be dictionary keys; lists
cannot.

📄 `../Lecture_03/python_examples/3.3_tuples.py`

## 2. Files

### Paths — use `pathlib`, always

```python
from pathlib import Path

folder = Path("data")
file = folder / "result.json"      # the / operator joins path parts

file.exists()
file.parent
file.name          # 'result.json'
file.stem          # 'result'
file.suffix        # '.json'
folder.mkdir(parents=True, exist_ok=True)   # create it, no error if present
```

Never build paths by gluing strings with `"/"` or `"\\"` — that breaks between
Windows and macOS, and it is the reason half of all "works on my machine"
problems exist.

**Where does a relative path point?** To your *current working directory* — the
folder your terminal is in, not the folder the script is in. To get a path
relative to the script itself:

```python
HERE = Path(__file__).parent
data = HERE / "data" / "input.json"
```

📄 `python_examples/7.2.1_path.py` … `7.3_pathlib.py`

### Reading and writing

```python
path = Path("notes.txt")

path.write_text("hello")        # simplest possible write
content = path.read_text()      # and read
```

For anything larger, or line by line, use `with`:

```python
with open(path, "w") as f:
    f.write("hello\n")

with open(path) as f:
    for line in f:
        print(line.rstrip())
```

`with` closes the file for you, **even if an error happens inside the block.**
That is the whole reason it exists.

Modes: `"r"` read (default), `"w"` write — **erases the file first** — `"a"`
append.

📄 `python_examples/7.1.1_write_file.py`, `7.1.2_with_statement.py`, `7.1.3_read_file.py`

## 3. JSON

JSON is a text format for structured data. Nearly every tool reads it, which
is why it is how your geometry will travel between your code, the viewer, git,
and Rhino.

```python
import json
from pathlib import Path

data = {"name": "wall", "courses": 12, "heights": [0.1, 0.2, 0.3]}

Path("wall.json").write_text(json.dumps(data, indent=2))   # write
loaded = json.loads(Path("wall.json").read_text())          # read back
```

`indent=2` makes the file human-readable *and* diffable in git — so a reviewer
can see what changed between two versions of your design. Always use it.

What JSON can hold: `dict`, `list`, `str`, `int`, `float`, `bool`, `None`.
What it cannot: tuples (they come back as lists), sets, and your own classes.

> COMPAS has its own JSON layer — `compas.json_dump` / `compas.json_load` —
> which *can* store geometry objects. You will meet it in Week 05 and rely on
> it from Week 06.

## 4. Errors, and reading a traceback

When Python fails it prints a **traceback**. Read it **from the bottom up**:
the last line is what went wrong, and the lines above show how you got there.

```
Traceback (most recent call last):
  File "script.py", line 12, in <module>
    area = rooms["kitchen"]["area"]
KeyError: 'kitchen'
```

Bottom line: `KeyError: 'kitchen'` — there is no such key. Line above: exactly
where. That is usually enough.

Common ones:

| Error | Usually means |
| ----- | ------------- |
| `NameError` | typo in a name, or used before it was defined |
| `TypeError` | wrong kind of value — often a `None` from a function that forgot to `return` |
| `KeyError` | dictionary key does not exist |
| `IndexError` | list index past the end |
| `ValueError` | right type, impossible value (`int("abc")`) |
| `AttributeError` | that object has no such method — often a typo, or it is `None` |
| `IndentationError` | your indentation is inconsistent |

### Handling errors on purpose

```python
try:
    value = int(user_input)
except ValueError:
    print("That was not a number.")
```

Catch only what you can actually handle. A bare `except:` that swallows
everything turns a loud, findable bug into a silent, unfindable one.

📄 `../Lecture_05/python_examples/try_statement.py`

## 5. Reading AI-generated code

You now know enough Python to review it — and that is the job.

An AI assistant produces code that is **fluent**: correct-looking names,
plausible structure, a confident docstring. Fluency is not correctness. The
model is not reasoning about your problem; it is producing text that resembles
solutions to problems like yours. Most of the time that lands. When it misses,
it misses in ways that look fine.

**The five places to look first** — nearly every bug you will meet this
semester is one of these:

1. **Off-by-one.** `range(1, n)` vs `range(n)`; slice `stop` is excluded.
2. **Mutable default arguments.** `def f(items=[])` — Week 03's trap. Extremely
   common in generated code.
3. **Silent mutation.** A function that says it returns a new list but
   modifies the one you passed in.
4. **Floats compared with `==`.** Looks right, fails on real data.
5. **Confidently wrong constants and formulas.** Degrees where radians belong;
   a plausible-looking formula that is not the one you asked for.

**How to actually review**, in order:

1. Read the *signature and docstring* first. Is this even the function you
   asked for?
2. Read the body and say out loud what each line does. Anything you cannot
   explain is a finding — either the code is unclear or you do not yet
   understand the problem. Both are blockers.
3. Check the edges: empty input, one item, zero, negative numbers.
4. **Run it on an example where you already know the answer.** Not one it
   suggested — one you chose.

> "It ran without an error" is not evidence that it is correct. Silent wrong
> answers are the expensive kind. This is also why Week 10 exists.

## 6. Optional: graphs and networks

`graph_examples/` contains a full set of COMPAS `Network` / networkx examples —
shortest paths, a brick-wall network, real data on the New York subway and
cholera outbreaks. **Not examined this semester**, and not needed for any
checkpoint. Kept because a graph is an excellent backbone for a final project
(circulation analysis, assembly sequencing, structural topology). Browse if it
is useful to you.

---

## Checkpoints

```bash
uv run check.py 04
```

| # | Task | Exercises |
| - | ---- | --------- |
| 1 | `tally(words)` | the counting pattern |
| 2 | `invert(mapping)` | dict iteration, and a case the spec has to decide |
| 3 | `merge_settings(defaults, overrides)` | copying vs mutating |
| 4 | `save_rooms` / `load_rooms` | pathlib + JSON round-trip |
| 5 | **`summarise_rooms(rooms)` — find the bugs** | reviewing AI-generated code |

Checkpoint 5 is different. The function is already written — by an AI
assistant, in one shot, and it looks fine. It is not. Your job is to find and
fix what is wrong. Read the code before you run the checks, and write down what
you think is broken *first*; then see how many the specification agrees with.
That comparison is the actual exercise.

## Self-test

1. When should you use `dict.get(key)` instead of `dict[key]`?
2. Why is `Path("data") / "out.json"` better than `"data/" + "out.json"`?
3. What does `with open(...)` do that a plain `open(...)` does not?
4. You call a function and get `TypeError: unsupported operand type(s) for +:
   'NoneType' and 'int'`. What is the most likely cause?
5. Name three bugs that AI-generated Python commonly contains.
