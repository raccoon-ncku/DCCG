# STARTER FILE — READ ONLY.
# Edit  answers_runner.py  instead (auto-created from this file on first run).

"""
Week 09 — THE RUNNER / ARTIFACT LAYER.

This file is allowed to touch the outside world: paths, files, JSON. What it
must NOT contain is geometry logic. It calls the core and saves what comes
back.

Notice how short it is supposed to be. That is the point -- the part of your
program that touches the world should be small enough to check by eye, and the
part that is complicated should be pure enough to check by test.
"""

from pathlib import Path

import compas

# Your core lives in answers_core.py (the editable copy of core.py), so that
# is the module the runner imports. Everything else refers to it as `core`.
import answers_core as core


def build_artifact(path, n_courses=8, **kwargs):
    """Build a wall with the core and save it as a COMPAS JSON artifact.

    - creates the parent folder if it does not exist
    - writes the list of Boxes with `compas.json_dump`
    - returns the list of Boxes as well, so a caller does not have to read the
      file back just to see what was made

    Parameters
    ----------
    path : str | pathlib.Path -- where to write the artifact
    n_courses : int           -- passed through to the core
    **kwargs                  -- any other core parameters, passed through

    Returns
    -------
    list[compas.geometry.Box]

    Hint: `compas.json_dump(data, path)` writes COMPAS objects; the plain
    `json` module (README section A3) cannot. `compas.json_load(path)` reads them back
    as real Boxes -- which is what makes the artifact useful rather than just a
    log file.
    """
    raise NotImplementedError("build_artifact")
