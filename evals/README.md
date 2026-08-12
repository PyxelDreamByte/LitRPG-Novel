# Workflow and agent evaluations

These specifications exercise repository workflows without creating canon. Static fixtures establish deterministic structure, isolation, hashes, and expected findings. They do not prove live model behaviour.

- `stories/experiments/isolation-suite/` is the contained noncanonical fixture work.
- `specs/skill-evals.md` covers all nine repository skills.
- `specs/agent-evals.md` covers all eight custom roles.
- Live evaluations must use fresh runs, disclose only the named fixture inputs, retain `live_eval_status: PENDING` until actually executed, and compare raw outputs against the stated invariants.

Never copy an evaluation artifact into an Authoring work. If an idea is worth retaining, restate it as a new `PROPOSED` Authoring artifact under a separately manifested work and use the normal Author gate.
