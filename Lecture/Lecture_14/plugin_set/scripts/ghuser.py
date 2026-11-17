# /// script
# requires-python = ">=3.11"
# ///
"""Build the shippable package: components/ -> dist/ghuser/*.ghuser + dist/*.yak.

    uv run scripts/ghuser.py                    # version 0.0.0-dev.0
    uv run scripts/ghuser.py --version 0.1.0    # the version you submit or release

The core is copied into the .yak (lib/), so the .yak is all a user installs. Runs
ghuser-build in Docker, the same as CI; any ghuser-build option passes through.
"""

import os
import subprocess
import sys

import _builder

cfg = _builder.config()
cmd = ["docker", "run", "--rm", "-v", f"{_builder.ROOT}:/work", "-w", "/work", "-e", "HOME=/tmp"]
if hasattr(os, "getuid"):  # files in dist/ belong to you, not root (not on Windows)
    cmd += ["-u", f"{os.getuid()}:{os.getgid()}"]
for name in ("GHUSER_VERSION", "GITHUB_REF_TYPE", "GITHUB_REF_NAME", "GITHUB_RUN_NUMBER"):
    cmd += ["-e", name]  # in CI, ghuser-build takes the version from the tag
cmd += [_builder.ensure_image(cfg), "ghuser-build", "--yak", cfg["yak-name"]]
for include in cfg.get("yak-include", []):
    cmd += ["--yak-include", include]
cmd += [*sys.argv[1:], "components", "dist"]
sys.exit(subprocess.run(cmd).returncode)
