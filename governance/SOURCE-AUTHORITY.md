# Source Authority

Use the narrowest authoritative source that actually governs the question. Authority is determined by scope and status, not by file length, recency alone, or confident wording.

## Precedence

When sources conflict, apply this order:

1. A current explicit Author instruction for the active decision.
2. An accepted, scoped decision record.
3. The authoritative accepted source for that domain.
4. Accepted chapter deltas and the manuscript passages they accompany.
5. Derived indexes, snapshots, ledgers, and summaries.
6. Proposals, plans, drafts, context packs, and workflow outputs.
7. Research, examples, fixtures, and archived material.

A higher item does not silently rewrite a lower artifact. Reconcile the change into the authoritative record and preserve the supersession trail.

## Domain authorities

| Domain | Authoritative source | Boundary |
|---|---|---|
| CAL0 mechanics | The baseline named by `governance/ACTIVE-SYSTEM-BASELINE.md`, plus that baseline's canonical sources and content-pinned manifest | The active canonical specification prevails over simplified guides |
| CAL0 calibrated reference behaviour | Accepted CAL0 registries and reports | Provisional parameters are not empirical facts or fixed story values |
| Project worldbuilding defaults | Accepted/provisional/deferred decisions under `worldbuilding/decisions/` | Reusable guardrails, not global or setting canon; future works must adopt them explicitly |
| Setting | The discoverable setting manifest, its indexed Author decision, and accepted records under `worldbuilding/settings/<setting-slug>/` | Project Hearthway has provisional authority only for its stable identity and main-series relationship; its staging capture, proposals, research, other settings, and unadopted project defaults are non-canon |
| Character definition | Accepted character profiles and scoped decisions | Story events may change state, not silently rewrite identity/history |
| Story events | Accepted manuscripts together with accepted chapter deltas | The pair forms the authoritative transaction |
| Plot intent | Current accepted series, book, arc, and chapter contracts | Plans guide drafting but do not establish events as having occurred |
| Research | `research/` | Evidence and inspiration only |
| Historical record | `archive/` | Superseded, never current authority |

## CAL0 fixture boundary

The following are reference or validation material unless the Author separately adopts them into the story:

- named reference characters and their sheets;
- worked story scenarios;
- cohort populations and outcomes;
- adversarial attacks and fixtures;
- notification examples;
- sample values and authoring examples.

Do not reuse fixture names, histories, values, or outcomes as story canon by implication.

## Guide compatibility

The CAL0 I6 guides are concise authoring projections and identify compatibility with specification v0.88 and annex v2.8. They remain useful within the content-pinned v0.7.0 bundle. If a guide conflicts with specification v0.89, calibration annex v2.9, a registered correction, or the bundle manifest, use the later canonical source and record the discrepancy.

## Citation and provenance

Proposals, findings, and deltas should cite stable file paths and identifiers. Copy only the minimum necessary context. Do not create alternative copies of canonical specifications, contracts, or chapters.

For System work, resolve the active baseline pointer first. Never assume the
folder named `cal0/` will remain the active version after an approved successor
is activated.
