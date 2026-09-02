# A0 — Setup

**Due: Week 01 (2026.09.09), by the end of the session if you can.**

This is the one assignment with no code to write. You are proving that your
machine can run the course, and making your first commit.

The full walkthrough is [Week 01's lecture](/Lecture/Lecture_00/README.md) —
follow that. This page is only the checklist and the deliverable.

## Checklist

1. **A GitHub account.** Register if you don't have one, and apply for the
   [Student Developer Pack](https://education.github.com/pack) while you're
   there — it is free and it unlocks Copilot.
2. **`uv`, `git`, and an editor** installed — see
   [Week 01 §2](/Lecture/Lecture_00/README.md#2-install). Zed is what the
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
   `Lecture/Lecture_00/checkpoints/tasks.py`.

## Deliverable

The push itself:

```bash
git add -A
git commit -m "Week 01: environment set up"
git push
```

That's it. Nothing to submit on Moodle — your commit is the submission.

Stuck? [Troubleshooting](/TROUBLESHOOTING.md), then bring the exact command
and the complete error to Week 02.

---

*The folder is named `0_copilot` for historical reasons — the assignment is no
longer Copilot-specific.*
