---
name: review-system-change
description: "Read-only classification and impact review for a requested change to the validated CAL0 LitRPG System, including evidence, regression, and successor-version planning. Use for System corrections, parameter changes, new mechanics, rule clarifications, balance changes, or requests that may reopen CAL0 architecture; do not implement unless the Author separately requests implementation."
---

# Review System Change

Treat CAL0 v0.7.0 as a locked validated baseline. Never edit it merely to make a scene work.

## Run boundary

Resolve exactly one initiating machine `work-manifest.json` or `*.work-manifest.json` and its paired `work-manifest.md`. Treat JSON as authority; require matching identity, type, mode, canonicality, promotion, root, and setting boundary, or stop. Record `work_id`, `work_root`, and `mode`. Work-specific presentation needs and extensions stay inside that work; shared CAL0 and governance remain read-only. Do not infer requirements from another work. In `EVALUATION`, create only a simulated classification/impact report beneath a fresh `runs_root/<run-id>/outputs/`; never overwrite fixture inputs, seek binding approval, create a successor, or update authoritative state.

Read [references/change-classes.md](references/change-classes.md) before classifying the request or proposing a successor.

## Workflow

1. State the request as an observable problem or desired capability. Separate story-presentation needs from mechanical change.
2. Run `python3 tools/route_system_context.py --topic <topic>` or `--decision <selected-option-id>`. Use the generated route before reading its guide/scenario projections, exact specification sections, registries, tests, closure evidence, and residual/change registers.
3. Classify the change and identify its required authority using the reference.
4. Map affected primitives, model families, invariants, parameters, schemas, scenarios, projections, reports, guides, tests, and story integrations.
5. Test whether existing rules already support the requested outcome. Prefer clarification or new story-side validation when no baseline change is needed.
6. For a real change, propose alternatives and analyse exploits, reward duplication, provenance loss, observability leaks, numerical drift, migration impact, and backward compatibility.
7. Define acceptance criteria, new or modified fixtures, cohort/adversarial regression where relevant, manifest/version changes, and documentation updates.
8. In `AUTHORING`, seek explicit Author approval through `$author-decision` for any canonical System change or architecture reopening. In `EVALUATION`, leave approval simulated and pending.
9. Preserve the work/source manifests, request, impact map, alternatives, required regression plan, and Author decision under the work's declared `runs_root/<run-id>/`. Produce a read-only successor-version proposal. Do not edit any file under `litrpg-system/cal0/`, including guides, code, fixtures, reports, or manifests. Do not implement the proposal unless the Author separately and explicitly requests implementation.
10. If implementation is separately authorized, create a governed successor outside the locked `cal0/` baseline, preserve the previous baseline, record supersession, and rebuild validation evidence for the successor rather than altering historical reports.

## Output

Return classification, current-rule finding, impact map, recommended disposition, evidence/tests required, proposed successor location/versioning plan, Author decision boundary, and confirmation that the locked baseline was not changed.
