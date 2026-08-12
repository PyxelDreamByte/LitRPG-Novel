# Governance Schemas

These schemas validate structured governance records. Human-readable Markdown remains the review surface; an automated workflow may emit a matching JSON record for deterministic checks.

New records separate `workflow_status` from `canon_status`. Decisions and world
records also retain their display codes while declaring stable machine-linkable
URI identities.

- `decision-record.schema.json` — binding or candidate decisions.
- `worldbuilding-record.schema.json` — proposed or accepted setting facts.
- `workflow-evidence-manifest.schema.json` — retained evidence from an ignored workflow run, with separate accepted-outcome and live-noncanonical-evaluation branches.

The single setting-manifest contract lives at
`litrpg-system/story-integration/schemas/setting-manifest.schema.json`. It is an
integration identity and authority contract, not a duplicate governance record.
Project-default adoption remains explicit in each work manifest and its
Author-reviewed setting constitution.

The schemas constrain valid status pairings. Completed provisional and deferred
Author dispositions require approval evidence; they are not incomplete drafts.
Structured decision and accepted-world-record templates live beside the
human-readable templates.

Story-event, chapter-delta, character-state, progression, and canon-proposal schemas belong to the story-integration layer under `litrpg-system/` and are intentionally not duplicated here.

`ACCEPTED_OUTCOME` evidence requires Author approval and at least one target
artifact. `LIVE_NONCANONICAL_EVALUATION` locks canonicality to
`NONCANONICAL_EVALUATION_ONLY`, promotion to `FORBIDDEN`, and approval to
`null`; its target-artifact list may be empty for a read-only run.
