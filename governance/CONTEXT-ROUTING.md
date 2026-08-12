# Context Routing

## Principle

Load the smallest authoritative context that can safely complete the task. Context packs are disposable projections; they never replace their cited sources.

## Universal context

Every workflow receives:

1. Root and nearest nested `AGENTS.md` files.
2. Author authority, canon policy, and source authority.
3. The active task contract and acceptance criteria.
4. Relevant accepted decisions and explicitly labelled provisional material.

## Task routes

### Worldbuilding

Load the project world index, the named setting manifest, directly affected
setting-local canon, related accepted decisions, relevant research citations,
and any System rules the proposal touches. Load a project default only when the
work manifest explicitly adopts it.

For setting initiation before a manifest exists, load only the current explicit
Author instruction, project world index, governance rules, and empty setting
templates. Limit output to identity, slug, title, authority envelope,
constitutional scope, and creation of an empty proposed shell after approval.

For setting authority work before or after adoption by a story work, use the discoverable setting
manifest and paired constitution as the mutable boundary. Load an unadopted
project default only when the Author explicitly asks to consider adoption.
Reading or comparing that default never adopts it, and it cannot be recorded as a work-level adoption until a work manifest confirms the decision URI, scope, and revision. Before a work exists, the Author may instead approve a setting-local rule with explicit provenance and scope.
Do not create story or character context to satisfy a setting-authority run.

Do not load unrelated settings, continents, cultures, history, work overlays, or
synthetic evaluation material.

### Character work

Load the character profile, arc contract, relationship edges, current accepted state, knowledge boundary, and directly relevant story/world sources. Keep private truth separate from viewpoint knowledge and reader disclosure.

### Chapter planning and drafting

Build a bounded pack containing:

- series and book contracts;
- current chapter card;
- previous accepted chapter summary and final scene;
- only the future cards needed to preserve planned destinations;
- active plot-thread obligations;
- POV character state, relationships, and knowledge;
- current time, location, inventory, equipment, injuries, conditions, and resources;
- relevant accepted world canon;
- relevant CAL0 rules, progression state, and presentation permissions;
- voice guidance and the chapter acceptance rubric.

### CAL0 mechanics

Use this escalation order:

1. story-facing guide;
2. relevant worked scenarios or authoring templates;
3. generated topic and decision indexes;
4. directly relevant sections of the canonical specification;
5. calibration annex, registries, or executable reports when exact behaviour matters.

Do not load the complete specification by default. The specification and annex prevail over projections if they conflict.

### Review and audit

Reviewers receive the manuscript or proposal, its contract, the sources governing their specialty, and the declared delta. They should not be primed with other reviewers' conclusions before their independent pass.

## Context-pack requirements

Every generated pack records:

- pack ID, purpose, workflow run, and creation time;
- target artifact and revision;
- source paths and immutable identifiers where available;
- accepted/provisional/proposed state of every source;
- explicit exclusions and unresolved questions;
- expiry condition.

Never infer authority from inclusion in a context pack. Delete or rebuild stale packs rather than editing them into a shadow canon.
