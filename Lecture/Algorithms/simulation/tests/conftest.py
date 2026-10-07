# Put ../tutorials on the import path, so tests can `import boids` etc.
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "tutorials"))
