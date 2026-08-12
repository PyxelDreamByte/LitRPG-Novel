# Stories

This directory contains story contracts, outlines, manuscripts, accepted deltas, and editorial evidence.

Every independent work begins with paired `work-manifest.md` and `<work-slug>.work-manifest.json`. The validated JSON is machine authority; Markdown is its matching human review surface. The pair fixes identity, root, type, mode, setting scope, explicitly adopted shared-world/default-guardrail references, character namespace, and run paths. No work inherits another work's setting overlay, characters, plans, or state.

- `series/` — multi-book works.
- `standalone-novels/` — novels outside a series.
- `novellas/` — medium-length fiction.
- `short-stories/` — contained fiction and workflow pilots.
- `experiments/` — explicitly non-canonical voice, form, or mechanism trials.
- `templates/` — series, book, chapter, manuscript, and delta contracts.

## Reusable work structure

```text
stories/<work-type-directory>/<work-slug>/
├── work-manifest.md
├── <work-slug>.work-manifest.json
├── work-contract.md
├── <work-type>-contract.md
├── characters/
├── world-overlay/
├── workbench/
│   ├── context-packs/
│   └── runs/
└── units/
    └── <unit-slug>/
        ├── outline/chapter-cards/
        ├── manuscript/chapters/
        ├── state/{deltas,snapshots}/
        ├── continuity/
        └── editorial/
```

Series may use `books/book-01/` instead of `units/<unit-slug>/` and add `series-contract.md` plus one `book-contract.md` per book. Standalone novels, novellas, short stories, and experiments use a single `units/main`, `units/story`, or `units/fixture` root without pretending to be a series or book.

The manuscript and accepted chapter deltas are primary story records. State snapshots and ledgers are derived and should be rebuilt when an accepted delta changes.

Standalone novels, novellas, and short stories use the same plan/write/accept artifacts with typed work and unit identifiers, while replacing the series/book contract combination with the appropriate work-type contract. Evaluation experiments set `mode: EVALUATION`, `canonicality: NONCANONICAL_EVALUATION_ONLY`, and `promotion: FORBIDDEN`; their simulated acceptance can never invoke promotion.

Machine-linked series, book, chapter, delta, character, event, and snapshot IDs
use the URI conventions in `governance/CANON-POLICY.md`. Human codes such as
`SER-001-B01-C001` remain `display_code` values and must not replace those URIs
in structured records.

## Acceptance boundary

A draft may be used for review but does not establish events. A chapter becomes accepted only when the Author approves the final manuscript and complete chapter delta together. New setting facts, character-state changes, progression, possessions, knowledge, relationships, and thread movement must be represented in that delta.
