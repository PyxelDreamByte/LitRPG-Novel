---
name: review-retcon
description: "Assess a proposed retroactive story, character, worldbuilding, or System change before implementation by mapping affected canon, chapters, state deltas, setup/payoff, and future plans. Use whenever an accepted fact or event may be contradicted, reinterpreted, replaced, or removed."
---

# Review Retcon

Treat retcons as dependency migrations, not local text edits.

## Workflow

1. State the proposed old truth, new truth, scope, motivation, and desired reader experience.
2. Locate the authoritative decision or accepted source and all direct references.
3. Trace downstream dependencies across manuscript, deltas, snapshots, character knowledge, relationships, worldbuilding, CAL0 applications, outlines, threads, foreshadowing, and planned payoffs.
4. Classify each dependency as incompatible, requires reinterpretation, requires revision, remains valid, or becomes newly available.
5. Compare viable strategies: explicit in-world revelation, reinterpretation, bounded rewrite, or full replacement. Preserve earned consequences wherever possible.
6. Estimate narrative benefit, continuity cost, reader-confusion risk, and implementation surface for each strategy.
7. Present the consequential choice through `$author-decision`. Do not implement until the Author approves the retcon and migration scope.
8. Preserve the source manifest, impact map, alternatives, decision, and migration plan under `workbench/runs/<run-id>/`. After approval, create a dependency-ordered migration plan with validation and rollback points. Do not implement it unless the Author separately requests implementation; when authorized, update authoritative sources before derived artifacts.

## Output

Return the impact map, strategy comparison, recommended option, affected files/chapters, migration order, validation plan, and explicit Author decision required.
