"""What scripts/ghuser.py and scripts/dev.py share: the pinned ghuser-builder.

The release is set once, in pyproject.toml [tool.ghuser]. The image is built on
this machine from that release's source, the first time it is needed.
GHUSER_BUILDER_SRC=<path to a checkout> uses that checkout instead (testing a branch).

Files go into the container and come back as a tar stream, not through a shared
folder: colima's default sharing (sshfs) can serve a file you just saved in its
old version, and this way every Docker builds exactly what is on disk.
"""

import io
import os
import platform
import shutil
import subprocess
import sys
import tarfile
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


def runtime():
    """Which Docker the docker command talks to: Docker Desktop, colima, OrbStack or another."""
    host = os.environ.get("DOCKER_HOST", "")
    name = ""
    if not host:
        r = subprocess.run(["docker", "context", "inspect", "--format", "{{.Name}} {{.Endpoints.docker.Host}}"],
                           capture_output=True, text=True)
        name, _, host = r.stdout.strip().partition(" ")
    if ".colima" in host or name.startswith("colima"):
        # ~/.colima/<profile>/docker.sock; the profile is what `colima start -p` takes
        profile = host.split(".colima")[-1].strip("/").split("/")[0] if ".colima" in host else "default"
        return "colima", profile
    if "orbstack" in (name + host).lower():
        return "OrbStack", None
    if name == "desktop-linux" or "dockerDesktop" in host or "/.docker/run/" in host:
        return "Docker Desktop", None
    if platform.system() == "Windows" and "docker_engine" in host:
        return "Docker Desktop", None
    return "Docker", None


def start_hint(kind, profile):
    if kind == "colima":
        return "start it: colima start" + ("" if profile in (None, "default") else f" -p {profile}")
    if kind == "Docker Desktop":
        return "open Docker Desktop and wait until it says Engine running"
    if kind == "OrbStack":
        return "open OrbStack"
    return "start the Docker daemon"


def check_docker(name):
    """Docker is installed and running; stop with what to do if not. Returns whether the image is there."""
    try:
        subprocess.run(["docker", "--version"], capture_output=True)
    except FileNotFoundError:
        sys.exit("ghuser: docker not found. Install Docker Desktop"
                 + (" (or OrbStack, or colima)" if platform.system() == "Darwin" else "") + ", then start it")
    if subprocess.run(["docker", "info"], capture_output=True).returncode:
        kind, profile = runtime()
        sys.exit(f"ghuser: {kind} is not running; {start_hint(kind, profile)}")
    return subprocess.run(["docker", "image", "inspect", name], capture_output=True).returncode == 0


# In the container: unpack stdin into a fresh folder, run the command, send out/ back.
IN_IMAGE = 'set -e; mkdir -p /tmp/work; cd /tmp/work; tar -xf -; "$@" >&2; tar -cf - -C out .'


def run_image(name, command, files, out, env=()):
    """Run command (which writes to out) in the image on a copy of files; replace out/ghuser with its result."""
    def no_caches(info):
        parts = info.name.split("/")
        return None if "__pycache__" in parts or parts[-1] == ".DS_Store" or info.name.endswith(".pyc") else info

    sent = io.BytesIO()
    with tarfile.open(fileobj=sent, mode="w") as tar:
        for f in files:
            tar.add(ROOT / f, arcname=f, filter=no_caches)
    cmd = ["docker", "run", "-i", "--rm", "-e", "HOME=/tmp"]
    for var in env:
        cmd += ["-e", var]
    run = subprocess.run([*cmd, name, "sh", "-c", IN_IMAGE, "sh", *command, "out"],
                         input=sent.getvalue(), stdout=subprocess.PIPE)
    if run.returncode:
        return run.returncode
    shutil.rmtree(ROOT / out / "ghuser", ignore_errors=True)
    with tarfile.open(fileobj=io.BytesIO(run.stdout)) as tar:
        extra = {"filter": "data"} if hasattr(tarfile, "data_filter") else {}
        tar.extractall(ROOT / out, **extra)
    return 0


def ensure_image(cfg):
    """Check Docker, then build the image once from the pinned source; later runs reuse it."""
    name = image(cfg)
    if not check_docker(name):
        print(f"ghuser: building the image {name} once; this takes a few minutes", flush=True)
        subprocess.run(["docker", "build", "-t", name, str(source(cfg))], check=True)
    return name
