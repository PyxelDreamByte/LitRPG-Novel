---
name: develop-worldbuilding
description: "Develop, challenge, or revise worldbuilding while preserving internal consistency and Author control of canon. Use for cultures, geography, ecology, history, institutions, cosmology, magic, locations, setting implications, or world facts introduced by planning or prose."
---

# Develop Worldbuilding

Treat research as evidence, `PROPOSED` material as non-canon, `PROVISIONAL` material as usable only within its declared boundary, and `ACCEPTED` worldbuilding as canon.

## Run boundary

Resolve exactly one machine `work-manifest.json` or `*.work-manifest.json` and its paired `work-manifest.md`. Treat JSON as authority; require matching identity, type, mode, canonicality, promotion, root, and setting boundary, or stop. Record `work_id`, `work_root`, and `mode`. Write work-specific proposals or overlays only inside `work_root`; read shared world canon without copying or modifying it. Reject undeclared cross-work sources and never import another work's overlay. In `EVALUATION`, write only beneath the fixture/evaluation root and never promote proposals, update `worldbuilding/`, or change authoritative character/story state.

## Workflow

1. Identify the requested scope and read its index, governing decisions, related canon, and story dependencies. Start from `worldbuilding/templates/worldbuilding-proposal.md`; search before inventing.
2. Classify the work as clarification, extension, reconciliation, replacement, or retcon.
3. Establish constraints from chronology, geography, ecology, material conditions, culture, magic, CAL0, character knowledge, and planned plot. When CAL0 matters, run `python3 tools/route_system_context.py --topic <topic>` or `--decision <selected-option-id>` before reading returned sources.
4. Develop the smallest coherent proposal that answers the request. Trace at least first-order consequences; trace later consequences when they affect active stories.
5. Test the proposal for contradictions, monocausal history, implausible logistics, cultural flattening, accidental omniscience, and exceptions created only to rescue a scene.
6. Distinguish direct canon, reasonable inference, open question, and invention. Cite sources for research-dependent factual claims.
7. Present material choices through `$author-decision`. Do not promote a proposal to canon without Author approval.
8. Preserve the proposal, source manifest, consistency review, and approval evidence under the work's declared run directory. In `AUTHORING`, apply the approved scope:
   - For `SHARED_WORLD`, update a global worldbuilding entry and index only when the manifest explicitly adopts that shared setting and the Author decision grants shared-setting authority; use `worldbuilding/templates/worldbuilding-decision.md` and validate any structured record against `governance/schemas/worldbuilding-record.schema.json`.
   - For `WORK_LOCAL` or `INDEPENDENT_SETTING`, record the accepted decision and update only the work-local overlay/index beneath `work_root`; never update global `worldbuilding/`.
   In `EVALUATION`, stop at findings and write evidence only beneath `runs_root/<run-id>/`; never overwrite hash-bound fixture inputs. Do not rewrite prose unless requested.

## Story-originated facts

Extract new facts introduced during drafting into a canon proposal. Classify local colour separately from setting extensions. Block contradictions and retcons; allow reversible local details to travel with the chapter only when repository policy permits it.

## Output

Return the proposal or accepted change, consistency findings, downstream implications, source/canon status, and unresolved questions.
