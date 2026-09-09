#!/usr/bin/env python3
"""
DCCG self-check runner.

    uv run check.py            # overview: how far you are in every week
    uv run check.py 03         # work on Week 03 (verbose, with hints)
    uv run check.py 03 -v      # ... and show the full failure output

Every week in Part I and II ships with a set of CHECKPOINTS: small functions
you implement in `checkpoints/tasks.py`, and a matching spec that decides
whether your implementation is right.

The spec is written with `pytest`. You are not expected to understand it yet
-- in Week 10 you will write these yourself, and at that point this runner
stops being magic and becomes something you built. Until then, treat it as an
automatic teaching assistant that is available at 3am and never gets bored.

Three possible states for a checkpoint:

    TODO   you have not implemented it yet (it still raises NotImplementedError)
    FAIL   you implemented it, but it does not behave as specified
    PASS   correct

A FAIL is not a bad grade. It is information -- and it is the whole point.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()

# (week, lecture folder, title). The folder numbers are historical and do not
# match the week numbers -- the course schedule in README.md is the authority.
COURSE = [
    ("00", "Lecture_00", "Toolchain: uv, Zed, git, and an AI assistant"),
    ("01", "Lecture_01", "Python I: values, types, lists, functions"),
    ("02", "Lecture_02", "Python II: control flow, modules, functions"),
    ("04", "Lecture_04", "Python III: dictionaries, files, JSON + AI literacy"),
    ("03", "Lecture_03", "COMPAS core: primitives and transformations"),
    ("06", "Lecture_06", "Software engineering I: the dual-mode architecture"),
    ("08", "Lecture_08", "Object-oriented programming  (self-paced week)"),
    ("07", "Lecture_07", "Recursion and self-similar geometry  (self-paced week)"),
    ("05", "Lecture_05", "Mesh: a real geometric data structure"),
]

# ----------------------------------------------------------------------------
# terminal colours (disabled automatically when piping to a file)
# ----------------------------------------------------------------------------
_TTY = sys.stdout.isatty()


def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _TTY else text


GREEN = lambda s: _c("92", s)   # noqa: E731
RED = lambda s: _c("91", s)     # noqa: E731
YELLOW = lambda s: _c("93", s)  # noqa: E731
BLUE = lambda s: _c("94", s)    # noqa: E731
DIM = lambda s: _c("2", s)      # noqa: E731
BOLD = lambda s: _c("1", s)     # noqa: E731


class _Collector:
    """A small pytest plugin that records the outcome of every checkpoint."""

    def __init__(self) -> None:
        self.results: dict[str, str] = {}   # nodeid -> PASS | FAIL | TODO
        self.hints: dict[str, str] = {}     # nodeid -> first line of docstring
        self.details: dict[str, str] = {}   # nodeid -> failure text
        self.order: list[str] = []

    def pytest_collection_modifyitems(self, items):
        for item in items:
            self.order.append(item.nodeid)
            doc = (item.function.__doc__ or "").strip()
            self.hints[item.nodeid] = doc.split("\n")[0] if doc else item.name

    def pytest_exception_interact(self, node, call, report):
        # NotImplementedError means "not attempted yet", anything else is a real failure.
        if call.excinfo is not None and call.excinfo.errisinstance(NotImplementedError):
            self.results[report.nodeid] = "TODO"

    def pytest_runtest_logreport(self, report):
        if report.when != "call" and not (report.when == "setup" and report.failed):
            return
        if self.results.get(report.nodeid) == "TODO":
            return
        if report.passed:
            self.results[report.nodeid] = "PASS"
        elif report.failed:
            self.results[report.nodeid] = "FAIL"
            self.details[report.nodeid] = str(report.longrepr)


def _purge_modules_under(folder: Path) -> None:
    """Forget any module imported from `folder`.

    Every week's checkpoints use the same file names (`tasks.py`,
    `test_tasks.py`). Python caches imported modules by NAME, so without this
    the second week checked in a single run would silently get the first
    week's `tasks` module -- and pytest would refuse to collect a second
    `test_tasks.py` at all. Clearing the cache between weeks keeps each run
    independent.
    """
    folder = folder.resolve()
    for name, module in list(sys.modules.items()):
        origin = getattr(module, "__file__", None)
        if not origin:
            continue
        try:
            if folder in Path(origin).resolve().parents:
                del sys.modules[name]
        except (OSError, ValueError):  # pragma: no cover - odd __file__ values
            continue


def _run(folder: Path, quiet: bool = True) -> _Collector | None:
    """Run one week's checkpoints and return the collected results."""
    import contextlib
    import io

    import pytest

    cp = folder / "checkpoints"
    if not cp.is_dir():
        return None

    _purge_modules_under(cp)
    collector = _Collector()
    args = [str(cp), "-p", "no:cacheprovider", "--no-header", "-q"]
    if quiet:
        args.append("--tb=no")

    buf = io.StringIO()  # keep pytest's own chatter out of our pretty output
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            pytest.main(args, plugins=[collector])
    finally:
        _purge_modules_under(cp)
        while str(cp) in sys.path:
            sys.path.remove(str(cp))
    return collector


def _bar(done: int, total: int, width: int = 18) -> str:
    if total == 0:
        return DIM("─" * width)
    filled = round(width * done / total)
    body = GREEN("█" * filled) + DIM("░" * (width - filled))
    return body


def overview() -> None:
    print()
    print(BOLD("  DCCG — where you are"))
    print(DIM("  " + "─" * 68))
    first_unfinished = None
    for week, folder, title in COURSE:
        path = ROOT / "Lecture" / folder
        collector = _run(path)
        if collector is None:
            print(f"  W{week}  {DIM('no checkpoints')}   {title}")
            continue
        total = len(collector.order)
        done = sum(1 for v in collector.results.values() if v == "PASS")
        fails = sum(1 for v in collector.results.values() if v == "FAIL")
        if done < total and first_unfinished is None:
            first_unfinished = week
        mark = GREEN("✔") if done == total and total else (RED("✗") if fails else YELLOW("●"))
        counter = f"{done}/{total}"
        print(f"  {BOLD('W' + week)}  {mark} {_bar(done, total)} {counter:>6}  {title}")
    print(DIM("  " + "─" * 68))
    if first_unfinished:
        print(f"  next:  {BLUE('uv run check.py ' + first_unfinished)}")
    else:
        print(f"  {GREEN('All checkpoints passed. ')}")
    print()


def detail(week: str, verbose: bool = False) -> int:
    week = week.lstrip("wW").zfill(2)
    match = [row for row in COURSE if row[0] == week]
    if not match:
        print(RED(f"  No week {week}. Try one of: " + ", ".join(w for w, _, _ in COURSE)))
        return 2
    _, folder, title = match[0]
    path = ROOT / "Lecture" / folder

    print()
    print(BOLD(f"  Week {week} — {title}"))
    editable = sorted(
        f.name for f in (path / "checkpoints").glob("*.py")
        if not f.name.startswith("test_") and f.name != "conftest.py"
    )
    where = path.relative_to(ROOT) / "checkpoints"
    print(DIM(f"  edit: {where}/{{{', '.join(editable)}}}" if len(editable) > 1
              else f"  edit: {where}/{editable[0] if editable else '?'}"))
    print(DIM("  " + "─" * 68))

    collector = _run(path, quiet=not verbose)
    if collector is None:
        print(RED(f"  {path}/checkpoints/ does not exist."))
        return 2

    for nodeid in collector.order:
        state = collector.results.get(nodeid, "TODO")
        hint = collector.hints.get(nodeid, "")
        if state == "PASS":
            print(f"  {GREEN('PASS')}  {hint}")
        elif state == "TODO":
            print(f"  {YELLOW('TODO')}  {hint}")
        else:
            print(f"  {RED('FAIL')}  {BOLD(hint)}")
            if verbose:
                for line in collector.details.get(nodeid, "").splitlines():
                    print(DIM("        " + line))
            else:
                # show just the assertion line -- enough to act on, not overwhelming
                text = collector.details.get(nodeid, "")
                for line in text.splitlines():
                    if line.strip().startswith("E "):
                        print(DIM("        " + line.strip()[2:].strip()))
                        break

    total = len(collector.order)
    done = sum(1 for v in collector.results.values() if v == "PASS")
    print(DIM("  " + "─" * 68))
    print(f"  {_bar(done, total)}  {done}/{total} checkpoints passed")
    if done < total:
        print(DIM("  Re-run this command after each edit. Use -v for full failure output."))
    else:
        print(GREEN("  Week complete. "))
    print()
    return 0 if done == total else 1


def main() -> int:
    args = [a for a in sys.argv[1:]]
    verbose = "-v" in args or "--verbose" in args
    args = [a for a in args if not a.startswith("-")]
    if not args:
        overview()
        return 0
    return detail(args[0], verbose=verbose)


if __name__ == "__main__":
    raise SystemExit(main())
