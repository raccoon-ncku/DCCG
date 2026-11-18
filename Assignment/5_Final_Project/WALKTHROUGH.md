# From the template to a .yak

The session of 2026.11.18. You start your final project from
[ghuser-template](https://github.com/rccn-dev/ghuser-template), take it once through
every stage (spec, core, Grasshopper, `.yak`, release), and see a finished project:
[brick-screen](https://github.com/rccn-dev/brick-screen). Then the [brief](README.md).

You need: a GitHub account, git, [uv](https://docs.astral.sh/uv/), Rhino 8 (open the
ScriptEditor once), and Docker running ([Setup](/SETUP.md)).

## 1. A repository of your own

On [ghuser-template](https://github.com/rccn-dev/ghuser-template), click **Use this
template**, name it, keep it public. Then:

```bash
git clone https://github.com/<you>/<name> ~/code/<name>
cd ~/code/<name>
uv sync
uv run pytest            # 72 passed
uv run scripts/dev.py    # start it now: the first run builds the builder image, a few minutes
```

On GitHub, **Actions** shows two workflows: `tests` and `build-ghuser`. Both turn green
on every push.

## 2. One feature, end to end

The template ships six sample components in a "My Tool" tab, one Grasshopper feature
each ([the list](https://github.com/rccn-dev/ghuser-template#the-samples)). Read **Span
Check** in this order:

| File | What it is |
| --- | --- |
| `src/my_tool/spans.py` | the core: a list of numbers in, a `SpanReport` out. No Rhino |
| `tests/test_spans.py` | the spec: what a client would say about it, as tests |
| `components/Mt_SpanCheck/metadata.json` | the component: its tab, panel, inputs (`"list"` access) and outputs |
| `components/Mt_SpanCheck/code.py` | the adapter: convert, call the core, convert back, warn |

The rule that holds it together: **`src/` never imports Rhino, and `components/`
never contains logic.**

## 3. Red, green, refactor

Span Check should also say how far each span is over the limit. Write the test
first, at the end of `tests/test_spans.py`:

```python
def test_excess_is_how_far_each_span_is_over_the_limit():
    assert check_spans([4.0, 9.0, 8.0], limit=7.5).excess == pytest.approx([0.0, 1.5, 0.5])
```

`uv run pytest`: **red**, `AttributeError`. Good: the test can fail. Now the core, in
`src/my_tool/spans.py`: add `excess` to `SpanReport` and return
`[max(0.0, s - limit) for s in spans]` for it. `uv run pytest`: **green**, 73 passed.
Tidy if anything is untidy, run it again, commit.

## 4. See it in Grasshopper

`dev.py` from step 1 has linked the components into Grasshopper. Restart Rhino: the
**My Tool** tab has four panels. Place Span Check, feed `spans` a Panel with one number
per line and `limit` a slider.

Now give it an `excess` output: add it to `outputParameters` in `metadata.json` and run
`uv run pytest`. It fails: `returns 4 values for 5 outputs`. Return `report.excess` as
the fifth value in `code.py`, and it passes. Run `uv run scripts/dev.py` after every
edit; what else to do depends on what you edited:

| You edit | Then |
| --- | --- |
| `src/` | nothing: the canvas recomputes |
| a `code.py` | replace that component on the canvas |
| a `metadata.json` or `icon.png` | restart Rhino, then replace it |

A component older than your last `dev.py` turns red and says which (`dev: replace`,
`dev: restart, replace`). The placed component keeps the code it was placed with,
even in a saved file.

## 5. Ship a .yak

```bash
uv run scripts/dev.py uninstall            # the dev link and the package must not both load
uv run scripts/ghuser.py --version 0.1.0   # dist/my-tool-0.1.0-rh8_0-any.yak
```

Drag the `.yak` onto Rhino, restart, and place Span Check from the tab: it now runs
from the package, core inside. This file is what you submit. Uninstall it in the
Package Manager before going back to `dev.py`.

## 6. Release from CI

```bash
git push
git tag v0.1.0 && git push --tags
```

CI tests, builds, and attaches the `.yak` to a Release on GitHub. The tag is the version.

## 7. What finished looks like

[**brick-screen**](https://github.com/rccn-dev/brick-screen) is a final project done
to the bar: a brick screen whose bricks turn towards attractors, with a check that
turned bricks do not collide. Look at:

- its README: install, use, run without Rhino; pictures of both modes;
- `git log --reverse --oneline`: the steps above, in order, the spec committed red;
- `tests/test_check.py`: a result you would not guess from a picture;
- `runner.py` and `output/screen.json`: the artifact, one brick per line, kept honest by a test;
- `examples/`: the core used outside Rhino, inputs written in code, shown in compas_viewer
  (`uv run --group viewer examples/02_too_tight.py`);
- `components/`: `Brick` objects passed from one component to the next;
- `log.md`: how AI was used, what was verified, a reflection.

## 8. The final project

The [brief](README.md): a Python Grasshopper plugin, professional, reproducible and
maintainable. Started from this template, submitted as a `.yak`.

**Before next week (11.25):** make the template yours (its README lists the four things
to rename; delete the samples you do not need), and prepare a 2-minute pitch: what it
does, who would use it, and the signature of its core function.
