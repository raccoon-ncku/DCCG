# /// script
# requires-python = ">=3.11"
# ///
"""Build the shippable package: components/ -> dist/ghuser/*.ghuser + dist/*.yak.

    uv run scripts/ghuser.py                    # version 0.0.0-dev.0
    uv run scripts/ghuser.py --version 0.1.0    # the version you release

The core is copied into the .yak (lib/), so the .yak is all a user installs. Runs
ghuser-build in Docker, the same as CI; any ghuser-build option passes through.
"""

import json
import sys

import _builder

cfg = _builder.config()
includes = cfg.get("yak-include", [])
# What the build reads, and nothing else: the components, the included core, the
# package description and the icon it names.
files = ["components", *(i.split(":")[0] for i in includes)]
if (_builder.ROOT / "yak.json").exists():
    files.append("yak.json")
    icon = json.loads((_builder.ROOT / "yak.json").read_text(encoding="utf-8")).get("icon")
    if icon:
        files.append(icon)
command = ["ghuser-build", "--yak", cfg["yak-name"]]
for include in includes:
    command += ["--yak-include", include]
command += [*sys.argv[1:], "components"]
# In CI, ghuser-build takes the version from the tag.
env = ("GHUSER_VERSION", "GITHUB_REF_TYPE", "GITHUB_REF_NAME", "GITHUB_RUN_NUMBER")
sys.exit(_builder.run_image(_builder.ensure_image(cfg), command, files, "dist", env))
