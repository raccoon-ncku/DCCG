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

## 4. Handling errors on purpose

Week 03 covered *reading* a traceback — bottom line first — and the errors you
meet most. Dictionaries and files add two more to that list:

| Error | Usually means |
| ----- | ------------- |
| `KeyError` | that dictionary key does not exist — use `.get()` if absence is normal |
| `FileNotFoundError` | the path is wrong, or relative to a different folder than you think |

This week is the other half: failure you **expect**, and choose to handle.

```python
try:
    value = int(user_input)
except ValueError:
    print("That was not a number.")
```

Catch only what you can actually handle, and name it. A bare `except:` swallows
everything — including the typo you have not found yet — and turns a loud,
findable bug into a silent, permanent one.

The distinction is worth stating plainly, because it is a design decision you
will make repeatedly from Week 06 onward:

- A missing key that means **your program is broken** should crash. Let it.
- A missing key that is **a normal situation** deserves `.get()` or a `try`.

Silencing the first kind is how a wall with eleven courses gets built.

📄 `../Lecture_05/python_examples/try_statement.py`

## 5. What an LLM actually is

You have been using an assistant since Week 01. Here is what it is doing, and
it is less than most people assume.

**A language model predicts plausible continuations of text.** Give it your
code and your question, and it produces what tends to follow text like that.
That is the whole mechanism. It is not executing your code, not checking your
units, not reasoning about your wall.

Three consequences that matter this week:

1. **It is a function, not a colleague.** Same input, same distribution of
   outputs. It has no memory of yesterday, and within one conversation it only
   sees what is on screen. If a constraint matters, it has to be in the prompt.
2. **Fluency is not correctness.** Confident prose, tidy variable names and a
   well-formed docstring are properties of the *writing*. They are not evidence
   about the code. This is the single most expensive misunderstanding available
   to you this semester.
3. **It fails silently and plausibly.** A human who does not know says so. A
   model produces its best guess in the same confident voice it uses when
   right — including inventing methods that do not exist and citing papers that
   were never written.

It follows that it is strongest where a mistake is cheap and obvious —
boilerplate, format conversion, a first draft, explaining unfamiliar code — and
weakest where a mistake is silent: numeric detail, units, edge cases, and
anything that depends on facts about your project it cannot see.

In Week 11 you will build the loop that drives one of these, from scratch, and
this description becomes a piece of code you can read.

### Asking well

The quality of what comes back tracks the specificity of the request more than
anything else you control.

| Instead of | Ask |
| ---------- | --- |
| "write a function for rooms" | "Write `summarise_rooms(rooms)` taking a list of dicts with `name` and `area` keys, returning the count, the total area, and the mean. Decide what an empty list should do and say why." |
| "fix this" | "This raises `KeyError: 'area'` on line 12. Here is the traceback and the input. What causes it?" |
| "is this good?" | "What happens for an empty list? For one item? For a negative area?" |
| "explain dictionaries" | "Explain line by line what `counts[word] = counts.get(word, 0) + 1` does." |

Four habits worth building now:

- **State the signature you want** — name, parameters, what comes back. You
  design the interface; let it fill the body.
- **Paste the real error**, complete, as text.
- **Ask one thing.** Four requests in a prompt get four mediocre answers.
- **Ask it to explain rather than produce** when you are trying to learn.
  Accepted-but-not-understood code is a debt, and Week 13 is when it comes due.

> If you cannot describe what you want precisely enough for a model to build
> it, you have not finished thinking about the problem. That difficulty is
> information. In Week 10 this becomes a formal idea: a brief you can turn into
> a test is a finished brief.

The general, non-course version of this — including where *not* to reach for an
assistant — is on the lab wiki:
[AI Assistants](https://kb.rccn.dev/computation/ai-assistants).

## 6. Reading AI-generated code

You now know enough Python to review it — and that is the job.

Most of the time a model lands it. When it misses, it misses in ways that look
fine — which is why review is a procedure and not a feeling.

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

## 7. Optional: graphs and networks

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
6. Why is "it ran without an error" not evidence that code is correct?
7. An assistant gives you a function and a test case that passes. Why should
   you not treat that as verification?
