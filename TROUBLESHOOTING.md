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

### Still stuck

Open an issue on the course repo with the **exact** command you ran and the
**complete** error output. "It doesn't work" is unanswerable; a traceback is
usually self-answering, and pasting one is how you learn to read them.
