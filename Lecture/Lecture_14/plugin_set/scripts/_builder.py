"""What scripts/ghuser.py and scripts/dev.py share: the pinned ghuser-builder.

The release is set once, in pyproject.toml [tool.ghuser]. The image is built on
this machine from that release's source, the first time it is needed.
GHUSER_BUILDER_SRC=<path to a checkout> uses that checkout instead (testing a branch).
"""

import io
import os
import subprocess
import sys
import tomllib
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = Path.home() / ".cache" / "ghuser-builder"


def config():
    with open(ROOT / "pyproject.toml", "rb") as f:
        return tomllib.load(f)["tool"]["ghuser"]


def image(cfg):
    return os.environ.get("GHUSER_BUILDER_IMAGE") or f"ghuser-builder:{cfg['builder']}"


def source(cfg):
    """A folder with ghuser-builder at the pinned release: local/ghuser_dev.py, the Dockerfile."""
    if os.environ.get("GHUSER_BUILDER_SRC"):
        return Path(os.environ["GHUSER_BUILDER_SRC"]).resolve()
    tag = f"v{cfg['builder']}"
    folder = CACHE / "src" / tag
    if not (folder / "Dockerfile").exists():
        url = f"{cfg['builder-repo']}/archive/refs/tags/{tag}.zip"
        print(f"ghuser: downloading ghuser-builder {tag} from {url}", flush=True)
        with urllib.request.urlopen(url) as r:
            archive = zipfile.ZipFile(io.BytesIO(r.read()))
        top = archive.namelist()[0].split("/")[0]
        tmp = folder.with_name(tag + ".tmp")
        archive.extractall(tmp)
        (tmp / top).rename(folder)
        tmp.rmdir()
    return folder


def ensure_image(cfg):
    """Build the image once from the pinned source; later runs reuse it."""
    name = image(cfg)
    try:
        found = subprocess.run(["docker", "image", "inspect", name], capture_output=True).returncode == 0
    except FileNotFoundError:
        sys.exit("ghuser: docker not found; install Docker Desktop (or OrbStack, colima) and start it")
    if not found:
        print(f"ghuser: building the image {name} once; this takes a few minutes", flush=True)
        subprocess.run(["docker", "build", "-t", name, str(source(cfg))], check=True)
    return name
