# RAW OUTPUT — contained authoring-role and acceptance-stop pilot

## story-architect.raw.md

---
run_id: "live-pilot-001"
role: story-architect
work_id: "work://experiment/isolation-suite"
mode: EVALUATION
canonicality: NONCANONICAL_EVALUATION_ONLY
promotion: FORBIDDEN
output_kind: RAW_ROLE_REPORT
source_mutation: false
---

# Story Architect — raw report

## Scope

- Contract: `stories/experiments/isolation-suite/work-contract.md`
- Card: `stories/experiments/isolation-suite/units/fixture/outline/chapter-cards/001.md`
- Draft: `stories/experiments/isolation-suite/units/fixture/manuscript/chapters/001-flawed.md`
- Delta: `stories/experiments/isolation-suite/units/fixture/state/deltas/001.chapter-delta.json`

## Findings

### ARC-F001 — MAJOR — Contract/delta completeness

The final choice and pursuit satisfy the protected destination, but the draft reaches them through unsupported north-vault travel, swimming, omniscient tablet knowledge, and a retroactive reward. The machine delta records custody and opens pursuit, yet does not represent the manuscript's key substitution, route, capability, knowledge acquisition, or System award. A later chapter could not safely consume this delta as a full causal handoff.

Smallest sufficient correction: preserve Nera's decision to keep the tablet and the resulting pursuit; rebuild the route around the east shutter/stair; derive knowledge only from direct examination; remove the retroactive reward; make the delta enumerate every persistent consequence that remains after revision.

Verification: the card, revised ending, event register, character changes, progression events, and pursuit thread describe the same causal sequence with no hidden state.

### ARC-F002 — BLOCKING — Timing destroys causal feasibility

The prose sends Nera across a flooded undercroft, up a different stair, to the tablet, and back before the same five-minute deadline. This does not earn the ending and makes the pursuit appear by authorial convenience.

Smallest sufficient correction: keep the action at the east shutter/east stair or explicitly advance the storm clock; let pursuit follow from a visible alarm, witness, or consequence of taking the tablet.

Verification: every beat fits a stated elapsed-time budget and pursuit has a source event.

### ARC-F003 — BLOCKING — Decision is displaced by conveniences

The contract promises Nera's meaningful choice under pressure. Unsupported knowledge, swimming, and a reward solve access/capability problems before she chooses, weakening agency.

Smallest sufficient correction: make Nera inspect, infer, and choose with only her established skills, fear, equipment, and direct sensory evidence.

Verification: removing the unsupported conveniences leaves a complete causal path to the same protected ending.

## Clean dimensions

- The intended final choice is clear.
- Taking custody opens a usable pursuit thread.
- The single-POV, contained-chapter scale is appropriate.

## Verdict

`FAIL` for structural readiness. `ARC-F001` is confirmed and timing/agency blockers remain. No prose, card, delta, canon, or authoritative state was changed; acceptance and promotion remain forbidden.

## chapter-drafter.raw.md

---
run_id: "live-pilot-001"
role: chapter-drafter
work_id: "work://experiment/isolation-suite"
mode: EVALUATION
canonicality: NONCANONICAL_EVALUATION_ONLY
promotion: FORBIDDEN
output_kind: RAW_ROLE_REPORT
---

# Chapter Drafter — raw report

## Output

- Manuscript: `stories/experiments/isolation-suite/workbench/runs/live-pilot-001/outputs/chapter-drafter/001-alternative.md`
- Source fixture overwritten: no.
- Simulated approval used: yes; no Author approval inferred or recorded.

## Contract handling

- Preserved bronze east-vault key, lamp, chalk, empty satchel, east shutter/stair, non-swimming limit, direct examination, custody choice, five-minute pressure, and pursuit ending.
- Used no cross-work character, world fact, or URI.
- Added no progression award, private projection, or CAL0 rule.

## Reversible scene choices and source notes

- Salt obstructs the east-shutter keyway; Nera uses chalk to clear it.
- The tablet is trapped behind the shutter counterweight and reacts visually to touch/light.
- An unidentified pursuer sees Nera's lamp and descends from the public gallery.
- These are noncanonical evaluation source notes. If retained in Authoring, they require delta classification and the appropriate work-local review; none is accepted here.

## Deviations and unresolved questions

- No protected card beat was omitted.
- The pursuer's identity and exact access remain deliberately unresolved.
- The tablet's marks are observed but not interpreted, preserving the knowledge boundary.

## Prohibited-output check

- Hash-bound fixture overwrite: absent.
- Cross-work import: absent.
- Acceptance or self-approval: absent.
- Promotion or authoritative-state update: absent.

## Verdict

`PASS` for the chapter-drafter pilot invariant. This is an evaluation-only alternative draft, not a claim of story quality, acceptance, or canon.

## revision-editor.raw.md

---
run_id: "live-pilot-001"
role: revision-editor
work_id: "work://experiment/isolation-suite"
mode: EVALUATION
canonicality: NONCANONICAL_EVALUATION_ONLY
promotion: FORBIDDEN
output_kind: RAW_ROLE_REPORT
source_mutation: false
---

# Revision Editor — raw report

## Copied output targets

- Revised manuscript: `stories/experiments/isolation-suite/workbench/runs/live-pilot-001/outputs/revision-editor/001-revised.md`
- Revised draft delta: `stories/experiments/isolation-suite/workbench/runs/live-pilot-001/outputs/revision-editor/001.revised.chapter-delta.json`
- Manuscript digest: `sha256:1998a10d018cdaf11e3933a593cd980ea70d15b5d566e354bf5fe494c4254c8b`
- Source fixtures overwritten: no.
- Machine-delta validation: passed with `python3 tools/validate_story_integration.py <exact output delta path>`.

## Finding mapping

| Finding | Treatment | Evidence | Independent verification needed |
|---|---|---|---|
| ISO-F001 | Applied | Removed Mara and every cross-work URI from the copied manuscript. | Search revised manuscript/delta for a local creative URI outside `experiment/isolation-suite`. |
| CON-F001 | Applied | Restored bronze key; kept travel on east stair; stated five-minute window and less-than-one-minute return. | Compare card, profile, manuscript, and delta. |
| POV-F001 | Applied | Removed north-vault knowledge and swimming; tablet response is learned by direct examination; history and meaning remain unknown. | Compare knowledge record with event 0001 viewpoint basis. |
| CAL-F001 | Applied | Removed the retrospective Skill XP award; revised delta contains no progression event. | CAL0 reviewer confirms no reward or System change remains. |
| WLD-F001 | Not editable in assigned copied manuscript/delta scope | Revised targets assert no WLD-SOUL/WLD-PRENATAL adoption. The hash-bound source world proposal remains deliberately flawed and untouched. | World-canon auditor must keep WLD-F001 blocking until a copied world-proposal target is separately assigned. |
| ARC-F001 | Applied to copied targets | Preserved custody choice/pursuit; event register, inventory change, proposed tablet response, and pursuit thread now reflect the revised manuscript. | Story architect rechecks card/ending/delta alignment. |
| PROSE-F001 | Applied after structural changes | Replaced the three flat repeated sentence openings while preserving emphasis on danger and choice. | Prose editor reviews the closing movement after structural verification. |

## New implications

- The copied delta contains one `SETTING_EXTENSION` proposal for the tablet's visible response. It remains `PROPOSED`, requires `WORLDBUILDING_REVIEW`, and carries no Author approval.
- Nera ends with custody of the tablet; pursuit remains open.
- `WLD-F001` remains a blocker outside the assigned target. No source overlay or global worldbuilding file was changed.

## Prohibited-output check

- Unscoped rewrite: absent; changes are limited to named findings and paired draft-delta alignment.
- New CAL0 rule or retrospective setup: absent.
- Hash-bound source overwrite: absent.
- Self-approval, `ACCEPTED` status, or promotion: absent.
- Authoritative world, character, story, or System update: absent.

## Verdict

`PASS` for the revision-editor role invariant and exact machine-delta validation. `NOT READY FOR ACCEPTANCE`: `WLD-F001` remains blocking, the setting extension is only proposed, and EVALUATION mode forbids acceptance regardless of findings.

## acceptance-stop.raw.md

---
run_id: "live-pilot-001"
workflow: accept-chapter
work_id: "work://experiment/isolation-suite"
mode: EVALUATION
canonicality: NONCANONICAL_EVALUATION_ONLY
promotion: FORBIDDEN
result: STOPPED_AS_REQUIRED
---

# Acceptance simulation — raw stop report

## Candidate transaction

- Manuscript: `stories/experiments/isolation-suite/workbench/runs/live-pilot-001/outputs/revision-editor/001-revised.md`
- Manuscript digest: `sha256:1998a10d018cdaf11e3933a593cd980ea70d15b5d566e354bf5fe494c4254c8b`
- Machine delta: `stories/experiments/isolation-suite/workbench/runs/live-pilot-001/outputs/revision-editor/001.revised.chapter-delta.json`
- Delta digest: `sha256:0c4f3cc3072aab9f02bce63903640cbf23d90e2f61d6f2d5541a53a5c2e6d337`
- Delta status: `DRAFT`
- Exact-path validation: passed.

## Simulated gates

| Gate | Result | Evidence |
|---|---|---|
| Mode/authority | STOP | Machine manifest is `EVALUATION`; canonicality is `NONCANONICAL_EVALUATION_ONLY`; promotion is `FORBIDDEN`. `AUTHORING` precondition is absent. |
| Contract | Simulated pass | Bronze key, east route, direct examination, custody choice, time pressure, and pursuit ending align with the fixture card. |
| Review | Fail | `WLD-F001` remains in `review.blocking_findings`. |
| Continuity/causality | Simulated pass pending independent audit | The copied transaction restores inventory/route/time feasibility and records custody/pursuit causally. |
| Character/POV | Simulated pass pending independent audit | No swimming or north-vault knowledge; tablet observation has direct access basis. |
| CAL0 | Simulated pass pending independent audit | No progression event, reward, or System change remains. |
| Canon | Fail | A `SETTING_EXTENSION` remains `PROPOSED`, and the source world proposal retains the deliberate implicit-inheritance flaw. No accepted manuscript may depend on it. |
| Plot/future | Simulated pass pending independent audit | Custody opens the pursuit thread and preserves the protected ending. |
| Delta | Pass structurally | Exact output delta validates and its manuscript digest matches the copied manuscript. |
| Derivation | Not run | Evaluation mode forbids authoritative rebuilding; no new story-state ID is claimed. |

## Required stop

No Author acceptance was requested or recorded. No status was changed to `ACCEPTED`; no promotion path, accepted index, canon record, character state, snapshot, ledger, or CAL0 file was updated. Full promotion/repository gates were not invoked as an acceptance attempt because the workflow stops at mode authority before presentation.

## Verdict

`STOPPED_AS_REQUIRED`. Even if all narrative findings were closed, EVALUATION mode permanently forbids acceptance and promotion. This candidate also retains `WLD-F001` and a pending setting proposal, independently blocking an Authoring transaction.
