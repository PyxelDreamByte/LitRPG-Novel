---
delta_id: "delta://[work-type]/[work-slug]/[unit-slug]/001"
work_id: "work://[work-type]/[work-slug]"
work_manifest_json: "stories/[work-type-directory]/[work-slug]/[work-slug].work-manifest.json"
work_manifest_review: "stories/[work-type-directory]/[work-slug]/work-manifest.md"
display_code: "[WORK-C001-D01]"
chapter_id: "chapter://[work-type]/[work-slug]/[unit-slug]/001"
workflow_status: DRAFT
run_mode: AUTHORING
canon_status: PROPOSED
manuscript_path: "stories/[work-type-directory]/[work-slug]/[unit-path]/manuscript/chapters/001-[slug].md"
manuscript_revision: "[Git commit or immutable revision ID]"
manuscript_sha256: "sha256:[64 lowercase hexadecimal characters]"
previous_accepted_delta: null
created_on: "[YYYY-MM-DD]"
author_accepted_on: null
author_decision_uri: null
author_approval_evidence: null
---

# Chapter Delta — [Chapter ID]

This Markdown record is the Author-facing review of chapter consequences. The paired machine-readable record must validate against the story-integration chapter-delta schema; this template does not define or replace that schema. In the v1 machine record, `status` is the machine spelling of `workflow_status`; `canon_status` remains an independent governance field.

## Transaction summary

- Manuscript path:
- Manuscript revision:
- Manuscript SHA-256:
- Chapter card:
- Context pack:
- Previous accepted story state:
- One-sentence causal change:

## Event register

| Event ID | Time | Location | Actors | Action/change | Cause and inputs | Immediate result | Source scene |
|---|---|---|---|---|---|---|---|
| `event://[work-type]/[work-slug]/[unit-slug]/001/0001` | [time] | [location URI] | [character URIs] | [change] | [provenance] | [result] | [scene/paragraph anchor] |

## Timeline and location

- Time elapsed:
- Travel path and feasible duration:
- Location-state changes:
- Concurrent-event dependencies:
- Calendar/timeline records to update:

## Character-state changes

| Character ID | Before | Change | Cause/event ID | After | Persistent? |
|---|---|---|---|---|---|
| `character://[work-type]/[work-slug]/[character-slug]` | [state] | [change] | [event URI] | [state] | [yes/no/conditional] |

Include injuries, conditions, fatigue, recovery, emotional commitments, identity/body changes, responsibilities, and access.

## Knowledge and belief changes

| Character ID | Fact/source | Access event | Interpretation/confidence | New belief or knowledge | Reader disclosure |
|---|---|---|---|---|---|
| `character://[work-type]/[work-slug]/[character-slug]` | [truth/source] | [event URI] | [view] | [state] | [shown/withheld/partial] |

## Relationship changes

| From | To | Typed relation | Previous state | Change and cause | New state |
|---|---|---|---|---|---|
| [ID] | [ID] | [trust/duty/etc.] | [state] | [event] | [state] |

## Possessions, resources, and claims

| Entity/resource | Change | Quantity/state | Provenance | Owner | Custodian/controller | Access/entitlement |
|---|---|---|---|---|---|---|
| [entity URI] | [gain/loss/use/damage] | [exact state] | [event/source URI] | [owner URI] | [custodian/controller URI] | [scope] |

Keep creation, ownership, possession, custody, access, authority, control, responsibility, contribution, and entitlement distinct.

## CAL0 progression and mechanics

| Character ID | Channel | Lineage/attribute/resource | Before | Evidence or load | Award/adaptation | Cost/recovery/assimilation | After | Provenance |
|---|---|---|---|---|---|---|---|---|
| [character URI] | [maturation/adaptation/Skill XP/Class XP/reinforcement/etc.] | [track ID] | [state] | [event URI] | [change] | [constraint] | [state] | [record URI] |

Checks:

- Natural maturation, organic adaptation, Skill XP, Class XP, reinforcement, and assimilation remain distinct.
- No retrospective XP, duplicated event credit, unfunded resource, or reward replay.
- Offers, acceptance, thresholds, evidence, and projection access are explicit.
- Exact decimal values and source records are preserved where required.

## World and series canon proposals

| Proposal ID | Classification | New claim | Scope | Existing source checked | Required review | Canon status |
|---|---|---|---|---|---|---|
| `canon-proposal://[work-type]/[work-slug]/[unit-slug]/001/01` | [`LOCAL_COLOUR`/`SETTING_EXTENSION`/`CHARACTER_STATE_CHANGE`/`SYSTEM_APPLICATION`/`SYSTEM_CHANGE`/`CONTRADICTION_OR_RETCON`] | [claim] | [scope] | [path/ID] | [`CHAPTER_ACCEPTANCE`/`WORLDBUILDING_REVIEW`/`CONTINUITY_REVIEW`/`CAL0_MECHANICS_REVIEW`/`AUTHOR_DECISION_REQUIRED`] | [`PROPOSED`/`ACCEPTED`/`REJECTED`/`SUPERSEDED`] |

Use the exact uppercase schema enumeration. No row is accepted merely because
the prose contains it. `SYSTEM_CHANGE` and `CONTRADICTION_OR_RETCON` require a
separate `AUTHOR_DECISION_REQUIRED` approval and block the chapter transaction
while unresolved. A `SETTING_EXTENSION` requires `WORLDBUILDING_REVIEW`, a
`CHARACTER_STATE_CHANGE` requires `CONTINUITY_REVIEW`, and a
`SYSTEM_APPLICATION` requires `CAL0_MECHANICS_REVIEW`.

## Plot-thread movement

| Thread ID | Prior state | Chapter action | New state | Promise/payoff affected | Future obligation |
|---|---|---|---|---|---|
| [ID] | [state] | [movement] | [state] | [effect] | [obligation] |

## Outline variance

- Chapter-card beats omitted or changed:
- Unplanned developments:
- Future chapter cards affected:
- Work/unit contract impact:
- Required replanning decision:

## Contradictions and unresolved questions

- Blocking contradictions:
- Intentional ambiguity:
- Deferred state:
- Questions requiring Author decision:

## Gate results

| Gate | Result | Evidence/findings |
|---|---|---|
| Chapter-card compliance | [pass/fail] | [IDs] |
| Continuity and causality | [pass/fail] | [IDs] |
| Character/POV knowledge | [pass/fail] | [IDs] |
| World canon | [pass/fail] | [IDs] |
| CAL0 mechanics | [pass/fail] | [IDs] |
| Plot/future alignment | [pass/fail] | [IDs] |
| Structured schema validation | [pass/fail] | [report] |

## Promotion plan

On acceptance, update or rebuild:

- character state snapshots;
- timeline, thread, and knowledge ledgers;
- inventory/resource/progression views;
- world and series canon records approved above;
- affected future cards and context sources.

## Author decision

- Exact manuscript path: `[path]`
- Exact manuscript revision: `[Git commit or immutable revision ID]`
- Exact manuscript SHA-256: `sha256:[digest]`
- Decision URI: `author-decision://chapter/[display-code]`
- Decided by: `Author`
- Decision: [`ACCEPT`/`REJECT`/`REVISE`]
- Decision date: `[YYYY-MM-DD]`
- Approval evidence: `[verbatim-enough instruction reference or retained evidence path]`
- Delta decision: [`ACCEPT`/`REJECT`/`REVISE`]
- Canon proposals: [per-row decisions and decision URIs]

The transaction is not accepted unless the exact manuscript digest and delta
are explicitly accepted together. Editing the manuscript after approval
invalidates this decision and requires a new revision, digest, validation, and
Author gate.
