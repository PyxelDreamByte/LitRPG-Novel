# Workflow Evaluations

Evaluation fixtures test whether skills and agents obey governance, not whether they merely produce fluent text.

**Current boundary:** use synthetic, explicitly non-canonical fixtures during
the environment-scaffold pass. They may validate static contracts, routing,
gates, failure detection, and deterministic state promotion without requiring
or creating a real setting or story. The CAL0 and story-integration suites do
not by themselves prove live multi-agent planning, drafting, revision quality,
Author judgement, or publication readiness. Report static/synthetic,
live/model-mediated, and end-to-end status separately; do not collapse them
into one “workflow proven” claim.

Initial suites should cover:

- silent canon promotion;
- research presented as fact;
- CAL0 fixture leakage into story canon;
- natural maturation incorrectly awarding XP;
- retrospective Skill or Class XP;
- duplicated rewards or progression;
- omniscient appraisal and viewpoint knowledge leakage;
- free dungeon spawning or inventory teleportation;
- a reviser approving its own work;
- a chapter accepted without a complete delta;
- stale context packs overriding current sources;
- an unregistered CAL0 baseline edit.

Each fixture should declare inputs, governing sources, expected findings, prohibited outputs, and pass/fail evidence.

Retain evidence from completed evaluation runs under
`governance/evidence/<run-id>/`; keep temporary context and raw run output in
the ignored workbench.
