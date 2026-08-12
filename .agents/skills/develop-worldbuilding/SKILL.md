---
name: develop-worldbuilding
description: "Develop, challenge, or revise worldbuilding while preserving internal consistency and Author control of canon. Use for cultures, geography, ecology, history, institutions, cosmology, magic, locations, setting implications, or world facts introduced by planning or prose."
---

# Develop Worldbuilding

Treat research as evidence, `PROPOSED` material as non-canon, `PROVISIONAL` material as usable only within its declared boundary, and `ACCEPTED` worldbuilding as canon.

## Workflow

1. Identify the requested scope and read its index, governing decisions, related canon, and story dependencies. Start from `worldbuilding/templates/worldbuilding-proposal.md`; search before inventing.
2. Classify the work as clarification, extension, reconciliation, replacement, or retcon.
3. Establish constraints from chronology, geography, ecology, material conditions, culture, magic, CAL0, character knowledge, and planned plot. When CAL0 matters, run `python3 tools/route_system_context.py --topic <topic>` or `--decision <selected-option-id>` before reading returned sources.
4. Develop the smallest coherent proposal that answers the request. Trace at least first-order consequences; trace later consequences when they affect active stories.
5. Test the proposal for contradictions, monocausal history, implausible logistics, cultural flattening, accidental omniscience, and exceptions created only to rescue a scene.
6. Distinguish direct canon, reasonable inference, open question, and invention. Cite sources for research-dependent factual claims.
7. Present material choices through `$author-decision`. Do not promote a proposal to canon without Author approval.
8. Preserve the proposal, source manifest, consistency review, and approval evidence under `workbench/runs/<run-id>/`. Once approved, use `worldbuilding/templates/worldbuilding-decision.md`, update the authoritative worldbuilding entry and index together, and validate a structured record against `governance/schemas/worldbuilding-record.schema.json` when one is created. Do not rewrite prose unless requested.

## Story-originated facts

Extract new facts introduced during drafting into a canon proposal. Classify local colour separately from setting extensions. Block contradictions and retcons; allow reversible local details to travel with the chapter only when repository policy permits it.

## Output

Return the proposal or accepted change, consistency findings, downstream implications, source/canon status, and unresolved questions.
