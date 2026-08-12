# LitRPG System agent instructions

These instructions apply to `litrpg-system/` and all descendants.

## Authority and immutability

- Treat `cal0/` as an imported, content-pinned baseline. Do not modify,
  reformat, rename, or regenerate any file inside it.
- A requested mechanical change must use the governed System-change workflow
  and create a successor version. It must not be smuggled in through prose,
  examples, indexes, fixtures, or story state.
- Treat `indices/` as disposable generated output. Change
  `tools/build_system_indexes.py`, then regenerate; do not hand-edit an index.
- Reference CAL0 by stable decision IDs, bundle IDs, parameter-set IDs, and
  source paths. Do not rely on remembered paraphrases where a binding outcome
  depends on the exact rule.

## Decimal and provenance rules

- Store all mechanical quantities as plain exact-decimal strings such as
  `"0"`, `"1.25"`, or `"-0.5"`. JSON binary floating-point numbers and
  exponent notation are forbidden in canonical story-integration records.
- Keep natural counting and ordering fields, such as event sequence numbers,
  as JSON integers.
- Every progression event must identify its causal chapter event, stable reward
  claim, CAL0 bundle, and applicable decision references.
- Never relabel prior nonmagical evidence as Mage/Class/Skill evidence
  retrospectively. Preserve source and lineage identity.
- Do not duplicate one causal reward through multiple views, ledgers, or
  chapter deltas.

## Canon and projections

- Draft prose and draft deltas are not accepted canon.
- New facts discovered during writing must be represented as canon proposals.
- System changes, contradictions, and retcons are blocking until the Author
  records a separate decision.
- Keep private backend, author-facing, character-accessible,
  appraisal-derived, institutional, and reader-facing information distinct.
  A projection may reveal only information its viewpoint can causally access.

## Required checks

Before completing a change in this directory, run the relevant narrow checks.
Before accepting a cross-cutting change, run from the repository root:

```bash
python3 tools/validate_system.py
```

