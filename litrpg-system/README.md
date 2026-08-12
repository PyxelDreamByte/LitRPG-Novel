# LitRPG System

This directory integrates the validated CAL0 mechanics baseline with the
story-facing records used by the novels. It deliberately separates immutable
mechanical authority from derived indexes and manuscript state.

Resolve `../governance/ACTIVE-SYSTEM-BASELINE.md` before System work. CAL0
v0.7.0 is active now; accepted successors live as immutable siblings under
`successors/` and become active only through the governed pointer update.

## Source authority

1. `cal0/manifests/cal0-i7.bundle.json` pins the executable CAL0 v0.7.0
   baseline and its content digests.
2. `cal0/canonical/litrpg-system-specification.md` is the authoritative
   architecture specification (v0.89).
3. `cal0/canonical/litrpg-system-calibration-annex.md` and the pinned
   registries govern numerical reference behaviour.
4. `cal0/guide/`, `cal0/scenarios/`, and `cal0/characters/` are authoring
   projections and reference fixtures, not fixed plot canon.
5. `indices/` is generated routing data. It is never an independent source of
   truth.
6. `story-integration/` describes story events and proposed state changes. A
   draft chapter or delta cannot amend CAL0 or world canon by implication.

The contents of `cal0/` are a locked imported baseline. Corrections or
mechanical changes require a governed successor version; never edit the
baseline in place.

## Story integration

The principal write-side artifact is a chapter delta. It records causal story
events, character changes, LitRPG progression, plot-thread movement, and canon
proposals as one reviewable transaction. Its schemas enforce these boundaries:

- mechanical quantities are plain exact-decimal strings, never JSON floats;
- every progression award names a causal chapter event and a CAL0 decision;
- change, progression-event, and canon-proposal identifiers are unique within
  their chapter delta;
- reward claims have stable identifiers and cannot be silently duplicated;
- new setting facts remain proposals until the Author accepts them;
- canon-proposal classifications follow fixed review routes;
- System changes and retcons always require a separate Author decision with an
  ID distinct from chapter acceptance; and
- character-facing knowledge is distinct from author/private projections.

See `story-integration/README.md` for the lifecycle and schema catalogue.

## Context routing

Agents should load the smallest authoritative context that can answer the
question:

1. Read `indices/topic-routing.json` to select a topic.
2. Read the relevant story guide or worked scenario named there.
3. Read the indexed specification section for binding rules.
4. Read the calibration annex or executable registries only when exact
   numerical behaviour matters.

Rebuild indexes after the canonical specification changes:

```bash
python3 tools/build_system_indexes.py
python3 tools/build_system_indexes.py --check
```

## Validation

Run the complete System gate from the repository root:

```bash
python3 tools/validate_system.py
```

For a faster story-layer-only check:

```bash
python3 tools/validate_story_integration.py
python3 tools/build_system_indexes.py --check
```
