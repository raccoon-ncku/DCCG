# /// script
# requires-python = ">=3.11"
# ///
"""Develop in Grasshopper: components linked to this folder, the core read from src/.

    uv run scripts/dev.py              # build dist-dev/, link it into Grasshopper, reload Rhino
    uv run scripts/dev.py status       # what Grasshopper loads, and what collides
    uv run scripts/dev.py uninstall    # remove the link (before testing your .yak)

Edit src/ and run it again: a running Rhino drops the old core and recomputes the
canvas. Edit components/ and run it again too; a component new to this build
appears after restarting Grasshopper. Runs ghuser-builder's ghuser_dev.py at the
release pinned in pyproject.toml; extra options pass through to it.
"""

import os
import platform
import subprocess
import sys

import _builder

cfg = _builder.config()
os.chdir(_builder.ROOT)
dev = str(_builder.source(cfg) / "local" / "ghuser_dev.py")
command, rest = (sys.argv[1], sys.argv[2:]) if sys.argv[1:2] in (["status"], ["uninstall"]) else ("deploy", sys.argv[1:])
if command == "deploy":
    args = ["deploy", "components", "dist-dev", "--env", "src", "--name", cfg["yak-name"] + "-dev"]
    # ghuser_dev.py builds with the installed Rhino on a Mac, in Docker elsewhere.
    mac_rhino = platform.system() == "Darwin" and os.path.isdir("/Applications/Rhino 8.app")
    if "docker" in rest or ("--builder" not in rest and not mac_rhino):
        args += ["--image", _builder.ensure_image(cfg)]
else:
    args = [command, "dist-dev"]
sys.exit(subprocess.run(["uv", "run", "-q", dev, *args, *rest]).returncode)
