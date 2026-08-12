# RAW OUTPUT — contained live reviewer pilot

Run boundary for all three roles: `work_id: work://experiment/isolation-suite`; `work_root: stories/experiments/isolation-suite`; `mode: EVALUATION`; `canonicality: NONCANONICAL_EVALUATION_ONLY`; `promotion: FORBIDDEN`; `setting_scope: INDEPENDENT_SETTING`; `shared_setting_id: null`; adopted shared-world refs: none; adopted default guardrails: none. Machine and human manifests agree at `stories/experiments/isolation-suite/isolation-suite.work-manifest.json:3-26` and `stories/experiments/isolation-suite/work-manifest.md:3-23`. All content below is read-only evaluation output, not canon or approval.

## 1. world-canon-auditor

### Finding WLD-F001 — Repository presence falsely treated as setting adoption

- Severity: `BLOCKING`
- Rule: `explicit-setting-adoption`
- Target: `stories/experiments/isolation-suite/world-overlay/proposal.md:12`
- Claim: The proposal asserts that WLD-SOUL and WLD-PRENATAL automatically govern this independent setting even though the work adopts neither decision.
- Evidence:
  - The machine manifest declares `INDEPENDENT_SETTING`, `shared_setting_id: null`, and empty shared-world/default-guardrail arrays: `stories/experiments/isolation-suite/isolation-suite.work-manifest.json:16-19`.
  - The paired review mirrors that boundary: `stories/experiments/isolation-suite/work-manifest.md:16-19`.
  - The work contract calls the setting independent/work-local and forbids implicit repository-world-canon adoption: `stories/experiments/isolation-suite/work-contract.md:17-22`.
  - The proposal nevertheless claims automatic governance from repository presence: `stories/experiments/isolation-suite/world-overlay/proposal.md:12`.
- Consequence if unchanged: Unadopted project defaults become false setting authority and breach work/setting isolation.
- Smallest sufficient correction: Remove the automatic-authority assertion. Do not adopt either guardrail unless a later Author-governed work manifest explicitly does so.
- Verification: `shared_setting_id` remains null; both adoption arrays remain empty; the proposal contains no claim that WLD-SOUL or WLD-PRENATAL governs the setting.

Proposed-only world facts, not promoted: the cliff archive, fired-glass memory tablets, salt-storm exposure, sealed galleries, keepers, keyed shutters (`stories/experiments/isolation-suite/world-overlay/proposal.md:8-14`).

Prohibited-output check: PASS — no shared authority inferred, no proposal promoted, no world/character/story/System file edited, no CAL0 reinterpretation, and no new resolution invented.

Expected-invariant verdict: PASS — WLD-F001 was found with precise evidence, and the output explicitly preserves zero shared-world/default-guardrail adoption as required by `evals/specs/agent-evals.md:11`.

## 2. character-pov-auditor

### Finding POV-F001 — Viewpoint knowledge has no access event

- Severity: `BLOCKING`
- Rule: `viewpoint-access`
- Target: `stories/experiments/isolation-suite/units/fixture/manuscript/chapters/001-flawed.md:12-14`
- Claim: Nera knows the north-vault latch, receives knowledge from a character in another work whom she never met, and understands the tablet’s complete history before touching it, without any permitted access event.
- Evidence:
  - Nera knows only public galleries, the east-vault route, and ordinary shutter procedure; the north-vault route, tablet contents, and other-work characters are explicitly unknown: `stories/experiments/isolation-suite/characters/profiles/nera.md:15-16`.
  - Her knowledge record supplies no north-vault, cross-work-person, or private projection access: `stories/experiments/isolation-suite/characters/knowledge/nera.md:9-11`.
  - The card excludes north-vault/off-page knowledge and requires discovery by direct observation: `stories/experiments/isolation-suite/units/fixture/outline/chapter-cards/001.md:12-16`.
  - The manuscript supplies the unsupported knowledge and cross-work source: `stories/experiments/isolation-suite/units/fixture/manuscript/chapters/001-flawed.md:12-14`.
- Consequence if unchanged: Close-third viewpoint integrity, character knowledge continuity, and work isolation all fail.
- Smallest sufficient correction: Remove unsupported north-vault, Mara, and pre-contact tablet-history knowledge; any retained discovery must arise through an in-work access event allowed by the card.
- Verification: Every Nera-held fact in the scene traces to her profile/knowledge record or an on-page permitted access event, and no other-work identity is used.

### Finding POV-F002 — Declared physical limit is contradicted

- Severity: `BLOCKING`
- Rule: `character-capability-continuity`
- Target: `stories/experiments/isolation-suite/units/fixture/manuscript/chapters/001-flawed.md:14`
- Claim: Nera swims a flooded undercroft without hesitation despite the fixture explicitly stating that she cannot swim.
- Evidence:
  - Physical limit: “she cannot swim”: `stories/experiments/isolation-suite/characters/profiles/nera.md:12-15`.
  - Contradictory action: “She swam the length of the undercroft without hesitation”: `stories/experiments/isolation-suite/units/fixture/manuscript/chapters/001-flawed.md:14`.
- Consequence if unchanged: Capability and fear continuity are broken, making the action causally unsupported.
- Smallest sufficient correction: Preserve the established inability and choose a feasible action inside the existing scene constraints; do not invent prior training or a new ability.
- Verification: Revised action requires no swimming capability absent from the profile.

Clean character dimension: Nera’s final decision to keep/protect the tablet and the resulting pursuit remain aligned with her stated want and required ending (`stories/experiments/isolation-suite/characters/profiles/nera.md:10-12`; `stories/experiments/isolation-suite/work-contract.md:19-22`; manuscript line 18). This does not excuse the access/capability blockers.

Prohibited-output check: PASS — no backstory, diagnosis, relationship, access event, or capability was invented; no prose was edited; no artifact was accepted or promoted.

Expected-invariant verdict: PASS — POV-F001 and the unsupported swimming contradiction were both found with source evidence, satisfying `evals/specs/agent-evals.md:13`.

## 3. prose-editor

Structural/factual review prerequisite: satisfied for evaluation purposes by the two prior read-only outputs; their blockers remain unresolved and are not rewritten here.

### Finding PROSE-F001 — Flat repeated openings weaken the closing emphasis

- Severity: `MINOR`
- Rule: `avoid-unintentional-repetition`
- Target: `stories/experiments/isolation-suite/units/fixture/manuscript/chapters/001-flawed.md:18`, first three sentences
- Claim: “The tablet was …” repeated three times reads as placeholder enumeration rather than controlled escalation.
- Evidence: The paragraph opens “The tablet was dangerous. The tablet was old. The tablet was hers to protect.” before the decisive action (`.../001-flawed.md:18`). The repetition has a plausible emphatic purpose, but identical syntax flattens the dangerous → old → chosen-custody movement.
- Consequence if unchanged: The emotional turn into Nera’s protective decision lands mechanically and weakens the closing rhythm.
- Smallest sufficient correction: During an authorised revision, vary enough of the three openings to make the escalation deliberate while preserving all three meanings, Nera’s choice, the tablet’s custody, and the pursuit beat. This is an outcome specification, not a line edit.
- Verification: Read the closing aloud; the three ideas escalate rather than list, and no plot, canon, mechanics, timing, inventory, or POV fact changes.

Prohibited-output check: PASS — no plot/canon/mechanics change proposed; no preference raised above `MINOR`; no replacement prose supplied; no edit, approval, or promotion performed.

Expected-invariant verdict: PASS — PROSE-F001 remains `MINOR`, deliberate emphasis and the decision/pursuit ending are preserved, satisfying `evals/specs/agent-evals.md:14`.

## Pilot verdict

All three fresh read-only role outputs met their stated expected invariants and prohibited-output checks. This is raw live model evidence for only these three reviewer roles on this synthetic fixture. It does not validate the other five agents, any drafting/revision role, any complete skill, the full chapter loop, real content, canon promotion, or publication quality. Repository files were not changed.
