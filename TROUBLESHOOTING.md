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

### `scripts/dev.py` or `scripts/ghuser.py` says Docker is not running

Do what it says: open Docker Desktop or OrbStack, or run `colima start`.

### A component says `dev: replace`, `dev: restart, replace` or `dev: not deployed`

It was placed from an older `dev.py` build, and stopped rather than run old code.
Replace it from the toolbar; restart Rhino first if it says so. `dev: not deployed`
means `dev.py uninstall` ran: replace it with the installed package's component.

### A component shows twice in Grasshopper

The dev link and an installed `.yak` both load it. `uv run scripts/dev.py status` names
the copy; uninstall the package in the Package Manager while you develop, or run
`dev.py uninstall` before testing the `.yak`.

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
