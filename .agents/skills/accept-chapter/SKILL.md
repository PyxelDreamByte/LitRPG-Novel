---
name: accept-chapter
description: "Validate and present an exact reviewed manuscript-plus-delta transaction for final Author acceptance, then promote and revalidate it without substantive changes. Use when the Author says a chapter is final, approved, accepted, or ready to enter the story's authoritative sequence."
---

# Accept Chapter

Acceptance is a transaction: approve prose, state changes, and canon implications together or not at all.

## Run boundary

Resolve exactly one target machine `work-manifest.json` or `*.work-manifest.json` and its paired `work-manifest.md`. Treat JSON as authority; require matching work identity, type, mode, canonicality, promotion, root, and setting boundary, or stop. Record `work_id`, `work_root`, and `mode`. Confirm every manuscript, delta, character/state dependency, overlay, context pack, and mutable output belongs to that work. Reject undeclared cross-work references. If `mode` is `EVALUATION`, stop after validating the fixture and reporting whether simulated gates pass: promotion, Author acceptance, accepted status, derived-state rebuilding, and authoritative world/character/story updates are forbidden.

Read [references/acceptance-gates.md](references/acceptance-gates.md) before changing authoritative story state.

## Workflow

1. Require `AUTHORING` mode. Identify the exact manuscript path and immutable revision/digest, the paired Author-facing delta, the exact machine-readable `*.chapter-delta.json` path, and the authoritative predecessor. Treat earlier approval language as intent to begin this gate, not acceptance of an unseen or subsequently changed transaction.
2. Verify that the approved chapter card is satisfied, the context pack is current, and all `BLOCKING` findings are closed. Verify accepted `MAJOR` corrections independently; preserve `MINOR` findings in the workflow evidence and resolve or explicitly defer them without downcasting them to `OPTIONAL`.
3. Validate the exact machine delta before presentation:

   ```bash
   python3 tools/validate_story_integration.py <path/to/chapter.chapter-delta.json>
   ```

   Reconcile it against the manuscript and current accepted state. Reject hidden or unsupported time, location, inventory, knowledge, relationship, condition, thread, or progression changes.
4. For each CAL0-bearing event, run `python3 tools/route_system_context.py --topic <topic>` or `--decision <selected-option-id>` before reading the returned guide, scenario, specification section, or numerical authority. Preserve exact-decimal and provenance rules.
5. Use only the canon-proposal schema classifications: `LOCAL_COLOUR`, `SETTING_EXTENSION`, `CHARACTER_STATE_CHANGE`, `SYSTEM_APPLICATION`, `SYSTEM_CHANGE`, and `CONTRADICTION_OR_RETCON`. Route setting extensions through `$develop-worldbuilding` and System changes through `$review-system-change`; neither is accepted merely through chapter approval. Before accepting the transaction, every extra-story fact the manuscript establishes as true must be accepted at its proper world, series, book, character, or System scope. No accepted manuscript may depend on a pending proposal. A `SYSTEM_CHANGE` or `CONTRADICTION_OR_RETCON` must cite a separate accepted Author decision or be rejected and removed from the transaction and dependent prose.
6. Complete every gate in `stories/templates/chapter-delta.md`, including character/POV knowledge, world canon, plot/future alignment, CAL0 mechanics, and structured-schema validation.
7. Preserve the work/source manifests, gate results, findings, validation output, and exact transaction manifest under the work's `runs_root/<run-id>/`. Present that exact transaction to the Author immediately before promotion: manuscript path plus revision/digest, Author-facing delta path, machine-delta path plus digest, canon-proposal dispositions, unresolved/deferred items, validation result, and intended promotion changes. Ask the Author to accept or reject both manuscript and delta explicitly. Stop and wait.
8. After explicit acceptance of that exact transaction, apply only deterministic acceptance metadata: accepted status, date, Author evidence, and accepted-location/index updates. Any substantive prose, event, state, progression, thread, or proposal change invalidates the approval and returns to step 3.
9. Revalidate the promoted machine-delta path with the exact-path command above, then run the full gate: `python3 tools/validate_repository.py`. Leave the accepted baseline unchanged if either fails.
10. Rebuild derived state only through a reproducible builder. If no builder exists, record derivation as pending and do not claim snapshots or ledgers were rebuilt; do not hand-edit them into agreement.

## Output

Return the accepted chapter identifier, exact transaction identifiers/digests, approved delta, accepted canon promotions or rejected/removed proposals, exact validation commands/results, and genuinely rebuilt derived artifacts or explicit pending derivations. Report a new authoritative story-state identifier only when a reproducible builder actually produced and validated it.
