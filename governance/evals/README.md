# Workflow Evaluations

Evaluation fixtures test whether skills and agents obey governance, not whether they merely produce fluent text.

**Current state:** the workflow instructions and specialist roles exist, but
the full chapter loop has not yet been empirically evaluated. The CAL0 tests and
story-integration schema fixtures do not constitute an evaluation of planning,
multi-agent drafting, revision quality, Author gating, or state promotion. Do
not mark the workflow proven or publication-ready until the suites below and a
representative end-to-end pilot pass.

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
