# Ensures the SPEC files in `spec/` can import from the student's file(s)
# in this directory (`tasks.py`, or `core.py`/`runner.py` in Week 06).
#
# Pytest normally puts each test file's parent dir on sys.path. Moving the
# spec into `spec/` breaks that link -- this bridges it back.
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
