# Governance Schemas

These schemas validate structured governance records. Human-readable Markdown remains the review surface; an automated workflow may emit a matching JSON record for deterministic checks.

New records separate `workflow_status` from `canon_status`. Decisions and world
records also retain their display codes while declaring stable machine-linkable
URI identities.

- `decision-record.schema.json` — binding or candidate decisions.
- `worldbuilding-record.schema.json` — proposed or accepted setting facts.

Story-event, chapter-delta, character-state, progression, and canon-proposal schemas belong to the story-integration layer under `litrpg-system/` and are intentionally not duplicated here.
