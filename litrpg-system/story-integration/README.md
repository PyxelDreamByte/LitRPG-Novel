# Story-integration contracts

This layer connects narrative events to continuity and CAL0 without treating a
manuscript as a database or permitting prose to mutate canon implicitly.

## Transaction lifecycle

1. A chapter draft produces ordered `chapter-event` records.
2. State changes and `progression-event` records cite those causal events.
3. New setting or System claims become `canon-proposal` records.
4. The complete `chapter-delta` is validated and reviewed.
5. The Author accepts, rejects, or returns the chapter and its delta.
6. Only an accepted delta may be applied to create the next
   `character-state` snapshot.

An accepted chapter does not automatically accept a `SYSTEM_CHANGE` or
`CONTRADICTION_OR_RETCON`; those classifications require a separate recorded
Author decision whose ID differs from the chapter-acceptance decision.
Acceptance also binds a repository-relative manuscript path, revision label,
and SHA-256 digest to the delta; requires timestamped Author approval with
evidence; and permits no open `BLOCKING` or `MAJOR` findings.

## Schemas

| Schema | Purpose |
|---|---|
| `chapter-event.schema.json` | Ordered causal facts established by the chapter |
| `progression-event.schema.json` | CAL0-governed XP, reinforcement, offers, and other progression |
| `character-state.schema.json` | Materialised character snapshot derived from accepted deltas |
| `canon-proposal.schema.json` | Explicitly proposed setting, character, or System facts |
| `chapter-delta.schema.json` | Atomic review and acceptance envelope for a chapter |
| `story-common.schema.json` | Shared exact-decimal, provenance, and approval definitions |

The JSON Schemas describe document shape. `tools/validate_story_integration.py`
also applies cross-record rules that JSON Schema cannot express conveniently,
including causal-reference integrity, decimal arithmetic, duplicate reward
claims, and the Author gate.

Editorial review uses the repository-wide four-level finding vocabulary:
`BLOCKING`, `MAJOR`, `MINOR`, and `OPTIONAL`. The corresponding arrays remain
separate so chapter acceptance can block only on the intended severity.

Canon proposals have fixed review routes: local colour to chapter acceptance,
setting extensions to worldbuilding review, character-state changes to
continuity review, System applications to CAL0 mechanics review, and System
changes or retcons to a separate Author decision.

Progression distinguishes `NATURAL_MATURATION` from purposeful
`ATTRIBUTE_ADAPTATION` and from `XP_GAIN`. Arithmetic equality
(`before + amount = after`) is enforced only for declared additive operations,
not offers or other state transitions. Skill and Class XP additionally require
evidence that the track lineage was already accepted in the delta's prior
state. Parameter-set references must name the pinned CAL0 I3 or I4 sets.

`character-state` files are materialised projections derived from accepted
deltas. The current validator checks their structure and local invariants, but
does not claim that it can generically reduce arbitrary deltas into snapshots.
Until a story-specific reducer exists, the acceptance workflow must compare a
new snapshot against its delta and prior accepted state explicitly.

## IDs

IDs are stable URI-like strings, for example:

- `chapter://first-awakening/book-01/001`
- `event://first-awakening/book-01/001/0001`
- `progression://first-awakening/book-01/001/0001`
- `claim://first-awakening/book-01/001/first-intentional-focus`
- `character://first-awakening/protagonist`
- `canon-proposal://first-awakening/book-01/001/01`

Renaming a chapter file must not change established record IDs.

## Validation

From the repository root:

```bash
python3 tools/validate_story_integration.py
```

The command checks the schemas, requires all valid fixtures to pass, and
requires every invalid fixture to fail for its named target condition.
