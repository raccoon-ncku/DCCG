# Exercises — Week 09 (The timber model)

## A timber frame of your own (compas_timber)

`uv sync --extra timber`, then start from
[`timber_frame.py`](/Lecture/Lecture_09/applications/timber_frame.py).
Replace `stud_wall()` with something of yours: a roof truss, a pergola, a
reciprocal frame. Report how many L, T and X candidates the model finds.
Change `JOINT_RULE` (try `LMiterJoint`, `TTenonMortiseJoint`) and see how the
BTLx machining counts change. Which beam has the highest degree in
`model.graph`, and what does that mean on site?
