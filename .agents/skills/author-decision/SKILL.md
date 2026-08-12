---
name: author-decision
description: "Turn a consequential creative or repository question into a bounded Author decision, record the chosen option and its implications, and update affected plans without silently changing canon. Use for explicit choices, unresolved design questions, canon promotion, or decisions that constrain later story, worldbuilding, or CAL0 work."
---

# Author Decision

Preserve the Author as the sole authority over canon, plot, voice, and acceptance.

## Run boundary

Resolve exactly one machine `work-manifest.json` or `*.work-manifest.json` and its paired `work-manifest.md` before analysis. Treat JSON as authority; require matching identity, type, mode, canonicality, promotion, root, and setting boundary, or stop. Record `work_id`, `work_root`, and `mode`; reject target or mutable dependency paths outside `work_root`. Shared governance, CAL0, research, and accepted global world canon are read-only dependencies, not part of the work. In `EVALUATION`, create only simulated options/findings inside the fixture or evaluation run: never request or record a binding Author decision, promote anything, or update authoritative world, character, or story state.

## Workflow

1. Read the governing policy, relevant canon, active proposal, and dependent plans. Load only the material needed for the decision.
2. State the decision boundary in one sentence. Separate the actual choice from consequences that follow automatically.
3. Present two to four viable options. Give each a stable local label, a concise description, benefits, costs, compatibility constraints, and likely downstream effects.
4. Recommend one option when evidence supports it. State the reasoning and uncertainty; do not manufacture neutrality.
5. In `AUTHORING`, ask the Author to choose before recording any binding decision. This always includes canon promotion, CAL0 reopening, retcons, and material plot or repository direction. Stop and wait; never infer a selection. In `EVALUATION`, compare the simulated output with expected invariants and leave the selection pending.
6. After the Author answers, assign or retain the decision ID and record the exact choice using `governance/templates/decision-record.md`: rationale, status, scope, approval evidence, consequences, affected sources, dependencies/conflicts, residual unknowns, supersession links, and reopening conditions. Validate a structured decision record against `governance/schemas/decision-record.schema.json` when one is created.
7. Preserve the option analysis, source manifest, validation, and approval evidence under the resolved work manifest's `runs_root/<run-id>/`. Update only the plans or proposals directly authorized by the choice. List further changes that require separate work.

## Status discipline

Use the repository's canonical status vocabulary. Never interpret silence, an agent consensus, or draft prose as Author approval. Preserve rejected options and rationale when they will prevent the question from being reopened accidentally.

## Output

Return the decision, its implications, files changed, validation performed, and any next decision in dependency order.
