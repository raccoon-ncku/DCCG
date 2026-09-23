# Two things this file does, both invisible to the student:
#
#   1) Add this folder to sys.path so tests in spec/ can `from answers import …`
#   2) On first run, COPY the shipped starter to a gitignored answer file:
#        tasks.py  ->  answers.py           (standard weeks)
#        core.py   ->  answers_core.py      (Week 06)
#        runner.py ->  answers_runner.py    (Week 06)
#
# The starter is read-only reference; students edit the copy. Every `git pull
# upstream main` refreshes the starter without touching student work.
# Delete your answer file to reset from the current starter.

import pathlib
import shutil
import sys

here = pathlib.Path(__file__).parent
sys.path.insert(0, str(here))

for starter, answer in [
    ("tasks.py",  "answers.py"),
    ("core.py",   "answers_core.py"),
    ("runner.py", "answers_runner.py"),
]:
    src, dst = here / starter, here / answer
    if src.exists() and not dst.exists():
        shutil.copy2(src, dst)
