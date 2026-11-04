"""Make `src/` importable for the tests when running from the course repo."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
