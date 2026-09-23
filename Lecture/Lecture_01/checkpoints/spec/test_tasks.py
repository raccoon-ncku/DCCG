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
The SPECIFICATION for Week 01.

You are meant to read this file. It is the precise statement of what has to be
true before you are set up correctly. In Week 10 you will write files like this
one yourself; for now, notice only that each test states exactly one fact.
"""

import shutil
import subprocess
import sys
from pathlib import Path

from answers import student_name

ROOT = Path(__file__).resolve().parents[3]


def test_python_is_new_enough():
    """Python 3.13+ is active (you are running through `uv run`)"""
    assert sys.version_info >= (3, 13), (
        f"This project needs Python 3.13+, but you are on {sys.version.split()[0]}.\n"
        "Are you running with `uv run check.py 01` from the repo root?"
    )


def test_running_inside_the_project_environment():
    """The project virtual environment in .venv/ is the one in use"""
    venv = ROOT / ".venv"
    assert venv.is_dir(), f"No .venv found at {venv}. Run `uv sync` in the repo root."
    assert str(venv) in sys.prefix or str(venv.resolve()) in str(Path(sys.prefix).resolve()), (
        f"Python is running from {sys.prefix}, not from the project's .venv.\n"
        "Use `uv run check.py 01` rather than `python check.py`."
    )


def test_compas_is_installed():
    """COMPAS imports -- the geometry library the whole course is built on"""
    try:
        import compas
    except ImportError as exc:  # pragma: no cover - the message is the point
        raise AssertionError(
            "Could not import compas. Run `uv sync` in the repo root, and make "
            "sure you are launching this with `uv run`."
        ) from exc
    assert compas.__version__ >= "2", f"Expected COMPAS 2.x, found {compas.__version__}"


def test_git_knows_who_you_are():
    """git is installed and your name + email are configured"""
    assert shutil.which("git"), "git is not installed, or not on your PATH."
    for key in ("user.name", "user.email"):
        result = subprocess.run(
            ["git", "config", "--get", key], capture_output=True, text=True
        )
        assert result.stdout.strip(), (
            f"git has no {key} configured. Run:\n"
            f'    git config --global {key} "..."'
        )


def test_you_introduced_yourself():
    """tasks.py: student_name() returns your actual name"""
    name = student_name()
    assert isinstance(name, str), "student_name() must return a string."
    assert name.strip(), "student_name() returned an empty string."
    assert name.strip().upper() != "CHANGE ME", (
        "Open Lecture/Lecture_01/checkpoints/tasks.py and put your own name in "
        "student_name(). This is the one edit for Week 01."
    )
