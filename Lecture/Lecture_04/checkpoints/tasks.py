"""
Week 04 checkpoints — dictionaries, files, JSON, and reviewing AI code.

Edit ONLY this file. Run from the repository root:

    uv run check.py 04

Checkpoints 1-4 are ordinary: implement the function. Checkpoint 5 is the
opposite -- the code is already there, and it is wrong. Read the banner above
it before you start.
"""

import json
from pathlib import Path


def tally(words):
    """Count how many times each word appears.

    tally(["a", "b", "a"])  ->  {"a": 2, "b": 1}
    tally([])               ->  {}

    Returns
    -------
    dict -- word (str) to count (int)

    Hint: the counting pattern in README section 1.
    """
    raise NotImplementedError("tally")


def invert(mapping):
    """Swap the keys and values of a dictionary.

    invert({"a": 1, "b": 2})  ->  {1: "a", 2: "b"}

    Two values could be the same, in which case one key has to win. The
    specification decides which -- see `test_invert_handles_duplicate_values`
    before you implement this. Do not guess.

    Returns
    -------
    dict
    """
    raise NotImplementedError("invert")


def merge_settings(defaults, overrides):
    """Combine two settings dictionaries, with `overrides` winning.

    merge_settings({"a": 1, "b": 2}, {"b": 99})  ->  {"a": 1, "b": 99}

    NEITHER input dictionary may be modified. This is the whole point of the
    checkpoint: a function that quietly edits its arguments is a bug that
    surfaces somewhere else entirely, long after you have stopped looking.

    Returns
    -------
    dict -- a NEW dictionary
    """
    raise NotImplementedError("merge_settings")


def save_rooms(rooms, path):
    """Write a list of room dictionaries to `path` as JSON.

    Requirements:
      - create the parent folder if it does not exist
      - format the JSON with indent=2 so a human (and git) can read it
      - `path` may be a str or a pathlib.Path

    Parameters
    ----------
    rooms : list[dict]
    path : str | pathlib.Path

    Returns
    -------
    None
    """
    raise NotImplementedError("save_rooms")


def load_rooms(path):
    """Read back a JSON file written by save_rooms().

    load_rooms(save_rooms(x, p) ... ) must give you x back unchanged.
    A "round trip" like this is the simplest useful test of any file format.

    Returns
    -------
    list[dict]
    """
    raise NotImplementedError("load_rooms")


# ---------------------------------------------------------------------------
# CHECKPOINT 5 — code review
# ---------------------------------------------------------------------------
# The function below was produced by an AI coding assistant from this prompt:
#
#     "Write a Python function summarise_rooms(rooms) that takes a list of
#      room dicts with 'name' and 'area' keys and returns a summary dict with
#      the total area, the average area, the name of the largest room, and a
#      list of the names of rooms bigger than 20 m2. Handle the empty case."
#
# It is fluent, it has a docstring, it runs without crashing on the obvious
# input, and it is WRONG in more than one way.
#
# Your job: fix it. Do not rewrite it from scratch -- read it, find the bugs,
# and repair them. Before you run `uv run check.py 04`, write down what you
# think is broken. Then compare your list with what the checks say.
#
# (The five things to look for are in README section 6.)
# ---------------------------------------------------------------------------


def summarise_rooms(rooms, summary={}):
    """Summarise a list of rooms.

    Parameters
    ----------
    rooms : list[dict] -- each with "name" (str) and "area" (float)

    Returns
    -------
    dict with keys: total_area, average_area, largest, large_rooms
    """
    summary["total_area"] = 0
    summary["large_rooms"] = []
    largest_area = 0
    largest_name = None

    for i in range(1, len(rooms)):
        room = rooms[i]
        summary["total_area"] += room["area"]
        if room["area"] > 20:
            summary["large_rooms"].append(room["name"])
        if room["area"] > largest_area:
            largest_area = room["area"]
            largest_name = room["name"]

    summary["average_area"] = summary["total_area"] / len(rooms)
    summary["largest"] = largest_name
    return summary
