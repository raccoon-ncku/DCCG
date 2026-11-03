# Lab: You Are the Planner and the Reviewer

A required, **ungraded** milestone (Weeks 15→17), checked for completion on GitHub.
You do **not** write the geometry code. You direct the coder/reviewer workflow from
Lecture 11 to produce a small COMPAS artifact: the brief, the reviews and the judgment
are yours.

## Task

Use `Lecture/Lecture_11/04_coder_reviewer.py` to produce a geometric
structure of your choice (tower, arch, wall bond, ramp, canopy...). It must
be built from at least 20 boxes and have some non-trivial logic (a pattern,
a curve, a rhythm — not a plain grid).

## Process (this is the actual assignment)

1. **Plan.** Write a brief in `brief.md`. Be precise: counts, dimensions,
   units, arrangement rules. A vague brief is the #1 cause of bad results.
2. **Run the loop.** Use the human gate (do NOT use `--auto`): read every
   version of the code before allowing it to run. Reject with written
   feedback at least once, even if the code looks acceptable — you need the
   experience of steering.
3. **Log.** Keep an iteration log in `log.md`: for each round, one or two
   lines on what the coder did, what crashed or what the reviewer agent
   flagged, and what feedback (yours or the agent's) changed the outcome.
4. **Review.** When the loop approves (or exhausts its rounds), do the senior
   review yourself: open the final script and annotate at least three points
   with `# REVIEW:` comments — things the reviewer agent missed, got wrong,
   or judged correctly.
5. **Verify.** Render the result with `view.py` and take a screenshot.

## Deliverables

```
your-repo/
├── brief.md          # your spec (include revisions if you changed it)
├── log.md            # iteration log
├── final_script.py   # the generated script, with your # REVIEW: comments
├── result.png        # screenshot from the viewer
└── reflection.md     # see below
```

`reflection.md` (~300 words): Where was the model reliable and where did it
fail? What did the reviewer agent catch, and what did only *you* catch?
What would you need to trust this workflow on a real project?

## What good looks like

A precise, testable brief; sharp reviews, with real `# REVIEW:` comments and at least
one logged rejection; an honest log and reflection. The result itself counts least: a
failed structure with an excellent log teaches more than a pretty one you waved through.

## Going further (optional, and directly useful for the project)

- **Spec, not prose.** Write your brief as a pytest file (like `Lecture_12/test_wall.py`)
  and drive `tdd_agent.py` with it instead of `04_coder_reviewer.py`.
- **Ship it.** Load your artifact into Rhino 8 with `Lecture_12/rhino_load.py`, or wrap
  your core as a component ([`plugin_set/`](/Lecture/Lecture_12/plugin_set/README.md)).

## Rules

- The model writes the geometry code; you may only edit it to add `# REVIEW:`
  comments. If the loop cannot converge, say so in the reflection — that is a
  valid (and interesting) outcome.
- Everything else (brief, log, reflection) must be written by you, not by an LLM.
