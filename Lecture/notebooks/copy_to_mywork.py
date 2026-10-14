"""Copy course notebooks into MyWork/notebooks/, where they are yours to edit.

    uv run Lecture/notebooks/copy_to_mywork.py 05           # every notebook of Week 05
    uv run Lecture/notebooks/copy_to_mywork.py 05/02        # one notebook
    uv run Lecture/notebooks/copy_to_mywork.py geometric    # a part of Lecture/Algorithms
    uv run Lecture/notebooks/copy_to_mywork.py all
    uv run Lecture/notebooks/copy_to_mywork.py 05 --force   # replace copies you already have

Why: the notebooks in Lecture/ are updated by the instructor. Edit them in
place and `git pull upstream main` turns into merge conflicts. MyWork/ is
never touched by the instructor (see MyWork/README.md), so a copy there can
be edited, run, broken and committed freely.

A copy lands in MyWork/notebooks/<Lecture_05 | geometric | ...>/ and is
self-contained: the pictures it shows are copied next to it (figures/), and
so are the few files a notebook reads (an image, a small helper). That
matters because JupyterLab only serves files inside the folder it was
started on. Links to lecture pages are pointed back at the lecture.

Never overwrites a copy you already have, unless you add --force.
"""

import json
import os
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
LECTURE = HERE.parent
ROOT = LECTURE.parent
TARGET = ROOT / "MyWork" / "notebooks"
IMAGE = re.compile(r"(!\[[^\]]*\]\()([^)\s]+)(\))")
LINK = re.compile(r"(?<!!)(\[[^\]]*\]\()(\.\./[^)\s]*)(\))")


def folders():
    """{what you type: the notebooks folder}"""
    found = {p.parent.name.replace("Lecture_", ""): p for p in sorted(LECTURE.glob("Lecture_*/notebooks"))}
    found.update({p.parent.name: p for p in sorted(LECTURE.glob("Algorithms/*/notebooks"))})
    return found


def copy_notebook(src, dst):
    """Copy a notebook, bringing its pictures along and pointing other links at the lecture."""
    def picture(match):
        link = match.group(2)
        if link.startswith(("http://", "https://")) or "/" not in link:
            return match.group(0)
        image = (src.parent / link).resolve()
        if not image.exists():
            return match.group(0)
        (dst.parent / "figures").mkdir(parents=True, exist_ok=True)
        shutil.copy2(image, dst.parent / "figures" / image.name)
        return f"{match.group(1)}figures/{image.name}{match.group(3)}"

    def page(match):
        target = os.path.normpath(src.parent / match.group(2).split("#")[0])
        anchor = "#" + match.group(2).split("#", 1)[1] if "#" in match.group(2) else ""
        return f"{match.group(1)}{os.path.relpath(target, dst.parent)}{anchor}{match.group(3)}"

    nb = json.loads(src.read_text())
    for cell in nb["cells"]:
        if cell["cell_type"] == "markdown":
            text = LINK.sub(page, IMAGE.sub(picture, "".join(cell["source"])))
            cell["source"] = text.splitlines(keepends=True)
    dst.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")


def main(which, force=False):
    available = folders()
    key, _, number = which.partition("/")
    chosen = [f for name, folder in available.items() if which == "all" or name == key.zfill(2) or name == key
              for f in sorted(folder.iterdir())
              if f.is_file() and (f.suffix != ".ipynb" or f.name.startswith(number.zfill(2) if number else ""))]
    if not any(f.suffix == ".ipynb" for f in chosen):
        sys.exit(f"nothing matches {which!r}; use all, one of ({', '.join(available)}), or week/number, e.g. 05/02")
    for src in chosen:
        dst = TARGET / src.parent.parent.name / src.name
        if dst.exists() and not force:
            print(f"kept   {dst.relative_to(ROOT)}  (you already have a copy; --force replaces it)")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        copy_notebook(src, dst) if src.suffix == ".ipynb" else shutil.copy2(src, dst)
        print(f"copied {dst.relative_to(ROOT)}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--force"]
    main(args[0] if args else "", force="--force" in sys.argv)
