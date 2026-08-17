---
capture_id: "WB-SYS-ANCESTRY-001"
related_setting_id: "setting://shared-universe-001"
editorial_title: "Ancestry Development"
workflow_status: DRAFT
canon_status: PROPOSED
active_baseline: "CAL0 v0.7.0"
created_on: "2026-08-13"
source: "Active Author worldbuilding conversation"
---

# Ancestry Development — System-Change Capture

## Status and boundary

This document preserves a desired design direction; it does not amend CAL0,
implement a successor, or establish a story-facing mechanic. CAL0 v0.7.0
remains the active, locked baseline.

The idea must later enter the governed System-change workflow beneath the
initiating work's run directory. Classification, successor design, regression
evidence, Author approval, implementation, and activation are separate gates.

## Desired capability

- Creatures participate in a species- or lineage-shaped developmental track
  provisionally called `Ancestry Development`.
- Development is prospective and evidence-bearing: it reflects what an
  organism does, survives, practises, integrates, and becomes. Mere ageing or
  passive maturation should not generate rewards.
- An organism normally follows an inherited developmental template rather than
  manually allocating statistics.
- Individuals may vary within bounded biological and experiential ranges.
- Higher development makes an animal materially more capable within its body
  plan and niche.
- The scale should primarily compare members or branches of the same lineage;
  it must not imply that equal numeric values make unrelated species equally
  dangerous or capable.
- Ordinary development usually reinforces anatomy and physiology: armour,
  claws, muscle, connective structures, circulation, endurance, sensory organs,
  temperature regulation, or other niche-relevant traits.
- Some branches can develop specialised Mana organs and associated abilities.
  These require anatomy, energy, resources, behavioural opportunity, and
  ecological trade-offs.
- The rare emergence of sapience may be possible for some creatures, but should
  not occur automatically at one universal level threshold.

## Relationship to CAL0

CAL0 presently treats ancestry or species as provenance and constraint rather
than a universally reward-bearing package. It also prevents passive maturation
from functioning as a level reward. A new first-class Ancestry Development
lineage therefore cannot be introduced as an informal world fact.

Preliminary classification:

- At least a subsystem revision if this becomes a distinct, prospective,
  evidence-bearing lineage with its own scope, thresholds, rewards, and state.
- An architecture reopening if ancestry itself, passive biological maturation,
  or species membership directly grants levels or rewards.

CAL0 already supports directed embodied self-development through Skills. A
future proposal must demonstrate why this concept needs a separate lineage
rather than a Skill, application, trait projection, or narrative description.

## Questions a successor proposal must answer

1. What events constitute admissible evidence, and how are farming loops prevented?
2. How are inherited template, individual experience, and environmental pressure separated?
3. What exactly develops: Skills, traits, statistics, organs, thresholds, or a new state object?
4. How are rewards represented without free stat allocation or ancestry-as-class?
5. How are unrelated species compared, if at all?
6. How do domestication, captivity, injury, metamorphosis, reproduction, and artificial enhancement interact with it?
7. Can development regress, branch, or become inaccessible after anatomical commitment?
8. What observability is available to the creature, humans, scholars, and the reader?
9. What conditions could enable sapience, and how is that distinguished from intelligence, language, System access, or a template upgrade?
10. Which story-integration schemas, validators, guides, fixtures, and regression tests must change?

## Prohibited shortcuts

- No automatic reward for simply being a member of a species.
- No XP or levels from passive ageing, growth, gestation, or ordinary maturation.
- No universal kill-XP assumption.
- No unrestricted manual statistic allocation for ordinary animals.
- No single cross-species number that erases body plan, scale, niche, ecology, or specialised capabilities.
- No automatic sapience at a fixed universal threshold.
- No silent edits to CAL0 canonical files, successor directories, generated indexes, or the active-baseline pointer.

## Next governed action

When the Author chooses to activate this question, open a bounded System-change
run under `stories/series/project-hearthway-main/workbench/runs/`. Produce a
change request, impact map, successor proposal, regression plan, and candidate
Author decision. Keep every artifact `DRAFT` / `PROPOSED` until the appropriate
gate; successor implementation and activation require separate explicit
authority.
