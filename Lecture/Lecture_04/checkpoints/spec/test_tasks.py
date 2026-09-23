# ──────────────────────────────────────────────────────────────────────────────
#  READ ONLY  ·  this file is the SPEC, not the answers.
#
#  Your work goes in  ../answers.py  (or ../answers_core.py + ../answers_runner.py
#  in Week 06). That file is auto-created from the shipped starter on first run
#  and is gitignored, so `git pull` never conflicts with it. Read the
#  assertions below to understand what each checkpoint is checking; do not
#  change them.
# ──────────────────────────────────────────────────────────────────────────────
"""
The SPECIFICATION for Week 04.

The last group of tests is a worked example of what a code review produces:
each one names a specific defect in `summarise_rooms` and shows the input that
exposes it. When you review AI-generated code in Week 11, this is the shape of
the output you are aiming for -- not "looks fine to me", but "here is the case
where it breaks".
"""

import json
from pathlib import Path

from answers import (
    invert,
    load_rooms,
    merge_settings,
    save_rooms,
    summarise_rooms,
    tally,
)

ROOMS = [
    {"name": "hall", "area": 12.0},
    {"name": "studio", "area": 45.0},
    {"name": "store", "area": 8.0},
    {"name": "library", "area": 30.0},
]


# --- 1. tally ---------------------------------------------------------------

def test_tally_counts_repeats():
    """tally() counts how often each word appears"""
    assert tally(["a", "b", "a"]) == {"a": 2, "b": 1}
    assert tally(["x"]) == {"x": 1}


def test_tally_of_nothing_is_an_empty_dict():
    """tally([]) is {}"""
    assert tally([]) == {}


# --- 2. invert --------------------------------------------------------------

def test_invert_swaps_keys_and_values():
    """invert() turns values into keys"""
    assert invert({"a": 1, "b": 2}) == {1: "a", 2: "b"}


def test_invert_handles_duplicate_values():
    """when two keys share a value, the LAST one wins"""
    # This is the decision the task docstring refused to make. Either answer
    # could be defended; what matters is that the spec picks one, so that
    # everybody's code -- and every future change to it -- agrees.
    # "Last one wins" is what a plain loop does naturally, so it is the least
    # surprising choice.
    assert invert({"a": 1, "b": 1}) == {1: "b"}


# --- 3. merge_settings ------------------------------------------------------

def test_merge_settings_overrides_win():
    """merge_settings() lets the second dictionary override the first"""
    assert merge_settings({"a": 1, "b": 2}, {"b": 99}) == {"a": 1, "b": 99}


def test_merge_settings_keeps_unrelated_keys():
    """keys present in only one input survive the merge"""
    assert merge_settings({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}


def test_merge_settings_does_not_modify_its_inputs():
    """neither argument is changed by the call"""
    defaults = {"a": 1, "b": 2}
    overrides = {"b": 99}
    merge_settings(defaults, overrides)
    assert defaults == {"a": 1, "b": 2}, (
        "You modified `defaults` in place. `defaults.update(overrides)` does "
        "exactly this -- make a copy first."
    )
    assert overrides == {"b": 99}


# --- 4. save / load ---------------------------------------------------------

def test_save_then_load_round_trips(tmp_path):
    """what save_rooms() writes, load_rooms() reads back unchanged"""
    path = tmp_path / "rooms.json"
    save_rooms(ROOMS, path)
    assert load_rooms(path) == ROOMS


def test_save_rooms_creates_missing_folders(tmp_path):
    """save_rooms() creates the parent folder if it does not exist"""
    path = tmp_path / "deep" / "nested" / "rooms.json"
    save_rooms(ROOMS, path)
    assert path.exists(), "The folder did not exist. mkdir(parents=True, exist_ok=True)."


def test_save_rooms_writes_readable_json(tmp_path):
    """the file is indented JSON a human and git can read"""
    path = tmp_path / "rooms.json"
    save_rooms(ROOMS, path)
    text = path.read_text()
    assert json.loads(text) == ROOMS, "The file is not valid JSON."
    assert "\n" in text.strip(), (
        "The JSON is all on one line. Pass indent=2 so the file is reviewable "
        "in a diff."
    )


def test_save_rooms_accepts_a_string_path(tmp_path):
    """`path` may be a plain string, not only a Path"""
    path = str(tmp_path / "rooms.json")
    save_rooms(ROOMS, path)
    assert load_rooms(path) == ROOMS


# --- 5. the code review -----------------------------------------------------
# Each test below is one defect in the AI-generated summarise_rooms().

def test_summarise_includes_the_first_room():
    """BUG 1: summarise_rooms() skips the first room in the list"""
    # `for i in range(1, len(rooms))` starts at index 1. Index 0 is never seen.
    # Total should be 12 + 45 + 8 + 30 = 95, not 83.
    result = summarise_rooms(ROOMS)
    assert result["total_area"] == 95.0, (
        "The first room was left out. Look at the range() in the loop -- "
        "range(1, n) starts at 1, but list indices start at 0."
    )


def test_summarise_finds_the_largest_room():
    """summarise_rooms() names the largest room, even when it is first"""
    assert summarise_rooms(ROOMS)["largest"] == "studio"
    # The list above happens to put the largest room at index 1, so it survives
    # the off-by-one. Move it to index 0 and the same bug shows up here too --
    # a reminder that a spec only catches what it actually looks at.
    biggest_first = [{"name": "atrium", "area": 99.0}] + ROOMS
    assert summarise_rooms(biggest_first)["largest"] == "atrium"


def test_summarise_lists_rooms_over_twenty():
    """summarise_rooms() lists the names of rooms larger than 20 m2"""
    assert summarise_rooms(ROOMS)["large_rooms"] == ["studio", "library"]


def test_summarise_averages_correctly():
    """summarise_rooms() divides the total by the number of rooms"""
    assert summarise_rooms(ROOMS)["average_area"] == 95.0 / 4


def test_summarise_does_not_leak_between_calls():
    """BUG 2: results from one call contaminate the next"""
    # `def summarise_rooms(rooms, summary={})` -- the default dict is created
    # ONCE, when the function is defined, and reused by every call that does
    # not pass its own. The Week 03 mutable-default trap, in the wild.
    first = summarise_rooms(ROOMS)
    second = summarise_rooms([{"name": "shed", "area": 5.0}])
    assert second["total_area"] == 5.0, (
        "The second call still remembers the first one's rooms. "
        "Look very carefully at the function signature."
    )
    assert second["large_rooms"] == [], (
        "The large_rooms list is being shared between calls."
    )
    assert first["total_area"] == 95.0, (
        "The first call's result was mutated by the second call -- both calls "
        "are handing back the same dictionary object."
    )


def test_summarise_handles_an_empty_list():
    """BUG 3: summarise_rooms([]) crashes with ZeroDivisionError"""
    # The prompt explicitly asked it to "handle the empty case". It does not.
    # The spec decides what "handled" means here:
    #
    #   total 0, average 0.0, largest None, large_rooms []
    #
    # Note this differs from Week 02's list_stats([]), which raises. That is
    # not an inconsistency: the minimum of no numbers genuinely does not exist,
    # but a summary of no rooms is legitimately "nothing here". Deciding which
    # of those two a situation is -- rather than defaulting to whichever is
    # easier -- is the judgment being trained.
    result = summarise_rooms([])
    assert result["total_area"] == 0
    assert result["average_area"] == 0.0
    assert result["largest"] is None
    assert result["large_rooms"] == []
