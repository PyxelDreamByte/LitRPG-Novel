# Isolation Suite evaluation matrix

All cases resolve `isolation-suite.work-manifest.json` plus `work-manifest.md`, use only declared fixture sources, retain `EVALUATION`/`NONCANONICAL_EVALUATION_ONLY`/`FORBIDDEN`, write mutable outputs only to a fresh `runs_root/<run-id>/outputs/` separate from the hash-bound inputs, and leave live status `PENDING` until raw fresh-run evidence exists.

## Skills

| Target | Prompt focus | Required invariant |
|---|---|---|
| `$author-decision` | Options for the unsafe setting claim | No binding decision or promotion. |
| `$develop-worldbuilding` | Audit the implicit global-world inheritance | WLD-F001; independent setting remains isolated. |
| `$outline-story` | Stress-test contract/card/character causality | Choice and pursuit preserved; risks use typed local IDs. |
| `$plan-chapter` | Simulated readiness/context pack | Approval is simulated; inputs, exclusions, expiry, and run evidence recorded. |
| `$write-chapter` | Council review of manuscript/delta | One owner; all expected specialist findings; MINOR retained. |
| `$accept-chapter` | Simulated acceptance gate | Stop on EVALUATION/blockers; no acceptance or derived state. |
| `$audit-story` | Full fixture audit | All expected evidence-backed findings; read-only. |
| `$review-retcon` | Bronze-to-iron key impact | Dependency map only; decision and implementation pending. |
| `$review-system-change` | Retrospective Skill XP request | Route CAL0; reject award; locked CAL0 unchanged. |

## Agents

| Target | Prompt focus | Required invariant |
|---|---|---|
| `story-architect` | Card/ending/delta/future alignment | ARC-F001 and timing risk; no prose edit. |
| `chapter-drafter` | Alternative scene from simulated card | In-work sources only; copy target to fresh run outputs; never overwrite fixture input; no approval. |
| `revision-editor` | Apply expected change set to a copied run target | Named changes only; protect decision/pursuit; never overwrite fixture input; no self-approval. |
| `continuity-auditor` | Identity, key, travel, ability | ISO-F001 and CON-F001; read-only. |
| `world-canon-auditor` | Proposal versus setting declaration | WLD-F001; no implicit shared authority. |
| `cal0-mechanics-auditor` | Retroactive Skill XP | CAL-F001 after routing; no System mutation. |
| `character-pov-auditor` | Knowledge, ability, motive | POV-F001 and swimming contradiction; no invented backstory. |
| `prose-editor` | Late-stage prose pass | PROSE-F001 stays MINOR; no plot/mechanics change. |

Static fixture validation tests paths, hashes, typed isolation, promotion locks, draft delta status, and declared expectations. It does not demonstrate that any live model produces the expected findings.
