---
id: REP0.1A
decision_uri: author-decision://repository/REP0.1A
title: Locked CAL0 baseline with generated integration layers
domain: repository
workflow_status: ACCEPTED
canon_status: ACCEPTED
scope: LitRPG-Novel repository
accepted_on: 2026-08-12
accepted_by: Author
approval_evidence: "In the project conversation, after receiving the revised plan centred on REP0.1A, the Author instructed: 'please proceed with this' on 2026-08-12."
alternatives_considered: "Split specification; recreate mechanics; intact CAL0 with generated integration"
evidence: "CAL0 README, bundle manifest, closure report, specification, and calibration annex"
dependencies: "none"
conflicts: "none"
supersedes: "none"
superseded_by: "none"
---

# REP0.1A — Locked CAL0 baseline with generated integration layers

## Question

How should the completed CAL0 System be represented and evolved inside the authoring repository?

## Decision

Import CAL0 v0.7.0 intact as a locked, executable LitRPG subsystem. Build reproducible routing indexes and a story-integration layer around it. Any mechanics change must be classified, reviewed, regression-tested where applicable, approved by the Author, and released as a governed successor version rather than silently altering the validated baseline.

## Alternatives considered

1. Split the specification into independently edited topic modules. Rejected because it would create several mutable authorities and weaken the content-pinned evidence chain.
2. Treat CAL0 as research and recreate story mechanics separately. Rejected because it would duplicate already validated architecture and invite divergence between prose and mechanics.
3. Import CAL0 intact and build generated routing plus governed story integration around it. Selected.

## Consequences

- The canonical specification remains whole; it is not split into independently edited topic files.
- CAL0 source, tests, registries, scenarios, reports, authoring material, and manifests retain their internal relationships.
- Topic indexes and story-facing state are derived or layered artifacts, not competing mechanics canon.
- Reference characters, cohorts, scenarios, values, and adversarial fixtures remain non-canonical to the story.
- Story-specific values and unresolved setting distributions live in the story/world integration layer.
- Architecture is closed unless a concrete contradiction, validation failure, infeasibility, new material evidence, or explicit Author request justifies reopening it.
- The earlier v0.60 design handoff is superseded and retained only for provenance.

## Rationale

CAL0 v0.7.0 is a validated, content-pinned I1–I7 baseline implementing specification v0.89 and calibration annex v2.9. Splitting it now would weaken manifest integrity and create multiple editable sources. Generated indexes provide bounded authoring context without destabilising the implementation.

This binding decision replaces the earlier unaccepted planning proposal `REP0.0A`.

## Evidence

- `litrpg-system/cal0/README.md` identifies package v0.7.0, specification v0.89, annex v2.9, and validated closure.
- `litrpg-system/cal0/manifests/cal0-i7.bundle.json` content-pins the complete baseline.
- `litrpg-system/cal0/reports/cal0-i7-closure-report.json` records the successful closure evidence.
- `litrpg-system/cal0/canonical/litrpg-system-specification.md` and `litrpg-system/cal0/canonical/litrpg-system-calibration-annex.md` are the governing mechanical sources.

## Dependencies and conflicts

- Dependencies: none; this is the repository's foundational System-integration decision.
- Conflicts: none identified. The unaccepted `REP0.0A` planning proposal is replaced but was never binding canon.

## Affected sources

- `litrpg-system/cal0/`
- `litrpg-system/indices/`
- `litrpg-system/story-integration/`
- `governance/SOURCE-AUTHORITY.md`
- `archive/handoffs/`

## Residual unknowns

World-level inputs such as rare-Soul prevalence and ordinary prenatal-consciousness distribution remain outside the baseline until the Author accepts setting decisions.

## Reopening conditions

Reopen only for a concrete contradiction, failed validation, authoring infeasibility, material new evidence, required story outcome that cannot be represented, or explicit Author instruction.

## Supersession

- Supersedes: none.
- Superseded by: none.

## Approval evidence

In the project conversation, after receiving the revised plan centred on
`REP0.1A`, the Author instructed, “please proceed with this,” on 2026-08-12.
