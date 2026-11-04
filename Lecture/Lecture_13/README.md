# Week 13 — Review

Tests answer one question. Review answers the others.

| Question | Who answers it |
| --- | --- |
| Is it **correct**? | the tests (automated) |
| Is it **good**: clear names, sane structure, no waste? | a reviewer |
| Was the **spec itself** right? | a reviewer |

## 1. Correct is not good

Open two files side by side:

- [`wall.py`](wall.py) — a first draft, exactly as a small language model
  produced it ([Week 15](/Lecture/Lecture_15/README.md#part-b--put-it-in-your-pipeline) shows how). It passes `test_wall.py`. It is also ~150 lines of the model arguing with itself in
  comments, re-deriving the same offset five times.
- [`plugin_set/src/compas_studio/wall.py`](/Lecture/Lecture_14/plugin_set/src/compas_studio/wall.py)
  — the reviewed version. Same behaviour, same passing tests, 20 readable lines.

**The tests cannot tell these apart. A reviewer can.** "The AI wrote it" is not a
defence: if you submitted it, you reviewed it, and you own it.

### A review checklist

Whether the author is a classmate or an agent, review the same way:

1. **Spec first.** Does it do what was asked — exactly, including units and edge
   cases (0 steps? a wall shorter than one brick?).
2. **Read for intent.** Can you explain every line? If not, the code is unclear
   or you do not yet understand the problem — both are blockers.
3. **Names and structure.** Would a stranger understand it? Is logic separated
   from IO? Is anything computed twice?
4. **Trust nothing implicit.** Magic numbers, silent unit assumptions, unhandled
   failure paths — this is where geometry bugs hide.
5. **Verify independently.** Run the tests yourself; open the artifact; measure
   something. Do not take the author's word, or the agent's.

## 2. Where review actually happens: git and pull requests

Even working alone:

```bash
git switch -c feature/canopy-component      # never work on main
# ... write the test, write the core, commit in small steps ...
git add -A && git commit -m "canopy: taper radius toward the apex"
git push -u origin feature/canopy-component
```

Then open a **pull request** on GitHub. The PR is the unit of review:

- it shows a **diff** — the exact change, reviewable line by line, by you or a
  teammate, *before* it becomes permanent;
- CI runs the tests on it automatically (your project's `test.yml`) and marks it red or green;
- the **artifact changes in the diff too** — a reviewer sees not just the code
  but what the geometry *became*, because the committed `.json`/`.ghuser`
  changed;
- nothing reaches `main` until tests pass and a human approves.

The loop is the same whether the author is a classmate, you last month, or an
agent. Write commit messages that say **why**; the diff already shows what:

```
bad:   "update"   "fixed stuff"   "changes to wall.py"
good:  "wall: place only full bricks; half-bricks were sticking past length"
```

### The review process, as steps

1. **Author:** one change per pull request, small enough to read in ten
   minutes. Say in the description *what* it is for and *how you checked it*.
2. **Reviewer:** check out the branch and **run it**: the tests, then the
   thing itself. A review of code you did not run is a review of its
   formatting.
3. **Reviewer:** read the diff against the checklist above. Comment on the
   line, and say what you would do instead, or ask the question you could
   not answer.
4. **Author:** answer every comment, with a change or with a reason. Push to
   the same branch; the PR updates.
5. **Merge** when the tests are green *and* the reviewer can explain the
   change to a third person.

In Week 13 you do this in pairs, on each other's final-project repos: one
real change each, opened as a pull request, reviewed by the other.
