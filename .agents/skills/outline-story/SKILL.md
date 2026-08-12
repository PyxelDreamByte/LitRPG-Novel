---
name: outline-story
description: "Create or revise a series, book, arc, scene, or chapter outline that aligns character causality, world canon, CAL0 mechanics, setup and payoff, and the Author's intended destination. Use for premises, story architecture, plot threads, chapter cards, pacing, or structural replanning."
---

# Outline Story

Build causal scaffolding, not a rigid synopsis. Preserve room for discovery while making promises and dependencies visible.

## Workflow

1. Determine the outline level: series, book, arc, chapter sequence, or scene.
2. Read the relevant story contract, accepted preceding material, character arcs, active thread ledger, world canon, and CAL0 constraints. For CAL0 questions, run `python3 tools/route_system_context.py --topic <topic>` or `--decision <selected-option-id>` before reading returned sources.
3. Define the start state, intended end state, central change, reader promise, and non-negotiable Author intentions.
4. Generate beats from character motives, constraints, decisions, and consequences. Do not rely on coincidence or hidden information unavailable to the acting character.
5. Track each setup, escalation, reversal, payoff, revelation, and intentionally unresolved thread.
6. Check timing, travel, resources, injuries, knowledge, relationships, and permitted LitRPG progression.
7. Mark uncertain world or system facts as proposals rather than embedding them as canon.
8. Stress-test the structure for dead chapters, repeated functions, premature payoffs, missing recovery, false choices, and future chapters that require earlier characters to behave irrationally.
9. Present material alternatives through `$author-decision`; then update the outline and affected chapter cards only within the Author-approved scope. Preserve the source manifest, structural analysis, decision, and changed contract revisions under `workbench/runs/<run-id>/`.

## Chapter cards

For each chapter, record POV, time/location, opening state, intended ending state, purpose, required beats, active threads, prior dependencies, future constraints, permitted progression, forbidden contradictions, and open questions. Describe outcomes without prewriting every line of the scene.

## Output

Return the revised outline, change summary, affected threads, canon proposals, and any decisions still needed.
