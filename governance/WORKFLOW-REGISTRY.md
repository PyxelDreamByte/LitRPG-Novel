# Workflow Registry

This registry defines the intended Author-callable workflows. The human-readable specification governs even when an automated skill is not yet implemented.

| Workflow | Purpose | Required gate | Current state |
|---|---|---|---|
| `author-decision` | Present material choices and record the Author's selection | Author accepts decision record | Implemented; evaluation pending |
| `develop-worldbuilding` | Research, propose, review, and integrate a setting addition | Author accepts world decision/canon change | Implemented; evaluation pending |
| `outline-story` | Develop series, book, arc, and chapter contracts | Author accepts the relevant contract | Implemented; evaluation pending |
| `plan-chapter` | Lock a chapter card and build a bounded context pack | Author approves chapter card | Implemented; evaluation pending |
| `write-chapter` | Plan, draft, review, revise, and present a chapter | Does not itself accept canon | Implemented; evaluation pending |
| `accept-chapter` | Validate and promote manuscript plus explicit delta | Author accepts the complete transaction | Implemented; evaluation pending |
| `audit-story` | Find continuity, causality, knowledge, mechanics, and thread defects | Findings only; no automatic edits | Implemented; evaluation pending |
| `review-retcon` | Map and assess a proposed change to accepted history | Author accepts retcon decision | Implemented; evaluation pending |
| `review-system-change` | Classify and validate a CAL0 correction, parameter change, extension, or reopening | Author accepts successor change | Implemented; evaluation pending |

## Standard chapter loop

1. Lock the chapter card and acceptance criteria.
2. Build and validate a bounded context pack.
3. Obtain independent planning advice from only the relevant specialists.
4. Give one drafter ownership of the manuscript.
5. Run independent editorial reviews.
6. Synthesize stable findings by severity and resolve material disagreements.
7. Give one reviser an approved change set.
8. Verify continuity, world canon, character knowledge, plot threads, and CAL0 mechanics.
9. Present the manuscript, delta, unresolved questions, and review summary to the Author.
10. On explicit acceptance, promote the transaction and rebuild derived state.

Review loops normally stop after two revision rounds. A third must have a stated reason. Remaining major disagreements escalate to the Author.

## Finding severity

- `BLOCKING`: contradiction, infeasible action, broken mechanics, false continuity, viewpoint leakage, or missing acceptance artifact.
- `MAJOR`: materially weakens causality, character, structure, promise, or clarity.
- `MINOR`: local issue worth correcting without reopening the chapter.
- `OPTIONAL`: preference or alternative, not a defect.

Only `BLOCKING` and `MAJOR` findings reopen a normal review round.

## Workflow evidence

Each run should create its contract, source manifest, independent findings,
synthesised change set, validation results, Author decision, and promoted
artifacts in the workbench. Workbench records remain disposable and ignored by
Git by default.

When a run supports an accepted decision, chapter, retcon, System change, or
workflow evaluation, retain the minimum sufficient evidence bundle under
`governance/evidence/<run-id>/` before the accepting commit. The retained bundle
for an accepted outcome must contain decision/approval evidence, final findings,
validation, and promoted-artifact digests. A live noncanonical evaluation
instead retains exact source/output hashes and per-target checks with no Author
approval or promotion claim. Do not retain redundant context copies or
sensitive research material.
