---
run_id: "eval://isolation-suite/static-001"
workflow_status: EXPECTED
canon_status: NONCANONICAL_EVALUATION_ONLY
---

# Expected review findings

| Finding ID | Reviewer role | Severity | Target | Rule ID | Smallest sufficient correction | Verification |
|---|---|---|---|---|---|---|
| ISO-F001 | continuity-auditor | BLOCKING | Manuscript paragraph 2 | work-scope-cross-reference | Remove the borrowed-work character and replace it only with an in-work access event if needed. | No local creative URI names another typed work identity. |
| CON-F001 | continuity-auditor | BLOCKING | Paragraphs 1 and 5 | inventory-time-continuity | Restore the bronze key and make travel fit the five-minute constraint. | Card, profile, prose, and delta agree on key and elapsed time. |
| POV-F001 | character-pov-auditor | BLOCKING | Paragraphs 2–3 | viewpoint-access | Remove unsupported north-vault and tablet-history knowledge or add permitted direct access events. | Every fact has an in-work access basis. |
| CAL-F001 | cal0-mechanics-auditor | BLOCKING | Paragraph 4 | no-retrospective-xp | Remove the retroactive Skill XP award; do not alter CAL0. | No old natural activity is reclassified as Skill XP. |
| WLD-F001 | world-canon-auditor | BLOCKING | World proposal | explicit-setting-adoption | Remove implicit WLD-SOUL/WLD-PRENATAL inheritance from the independent overlay. | Adopted shared-world and guardrail arrays remain empty. |
| ARC-F001 | story-architect | MAJOR | Ending and machine delta | contract-delta-completeness | Preserve the pursuit-causing choice and enumerate all resulting state that survives revision. | Card, ending, event register, and thread movement align. |
| PROSE-F001 | prose-editor | MINOR | Paragraph 5 | avoid-unintentional-repetition | Replace the three flat repeated sentence openings while preserving emphasis. | Repetition reads as deliberate rhythm rather than placeholder exposition. |

These are expected fixture outcomes, not proof that a live model will find them.
