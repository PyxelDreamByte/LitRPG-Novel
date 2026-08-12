# Chapter Acceptance Gates

All applicable gates must pass:

| Gate | Pass condition |
|---|---|
| Authority | The Author explicitly approved the exact final manuscript-plus-delta transaction immediately before promotion. |
| Contract | Required start/end states, purpose, and future constraints are satisfied. |
| Review | No open `BLOCKING` findings remain; accepted `MAJOR` findings are verified; `MINOR` findings are preserved and resolved or explicitly deferred. |
| Continuity | Time, location, inventory, injuries, conditions, relationships, and knowledge reconcile. |
| Causality | Actions are feasible and consequences follow established causes. |
| Character/POV | Motivation, agency, emotional continuity, viewpoint knowledge, and disclosure boundaries reconcile. |
| CAL0 | Progression, costs, rewards, observations, and provenance obey the validated baseline. |
| Canon | Every extra-story fact established as true is accepted at its proper world, series, book, character, or System scope; the manuscript depends on no pending proposal. `SYSTEM_CHANGE` and `CONTRADICTION_OR_RETCON` entries cite separate accepted Author decisions or are rejected and removed with dependent prose. |
| Plot/future | Thread movement, promises, outline variance, and protected future destinations are explicit. |
| Delta | The paired machine-readable `*.chapter-delta.json` is complete, supported by prose, and passes exact-path validation. |
| Derivation | Snapshots and ledgers are reproducibly rebuildable; absent tooling is reported rather than replaced by hand edits. |

If a gate fails, preserve the reviewed draft, report the smallest corrective action, and leave the authoritative baseline unchanged.

Never hand-edit a derived snapshot to make it agree with prose. Correct the accepted source or delta, obtain renewed approval if substantive content changed, then rebuild.
