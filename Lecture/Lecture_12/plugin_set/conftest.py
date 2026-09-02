"""
Make `src/` importable when running the tests locally, so `uv run pytest`
works straight from this folder without a separate install step.

In CI (see .github/workflows/test.yml) we instead do the real thing --
`pip install -e .` -- because that is how the package will actually be
installed by anyone who uses it. This file is only a local convenience.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
