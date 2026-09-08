# Troubleshooting

The handful of problems that account for almost every "it doesn't work" in this
course. For setup and commands, see [SETUP.md](SETUP.md).

### `ModuleNotFoundError: No module named 'compas'`

You ran `python foo.py` instead of `uv run foo.py`. This is the single most
common error in the course. Always `uv run`.

### `uv: command not found`

Your terminal hasn't picked up the new PATH. Close it and open a new one. If it
persists, the `uv` installer printed a line to add to your shell profile — add
it.

### The environment is broken in some way you can't name

Rebuild it. This is fast and is not a defeat:

```bash
rm -rf .venv && uv sync
```

### A viewer window crashes or refuses to open

A graphics-driver problem, not a Python one. Every checkpoint in this course can
be completed headlessly, and from Week 06 the JSON artifact is the primary
output anyway. Write a headless runner that saves `output/*.json` and preview it
separately.

### A checkpoint says `PASS` on code you don't understand

That's not success. In Weeks 11–14 your job becomes reviewing exactly this kind
of code, and code you can't explain will cost you there. Try it yourself, then
ask the AI, then diff the two and work out who was right.

### Git said something scary

Not scary — solvable. Every common failure mode has a named recovery:

- **Merge conflict on `git pull`** — the instructor changed a file you also
  changed. Not a bug; a moment where git needs your decision.
- **`git push` rejected as non-fast-forward** — your fork moved ahead of your
  clone. Pull first, then push.
- **Authentication failed** — GitHub removed password login; you need a
  personal access token or an SSH key.
- **Accidentally committed a `.env` or an API key** — rotate the secret first,
  then remove the file from tracking.
- **"I committed to the wrong branch"** — `cherry-pick`, then reset.

Full list with the three-line recovery for each is on the wiki:
[rccn wiki ▸ Git for coursework ▸ What can go wrong](https://kb.rccn.dev/computation/development-environment/version-control/coursework-git#what-can-go-wrong).
It is worth reading once now, before you need it.

For the fork-based workflow itself (why `upstream` and `origin` are separate,
where `MyWork/` fits), see [SETUP.md ▸ Git for this course](SETUP.md#git-for-this-course).

### Still stuck

Open an issue on the course repo with the **exact** command you ran and the
**complete** error output. "It doesn't work" is unanswerable; a traceback is
usually self-answering, and pasting one is how you learn to read them.
