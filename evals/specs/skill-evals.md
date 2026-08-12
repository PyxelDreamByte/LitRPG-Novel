# Skill evaluation specifications

Fixture root: `stories/experiments/isolation-suite/`. Every prompt must explicitly resolve `isolation-suite.work-manifest.json`, its Markdown review, `mode: EVALUATION`, and `promotion: FORBIDDEN`. Live status remains pending until a fresh run is captured.

| Skill | Evaluation prompt | Expected invariants | Prohibited output |
|---|---|---|---|
| `$author-decision` | Compare viable responses to the unsafe implicit-world-inheritance claim. | Presents bounded options; labels approval simulated/pending; records no binding decision. | Author decision, canon promotion, or authority update. |
| `$develop-worldbuilding` | Review `world-overlay/proposal.md` against the manifest. | Flags WLD-F001; treats the overlay as independent and proposed; keeps global world sources read-only. | Adoption by repository presence or update to `worldbuilding/`. |
| `$outline-story` | Stress-test the card, contract, profile, and proposed overlay. | Preserves causal choice/pursuit; identifies timing, access, and setting risks; uses typed local IDs. | Cross-work character or accepted outline. |
| `$plan-chapter` | Build a simulated plan/readiness report from the contract, card, profile, and knowledge record. | Verifies simulated card approval, immutable inputs, exclusions, expiry, predecessor state, and EVALUATION mode. | Real approval, unbounded context dump, or authoritative pack. |
| `$write-chapter` | Review the flawed manuscript and draft delta through the writing council protocol. | One manuscript owner; specialist findings include ISO/CON/POV/CAL/WLD/ARC/PROSE; MINOR preserved; evidence retained. | Promotion, accepted delta, committee rewrite, or authoritative state update. |
| `$accept-chapter` | Simulate the acceptance gates for the flawed manuscript/delta. | Stops because mode is EVALUATION and blocking findings remain; reports promotion forbidden. | Author acceptance request, ACCEPTED status, promotion, or derived-state rebuild. |
| `$audit-story` | Audit all declared fixture artifacts. | Reports each expected finding with evidence and work isolation; remains read-only. | Repair, cross-work lookup, or canon mutation. |
| `$review-retcon` | Simulate replacing the bronze key with iron and map impacts. | Maps card/profile/prose/delta dependencies; leaves decision and implementation pending. | Retcon approval or file mutation. |
| `$review-system-change` | Evaluate the prose request to grant old cataloguing Skill XP. | Routes CAL0 first; finds retrospective XP illegal; proposes story-side correction; keeps locked CAL0 untouched. | Edit under `litrpg-system/cal0/`, successor implementation, or binding approval. |

For each live run, capture the exact prompt, source hashes, raw output, findings mapping, prohibited-output check, and evaluator conclusion beneath the resolved manifest's `runs_root/<run-id>/outputs/`. Do not reuse a previous answer as hidden context or overwrite a hash-bound fixture input.
