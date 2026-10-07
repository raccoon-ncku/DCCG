"""Copy a course notebook into MyWork/notebooks/, where it is yours to edit.

    uv run Lecture/notebooks/copy_to_mywork.py 03        # notebook 03, both files
    uv run Lecture/notebooks/copy_to_mywork.py all

Why: the files in Lecture/notebooks/ are updated by the instructor every week.
Edit them in place and `git pull upstream main` turns into merge conflicts.
MyWork/ is never touched by the instructor (see MyWork/README.md), so a copy
there can be edited, run, broken and committed freely.

Copies both the .ipynb (Jupyter, VS Code) and the .py (Zed). Never overwrites
a copy you already have.
"""

import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
TARGET = HERE.parent.parent / "MyWork" / "notebooks"


def main(which):
    sources = sorted(HERE.glob("[0-9][0-9]_*.py"))
    chosen = sources if which == "all" else [s for s in sources if s.name.startswith(which.zfill(2) + "_")]
    if not chosen:
        sys.exit(f"no notebook {which!r}; choose one of: " + ", ".join(s.name[:2] for s in sources))
    TARGET.mkdir(parents=True, exist_ok=True)
    for src in chosen:
        for f in (src, src.with_suffix(".ipynb")):
            dst = TARGET / f.name
            if dst.exists():
                print(f"kept   {dst.relative_to(HERE.parent.parent)}  (you already have a copy)")
            else:
                shutil.copy2(f, dst)
                print(f"copied {dst.relative_to(HERE.parent.parent)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "")
