---
schema_version: "1.0.0"
work_id: "work://[work-type]/[work-slug]"
display_code: "WORK-001"
title: "[Working title]"
work_type: "[SERIES|STANDALONE_NOVEL|NOVELLA|SHORT_STORY|EXPERIMENT]"
mode: AUTHORING
canonicality: PROPOSED
promotion: ALLOWED_WITH_AUTHOR_GATE
work_root: "stories/[work-type-directory]/[work-slug]"
contract_path: "stories/[work-type-directory]/[work-slug]/work-contract.md"
characters_root: "stories/[work-type-directory]/[work-slug]/characters"
world_overlay_root: "stories/[work-type-directory]/[work-slug]/world-overlay"
context_packs_root: "stories/[work-type-directory]/[work-slug]/workbench/context-packs"
runs_root: "stories/[work-type-directory]/[work-slug]/workbench/runs"
setting_scope: "[SHARED_WORLD|WORK_LOCAL|INDEPENDENT_SETTING]"
shared_setting_id: null
adopted_shared_world_refs: []
adopted_default_guardrails: []
shared_read_only_authorities: ["governance/","litrpg-system/cal0/"]
created_on: "[YYYY-MM-DD]"
accepted_on: null
approval_decision_uri: null
---

# Work Manifest — [Title]

This is the human review surface paired with `work-manifest.json` or a discoverable `<work-slug>.work-manifest.json`. The JSON record validated by `litrpg-system/story-integration/schemas/work-manifest.schema.json` is the machine authority. Both files must match field for field; any mismatch blocks work. Encode every frontmatter array as a single-line JSON array so parity is machine-checkable.

Copy `work-manifest.example.json` beside the populated Markdown file as `<work-slug>.work-manifest.json` (recommended) or `work-manifest.json`, replace every example value, mirror it here, and validate the exact JSON path before authoring. Both names are discovered by the repository validator.

## Identity and mode

- Work ID/type:
- Mode: `AUTHORING` or `EVALUATION`
- Canonicality and promotion rule:
- Work root:

`EVALUATION` requires `canonicality: NONCANONICAL_EVALUATION_ONLY` and `promotion: FORBIDDEN`. Evaluation artifacts can never be converted in place; extract an idea as a new `PROPOSED` Authoring artifact through a separate workflow.

## Setting declaration

- `SHARED_WORLD`: name `shared_setting_id` and enumerate every adopted world decision/record and default guardrail.
- `WORK_LOCAL`: use only the work overlay plus explicitly enumerated shared references.
- `INDEPENDENT_SETTING`: adopt no global world facts unless individually listed as inspiration, never authority.

Repository presence is not adoption. In particular, WLD-SOUL, WLD-PRENATAL, and any default world guardrails apply only when explicitly listed.

Each `adopted_default_guardrails` item is an object with `decision_uri`, `adopted_scope`, and `effective_revision`; do not use an unscoped string.

In `AUTHORING`, `PROVISIONAL` or `ACCEPTED` canonicality requires both `accepted_on` and `approval_decision_uri`. In `EVALUATION`, both remain null.

## Path boundary

All mutable story, character, overlay, context-pack, run, editorial, and derived-state paths remain beneath `work_root`. Character and story URIs begin `character://[work-type]/[work-slug]/...` and `chapter://[work-type]/[work-slug]/...`, matching the typed work ID. Cross-work dependencies are forbidden unless listed below and separately approved.

## Explicit cross-work dependencies

- [Normally none. Include source work ID, exact read-only artifact, reason, and Author decision.]

## Validation

- Manifest revision/digest:
- Last isolation check:
- Unresolved boundary questions:
