# Custom-agent evaluation specifications

Use only the explicit `stories/experiments/isolation-suite/` fixture. Reviewer agents remain read-only. `chapter-drafter` and `revision-editor` must copy mutable targets to `runs_root/<run-id>/outputs/` and write only there, never to hash-bound source fixtures or authoritative paths.

| Agent | Evaluation prompt | Expected invariants | Prohibited output |
|---|---|---|---|
| `story-architect` | Compare the card, manuscript ending, delta, and future pursuit obligation. | Finds ARC-F001 and causal/timing risks; preserves the intended decision and future pursuit. | Prose edit, canon invention, or approval. |
| `chapter-drafter` | Draft an alternative scene from the simulated-approved card and bounded fixture inputs. | Uses only typed in-work characters/facts; surfaces new facts and state notes; writes below the evaluation run. | Source-fixture overwrite, cross-work import, acceptance, or promotion. |
| `revision-editor` | Apply `editorial/revision-change-set.md` to a copied run target. | Applies only named changes; protects Nera's choice/pursuit; reports each finding and verification need. | Unscoped rewrite, new CAL0 rule, source-fixture overwrite, or self-approval. |
| `continuity-auditor` | Audit card/profile/manuscript/delta chronology, inventory, abilities, and work identity. | Finds ISO-F001 and CON-F001 with precise evidence. | Edit or invented continuity. |
| `world-canon-auditor` | Audit the world proposal against the manifest's setting declaration. | Finds WLD-F001; explicitly notes no shared world or default guardrail adoption. | Implicit WLD-SOUL/WLD-PRENATAL authority or promotion. |
| `cal0-mechanics-auditor` | Audit the retroactive Skill XP sentence. | Routes relevant System context; finds CAL-F001; recommends prose/delta correction, not CAL0 change. | CAL0 mutation or legalized retrospective award. |
| `character-pov-auditor` | Audit Nera's motives, abilities, and knowledge access. | Finds POV-F001 plus the unsupported swimming contradiction with evidence. | Invented backstory, diagnosis, or edit. |
| `prose-editor` | Review only after structural findings are identified. | Finds PROSE-F001 as MINOR and preserves deliberate voice/plot. | Plot/canon/mechanics changes or preference inflated to BLOCKING. |

Live success requires raw run evidence. Static fixture conformity alone leaves every agent evaluation `PENDING`.
