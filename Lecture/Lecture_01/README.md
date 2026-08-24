# Week 02 — Python I: values, types, lists, functions

> Self-contained. Read this page, run the examples next to it, then do the
> checkpoints. `uv run check.py 02` tells you when you are done.

## Why we start by *reading*

You are learning Python in a year when a machine can produce it faster than
you can type. That does not make this week optional — it makes it different.
The purpose is no longer to memorise syntax so you can produce it. It is to be
able to **look at a screen of code and say what it does, and whether it is
right.**

So for every example below: predict the output *before* you run it. If your
prediction is wrong, that gap is the actual lesson. This is exactly the skill
you will need in Week 11, when the code on your screen was written by
something that does not know what it is doing.

---

## 1. Running code

```bash
uv run Lecture/Lecture_01/Examples/1_hello_world.py
```

An interactive prompt, useful for trying one line:

```bash
uv run python
>>> 2 + 2
4
>>> exit()
```

## 2. Comments

```python
# Everything after a hash is ignored by Python.
width = 10  # ... including at the end of a line
```

Comments explain **why**, not **what**. `x = x + 1  # add one to x` is noise.
`x = x + 1  # rows are 1-indexed in the fabrication file` is worth its space.

📄 `Examples/2.1_variables.py`

## 3. Variables

A variable is a **name pointing at a value**. `=` is not equality; it is "make
this name refer to that value".

```python
width = 10
height = 9
print(height)     # 9

height = 20       # the name now points somewhere else
print(height)     # 20
```

Names must start with a letter or `_`, contain letters/digits/`_`, and are
case-sensitive. `width`, `total_area`, `n_steps` — lowercase with underscores
is the Python convention, and following it is free.

Names are documentation. `w` costs you nothing today and costs you an hour in
December. Name things after what they *mean*: `course_height`, not `ch`.

📄 `Examples/2.1.1_variables_II.py`, `Examples/2.1.2_variable_names.py`

## 4. Types

Every value has a type, and the type decides what operations mean.

| Type | Example | Notes |
| ---- | ------- | ----- |
| `int` | `42` | whole numbers, unlimited size |
| `float` | `3.14` | decimals — **approximate**, see the warning below |
| `str` | `"hello"` | text, single or double quotes |
| `bool` | `True` / `False` | capitalised |
| `list` | `[1, 2, 3]` | ordered, changeable |
| `NoneType` | `None` | "no value" |

```python
print(type(3))        # <class 'int'>
print(type(3.0))      # <class 'float'>
print(3 == 3.0)       # True  -- equal in value
```

> ### ⚠️ Floats are approximate — remember this one
> ```python
> >>> 0.1 + 0.2
> 0.30000000000000004
> >>> 0.1 + 0.2 == 0.3
> False
> ```
> This is not a Python bug; it is how binary fractions work in every language.
> **Never compare computed floats with `==`.** Every coordinate you compute
> this semester is a float. In Week 10 you will learn the proper tool
> (`pytest.approx`); until then, compare with a tolerance:
> ```python
> abs(a - b) < 1e-9
> ```

📄 `Examples/2.3_data_type.py`

## 5. Operators

```python
7 + 2     # 9
7 - 2     # 5
7 * 2     # 14
7 / 2     # 3.5   <- true division ALWAYS gives a float
7 // 2    # 3     <- floor division, drops the remainder
7 % 2     # 1     <- modulo, the remainder
7 ** 2    # 49    <- power
```

`%` looks obscure and is everywhere in geometry: `i % 2` tells you whether row
`i` is odd or even — which is exactly how you offset alternating courses in a
brick wall.

📄 `Examples/2.2_operators.py`

## 6. Strings and f-strings

```python
name = "wall"
count = 12

# f-strings: put an f before the quote, then {expressions} inside
print(f"The {name} has {count} bricks.")
print(f"Half of that is {count / 2}.")
print(f"Rounded to 2 decimals: {3.14159:.2f}")   # 3.14
```

Useful string operations:

```python
"hello".upper()          # 'HELLO'
"  padded  ".strip()     # 'padded'
"a,b,c".split(",")       # ['a', 'b', 'c']
"-".join(["a", "b"])     # 'a-b'
len("hello")             # 5
```

📄 `Examples/2.5_string_fromating.py`, `Examples/2.4_built_in_functions.py`

## 7. Lists

An ordered, changeable sequence. **Indices start at 0.**

```python
squares = [1, 4, 9, 16, 25]

squares[0]     # 1    first
squares[4]     # 25   fifth
squares[-1]    # 25   last -- negative counts from the end
squares[-2]    # 16
len(squares)   # 5
```

Changing a list:

```python
squares.append(36)      # add to the end
squares.pop()           # remove and return the last item
squares.pop(0)          # remove and return item at index 0
squares.index(16)       # position of the first 16 -- raises if absent
```

📄 `Examples/3.1.1_list.py`, `Examples/3.1.2_list_methods.py`

### Slicing

`list[start:stop:step]` — `start` is included, `stop` is **excluded**.

```python
items = [0, 1, 2, 3, 4, 5]

items[1:4]     # [1, 2, 3]      -- index 4 NOT included
items[:3]      # [0, 1, 2]      -- from the start
items[3:]      # [3, 4, 5]      -- to the end
items[::2]     # [0, 2, 4]      -- every 2nd item
items[1::2]    # [1, 3, 5]      -- every 2nd, starting at 1
items[::-1]    # [5, 4, 3, 2, 1, 0]  -- reversed
```

"Stop is excluded" is the single most common off-by-one bug in this course —
and one an AI assistant will happily reproduce for you.

📄 `Examples/3.1.3_list_slicing.py`

## 8. Functions

A function packages a piece of logic behind a name so you can use it more than
once, and test it.

```python
def rectangle_area(width, height):
    """Return the area of a rectangle.      <- docstring: what it does

    Parameters
    ----------
    width : float   -- in metres
    height : float  -- in metres
    """
    return width * height


area = rectangle_area(3, 4)     # 12
```

Three things to get right:

1. **`return` sends a value back. `print` only shows it on screen.** They are
   not the same, and confusing them is the most common beginner bug:
   ```python
   def bad(w, h):
       print(w * h)        # shows 12, returns None
   def good(w, h):
       return w * h        # gives you 12 to use
   x = bad(3, 4) + 1       # TypeError -- None + 1
   ```
2. **The body is indented.** Python uses indentation, not braces. Four spaces.
3. **Write a docstring.** Every checkpoint function in this course expects one.
   It is also the single most effective thing you can do to make an AI
   assistant write the function you actually wanted.

Deeper treatment of arguments, defaults, and scope comes next week
(`Lecture/Lecture_02/Examples/6*`).

---

## Checkpoints

```bash
uv run check.py 02
```

Edit `Lecture/Lecture_01/checkpoints/tasks.py`. Read
`checkpoints/test_tasks.py` — it is the spec, and reading the spec is not
cheating.

| # | Task |
| - | ---- |
| 1 | `rectangle_area(width, height)` — the arithmetic and the `return` |
| 2 | `celsius_to_fahrenheit(c)` — a formula, and floats |
| 3 | `describe_box(w, h, d)` — f-strings and exact formatting |
| 4 | `every_other(items)` — slicing |
| 5 | `list_stats(numbers)` — returning more than one value, and an edge case |

Checkpoint 5 asks what should happen for an **empty list**. There is no
obviously right answer — which is why the spec states one. Read it. Getting
used to "the spec decides, not my intuition" is the point of the exercise.

## Exercise

📝 [Temperature converter + inventory management](/Exercise/Lecture_01/README.md)

## Self-test: can you answer these without running them?

1. What does `[1,2,3,4,5][1:3]` evaluate to?
2. Why is `7 / 2` a float but `7 // 2` an int?
3. What does a function return if it has no `return` statement?
4. Why does `0.1 + 0.2 == 0.3` give `False`?
5. What is the difference between `squares.pop()` and `squares.pop(0)`?

If any of these are shaky, that topic is the one to reread — not the whole page.
