# LitRPG Novel

This repository is the shared source of truth for a canon-governed LitRPG web-novel project. It combines story planning and prose with worldbuilding, character continuity, and the validated CAL0 mechanics baseline.

**Security:** this is intended to remain a private repository. It contains full
manuscripts, unreleased story plans, System internals, and spoiler-bearing
research. Treat forks, exports, logs, artifacts, and connector access as
confidential; do not publish or change repository visibility without the
Author's explicit instruction.

The Author is the sole authority for accepting canon, plot, voice, and changes to the LitRPG System. Agents may draft, analyse, challenge, and propose. They may not silently promote material into canon.

## Start here

- [`STATUS.md`](STATUS.md) — current project state and next milestones.
- [`governance/`](governance/) — authority, canon, decisions, context routing, and workflow rules.
- [`litrpg-system/`](litrpg-system/) — System authority, generated routing, story integration, and validation.
- [`governance/ACTIVE-SYSTEM-BASELINE.md`](governance/ACTIVE-SYSTEM-BASELINE.md) — authoritative pointer to the active System baseline.
- [`litrpg-system/cal0/`](litrpg-system/cal0/) — locked CAL0 v0.7.0 executable baseline.
- [`litrpg-system/story-integration/`](litrpg-system/story-integration/) — machine-readable chapter, progression, and state contracts.
- [`.agents/skills/`](.agents/skills/) — Author-callable repository workflows.
- [`.codex/agents/`](.codex/agents/) — specialist drafting and review roles.
- [`worldbuilding/`](worldbuilding/) — project defaults plus isolated settings, including the provisionally authorized Project Hearthway development container.
- [`characters/`](characters/) — profiles, knowledge, relationships, arcs, and story state.
- [`stories/`](stories/) — series, books, shorter fiction, and drafting templates.
- [`research/`](research/) — non-canonical evidence and inspiration.
- [`workbench/`](workbench/) — disposable proposals, context packs, and workflow runs.
- [`archive/`](archive/) — superseded material retained for provenance.

## Operating model

1. Work begins from a bounded contract, proposal, or chapter card.
2. Agents use only the sources required by the context-routing policy.
3. Drafts and discoveries are reviewed as explicit proposals or deltas.
4. The Author accepts, revises, defers, or rejects those changes.
5. `main` holds the accepted repository baseline: authoritative canon where
   declared, plus clearly labelled non-canonical research, fixtures, templates,
   and tooling. Accepted chapter deltas update story state and canon indexes.

Research, examples, calibration fixtures, agent output, and manuscript inventions are non-canon until explicitly accepted through the appropriate workflow.

## Current worldbuilding boundary

The shared-universe container `setting://shared-universe-001`, temporarily
titled Project Hearthway, now has narrow `ACCEPTED` / `PROVISIONAL` authority
for its identity and relationship to the proposed main series
`work://series/project-hearthway-main`. Four bounded Lineage II records, three
bounded basin-flora records, the initial basin's coupled pulse-mosaic and wider
regional-horizon record, its spring lake breeding-migrant pulse, the mass
breeder's foundational aquatic body plan, ordinary Mana boundary, and selected
salt-organ and wax-like-gel physiology, the family-care migrant's selected
three-lobed living-vault body plan and mobile shelter–forage–regroup care
  interface plus its qualitative, fallible margin-ratchet outlet choreography,
  the qualitative river-glacial geography and transitional-climate scaffold,
  and the outlet's mixed sequence of bedrock throat, irregular boulder steps,
  lateral shelves, and state-dependent holding pockets, plus the initial
  ridge-spur settlement's unequal-shoulder working landscape, lakeward road,
  finite combined spring–well–cistern water system, and broad fair-weather
  unladen-downhill and laden-uphill lake-road journey anchors, plus its
  recurring upper-shore staging place and several short seasonal spurs to
  changeable nearby shore contacts, are also provisional; no detailed
  fictional record is yet fully accepted.

A parallel shared-setting bootstrap, `setting://continuity-one` (Continuity
One), was consolidated into Project Hearthway on 2026-08-17 by
`author-decision://world/WLD-SETTING-002A`; its authority topology was
absorbed and its shell is archived under
[`archive/settings/continuity-one/`](archive/settings/continuity-one/) as
provenance, never current authority.

Two reusable provisional human-reference modelling defaults are also recorded:
rare-Soul prevalence `0.001` with typed non-scalar Souls, and no ordinary
persistent self-aware continuity or directed prenatal System practice in
population models. A future work must explicitly adopt either default; the main
series currently adopts neither, and neither silently binds Project Hearthway
or an independent world. Universal rarity proportions are
Author-deferred until their object type, rarity dimension, eligible denominator,
population, period, and evidence are defined. See
[`worldbuilding/INDEX.md`](worldbuilding/INDEX.md).

## CAL0 boundary

CAL0 v0.7.0 implements the closed I1–I7 model-family topology against specification v0.89 and calibration annex v2.9. Treat its canonical files, registries, manifests, tests, and reports as one content-pinned baseline. Story-specific values and unresolved setting distributions must be supplied outside CAL0. Changes to the baseline require the governed successor-change workflow, regression evidence, and Author approval.

## Repository conventions

- Use Markdown for human-authored source material and JSON for validated machine-readable records.
- Preserve stable decision, finding, chapter, character, and event identifiers.
- Link to authoritative sources rather than copying them into competing files.
- Use Git history for versions; do not create filenames such as `final-v2-revised.md`.
- Keep generated indexes and snapshots reproducible from accepted source material.

## Validation

Run the complete current System gate from the repository root:

```bash
python3 tools/validate_repository.py
```

This is the full CI entrypoint. It validates repository structure, skills and
agents, non-CAL0 JSON, CAL0, its regression suite, generated routing indexes,
and the current story-integration schemas and fixtures. Use
`python3 tools/validate_system.py` only for the narrower System gate. Neither
command proves that the multi-agent chapter workflow produces publication-ready
fiction; that requires the pending workflow evaluations and further successful
end-to-end evidence described in [`governance/evals/`](governance/evals/).
