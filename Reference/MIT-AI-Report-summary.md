# MIT report on AI in education — summary & how ARCH3045 responds

Source: **Report of MIT's Ad Hoc Committee on AI Use in Teaching, Learning, and
Research Training**, 13 Aug 2026 (`AI-Committee-Final-Report.pdf`, this folder).
This note is course-design documentation — the rationale behind the AI policy
stated in the [main README](/README.md#ai-usage).

## What the report says

A five-month, Institute-wide committee (students, faculty from every school,
staff) found generative AI is already pervasive and is eroding foundational
practices — problem sets, take-home exams, office hours, study groups, UROPs.
Its verdict: nearly every subject must be re-examined to become **"AI-aware,"**
and the response should be a deliberate redesign, not patches.

**Eight guiding principles:** be humble · be bold · put humanity front and
center · lean into learning · teach with intentionality · no one-size-fits-all ·
**augmentation not automation** · think beyond the classroom.

**Recommendations that bear directly on a syllabus:**

- **§3.1.8 — every course must state a clear AI policy *with a rationale* tied
  to its learning goals**, posted in the syllabus. Tell students LLMs fabricate
  facts/citations and emit incorrect or insecure code, and that they own
  everything they submit.
- **Appendix B — a four-option policy menu** (traffic-light), usable per-course
  *or per-assignment*:
  1. **Unrestricted** — any AI, any purpose. Suits work where AI use doesn't
     undermine the objective (e.g. ambitious software projects) or where
     evaluating AI output *is* the work.
  2. **Limited (support tool only)** — brainstorm/edit/debug, but not full
     solutions.
  3. **Required** — students *must* use AI in a specified way; suits objectives
     like AI-assisted programming, prompt engineering, and critiquing model
     output.
  4. **Prohibited** — no AI; hard to enforce and prone to false accusations.
- **Assess in ways AI can't shortcut** (§3.1.2) — oral exams, portfolios,
  in-class conversation, and **process evidence** (version history). Explicitly
  **do not rely on AI detectors** (§3.1.9) — unreliable, and they poison the
  student–instructor relationship.
- **Emphasize experiential / project-based learning** (§3.1.3) — AI now lets
  students build "near production-quality software artifacts in a single
  academic term." The report names **architecture** and software-engineering
  capstones as models.
- **Teach effective / responsible / ethical AI use** (§3.2.4) as three distinct
  skills: specify a problem → verify output → know when *not* to reach for AI;
  augmentation vs. automation and honest disclosure; provenance, bias, IP, and
  environmental cost.

## How this course maps to it

The course was already close to the report's recommended shape; the update makes
the policy and its rationale explicit, as §3.1.8 asks.

| Report asks for | Where this course does it |
| --- | --- |
| A stated policy **with rationale**, on the menu | [README § AI usage](/README.md#ai-usage) — declared **Required use**, with the "why" |
| Assessment AI can't shortcut | Final **oral defense** (explain every line, live); no AI detectors used |
| **Process evidence**, not detection | Git history + `log.md` disclosure are part of the evidence |
| Experiential, artifact-scale projects | The [final project](/Assignment/5_Final_Project/README.md): a real, tested plugin |
| Augmentation not automation | Intro framing; the agentic lecture's human-gate and "why `--auto` is dangerous" |
| Effective/responsible/ethical AI as taught skills | W04 (reviewing generated code), W10–14 (spec → verify → review loop) |
| Deliberately AI-free work | Agentic-lab brief/log/reflection are human-written; the live demo |

**Policy placement, precisely:** the course sits at **Required use** overall
(building with AI is the point), with specific components set to **Prohibited**
(the agentic lab's written reflection, and the oral defense) — exactly the
per-assignment mixing the menu is designed for.
