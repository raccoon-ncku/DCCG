# A0 — Setup

**Due:** by the end of Week 01. Follow [Week 01's lecture](/Lecture/Lecture_01/README.md);
this page is only the checklist.

1. **A GitHub account**, and the [Student Developer Pack](https://education.github.com/pack)
   (free, and it unlocks Copilot).
2. **`uv`, `git` and an editor**: [Week 01 §2](/Lecture/Lecture_01/README.md#2-install).
3. **An AI assistant.** Read the [AI usage policy](/README.md#ai-usage) first.
4. **The repository, with its environment:**
   ```bash
   git clone https://github.com/raccoon-ncku/DCCG.git DCCG
   cd DCCG
   uv sync
   ```
5. **Five green checkpoints:** `uv run check.py 01`.

## Deliverable

```bash
git add -A
git commit -m "Week 01: environment set up"
```

**That commit is A0.** No push and no upload. In Week 02 you set up your fork and push
it: [SETUP ▸ Git for this course](/SETUP.md#git-for-this-course).

Stuck? [Troubleshooting](/TROUBLESHOOTING.md).
