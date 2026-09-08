# MyWork/ — your namespace

This folder is yours. The instructor promises to **never add, edit, or delete
files inside it**, so `git pull upstream main` will never create a merge
conflict here.

Put in it:

- Weekly notes (`week03-notes.md`, sketches of what you learned)
- Practice code — variations on the checkpoints, things you want to try
- Scratch scripts that don't belong in `Lecture/…/`
- One-liners you want to keep, a diary of what you tried, a list of things
  that confused you

The idea is that by Week 18 this folder — plus your commit history — is a
record of what you did this term, kept in the same repo as the material you
learned from.

## Rules

1. **This folder is tracked** — everything you commit here goes to your fork
   and is part of the record. That's the point.
2. **Nothing else is off-limits to you** — you edit `Lecture/…/checkpoints/tasks.py`
   as normal. This folder is just where your *own* stuff lives.
3. **For truly private files** that should never leave your laptop
   (half-baked ideas, private diary, sensitive data), use a folder named
   `Notes/` at the repo root — it's in `.gitignore`, so git will not track
   it. But then it also doesn't get pushed and doesn't survive a re-clone.

## Where to learn more

- [rccn wiki ▸ Git for coursework](https://kb.rccn.dev/computation/development-environment/version-control/coursework-git) — the fork-and-pull loop, and the failure catalogue for what goes wrong.
- Course [`SETUP.md`](../SETUP.md#git-for-this-course) — the four commands you need.
