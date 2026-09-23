# A0 — Setup

**Due:** by the end of Week 01. If you don't finish in the session, finish
before Week 02 — checkpoints stack on it. See the [schedule](/README.md#schedule-2026-fall)
for dates.

This is the one assignment with no code to write. You are proving that your
machine can run the course, and making your first commit.

The full walkthrough is [Week 01's lecture](/Lecture/Lecture_01/README.md) —
follow that. This page is only the checklist and the deliverable.

## Checklist

1. **A GitHub account.** Register if you don't have one, and apply for the
   [Student Developer Pack](https://education.github.com/pack) while you're
   there — it is free and it unlocks Copilot.
2. **`uv`, `git`, and an editor** installed — see
   [Week 01 §2](/Lecture/Lecture_01/README.md#2-install). Zed is what the
   course uses; the editor is the one tool here you may substitute.
3. **An AI assistant**, one of:
   - Zed's built-in assistant (sign in with GitHub; the free tier is enough)
   - GitHub Copilot (free for students, via the pack above)
   - Claude Code / Codex CLI — we use these properly in Weeks 11–14; you do
     not need one yet

   You are *expected* to use it. Read the
   [AI usage policy](/README.md#ai-usage) before you do — the rules are short,
   and they hold from today.
4. **The repository cloned and the environment built:**
   ```bash
   git clone https://github.com/raccoon-ncku/DCCG.git DCCG
   cd DCCG
   uv sync
   ```
5. **Five green checkpoints:**
   ```bash
   uv run check.py 01
   ```
   Four of these check your machine. The fifth asks you to edit one line in
   `Lecture/Lecture_01/checkpoints/tasks.py`.

## Deliverable — Week 01

Commit locally. No push this week; you do not have a fork yet.

```bash
git add -A
git commit -m "Week 01: environment set up"
```

**That commit is A0.** No Moodle upload — the commit itself is the record.

## Then — Week 02, first ten minutes

We set up your fork on GitHub together and push that commit for the first
time. If you want to do it ahead of class, the full instructions are in
[SETUP.md ▸ Git for this course](/SETUP.md#git-for-this-course) and the
[wiki page on coursework git](https://kb.rccn.dev/computation/development-environment/version-control/coursework-git).

The short version:

```bash
# on GitHub, one click: fork raccoon-ncku/DCCG to <your-username>/DCCG
# then, in your terminal:
git remote add upstream https://github.com/raccoon-ncku/DCCG.git
git remote set-url origin https://github.com/<your-username>/DCCG.git
git push -u origin main
```

From then on: `git pull upstream main` weekly for new material,
`git push` to your fork for your own work. Your notes and practice live in
[`MyWork/`](/MyWork/README.md).

Stuck? [Troubleshooting](/TROUBLESHOOTING.md), then bring the exact command
and the complete error to Week 02.

---

*The folder is named `0_copilot` for historical reasons — the assignment is no
longer Copilot-specific.*
