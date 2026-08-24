# Exercises — Week 02 (Python I)

> **Practice, not checkpoints.** The [Week 02 checkpoints](/Lecture/Lecture_01/README.md#checkpoints)
> prove you *can* do something, with an automatic yes/no. These exercises are
> open-ended: no checker, no single right answer, room to play. Do the
> checkpoints first; come here to stretch.
>
> Run your solutions with `uv run your_script.py`.

## 1. Temperature converter

Ask the user for a temperature in Celsius and convert it to Fahrenheit:
`F = C * 9/5 + 32`. Print the result.

Then extend it:
- convert the other way too (Fahrenheit → Celsius), asking which direction;
- round the answer to one decimal place with an f-string (`f"{value:.1f}"`).

A worked version is in `../../Practices/` and the checkpoint
`celsius_to_fahrenheit` covers the core of it.

## 2. Inventory management

Given four parallel lists:

```python
item_ids        = [1, 2, 3, 4, 5]
item_names      = ["bolt", "screw", "nail", "washer", "nut"]
item_prices     = [0.25, 0.30, 0.15, 0.10, 0.20]
item_quantities = [150, 100, 10, 500, 300]
```

Ask the user for an item id and print its name, quantity, and total value
(price × quantity):

```
Enter an item id (1-5): 1
bolt — quantity 150, total value 37.50
```

Then think about what this exercise is really showing you: four lists that must
stay lined up by index are fragile — delete one item from three of them and the
data is silently corrupt. In **Week 04** you will meet the dictionary, which
fixes exactly this. Keep this version; you will rewrite it then and feel the
difference.

Handle an id that does not exist, rather than crashing with an `IndexError`.
