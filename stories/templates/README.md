# Story Templates

- [`series-contract.md`](series-contract.md)
- [`book-contract.md`](book-contract.md)
- [`work-manifest.md`](work-manifest.md)
- [`work-manifest.example.json`](work-manifest.example.json)
- [`work-contract.md`](work-contract.md)
- [`standalone-novel-contract.md`](standalone-novel-contract.md)
- [`novella-contract.md`](novella-contract.md)
- [`short-story-contract.md`](short-story-contract.md)
- [`work-world-overlay.md`](work-world-overlay.md)
- [`chapter-card.md`](chapter-card.md)
- [`chapter-manuscript.md`](chapter-manuscript.md)
- [`chapter-delta.md`](chapter-delta.md)

Contracts define intended work. Manuscripts describe reader-visible events. Accepted deltas record their authoritative consequences. Do not collapse these roles into one file.

Use URI identifiers as primary IDs and retain human-friendly values only in
`display_code`. Follow `governance/CANON-POLICY.md` for the separate
`workflow_status` and `canon_status` fields. A Markdown chapter delta and its
machine-readable partner must name the same `chapter_id` and `delta_id`.

Create paired `work-manifest.md` and machine JSON first. Name the machine authority either `work-manifest.json` or `<work-slug>.work-manifest.json`; both are discovered, while the slugged form is recommended for unambiguous search results. Markdown is its human review surface, and every manifest field must match. All other IDs and mutable paths resolve through that pair. A work may explicitly adopt shared global world canon, keep a work-local overlay, or declare an independent setting; it never inherits setting decisions from repository presence.

Use these tokens consistently:

| Work type | URI token | Directory | Unit token | Unit path |
|---|---|---|---|---|
| Series | `series` | `series` | `book-01` | `books/book-01` |
| Standalone novel | `standalone-novel` | `standalone-novels` | `main` | `units/main` |
| Novella | `novella` | `novellas` | `main` | `units/main` |
| Short story | `short-story` | `short-stories` | `story` | `units/story` |
| Evaluation experiment | `experiment` | `experiments` | `fixture` | `units/fixture` |

The chapter card, manuscript, and delta templates use `[work-type]`, `[work-type-directory]`, `[work-slug]`, `[unit-slug]`, and `[unit-path]` from this table so every work form can use the same plan/write/accept transaction.
