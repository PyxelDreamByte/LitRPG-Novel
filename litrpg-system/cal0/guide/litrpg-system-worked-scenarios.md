# CAL0-I6 worked story scenarios

**Specification:** 0.88  
**Calibration annex:** 2.8  
**Scope:** Worked causal references, not fixed plot.

Each scenario exposes the same seven planning layers: inputs, actor knowledge, causal sequence, state changes, interface output, reader projection, and locked checks.

## 1. Fetal and childhood attributes rise through maturation

**Family:** `natural_growth_without_xp`  
**Scenario ID:** `scenario://cal0/i6/natural-growth@1`

### Inputs

| Input | Value |
|---|---|
| start_capacity | 0.01928119 |
| birth_capacity | 0.65381944 |
| child_capacity | 0.82 |
| formal_xp | 0 |

### What the actors know

- author knows developmental programme
- character has no ordinary fetal interface

### Causal sequence

1. structures mature
2. foundation becomes realised
3. rated capacities rise
4. no progression reward is issued

### State changes

| Ledger / state | Change |
|---|---|
| natural_maturation | positive |
| skill_xp | 0 |
| class_xp | 0 |
| reinforcement | 0 |

### Interface output

- Physical development increased
- No Skill notification

### Reader-facing projection

The child grows stronger because a body is forming and maturing, not because infancy awards levels.

### Locked checks

- `maturation_positive`
- `xp_zero`
- `ledgers_separate`

## 2. Prenatal Skill acceptance, reinforcement, and partial assimilation

**Family:** `prenatal_skill_progression`  
**Scenario ID:** `scenario://cal0/i6/prenatal-skill@1`

### Inputs

| Input | Value |
|---|---|
| directed_load | 0.18 |
| conscious_fraction | 0.12 |
| skill_xp | 0.216 |
| reinforcement_claim | 0.0015 |
| assimilated | 0.000375 |
| backlog | 0.001125 |

### What the actors know

- protagonist can access self-only interface
- he does not know the backend formula

### Causal sequence

1. repeat intent-sensation calibration
2. System recognises coherent domain
3. accept Embodied Integration
4. earn prospective XP
5. create absolute claim
6. safe governor assimilates part

### State changes

| Ledger / state | Change |
|---|---|
| natural_maturation | unchanged route |
| skill_xp | 0.216 |
| reinforcement | 0.0015 |
| assimilation | 0.000375 |
| backlog | 0.001125 |

### Interface output

- Embodied Integration accepted
- Reinforcement partially assimilated
- Recovery demand elevated

### Reader-facing projection

A tiny success matters because it is coherent and repeatable; most of the fetus's growth still comes from gestation.

### Locked checks

- `claim_conserved`
- `partial_assimilation`
- `no_retroactive_xp`

## 3. Press-ups create adaptation and Skill evidence

**Family:** `resistance_training`  
**Scenario ID:** `scenario://cal0/i6/resistance@1`

### Inputs

| Input | Value |
|---|---|
| sessions | 24 |
| challenge | 0.65 |
| supported_adaptation | 0.018 |
| skill_xp | 0.52 |

### What the actors know

- trainee knows technique and recovery plan

### Causal sequence

1. load chest, arms, trunk
2. recover
3. remodel loaded structures
4. record movement-quality evidence

### State changes

| Ledger / state | Change |
|---|---|
| purposeful_training | 15.60 load-units |
| organic_adaptation | 0.018 |
| skill_xp | 0.52 |
| class_xp | 0 |

### Interface output

- Condition: fatigued
- Calisthenics evidence increased

### Reader-facing projection

Repeated press-ups improve the structures actually loaded; renaming each set would not multiply the gain.

### Locked checks

- `adaptation_supported`
- `skill_and_attribute_separate`
- `no_label_duplication`

## 4. Running and an assault course create a different portfolio

**Family:** `running_and_assault_course`  
**Scenario ID:** `scenario://cal0/i6/assault-course@1`

### Inputs

| Input | Value |
|---|---|
| sessions | 16 |
| endurance_load | 0.58 |
| coordination_load | 0.72 |
| adaptation | 0.021 |

### What the actors know

- coach sees gait and obstacle errors

### Causal sequence

1. sustain running
2. climb and vault
3. receive feedback
4. recover

### State changes

| Ledger / state | Change |
|---|---|
| Might | 0.003 |
| Alacrity | 0.006 |
| Vitality | 0.008 |
| Finesse | 0.004 |
| organic_adaptation | 0.021 |

### Interface output

- Movement portfolio improved
- Fatigue elevated

### Reader-facing projection

The runner gains endurance, timing, balance, and obstacle method rather than the same portfolio as a lifter.

### Locked checks

- `portfolio_distinct`
- `recovery_required`
- `headroom_respected`

## 5. Mathematics separates knowledge, Skill, Cognition, and Focus

**Family:** `mathematics_and_puzzles`  
**Scenario ID:** `scenario://cal0/i6/mathematics@1`

### Inputs

| Input | Value |
|---|---|
| novel_problems | 40 |
| repeated_solved_problems | 60 |
| study_hours | 32 |

### What the actors know

- student knows the taught methods
- teacher supplies corrective feedback

### Causal sequence

1. learn representation
2. solve novel problems
3. receive correction
4. consolidate knowledge

### State changes

| Ledger / state | Change |
|---|---|
| knowledge_units | 12 |
| Mathematics_skill_xp | 0.90 |
| Cognition_adaptation | 0.006 |
| Focus_adaptation | 0.008 |
| repeated_problem_extra_gain | 0 |

### Interface output

- Mathematics evidence increased
- Focus strained

### Reader-facing projection

Knowing a theorem, practising mathematical method, and developing reliable mental capacity are related but not interchangeable.

### Locked checks

- `knowledge_separate`
- `skill_xp_separate`
- `repetition_deduplicated`

## 6. Meditation separates attention, regulation, and Soul contact

**Family:** `meditation`  
**Scenario ID:** `scenario://cal0/i6/meditation@1`

### Inputs

| Input | Value |
|---|---|
| sessions | 30 |
| minutes | 20 |
| verified_soul_contact_events | 3 |

### What the actors know

- practitioner can distinguish breath, attention, emotion, and anomalous contact imperfectly

### Causal sequence

1. stabilise attention
2. observe emotion
3. recover
4. test suspected Soul contact

### State changes

| Ledger / state | Change |
|---|---|
| Focus_adaptation | 0.007 |
| Will_adaptation | 0.003 |
| attention_skill_xp | 0.64 |
| soul_contact_evidence | 3 |
| unsupported_spiritual_power | 0 |

### Interface output

- Attention steadier
- Possible Soul contact: low confidence

### Reader-facing projection

Calm attention becomes more reliable; three unusual contacts justify investigation, not a universal spiritual-power bonus.

### Locked checks

- `attention_and_soul_separate`
- `unsupported_claim_zero`
- `evidence_confidence_present`

## 7. Civilian vocational mastery without generic combat

**Family:** `civilian_vocation`  
**Scenario ID:** `scenario://cal0/i6/civilian@1`

### Inputs

| Input | Value |
|---|---|
| years | 14 |
| baking_level | 47 |
| class_level | 28 |

### What the actors know

- baker knows recipes, ovens, suppliers, and local demand

### Causal sequence

1. work repeatedly with variation
2. correct failures
3. teach apprentices
4. manage production

### State changes

| Ledger / state | Change |
|---|---|
| Baking_skill | 47 |
| Baker_class | 28 |
| combat_readiness | 0.06 |

### Interface output

- Baking 47
- Baker 28

### Reader-facing projection

Mara can run a bakery under pressure and teach others; she has not become a fighter merely by gaining levels.

### Locked checks

- `vocation_capable`
- `combat_not_generic`
- `institutional_support_causal`

## 8. Elite academy and under-resourced trainee diverge causally

**Family:** `institutional_inequality`  
**Scenario ID:** `scenario://cal0/i6/institutional-inequality@1`

### Inputs

| Input | Value |
|---|---|
| same_endowment | yes |
| years | 6 |
| elite_support | 0.90 |
| low_support | 0.35 |

### What the actors know

- author knows nutrition, coaching, safety, peers, and archives differ

### Causal sequence

1. assign equal initial aptitude
2. vary support
3. train
4. record interruptions and recovery

### State changes

| Ledger / state | Change |
|---|---|
| elite_skill_level | 54 |
| low_resource_skill_level | 31 |
| elite_injury_days | 12 |
| low_resource_injury_days | 49 |

### Interface output

- Progress differs; cause: support and interruption

### Reader-facing projection

The academy does not create talent from nothing; it converts resources and institutional capability into more reliable development.

### Locked checks

- `same_endowment_retained`
- `support_causes_difference`
- `no_free_institutional_skill`

## 9. Party contribution and reward dispute

**Family:** `party_contribution_dispute`  
**Scenario ID:** `scenario://cal0/i6/party-dispute@1`

### Inputs

| Input | Value |
|---|---|
| event_id | event:ogre-bridge |
| contributions | {"fighter": "0.42", "healer": "0.25", "porter": "0.15", "scout": "0.18"} |
| reward_units | 100 |

### What the actors know

- party observes only part of each contribution
- ledger has evidence with uncertainty

### Causal sequence

1. fight and evacuate
2. record causal contribution
3. compare claims
4. allocate scoped reward

### State changes

| Ledger / state | Change |
|---|---|
| fighter_reward | 42 |
| healer_reward | 25 |
| scout_reward | 18 |
| porter_reward | 15 |
| personal_kill_claims | 1 |

### Interface output

- Contribution ledger contested
- Allocation recorded with evidence scope

### Reader-facing projection

The killing blow matters, but so do warning, treatment, supply, and evacuation; one event is not four personal solo victories.

### Locked checks

- `contribution_sums_one`
- `reward_conserved`
- `event_not_duplicated`

## 10. Dungeon spawning and treasure economy remain source-bounded

**Family:** `dungeon_spawn_economy`  
**Scenario ID:** `scenario://cal0/i6/dungeon-economy@1`

### Inputs

| Input | Value |
|---|---|
| mana_input | 1000 |
| biomass_input | 500 |
| spawn_cost | 800 |
| treasure_input | 150 |
| maintenance | 500 |
| harvest | 700 |

### What the actors know

- controller knows measured flows, not hidden maximums

### Causal sequence

1. collect inputs
2. spawn organisms
3. form treasure
4. harvest
5. allow recovery

### State changes

| Ledger / state | Change |
|---|---|
| total_input | 1500 |
| total_committed | 1450 |
| residual | 50 |
| unwitnessed_restock | 0 |

### Interface output

- Dungeon reserve low
- Spawn rate reduced

### Reader-facing projection

Industrial use is possible, but heavy harvest lowers later output unless real inputs and recovery restore the mechanism.

### Locked checks

- `matter_conserved`
- `mana_conserved`
- `renewal_witnessed`

## 11. Research, spell construction, teaching, and derivative invention

**Family:** `magical_research_and_invention`  
**Scenario ID:** `scenario://cal0/i6/magical-research@1`

### Inputs

| Input | Value |
|---|---|
| experiments | 18 |
| successful_replications | 5 |
| teacher_scaffolding | yes |

### What the actors know

- researcher knows anatomy and current spell grammar
- student receives method but not mastery

### Causal sequence

1. form hypothesis
2. build spell graph
3. test
4. replicate
5. document
6. teach
7. student reconstructs derivative

### State changes

| Ledger / state | Change |
|---|---|
| knowledge_claims | 7 |
| research_skill_xp | 2.40 |
| spell_identity | derived-method |
| student_skill_xp | 0.48 |
| teacher_xp_from_student_work | 0 |

### Interface output

- New method validated: narrow scope
- Derivative method recorded

### Reader-facing projection

Teaching transmits representation and correction; the student still has to build a working method and the teacher does not own the student's progress.

### Locked checks

- `knowledge_and_skill_separate`
- `replication_required`
- `derivative_provenance_preserved`

## 12. Crafting, repair, appraisal, salvage, and ownership

**Family:** `craft_repair_appraisal_salvage`  
**Scenario ID:** `scenario://cal0/i6/craft-salvage@1`

### Inputs

| Input | Value |
|---|---|
| item | river-sword |
| replaced_components | ["grip", "guard"] |
| salvaged_fragment | old-guard |

### What the actors know

- smith sees material and wear
- enchantment remains partly unidentified

### Causal sequence

1. appraise facets
2. repair grip
3. replace guard
4. test
5. record salvage and owner consent

### State changes

| Ledger / state | Change |
|---|---|
| item_identity | preserved |
| quality | improved |
| unknown_enchantment | still unknown |
| salvage_identity | derived component |
| ownership | unchanged |

### Interface output

- Condition improved
- Enchantment: unresolved facet

### Reader-facing projection

Repair can restore function without revealing every secret, changing ownership, or cloning the sword's history onto a discarded guard.

### Locked checks

- `identity_preserved_once`
- `unknown_not_erased`
- `ownership_separate`

## 13. Injury, healing, rehabilitation, death, and return

**Family:** `injury_rehabilitation_resurrection`  
**Scenario ID:** `scenario://cal0/i6/injury-return@1`

### Inputs

| Input | Value |
|---|---|
| injury | severed_tendon |
| death_minutes | 4 |
| return_mechanism | exclusive-soul-reconstitution |

### What the actors know

- healer knows anatomy and ritual limits
- identity evidence is incomplete until return

### Causal sequence

1. stabilise
2. repair
3. rehabilitate
4. death occurs in counterfactual branch
5. verify exclusive identity
6. reconstitute if feasible

### State changes

| Ledger / state | Change |
|---|---|
| healing | repair incomplete without rehabilitation |
| skill_xp_preserved | yes |
| reinforcement_reclaimed | no |
| continuing_identity_holders | 1 |

### Interface output

- Condition: recovering
- Return confirmed; no duplicate continuity

### Reader-facing projection

Magic can restore a life only through a supported path; it does not erase rehabilitation, create a spare original, or repay completed levels.

### Locked checks

- `healing_staged`
- `identity_exclusive`
- `rewards_not_replayed`

## 14. Prepared institution opposes a powerful individual

**Family:** `powerful_individual_vs_institution`  
**Scenario ID:** `scenario://cal0/i6/institution-vs-power@1`

### Inputs

| Input | Value |
|---|---|
| individual_mana | 6.20 |
| ward_nodes | 24 |
| responders | 80 |
| preparation_days | 12 |

### What the actors know

- institution has partial intelligence
- individual does not know every ward

### Causal sequence

1. prepare layered wards
2. disperse reserves
3. deny information
4. force repeated commitments
5. rotate responders

### State changes

| Ledger / state | Change |
|---|---|
| individual_first_breach | successful |
| second_layer | holds |
| individual_mana_remaining | 1.10 |
| institutional_losses | 7 |

### Interface output

- Ward layer one breached
- Countermeasure network adapting

### Reader-facing projection

The mage is terrifying and wins local exchanges, but preparation, information, distributed capacity, and recovery prevent one number from deciding the conflict.

### Locked checks

- `individual_power_real`
- `institutional_capability_real`
- `no_total_power_score`

## 15. Anatomy and mathematics become inputs to a new magical method

**Family:** `nonmagical_knowledge_to_magic`  
**Scenario ID:** `scenario://cal0/i6/knowledge-to-magic@1`

### Inputs

| Input | Value |
|---|---|
| anatomy_knowledge | advanced |
| mathematical_model | validated |
| arcane_experiments | 27 |

### What the actors know

- protagonist remembers concepts but must map them to local bodies, Mana, and spell grammar

### Causal sequence

1. observe local anatomy
2. test Earth-derived hypothesis
3. build magical representation
4. run failed experiments
5. validate narrow repair method

### State changes

| Ledger / state | Change |
|---|---|
| earth_knowledge_xp_transfer | 0 |
| local_research_skill_xp | 3.10 |
| arcane_method_skill_xp | 2.20 |
| new_spell | Tendon Alignment Lattice |
| failed_experiments | 19 |

### Interface output

- New spell validated: tendon alignment only
- Source knowledge recorded; mastery earned locally

### Reader-facing projection

Old knowledge shortens the path to a useful question; the magical answer is still invented, tested, and learned in this world.

### Locked checks

- `no_retroactive_mage_xp`
- `local_validation_required`
- `new_method_provenance_complete`
