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
- [`worldbuilding/`](worldbuilding/) — project defaults plus the isolated Continuity One proposed setting shell.
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

The first real shared-setting shell exists at
[`worldbuilding/settings/continuity-one/`](worldbuilding/settings/continuity-one/).
Its stable ID is `setting://continuity-one`; `Continuity One` is a provisional
display title. Its manifest and constitution are `DRAFT`/`PROPOSED`, its layered
foundation map is unanswered, and it has no adopting works or accepted detailed
setting canon.

Two reusable provisional human-reference modelling defaults and one rarity
deferral remain at project level. Continuity One does not adopt or assume
`WLD-SOUL-001A` or `WLD-PRENATAL-001A`, and `WLD-RARITY-001D` is not a setting
distribution. See [`worldbuilding/INDEX.md`](worldbuilding/INDEX.md).

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
