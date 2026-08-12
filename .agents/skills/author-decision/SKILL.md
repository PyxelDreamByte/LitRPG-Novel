---
name: author-decision
description: "Turn a consequential creative or repository question into a bounded Author decision, record the chosen option and its implications, and update affected plans without silently changing canon. Use for explicit choices, unresolved design questions, canon promotion, or decisions that constrain later story, worldbuilding, or CAL0 work."
---

# Author Decision

Preserve the Author as the sole authority over canon, plot, voice, and acceptance.

## Run boundary

Resolve exactly one authoring boundary before analysis:

- **Setting-init boundary:** only when the current Author instruction explicitly begins a real setting and the project index confirms that no target setting manifest exists. Load only the root governance/world index and empty setting templates. Record mode `SETTING_INIT`. Limit decisions to stable setting identity, slug, title, shared-setting authority envelope, and the location/status of a `DRAFT`/`PROPOSED` shell. After explicit Author approval, this mode may create only the required setting directory, manifest, constitution, local registers, an index containing its setting-local initiation decision, and that initiation decision. Transient evidence may use `workbench/runs/setting-bootstrap/<proposed-slug>/<run-id>/`. It may not establish fictional facts or create any work, story, character, protagonist, outline, chapter, or overlay.
- **Work boundary:** one machine `work-manifest.json` or `*.work-manifest.json` and its paired `work-manifest.md`. Treat JSON as authority; require matching identity, type, mode, canonicality, promotion, root, and setting boundary, or stop. Record `work_id`, `work_root`, and `mode`; reject target or mutable dependency paths outside `work_root`.
- **Setting-authority boundary:** one discoverable `<setting-slug>.setting-manifest.json` and its paired `setting-constitution.md` beneath the declared `setting_root`, used before or after works adopt that shared setting. Require matching setting identity, manifest filename, workflow/canon status, root, and index, or stop. Record `setting_id`, `setting_root`, and mode `SETTING_AUTHORITY`. Setting artifacts remain beneath `setting_root`; transient run evidence may use `workbench/runs/setting-bootstrap/<setting-slug>/<run-id>/`. Never create or change a work manifest, work contract, story, character, protagonist, outline, chapter, or work-local overlay in this mode.

Shared governance, CAL0, and research are read-only dependencies. Unadopted project defaults may be read only when the Author explicitly asks to consider them; reading never adopts them, and setting authority work cannot label a project default as work-manifest-adopted without a confirming work manifest. Before a work exists, the Author may instead select a setting-local rule with explicit provenance and scope. In `EVALUATION`, create only simulated options/findings inside the fixture or evaluation run: never request or record a binding Author decision, promote anything, or update authoritative world, character, or story state.

## Workflow

1. Read the governing policy, relevant canon, active proposal, and dependent plans. Load only the material needed for the decision.
2. State the decision boundary in one sentence. Separate the actual choice from consequences that follow automatically.
3. Present two to four viable options. Give each a stable local label, a concise description, benefits, costs, compatibility constraints, and likely downstream effects.
4. Recommend one option when evidence supports it. State the reasoning and uncertainty; do not manufacture neutrality.
5. In `AUTHORING`, ask the Author to choose before recording any binding decision. This always includes canon promotion, CAL0 reopening, retcons, and material plot or repository direction. Stop and wait; never infer a selection. In `EVALUATION`, compare the simulated output with expected invariants and leave the selection pending.
6. After the Author answers, assign or retain the decision ID and record the exact choice using `governance/templates/decision-record.md`: rationale, status, scope, approval evidence, consequences, affected sources, dependencies/conflicts, residual unknowns, supersession links, and reopening conditions. Validate a structured decision record against `governance/schemas/decision-record.schema.json` when one is created. A setting-init or setting-authority decision must declare the matching `setting_id` and live under `<setting_root>/decisions/` once the proposed shell exists.
7. Preserve the option analysis, source manifest, validation, and approval evidence under the resolved work manifest's `runs_root/<run-id>/` or the setting-bootstrap run root. Update only the plans or proposals directly authorized by the choice. List further changes that require separate work.

## Status discipline

Use the repository's canonical status vocabulary. Never interpret silence, an agent consensus, or draft prose as Author approval. Preserve rejected options and rationale when they will prevent the question from being reopened accidentally.

## Output

Return the decision, its implications, files changed, validation performed, and any next decision in dependency order.
