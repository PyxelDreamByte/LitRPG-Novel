# Story Templates

- [`series-contract.md`](series-contract.md)
- [`book-contract.md`](book-contract.md)
- [`chapter-card.md`](chapter-card.md)
- [`chapter-manuscript.md`](chapter-manuscript.md)
- [`chapter-delta.md`](chapter-delta.md)

Contracts define intended work. Manuscripts describe reader-visible events. Accepted deltas record their authoritative consequences. Do not collapse these roles into one file.

Use URI identifiers as primary IDs and retain human-friendly values only in
`display_code`. Follow `governance/CANON-POLICY.md` for the separate
`workflow_status` and `canon_status` fields. A Markdown chapter delta and its
machine-readable partner must name the same `chapter_id` and `delta_id`.
