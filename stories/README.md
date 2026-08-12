# Stories

This directory contains story contracts, outlines, manuscripts, accepted deltas, and editorial evidence.

- `series/` — multi-book works.
- `standalone-novels/` — novels outside a series.
- `novellas/` — medium-length fiction.
- `short-stories/` — contained fiction and workflow pilots.
- `experiments/` — explicitly non-canonical voice, form, or mechanism trials.
- `templates/` — series, book, chapter, manuscript, and delta contracts.

## Recommended book structure

```text
stories/series/<series-slug>/
├── series-contract.md
└── books/
    └── book-01/
        ├── book-contract.md
        ├── outline/
        │   ├── book-outline.md
        │   ├── arcs/
        │   └── chapter-cards/
        ├── manuscript/
        │   └── chapters/
        ├── state/
        │   ├── deltas/
        │   └── snapshots/
        ├── continuity/
        │   ├── timeline.md
        │   ├── thread-ledger.md
        │   └── knowledge-ledger.md
        └── editorial/
```

The manuscript and accepted chapter deltas are primary story records. State snapshots and ledgers are derived and should be rebuilt when an accepted delta changes.

Machine-linked series, book, chapter, delta, character, event, and snapshot IDs
use the URI conventions in `governance/CANON-POLICY.md`. Human codes such as
`SER-001-B01-C001` remain `display_code` values and must not replace those URIs
in structured records.

## Acceptance boundary

A draft may be used for review but does not establish events. A chapter becomes accepted only when the Author approves the final manuscript and complete chapter delta together. New setting facts, character-state changes, progression, possessions, knowledge, relationships, and thread movement must be represented in that delta.
