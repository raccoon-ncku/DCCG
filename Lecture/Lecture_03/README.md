# Week 03 — Python II: control flow, modules, functions

> Self-contained. Read, run the examples, do the checkpoints:
> `uv run check.py 03`.

Last week your code ran top to bottom, once. This week it makes **decisions**
and **repeats** — which is where the interesting bugs start, and where reading
code carefully starts to pay.

---

## 1. `if` / `elif` / `else`

```python
temperature = 18

if temperature > 25:
    print("hot")
elif temperature > 15:
    print("mild")
else:
    print("cold")
```

Rules that catch everyone once:

- The colon `:` at the end of the line is required.
- The body is **indented** — four spaces. Python has no `{}`.
- `elif` branches are tested **in order**, and only the first true one runs.
  Order therefore changes behaviour: swap the two conditions above and every
  mild day prints "hot".
- `=` assigns, `==` compares. `if x = 5:` is a syntax error.

📄 `Examples/4.1_if_statement.py`, `4.1.1_elif_statement.py`, `4.1.2_else_statement.py`

### Comparison and logical operators

```python
a == b     a != b     a < b     a <= b     a > b     a >= b

x > 0 and x < 10       # both must be true
x < 0 or x > 10        # at least one
not x                  # inverts
0 < x < 10             # Python allows this chain, and it reads well
```

📄 `Examples/4.1.3_logical_operator.py`

### Truthiness

Empty things are false; non-empty things are true.

```python
if items:          # better than  if len(items) > 0:
    ...
```
Falsy values: `False`, `None`, `0`, `0.0`, `""`, `[]`, `{}`.

## 2. `for` loops

A `for` loop walks through a sequence, one item at a time.

```python
for colour in ["red", "green", "blue"]:
    print(colour)
```

### `range()`

```python
range(5)          # 0 1 2 3 4          -- stop is EXCLUDED
range(2, 6)       # 2 3 4 5
range(0, 10, 3)   # 0 3 6 9            -- step
range(5, 0, -1)   # 5 4 3 2 1          -- counting down
```

`range(n)` gives you `n` numbers starting at 0. This is why a list of `n`
items has indices `0` to `n-1`, and why `range(1, n)` is a classic off-by-one.

📄 `Examples/4.2_for_statement.py`, `4.2.3_range_function.py`

### `enumerate()` — when you need the index too

```python
for i, colour in enumerate(["red", "green", "blue"]):
    print(i, colour)      # 0 red / 1 green / 2 blue
```

Reach for this instead of `for i in range(len(items))`. It is shorter, and it
cannot go out of range.

📄 `Examples/4.2.6_enumerate.py`

### `break` and `continue`

```python
for n in range(100):
    if n == 5:
        break        # leave the loop entirely
    if n % 2 == 0:
        continue     # skip to the next iteration
    print(n)         # 1 3
```

📄 `Examples/4.2.2_break_continue.py`

### Nested loops — the grid pattern

This one you will use constantly in geometry:

```python
for row in range(3):
    for col in range(4):
        print(row, col)     # 12 combinations: a 3 x 4 grid
```

📄 `Examples/4.2.4_nested_for.py`, `4.2.5_for_if_statement.py`

### Accumulating a result

The most common shape in this course: start empty, append as you go, return.

```python
def squares_up_to(n):
    """Return [0, 1, 4, 9, ...] for n terms."""
    result = []                 # 1. start empty
    for i in range(n):
        result.append(i * i)    # 2. add one item per pass
    return result               # 3. return AFTER the loop
```

> ⚠️ `return` inside the loop exits on the **first** pass. Indentation decides
> whether you get a list of `n` items or a list of 1. This is the bug you will
> most often find in AI-generated code, because it looks completely fine.

## 3. `while` loops

Use `while` when you do not know in advance how many repetitions you need.

```python
total = 0
n = 1
while total < 100:
    total += n
    n += 1
```

**Every `while` loop needs something that eventually makes the condition
false.** If you write an infinite loop, `ctrl + C` stops it.

📄 `Examples/4.3.while_statement.py`

## 4. Modules

A module is a file of Python you can use from another file. The standard
library ships with hundreds.

```python
import math
print(math.pi)          # 3.141592653589793
print(math.sqrt(16))    # 4.0
print(math.cos(0))      # 1.0

from math import pi, cos      # import specific names
import math as m             # import under a shorter name
```

Useful ones this semester:

| Module | For |
| ------ | --- |
| `math` | `pi`, `sqrt`, `sin`, `cos`, `radians`, `floor`, `ceil` |
| `random` | `random()`, `randint()`, `choice()`, `shuffle()`, `seed()` |
| `pathlib` | file paths (Week 04) |
| `json` | reading/writing data (Week 04) |

📄 `Examples/5_modules.py`, `5.3_math.py`, `5.4_import.py`

> ### Angles are in radians
> `math.sin`, `math.cos` and COMPAS all take **radians**, not degrees.
> `math.radians(90)` converts. Forgetting this produces geometry that is wrong
> but not obviously wrong — the worst kind.

### Random, and why seeding matters

```python
import random
random.seed(42)         # fix the starting point
print(random.randint(1, 6))   # same number every single run
```

Without a seed, a random result is different each run — which means you cannot
reproduce a bug, and you cannot test it. `seed()` makes randomness
**deterministic**: still varied, but repeatable. One of this week's checkpoints
depends on this, and it is a real engineering habit, not a classroom trick.

📄 `Examples/5.1.1_random.py`, `5.1.2_random_seed.py`

## 5. Functions, properly

Last week: `def`, `return`, docstrings. Now the rest.

### Default arguments

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Ada")                    # 'Hello, Ada!'
greet("Ada", "Good morning")    # 'Good morning, Ada!'
```

Parameters with defaults must come **after** those without.

### Keyword arguments

```python
def box(width, height, depth):
    ...

box(2, 3, 4)                          # positional -- which is which?
box(width=2, height=3, depth=4)       # unambiguous, and self-documenting
```

For anything with more than two numbers, use keywords. Your future self and
your reviewer will both thank you.

📄 `Examples/6.1.1`–`6.1.4_function_arguments_*.py`

### Returning several values

```python
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 4])      # unpacking
```

📄 `Examples/6.2.1_return_statement_I.py`, `6.2.2_return_statement_II.py`

### Scope

Names created inside a function are local to it and vanish when it returns.

```python
def f():
    x = 10        # local
    return x

f()
print(x)          # NameError -- x does not exist out here
```

A function can *read* names from outside, but relying on that makes it
impossible to test in isolation. **Pass what you need in as an argument.**
This habit is what makes the Week 06 architecture possible.

📄 `Examples/6.3.1`, `6.3.2_function_variable_scope_*.py`

> ### ⚠️ The mutable default argument trap
> ```python
> def add_item(item, basket=[]):     # WRONG
>     basket.append(item)
>     return basket
>
> add_item("a")     # ['a']
> add_item("b")     # ['a', 'b']   <- the SAME list, still there
> ```
> The default is created once, when the function is defined. Use `None`:
> ```python
> def add_item(item, basket=None):
>     if basket is None:
>         basket = []
>     basket.append(item)
>     return basket
> ```
> Worth knowing because AI assistants reproduce this bug regularly — it is
> common in their training data.

## 6. When it goes wrong

This is the first week your code can fail in interesting ways, so this is the
week to learn what to do about it. There are two different problems here and
they need different tools.

### It crashed: read the traceback

Python tells you exactly what happened. Read it **from the bottom up** — the
last line is *what*, the lines above are *where* and *how you got there*.

```
Traceback (most recent call last):
  File "primes.py", line 18, in <module>
    print(primes_below(20))
  File "primes.py", line 12, in primes_below
    if n % candidates[i] == 0:
IndexError: list index out of range
```

Bottom line: `IndexError` — an index past the end of a list. Line above: the
exact expression, at line 12. Above that: who called it. Two lines is usually
the whole answer.

The ones you will meet this week:

| Error | Usually means |
| ----- | ------------- |
| `NameError` | typo, or used before it was defined |
| `TypeError` | wrong kind of value — very often a `None` from a function that forgot to `return` |
| `IndexError` | list index past the end — check your `range()` |
| `ValueError` | right type, impossible value — `int("abc")` |
| `IndentationError` | inconsistent indentation |
| `ZeroDivisionError` | you divided by a count that turned out to be 0 |

> An error message is not an insult. It is the most specific and most accurate
> information you will get all day, and it is free. When you ask anyone —
> including an AI assistant — for help, paste the **whole** traceback. "It
> doesn't work" is unanswerable.

### It didn't crash, and the answer is wrong

Harder, and much more common in this course. Staring at the code does not
work. Do this instead:

**1. Print the value you are assuming.** Most bugs are a gap between what you
believe a variable holds and what it actually holds.

```python
for i in range(n):
    print(f"{i=} {total=}")     # the = prints both the name and the value
```

**2. Narrow it down.** Does it fail with 100 items? With 3? With 1? With 0?
Does the first pass of the loop produce the right value? Each answer halves
the search; four or five halvings is usually enough.

**3. Check the boundaries.** Bugs live at the edges — the first and last
iteration, empty input, one item, zero. Not in the middle.

**4. Run it on an answer you already know.** If `fizz_buzz(5)` doesn't give you
what you worked out by hand, you have found the bug without understanding the
code at all.

**5. Say it out loud.** Explain each line, in order, as though to someone else.
The sentence you cannot finish is the line with the bug.

📄 A worked example: run `Examples/4.2.5_for_if_statement.py` and predict the
grid before you look.

> Reference version, with more errors and the interactive debugger:
> [rccn wiki → Errors & Debugging](https://kb.rccn.dev/computation/python/syntax-essentials/errors-and-debugging).
> Deliberate error *handling* — `try` / `except` — is next week.

---

## Checkpoints

```bash
uv run check.py 03
```

| # | Task | Exercises |
| - | ---- | --------- |
| 1 | `fizz_buzz(n)` | `if`/`elif`/`else`, `%`, accumulating a list |
| 2 | `triangle(n)` | nested repetition, string building |
| 3 | `is_palindrome(text)` | strings, slicing, normalising input |
| 4 | `primes_below(n)` | nested loops, `break`, an algorithm |
| 5 | `circle_points(count, radius)` | `math`, radians, floats |
| 6 | `roll_dice(seed, count)` | `random`, and why seeding makes code testable |

Checkpoint 4 (`primes_below`) is the one people find hardest. It is a real
algorithm rather than a syntax drill, and it is worth the struggle — if you can
write it and explain it, you can read most of what an assistant hands you.
There is optional extra practice on the same ground in
[0_prime_numbers](/Assignment/0_prime_numbers/README.md), retired as a graded
assignment but kept because the write-up is good.

## Exercise

📝 [Asterisk pattern, factorial, guess-the-number, palindrome](/Exercise/Lecture_03/README.md)

## Self-test

1. How many times does `for i in range(2, 10, 3)` run, and what are the values?
2. What is the difference between `break` and `continue`?
3. Why does `def f(items=[])` behave surprisingly on the second call?
4. `math.sin(90)` returns `0.894...`, not `1.0`. Why?
5. When would you use `while` instead of `for`?
6. A loop builds a list but returns only one item. What is almost certainly wrong?
7. Which line of a traceback do you read first, and why?
8. Your function returns the wrong number but raises no error. What are the
   first two things you do?
