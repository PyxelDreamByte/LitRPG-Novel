# CAL0-I6 authoring templates and change control

**Specification:** 0.88  
**Calibration annex:** 2.8

Use the artifact template before drafting, the scene template immediately before prose, and the change register whenever an apparent contradiction or desired exception appears.

## Artifact checklists

### Character

Required questions:

- What is causally true?
- What source records or observes it?
- Who can access and interpret it?
- What costs, dependencies, recovery, and failure remain?
- What provenance key prevents semantic duplication?
- What should the viewpoint and reader actually see?

Locked checks:

- no universal total power
- no label-created capability
- no retrospective progression
- no duplicated identity or entitlement
- no unwitnessed resource or renewal
- no damage-derived free growth

Type-specific checks:

- species and life stage
- absolute attributes
- condition
- Skills/classes separately
- access and relationships

### Skill

Required questions:

- What is causally true?
- What source records or observes it?
- Who can access and interpret it?
- What costs, dependencies, recovery, and failure remain?
- What provenance key prevents semantic duplication?
- What should the viewpoint and reader actually see?

Locked checks:

- no universal total power
- no label-created capability
- no retrospective progression
- no duplicated identity or entitlement
- no unwitnessed resource or renewal
- no damage-derived free growth

Type-specific checks:

- coherent domain
- evidence
- acceptance
- XP
- attestation
- techniques
- reinforcement

### Class

Required questions:

- What is causally true?
- What source records or observes it?
- Who can access and interpret it?
- What costs, dependencies, recovery, and failure remain?
- What provenance key prevents semantic duplication?
- What should the viewpoint and reader actually see?

Locked checks:

- no universal total power
- no label-created capability
- no retrospective progression
- no duplicated identity or entitlement
- no unwitnessed resource or renewal
- no damage-derived free growth

Type-specific checks:

- role pattern
- prospective acceptance
- responsibility
- Class XP
- successor ancestry

### Spell

Required questions:

- What is causally true?
- What source records or observes it?
- Who can access and interpret it?
- What costs, dependencies, recovery, and failure remain?
- What provenance key prevents semantic duplication?
- What should the viewpoint and reader actually see?

Locked checks:

- no universal total power
- no label-created capability
- no retrospective progression
- no duplicated identity or entitlement
- no unwitnessed resource or renewal
- no damage-derived free growth

Type-specific checks:

- method graph
- Mana source
- control
- casting stages
- interruption
- residuals

### Item

Required questions:

- What is causally true?
- What source records or observes it?
- Who can access and interpret it?
- What costs, dependencies, recovery, and failure remain?
- What provenance key prevents semantic duplication?
- What should the viewpoint and reader actually see?

Locked checks:

- no universal total power
- no label-created capability
- no retrospective progression
- no duplicated identity or entitlement
- no unwitnessed resource or renewal
- no damage-derived free growth

Type-specific checks:

- components
- identity continuity
- quality
- condition
- ownership
- appraisal uncertainty

### Dungeon

Required questions:

- What is causally true?
- What source records or observes it?
- Who can access and interpret it?
- What costs, dependencies, recovery, and failure remain?
- What provenance key prevents semantic duplication?
- What should the viewpoint and reader actually see?

Locked checks:

- no universal total power
- no label-created capability
- no retrospective progression
- no duplicated identity or entitlement
- no unwitnessed resource or renewal
- no damage-derived free growth

Type-specific checks:

- site/controller
- inputs
- spawn mechanism
- recovery
- ecology
- claims

### Institution

Required questions:

- What is causally true?
- What source records or observes it?
- Who can access and interpret it?
- What costs, dependencies, recovery, and failure remain?
- What provenance key prevents semantic duplication?
- What should the viewpoint and reader actually see?

Locked checks:

- no universal total power
- no label-created capability
- no retrospective progression
- no duplicated identity or entitlement
- no unwitnessed resource or renewal
- no damage-derived free growth

Type-specific checks:

- people
- assets
- procedures
- authority scopes
- distributed capability
- turnover

### Progression Event

Required questions:

- What is causally true?
- What source records or observes it?
- Who can access and interpret it?
- What costs, dependencies, recovery, and failure remain?
- What provenance key prevents semantic duplication?
- What should the viewpoint and reader actually see?

Locked checks:

- no universal total power
- no label-created capability
- no retrospective progression
- no duplicated identity or entitlement
- no unwitnessed resource or renewal
- no damage-derived free growth

Type-specific checks:

- canonical event origin
- live requirements
- contribution
- entitlement
- assimilation

### Notification

Required questions:

- What is causally true?
- What source records or observes it?
- Who can access and interpret it?
- What costs, dependencies, recovery, and failure remain?
- What provenance key prevents semantic duplication?
- What should the viewpoint and reader actually see?

Locked checks:

- no universal total power
- no label-created capability
- no retrospective progression
- no duplicated identity or entitlement
- no unwitnessed resource or renewal
- no damage-derived free growth

Type-specific checks:

- source
- access
- confidence
- significance
- reader relevance

### Scene

Required questions:

- What is causally true?
- What source records or observes it?
- Who can access and interpret it?
- What costs, dependencies, recovery, and failure remain?
- What provenance key prevents semantic duplication?
- What should the viewpoint and reader actually see?

Locked checks:

- no universal total power
- no label-created capability
- no retrospective progression
- no duplicated identity or entitlement
- no unwitnessed resource or renewal
- no damage-derived free growth

Type-specific checks:

- truth
- record
- access
- interpretation
- presentation
- reader need

## Notification templates

### Skill Progress

> {skill} increased. Improved: {facet}. Reinforcement: {assimilation_state}. Recovery demand: {recovery_state}.

Must not imply: full backend access, instant assimilation.

### Offer

> New {lineage_type} offer: {name}. Basis: {evidence_summary}. Acceptance creates prospective progression.

Must not imply: retroactive XP, random reroll.

### Condition

> Condition: {label}. Known cause: {cause_or_unknown}. Current risk: {risk_scope}. Recommended response: {response}.

Must not imply: perfect diagnosis, fixed timer.

### Appraisal

> Appraisal result ({confidence}): {disclosed_facets}. Unresolved: {unknown_facets}.

Must not imply: omniscience, authority, ownership.

## Change-control classifications

| Classification | Use when |
|---|---|
| `PRESENTATION_CLARIFICATION` | Meaning is preserved while its interface, explanation, or story-facing projection is made unambiguous. |
| `PARAMETER_CHANGE` | A numerical or categorical calibration value changes without changing its model family. |
| `IMPLEMENTATION_CORRECTION` | Executable behavior is brought back into agreement with an already-governing rule. |
| `LOCAL_RULE_REPAIR` | A bounded rule is added or narrowed to protect existing architecture and invariants. |
| `SUBSYSTEM_REVISION` | One subsystem contract changes and requires explicit downstream migration. |
| `ARCHITECTURE_REOPENING` | A protected cross-system invariant or model-family decision is reconsidered. |

## Closed change register

| Entry | Stage | Classification | Resolution |
|---|---|---|---|
| CAL0-I5-R01 — Canonical semantic-origin entitlement key | CAL0-I5 | `LOCAL_RULE_REPAIR` | Entitlements are keyed by recipient, protected facet, and canonical causal origin before aliases are evaluated. |
| CAL0-I5-R02 — Source-bounded renewal witness | CAL0-I5 | `IMPLEMENTATION_CORRECTION` | Recovery and spawning require a typed source witness and cannot exceed the witnessed renewable input or remaining capacity. |
| CAL0-I5-R03 — Projection, evidence, access, and authority separation | CAL0-I5 | `PRESENTATION_CLARIFICATION` | Every consequential projection requires source evidence, audience permission, scope, and a distinct authority or capability witness. |
| CAL0-I5-R04 — Exclusive identity-continuation ledger | CAL0-I5 | `LOCAL_RULE_REPAIR` | One identity lineage may have at most one continuing holder; copies and successors receive explicit derived identities unless a witnessed exclusive transfer occurs. |
| CAL0-I5-R05 — Stimulus-origin deduplication and harm gate | CAL0-I5 | `LOCAL_RULE_REPAIR` | Adaptation is bounded by unique causal stimulus origins, loaded structures, recovery, and headroom; damage cannot itself become positive adaptation. |
| CAL0-I6-C01 — Replace the proposed protagonist Soul multiplier with a non-scalar profile | CAL0-I6 | `PRESENTATION_CLARIFICATION` | No universal Soul multiplier exists. Reincarnate Continuity preserves identity; Embodied Integration and Soul Consolidation earn facet-specific development in Depth, Coherence, Resonance, boundary integrity, coupling, recovery, and safe assimilation. |

There are no open I6 change entries. Any future change must state its classification, affected protected facets, evidence, regression identity, migration impact, and whether architecture is being reopened.
