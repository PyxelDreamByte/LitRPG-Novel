---
name: develop-worldbuilding
description: "Develop, challenge, or revise worldbuilding while preserving internal consistency and Author control of canon. Use for cultures, geography, ecology, history, institutions, cosmology, magic, locations, setting implications, or world facts introduced by planning or prose."
---

# Develop Worldbuilding

Treat research as evidence, `PROPOSED` material as non-canon, `PROVISIONAL` material as usable only within its declared boundary, and `ACCEPTED` worldbuilding as canon.

## Run boundary

Resolve exactly one authoring boundary:

- **Setting-init boundary:** only when the current Author instruction explicitly begins a real setting and the project index confirms that no target setting manifest exists. Load only the root governance/world index and empty setting templates. Record mode `SETTING_INIT`. This mode may prepare options for identity, slug, title, authority envelope, and constitutional scope; after explicit Author approval it may create only the `DRAFT`/`PROPOSED` setting shell, registers and an index containing the setting-local initiation decision. Transient evidence may use `workbench/runs/setting-bootstrap/<proposed-slug>/<run-id>/`. It must not establish fictional facts or create any work, story, character, protagonist, outline, chapter, or overlay.
- **Work boundary:** one machine `work-manifest.json` or `*.work-manifest.json` and its paired `work-manifest.md`. Treat JSON as authority; require matching identity, type, mode, canonicality, promotion, root, and setting boundary, or stop. Record `work_id`, `work_root`, and `mode`. Write work-specific proposals or overlays only inside `work_root`; read explicitly adopted shared world canon without copying or modifying it.
- **Setting-authority boundary:** one discoverable `<setting-slug>.setting-manifest.json` and paired `setting-constitution.md` beneath the declared `setting_root`, used before or after works adopt that shared setting. Require matching setting identity, manifest filename, workflow/canon status, root, and index, or stop. Record `setting_id`, `setting_root`, and mode `SETTING_AUTHORITY`. Write setting proposals, decisions, canon, and indexes only beneath `setting_root`; transient run evidence may use `workbench/runs/setting-bootstrap/<setting-slug>/<run-id>/`. Never create or change story, character, protagonist, outline, chapter, work manifest, work contract, or work-local overlay artifacts in this mode.

Reject undeclared cross-work sources and never import another work's overlay. Unadopted project defaults may be read only when the Author explicitly asks to consider them; reading never adopts them, and setting authority work cannot label a project default as work-manifest-adopted without a confirming work manifest. Before a work exists, the Author may instead select a setting-local rule with explicit provenance and scope. In `EVALUATION`, write only beneath the fixture/evaluation root and never promote proposals, update `worldbuilding/`, or change authoritative character/story state.

## Workflow

1. Identify the requested scope and read its index, governing decisions, related canon, and story dependencies. Start from `worldbuilding/templates/worldbuilding-proposal.md`; search before inventing.
2. Classify the work as clarification, extension, reconciliation, replacement, or retcon.
3. Establish constraints from chronology, geography, ecology, material conditions, culture, magic, CAL0, character knowledge, and planned plot. When CAL0 matters, run `python3 tools/route_system_context.py --topic <topic>` or `--decision <selected-option-id>` before reading returned sources.
4. Develop the smallest coherent proposal that answers the request. Trace at least first-order consequences; trace later consequences when they affect active stories.
5. Test the proposal for contradictions, monocausal history, implausible logistics, cultural flattening, accidental omniscience, and exceptions created only to rescue a scene.
6. Distinguish direct canon, reasonable inference, open question, and invention. Cite sources for research-dependent factual claims.
7. Present material choices through `$author-decision`. Do not promote a proposal to canon without Author approval.
8. Preserve the proposal, source manifest, consistency review, and approval evidence under the resolved run directory. In `AUTHORING`, apply the approved scope:
   - For `SETTING_INIT`, create only the Author-approved setting shell, local registers, index containing its initiation decision, and the setting-local initiation decision; then stop and use `SETTING_AUTHORITY` for foundational constraints.
   - For `SETTING_AUTHORITY`, update only the setting-local constitution, proposals, decisions, canon, and indexes beneath `setting_root`. A constitution or setting authority may become binding only through an indexed setting-local Author decision. Preserve reciprocal `adopting_work_ids`. A project default never transfers by presence: if the Author wants its substance to govern the shared setting before a work exists, record a new setting-local rule and decision with explicit provenance and scope; later work manifests adopt that setting-local authority. Work-level adoption of the reusable project default still requires the manifest fields defined by repository policy.
   - For `SHARED_WORLD`, keep shared-setting authority read-only inside the work run. Route proposed shared changes to a separate `SETTING_AUTHORITY` run and Author decision.
   - For `WORK_LOCAL` or `INDEPENDENT_SETTING`, record the accepted decision and update only the work-local overlay/index beneath `work_root`; never update global `worldbuilding/`.
   In `EVALUATION`, stop at findings and write evidence only beneath `runs_root/<run-id>/`; never overwrite hash-bound fixture inputs. Do not rewrite prose unless requested.

## Story-originated facts

Extract new facts introduced during drafting into a canon proposal. Classify local colour separately from setting extensions. Block contradictions and retcons; allow reversible local details to travel with the chapter only when repository policy permits it.

## Output

Return the proposal or accepted change, consistency findings, downstream implications, source/canon status, and unresolved questions.
