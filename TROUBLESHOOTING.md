# Troubleshooting

For setup and commands, see [SETUP.md](SETUP.md).

### `ModuleNotFoundError: No module named 'compas'`

You ran `python foo.py` instead of `uv run foo.py`.

### `uv: command not found`

Close the terminal and open a new one. If it persists, the `uv` installer printed a
line to add to your shell profile.

### The environment is broken in some way you can't name

```bash
rm -rf .venv && uv sync
```

### A viewer window crashes or refuses to open

A graphics-driver problem, not a Python one. Every checkpoint can be done without a
viewer: write `output/*.json` and preview it separately.

### A 3D view in a notebook stays blank

Open the notebook in JupyterLab in a browser (`uv run jupyter lab`). The compas_timber
notebooks need `uv run --extra timber jupyter lab`.

### `scripts/ghuser` says "no components directory", or misses a new component

Docker cannot see the folder: keep the project under your home directory. On colima, a
folder you have just added can take a minute to appear; check the `(N components)` line.

### A checkpoint says `PASS` on code you don't understand

That is not success. Try it yourself, ask the AI, then diff the two.

### Git said something scary

- **Merge conflict on `git pull`:** the instructor changed a file you also changed.
- **`git push` rejected as non-fast-forward:** pull first, then push.
- **Authentication failed:** you need a personal access token or an SSH key.
- **Committed a `.env` or an API key:** rotate the secret first, then remove the file.
- **Committed to the wrong branch:** `cherry-pick`, then reset.

The three-line recovery for each is on the
[wiki](https://kb.rccn.dev/computation/development-environment/version-control/coursework-git#what-can-go-wrong).

### Still stuck

Open an issue with the **exact** command and the **complete** error output.
