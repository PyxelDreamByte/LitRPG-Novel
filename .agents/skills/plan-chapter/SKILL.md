---
name: plan-chapter
description: "Prepare a bounded chapter contract and context pack before prose is drafted. Use when the Author wants to plan, prepare, unblock, or hand off a chapter while preserving continuity with prior chapters, future outline constraints, world canon, character knowledge, and CAL0 mechanics."
---

# Plan Chapter

Create a compact, traceable context pack. Do not substitute a repository-wide dump for routing judgement.

## Workflow

1. Identify the exact story, book, chapter, branch, and authoritative predecessor.
2. Read the story/book contract, current chapter card, preceding accepted chapter summary and final scene, relevant future cards, active threads, character states, world facts, and CAL0 story guidance.
3. Resolve conflicts among sources using the repository source-authority policy. Use `$author-decision` if the conflict changes intended plot or canon.
4. Prepare or verify the chapter contract: opening state, intended ending state, POV, time/location, purpose, promises, required beats, constraints, allowed discoveries, and acceptance criteria. If the card is not explicitly Author-approved under the workflow's declared rule, present it for approval and stop; do not label it locked.
5. After approval, record the approval evidence and immutable card revision. Run `python3 tools/route_system_context.py --topic <topic>` or `--decision <selected-option-id>` for each relevant System topic. Use the generated route before reading the returned guide, scenario, specification sections, or numerical authorities.
6. Save the bounded context pack under `workbench/context-packs/`. Record:
   - stable pack ID, purpose, workflow run ID, and creation time;
   - target chapter and immutable card/predecessor revision;
   - every source path, immutable identifier/digest where available, and `ACCEPTED`, `PROVISIONAL`, or `PROPOSED` status;
   - explicit exclusions, unresolved questions, and drafting freedoms;
   - expiry condition, including any predecessor, card, canon, character-state, or CAL0 authority change;
   - preceding state and immediate continuity;
   - future obligations and forbidden outcomes;
   - character motives, relationships, knowledge, inventory, injuries, and conditions;
   - relevant world and System rules;
   - voice/style constraints;
   - expected chapter-delta fields;
7. Save a run manifest under `workbench/runs/<run-id>/` linking the approved card, context pack, source manifest, readiness result, and validation evidence.
8. Run a readiness and staleness check. Distinguish blockers from choices the drafter may make locally.

## Boundaries

Do not decide unresolved canon, invent retroactive setup, award progression, or draft the full chapter unless the Author also invokes the corresponding workflow.

## Output

Return the approved card revision, bounded context-pack ID/path, run-manifest path, readiness result, sources and exclusions, expiry condition, and blocking decisions.
