# Put ../algorithms on the import path, so tests can `import smoothing` etc.
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "tutorials"))
