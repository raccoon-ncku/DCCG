"""Tests for scripts/: what they send to Docker and what they bring back. No Docker needed.

    uv run --no-project --python 3.12 --with pytest pytest scripts/tests

Each script runs as `uv run` would run it, with subprocess.run replaced by a fake
Docker (and uv) that records the commands and plays the builder image's part.
"""

import io
import json
import runpy
import shutil
import subprocess
import sys
import tarfile
import tomllib
from pathlib import Path

import pytest

TEMPLATE = Path(__file__).resolve().parents[2]
FILES = ["pyproject.toml", "yak.json", "icon.png", "components", "src", "tests", "scripts/_builder.py",
         "scripts/dev.py", "scripts/ghuser.py"]
CFG = tomllib.loads((TEMPLATE / "pyproject.toml").read_text(encoding="utf-8"))["tool"]["ghuser"]
IMAGE = f"ghuser-builder:{CFG['builder']}"
YAK = f"{CFG['yak-name']}-0.1.0-rh8_0-any.yak"


def files_under(root, folder):
    return [str(p.relative_to(root)).replace("\\", "/") for p in (root / folder).rglob("*")
            if p.is_file() and "__pycache__" not in p.parts]


@pytest.fixture
def project(tmp_path, monkeypatch):
    """A copy of the template, with the clutter a real checkout has."""
    root = tmp_path / "project"
    for f in FILES:
        src, dst = TEMPLATE / f, root / f
        if not src.exists():
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
        else:
            shutil.copy2(src, dst)
    (root / ".venv").mkdir()
    (root / ".venv" / "junk").write_text("not sent")
    core = root / CFG["yak-include"][0].split(":")[0]
    (core / "__pycache__").mkdir()
    (core / "__pycache__" / "x.cpython-39.pyc").write_bytes(b"not sent")
    (root / "dist" / "ghuser").mkdir(parents=True)
    (root / "dist" / "ghuser" / "Removed.ghuser").write_text("from an older build")
    source = tmp_path / "ghuser-builder"
    (source / "local").mkdir(parents=True)
    (source / "Dockerfile").write_text("FROM scratch\n")
    (source / "local" / "ghuser_dev.py").write_text("")
    monkeypatch.setenv("GHUSER_BUILDER_SRC", str(source))
    for var in ("GHUSER_BUILDER_IMAGE", "DOCKER_HOST"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.syspath_prepend(str(root / "scripts"))
    sys.modules.pop("_builder", None)
    return root


class FakeDocker:
    """subprocess.run, as Docker (and uv) would answer it."""

    def __init__(self, running=True, image=True, context="colima unix:///Users/me/.colima/default/docker.sock",
                 build_fails=False):
        self.running, self.image, self.context, self.build_fails = running, image, context, build_fails
        self.calls, self.sent = [], None

    def __call__(self, cmd, input=None, **kwargs):
        self.calls.append(list(cmd))
        done = lambda code=0, out=b"": subprocess.CompletedProcess(cmd, code, out if not kwargs.get("text") else out.decode(), "")  # noqa: E731
        if cmd[0] == "uv":
            return done()
        if cmd[0] != "docker":
            raise FileNotFoundError(cmd[0])
        if cmd[1] == "--version":
            return done()
        if cmd[1:3] == ["context", "inspect"]:
            return done(0, self.context.encode())
        if cmd[1] == "info":
            return done(0 if self.running else 1)
        if cmd[1:3] == ["image", "inspect"]:
            return done(0 if self.image else 1)
        if cmd[1] == "build":
            self.image = True
            return done()
        if cmd[1] == "run":
            self.sent = sorted(m.name for m in tarfile.open(fileobj=io.BytesIO(input)).getmembers() if m.isfile())
            if self.build_fails:
                return done(2)
            back = io.BytesIO()
            with tarfile.open(fileobj=back, mode="w") as tar:
                for name, data in (("ghuser/Built.ghuser", b"built"), (YAK, b"yak")):
                    info = tarfile.TarInfo(name)
                    info.size = len(data)
                    tar.addfile(info, io.BytesIO(data))
            return done(0, back.getvalue())
        raise AssertionError(f"unexpected docker call {cmd}")

    def run_call(self):
        return next(c for c in self.calls if c[:2] == ["docker", "run"])


def run_script(project, monkeypatch, name, *args, docker=None):
    """Run scripts/<name> with argv, from another folder (it must not matter); return its exit code."""
    docker = docker or FakeDocker()
    monkeypatch.setattr(subprocess, "run", docker)
    monkeypatch.setattr(sys, "argv", [str(project / "scripts" / name), *args])
    monkeypatch.chdir(project.parent)
    try:
        runpy.run_path(str(project / "scripts" / name), run_name="__main__")
    except SystemExit as e:
        return e.code
    return 0


# --- ghuser.py: the .yak ---------------------------------------------------------


def test_ghuser_sends_what_the_build_reads_and_nothing_else(project, monkeypatch):
    docker = FakeDocker()
    assert run_script(project, monkeypatch, "ghuser.py", "--version", "0.1.0", docker=docker) == 0
    includes = [i.split(":")[0] for i in CFG["yak-include"]]
    icon = json.loads((project / "yak.json").read_text()).get("icon")
    assert docker.sent == sorted(files_under(project, "components") + [f for i in includes for f in files_under(project, i)]
                                 + ["yak.json"] + ([icon] if icon else []))
    run = docker.run_call()
    assert "-v" not in run, "the project is sent as a tar stream, never mounted"
    image = run.index(IMAGE)
    assert run[image + 1:image + 5] == ["sh", "-c", run[image + 3], "sh"]
    command = ["ghuser-build", "--yak", CFG["yak-name"]]
    for include in CFG["yak-include"]:
        command += ["--yak-include", include]
    assert run[image + 5:] == command + ["--version", "0.1.0", "components", "out"]
    for var in ("GHUSER_VERSION", "GITHUB_REF_TYPE", "GITHUB_REF_NAME", "GITHUB_RUN_NUMBER"):
        assert var in run[:image]


def test_ghuser_replaces_dist_ghuser_and_keeps_other_yaks(project, monkeypatch):
    older = project / "dist" / YAK.replace("0.1.0", "0.0.9")
    older.write_text("an older release")
    assert run_script(project, monkeypatch, "ghuser.py", "--version", "0.1.0") == 0
    assert sorted(p.name for p in (project / "dist" / "ghuser").iterdir()) == ["Built.ghuser"]
    assert (project / "dist" / YAK).read_bytes() == b"yak"
    assert older.exists()


def test_a_failed_build_returns_its_code_and_leaves_dist_alone(project, monkeypatch):
    assert run_script(project, monkeypatch, "ghuser.py", docker=FakeDocker(build_fails=True)) == 2
    assert (project / "dist" / "ghuser" / "Removed.ghuser").exists()


def test_the_image_is_built_once_from_the_pinned_source(project, monkeypatch, tmp_path):
    docker = FakeDocker(image=False)
    assert run_script(project, monkeypatch, "ghuser.py", docker=docker) == 0
    builds = [c for c in docker.calls if c[:2] == ["docker", "build"]]
    assert builds == [["docker", "build", "-t", IMAGE, str(tmp_path / "ghuser-builder")]]
    docker.calls.clear()
    assert run_script(project, monkeypatch, "ghuser.py", docker=docker) == 0
    assert not [c for c in docker.calls if c[:2] == ["docker", "build"]]


# --- dev.py: the linked dev build -------------------------------------------------


def uv_call(docker):
    return next(c for c in docker.calls if c[0] == "uv")


def test_dev_deploys_with_the_pinned_tools_and_image(project, monkeypatch, tmp_path):
    docker = FakeDocker()
    assert run_script(project, monkeypatch, "dev.py", docker=docker) == 0
    tool = str(tmp_path / "ghuser-builder" / "local" / "ghuser_dev.py")
    assert uv_call(docker) == ["uv", "run", "-q", tool, "deploy", "components", "dist-dev", "--env", "src",
                               "--name", CFG["yak-name"] + "-dev", "--image", IMAGE]


@pytest.mark.parametrize("command", ["status", "uninstall"])
def test_dev_status_and_uninstall_need_no_docker(project, monkeypatch, command):
    docker = FakeDocker(running=False)
    assert run_script(project, monkeypatch, "dev.py", command, docker=docker) == 0
    assert uv_call(docker)[4:] == [command, "dist-dev"]
    assert not [c for c in docker.calls if c[0] == "docker"]


def test_dev_with_the_rhino_builder_needs_no_docker(project, monkeypatch):
    docker = FakeDocker(running=False)
    assert run_script(project, monkeypatch, "dev.py", "--builder", "rhino", docker=docker) == 0
    assert "--image" not in uv_call(docker) and uv_call(docker)[-2:] == ["--builder", "rhino"]


def test_options_pass_through_to_the_dev_tool(project, monkeypatch):
    docker = FakeDocker()
    assert run_script(project, monkeypatch, "dev.py", "--no-reload", docker=docker) == 0
    assert uv_call(docker)[-1] == "--no-reload"


# --- which Docker, and what to do when it is not running ---------------------------


@pytest.mark.parametrize("context, host, system, kind, hint", [
    ("colima unix:///Users/me/.colima/default/docker.sock", "", "Darwin", "colima", "colima start"),
    ("colima-work unix:///Users/me/.colima/work/docker.sock", "", "Darwin", "colima", "colima start -p work"),
    ("", "unix:///Users/me/.colima/lab/docker.sock", "Darwin", "colima", "colima start -p lab"),
    ("desktop-linux unix:///Users/me/.docker/run/docker.sock", "", "Darwin", "Docker Desktop", "open Docker Desktop"),
    ("desktop-linux npipe:////./pipe/dockerDesktopLinuxEngine", "", "Windows", "Docker Desktop", "open Docker Desktop"),
    ("default npipe:////./pipe/docker_engine", "", "Windows", "Docker Desktop", "open Docker Desktop"),
    ("orbstack unix:///Users/me/.orbstack/run/docker.sock", "", "Darwin", "OrbStack", "open OrbStack"),
    ("default unix:///var/run/docker.sock", "", "Linux", "Docker", "start the Docker daemon"),
])
def test_a_stopped_docker_says_how_to_start_it(project, monkeypatch, capsys, context, host, system, kind, hint):
    if host:
        monkeypatch.setenv("DOCKER_HOST", host)
    import platform
    monkeypatch.setattr(platform, "system", lambda: system)
    code = run_script(project, monkeypatch, "ghuser.py", docker=FakeDocker(running=False, context=context))
    assert code == f"ghuser: {kind} is not running; " + code.split("; ", 1)[1]
    assert hint in code


def test_no_docker_at_all(project, monkeypatch):
    def missing(cmd, **kwargs):
        raise FileNotFoundError(cmd[0])
    monkeypatch.setattr(subprocess, "run", missing)
    monkeypatch.setattr(sys, "argv", ["ghuser.py"])
    with pytest.raises(SystemExit) as e:
        runpy.run_path(str(project / "scripts" / "ghuser.py"), run_name="__main__")
    assert str(e.value.code).startswith("ghuser: docker not found")
