# LitRPG System Design Handoff

**Project:** LitRPG WebNovel  
**Handoff date:** 2026-08-11  
**Handoff revision:** 2.0  
**Canonical specification at handoff:** version 0.60  
**Architecture state:** all core architecture decisions complete  
**Binding decisions:** 106  
**Current frontier:** numerical implementation and validated closure  
**Immediate task:** define the versioned numerical schema and parameter registry

## Quick-start message for the new chat

The user can paste this:

> Open `litrpg-system-design-handoff.md` and the canonical `/LitRPG WebNovel/litrpg-system-specification.md` from my Library. Read the specification as authoritative and use the handoff as the operational continuation guide. Verify that the specification is version 0.60, contains 106 binding architecture decisions, has no remaining core architecture questions, and distinguishes architecture decision closure from validated closure. Then begin the numerical implementation phase with the versioned parameter schema and registry. First inventory all locked constants, calibratable parameters, derived values, distributions, units, constraints, and provenance required by the specification. Propose a coherent schema and the smallest deterministic reference scenarios needed to test it before we build the 10,000-birth cohort model. Preserve decimal precision, causal provenance, natural maturation, purposeful training, Skill XP, Class XP, reinforcement, and assimilation as distinct mechanisms. Do not reopen accepted architecture without a concrete contradiction or test failure, do not silently invent numerical values, and stop for my selection whenever a materially different calibration choice is required.

## Canonical files and authority order

1. `/LitRPG WebNovel/litrpg-system-specification.md` is the sole canonical mechanics document.
2. This handoff is an operational summary and continuation guide. It does not override the specification.
3. `litrpg-system-research-dossier.md`, where present, is research context rather than binding mechanics.
4. Explicit user selections override proposals only after they have been reconciled into the canonical specification or a clearly identified calibration annex.
5. Architecture decisions and calibration parameters must remain distinguishable. A changed coefficient is not automatically an architecture revision.
6. Never create numbered copies of the canonical specification. Update the same file identity when a formal revision is required.

The new chat must read the latest canonical specification before doing numerical work. If its internal version is later than 0.60, the later decision register and implementation roadmap supersede this snapshot.

## Verified current state

- Specification version: **0.60**.
- Binding architecture decisions: **106**.
- Core architecture questions remaining: **0**.
- Deferred architecture questions remaining: **0**.
- Architecture decision closure: **complete**.
- Validated closure: **not yet complete**.
- Completed phases: attributes; reinforcement and prenatal access; resources and action resolution; Skills and abilities; traits and bloodlines; classes; progression; magic; items, storage, crafting, identification, and loot; parties, companions, factions, and institutions; interface, information, appraisal, and privacy; awakening and creature progression; dungeons, ecology, and population distributions; protagonist configuration; calibration and validation architecture.
- Immediate implementation frontier: **versioned numerical schema and parameter registry**.
- Next major milestones: individual-scale model, deterministic reference scenarios, 10,000-birth cohort simulation, sensitivity analysis, adversarial validation, story-facing sheets and guide, validated closure review.

`VAL1.0D`, `VAL1.1D`, and `VAL1.2D` are already selected and formalised. They must not be presented again as open architecture questions.

## Project objective

Design and validate a sufficiently complete, internally consistent LitRPG System for a web novel about an Earth reincarnate who becomes aware in the womb, starts genuinely weak, and develops toward overwhelming capability while remaining fundamentally a pure Mage.

The System should remain recognisably LitRPG—attributes, numbers, levels, XP, Skills, classes, offers, rarity, spells, traits, bloodlines, achievements, quests, parties, equipment, inventory views, loot, dungeons, and readable sheets—while functioning as deep natural law rather than a disconnected collection of game conventions.

Familiar displays are scoped projections of an underlying causal world. They cannot create capability, erase material constraints, duplicate rewards, overwrite identity, or replace the mechanisms they summarise.

The architecture must scale from fetal development and one person's training to parties, institutions, economies, magical ecologies, armies, and population-wide distributions.

## Binding design constitution

All implementation and calibration work must preserve these rules:

1. The System is natural law of unknown origin, perceived through culturally influenced interfaces.
2. It is selectively crunchy: useful exact values may be shown within authorised scopes, but the complete hidden model is not universally exposed.
3. Classes and Skills recognise demonstrated conduct, accumulated evidence, meaningful milestones, and coherent development.
4. Class XP and Skill XP are separate and local to accepted lineages.
5. Offers may be accepted, deferred, or rejected. Deferral preserves a real offer; rejection is not a free reroll.
6. A capped form stops levelling. Later evidence may remain directionally relevant without banking reinforcement-bearing levels.
7. Attributes and rewards use decimal values where useful.
8. Natural maturation, organic training adaptation, Skill XP, Class XP, and level reinforcement are distinct causes that may operate simultaneously.
9. Legitimately earned class and Skill reinforcement is guaranteed, although safe expression may be delayed by assimilation limits.
10. A class or Skill has a stable core reinforcement signature plus evidence-shaped adaptive expression.
11. Rarer or higher-grade forms may grant more or broader reinforcement only through fixed prospective schedules; no retroactive recalculation or rarity farming is permitted.
12. One event cannot duplicate XP, evidence, milestones, achievements, reinforcement, rewards, identity, loot, contribution, or entitlement merely because several systems or labels describe it.
13. Creation, ownership, possession, custody, access, authority, control, responsibility, contribution, and entitlement remain distinct.
14. Information is capability-gated, observer-relative, scoped, and uncertainty-aware. A display does not create the state it reports.
15. Matter, energy, Mana, identity, evidence, and rewards preserve provenance.
16. Time, resources, load, recovery, preparation, access, compatibility, maintenance, and failure remain causal.
17. Exclusive personal identity cannot be copied by duplicating memories, sheets, bodies, Souls, or records.
18. Agency and consent remain meaningful unless an explicit causal compulsion, binding, or control mechanism applies.
19. Legitimate optimisation remains possible. A powerful result is an exploit only when it violates a mechanism or invariant rather than merely being effective.

## Binding architecture snapshot

This table is a routing summary. The canonical sections and decision register contain the governing definitions, equations, examples, and locked consequences.

| Phase | Decided codes | Binding result |
|---|---|---|
| Attributes | `ATR0C`, `ATR1C`, `ATR2B` | Layered absolute capacity; eleven Body, Mind, and Soul attributes; anchored geometric decimal scale. |
| Reinforcement and early development | `ATR3.0C–ATR3.4.2.0D` | Organic growth and guaranteed reinforcement remain typed; source-rated rewards assimilate through coupled constraints under a safe governor; diagnosis and prenatal access are capability-gated. |
| Resources and action resolution | `RES0.0D–RES0.16D` | Typed carrier networks; Mana topology; affinity; containment; casting demand; physical, mental, and Soul load; injury, death, conditions, defence, uncertainty, and multi-timescale action economy. |
| Skills and abilities | `SKL0.0D–SKL4.2D` | Layered ability ontology; staged acquisition; composable expression contracts; coherent Skill lineages; evidence XP; dual-gated 100-level forms; portfolios, evolution, fusion, teaching, grants, loss, and recovery. |
| Traits and bloodlines | `TRT1.0D–TRT2.2D` | Provenance-layered traits and talents; descent and individual development; bloodline inheritance; boons, curses, mutations, transformations, conflict, fusion, replacement, and suppression. |
| Classes | `CLS1.0D–CLS4.2D` | Evidence-derived role lineages; no universal class slots; class-local XP; persistent offers; dual-gated 100-level forms; perks; orthogonal grade and rarity; successor continuity; magic-centred pure-Mage orientation. |
| General progression | `PRG1.0D–PRG3.2D` | No reward-bearing Character Level; exact lineage-local XP; conserved milestones; achievements, titles, perks, quests, rarity, contribution, discovery, groups, and anti-farming attribution. |
| Magic | `MAG1.0D–MAG2.2D` | Spells as executable method graphs; magical models and axioms; componentwise learning; stateful casting; research; rituals, wards, enchantments, constructs, familiars, and earned breadth. |
| Items and storage | `ITM1.0D–ITM1.2D` | Provenance-bearing assemblies; typed quality and durability; causal equipment integration; embodied storage and capability-gated inventory projections without universal free storage. |
| Crafting, relics, and loot | `ITM2.0D–ITM2.2D` | Production graphs; recipes as information; facet-specific identification; safe-use envelopes; causal remains, salvage, claims, allocation, and System rewards without universal corpse drops. |
| Social systems | `SOC1.0D–SOC1.2D` | Layered cooperation and party structures; typed companion, follower, summon, familiar, and construct relationships; provenance-bearing institutions, authority, reputation, and collective capability. |
| Interface and information | `UI1.0D–UI1.2D` | Fact–access–view–presentation topology; causal notifications and logs; observer-relative appraisal, privacy, concealment, consent, proof, and cultural translation. |
| Awakening and creatures | `WLD1.0D–WLD1.2D` | Staged awakening and consent; function-specific eligibility rather than species essentialism; animals and nonhumans develop through the shared causal architecture. |
| Exceptional places and populations | `WLD2.0D`, `WLD2.1A+D`, `WLD2.2D` | Causal dungeons and labyrinths; true spawning only inside those bounded sites; ordinary, mythological, magical, Mana-based, and alien life possess real life cycles; population power emerges from life histories and institutions. |
| Protagonist | `PRO1.0D–PRO1.2D` | Narrow reincarnate continuity; earned `Embodied Integration` and differentiated `Soul Consolidation`; real prenatal progression and staged self-knowledge; anchored emergent pure-Mage lineage with constructed breadth. |
| Validation and closure | `VAL1.0D–VAL1.2D` | Reproducible causal cohort calibration; invariant-led adversarial testing; layered authoring artifacts and explicit architecture-versus-validated closure. |

## Attribute and development rules that numerical work must preserve

### Attribute ontology and scale

The eleven attributes are:

| Domain | Attributes |
|---|---|
| Body | Might, Finesse, Alacrity, Vitality |
| Mind | Perception, Cognition, Focus, Will |
| Soul | Depth, Coherence, Resonance |

Attributes measure enduring absolute capacity under ordinary healthy and rested conditions. They are not age-normalised ranks, knowledge, personality, current resources, or final task performance.

The locked reference relationship is:

\[
\frac{C}{C_{10}} = 2^{A/10} - 1
\]

`10.00` is the fixed mature-human reference point. The numerical model must not quietly reinterpret a child's `10.00` as age-relative or convert the attribute into a linear percentage.

### Five distinct development channels

| Channel | What changes | XP treatment |
|---|---|---|
| Natural maturation | Absolute stats rise as muscles, bones, organs, circulation, nerves, senses, brain, Mind, and Soul structures genuinely develop | No XP is required or awarded merely for growth or elapsed time |
| Organic adaptation | Training, use, challenge, recovery, and safe load can change underlying physical, cognitive, perceptual, regulatory, magical, or Soul capacity | Not itself XP; may occur alongside recognised learning |
| Skill development | A coherent accepted capability lineage gains Skill XP and attestation from genuine learning, discrimination, control, judgement, correction, and integration | Prospective lineage-local Skill XP only |
| Class development | A coherent accepted role lineage gains Class XP and attestation from integrated conduct, responsibility, judgement, and contribution | Prospective lineage-local Class XP only |
| Level reinforcement | Legitimately completed class or Skill thresholds create fixed, source-rated, guaranteed fractional attribute claims | Reward is not XP and cannot recursively level its source |

Natural growth directly raises stats. It does not merely unlock potential for a later birthday or awakening. A newborn is stronger and more capable than its earlier fetal self because its body, brain, Mind, and Soul have developed.

Purposeful training also directly raises the stats whose foundations genuinely adapt. Examples include press-ups, weight training, running, swimming, climbing, assault courses, mathematics, difficult puzzles, study, memory work, meditation, attention practice, rehabilitation, Mana exercises, and Soul-directed practice.

Training does not provide generic points. Outcome depends on:

- the actual stimulus and capacity exercised;
- challenge, novelty, technique, feedback, and correction;
- individual foundation and current developmental stage;
- nutrition, sleep, recovery, equipment, environment, and safety;
- accumulated load, injury, interference, and opportunity cost;
- diminishing returns and the need for changed or more demanding stimuli.

Repeated easy activity cannot create unlimited growth. Semantic relabelling cannot make one exercise train several capacities twice. Injury and overtraining do not automatically become progress. Mathematics can develop relevant cognitive capacities through genuine adaptation, but memorising facts is not identical to raising Cognition. Meditation can develop Focus, Perception, Will, or Soul capacities only where the practice actually exercises and adapts those mechanisms.

### Locked reinforcement anchors

- A standard form contains 100 reinforcement-bearing thresholds.
- A complete ordinary grade-0 class form grants `3.000` units of source-rated reference capacity.
- A complete ordinary grade-0 Skill form grants `0.150` units.
- The ordinary class-to-Skill ratio is 20:1.
- Grade increases double the base reinforcement schedule prospectively.
- Rarity coefficients are bounded and prospective.
- Previous rewards are never recalculated when a form evolves, diverges, becomes rarer, fuses, splits, or is reclassified.
- Safe assimilation may delay expression but does not erase legitimately earned reinforcement.

The specification contains additional locked assimilation anchors, including the non-transformative `×2.00` support boundary, the overload-strain form `12x + 88x²` per day, state-dependent recovery reservations, a 20% post-recovery accommodation share, and bounded deficit credit `Q₀ = 0.0010`. These must enter the parameter registry as locked constants or explicitly versioned architecture-derived values, not be rediscovered by fitting.

## Protagonist configuration to preserve

### Reincarnate Continuity

`Reincarnate Continuity` preserves exclusive identity, memory patterns, personal perspective, and the basis for anomalous prenatal recognition. It does not transfer Earth attributes, formal Skills, classes, XP, magical mastery, bodily conditioning, or a mature brain-independent intellect.

### Embodied Integration

`Embodied Integration` is an earned prenatal Skill built through self-observation, attention, interoception, memory retrieval, brain–Soul–body calibration, recovery awareness, and safe self-regulation. It coordinates development; it does not grant arbitrary biological command or universal magic.

### Soul Consolidation

`Soul Consolidation` may differentiate into its own earned Skill when Soul-local practice develops independent methods, evidence, load, failure, and progression. It can strengthen `Depth`, `Coherence`, and `Resonance` through real organic adaptation and Skill reinforcement without creating a single universal Soul Strength statistic.

### Prenatal progression

The protagonist can:

- gain ordinary natural stats as his fetal body, brain, Mind, and Soul develop;
- generate organic adaptation through safe directed use;
- accept genuine Skills before birth;
- earn prospective Skill XP, levels, and fractional reinforcement during gestation;
- partially assimilate earned reinforcement before birth where capacity permits;
- use unusually early self-only appraisal and overload warnings.

Pre-offer effort can justify recognition and shape the candidate lineage, but cannot become banked formal XP. His periods of sleep and unconscious development remain biologically important. Consciousness is neither required for all genuine learning nor sufficient to make repetition developmental.

### Pure-Mage arc

The protagonist has no preloaded Archmage tree or inherited all-magic class. His first Mage offer must emerge from sustained magical conduct. Once accepted, Mage ancestry remains protected, while exact successors, rarity, specialisations, breadth, and power remain evidence-derived.

Nonmagical Skills and classes remain real. Anatomy, medicine, mathematics, crafting, languages, combat, agriculture, or administration may improve his models and enable later magical invention, but they do not retroactively become Mage XP. He becomes overwhelming through constructed synthesis, research, preparation, tools, infrastructure, and numerous genuinely developed magical disciplines—not universal omnipotence.

## Ecology and population constraints relevant to calibration

- Ordinary-world animals, plants, mythological creatures, magical organisms, Mana-based life, and alien lifeforms reproduce, grow, migrate, compete, die, and renew through genuine—even if unfamiliar—life cycles.
- True spawning and spawn points exist only inside causally bounded dungeons and labyrinths.
- Dungeon spawning must account for inputs, patterns, capacity, identity, costs, renewal, failure, and ecological consequence.
- Time supplies developmental opportunities but does not award XP.
- Long life provides more opportunities, not automatic endless advancement.
- Institutions reshape distributions through nutrition, safety, teachers, records, equipment, controlled practice, access, monopoly, exclusion, and preserved knowledge.
- Grade, rarity, scope, quality, capability, equipment, social authority, and combat readiness must remain separate outputs. Do not collapse them into a hidden Character Level.
- Combat capability must be reported by role and circumstances rather than one universal power number.

## Validation architecture already selected

### Numerical calibration — `VAL1.0D`

The reference implementation follows at least 10,000 births across complete lives per seeded run. It uses multiple seeds, parameter sweeps, comparison cohorts, deliberately varied social environments, uncertainty ranges, and sensitivity analysis.

The model must report at least:

- prenatal, newborn, childhood, adult, ageing, and injury-affected stat curves;
- attributes by foundation, health, training, and developmental history;
- accepted, deferred, and rejected Skill and class lineages;
- lineage-local XP, attestation, levels, completion, and successors;
- organic adaptation, reinforcement claims, assimilation, strain, and recovery;
- magical access and independent capability;
- occupation, household, geography, culture, institution, resources, and equipment;
- rarity profiles without turning rarity into power;
- injury, disability, interruption, retirement, and death;
- combat readiness by role and conditions;
- exceptional outliers and the causal histories that produced them;
- sensitivity to every material parameter.

The protagonist must be simulated separately against ordinary and relevant exceptional comparison cohorts so his advantage can be measured without distorting the general population.

### Adversarial validation — `VAL1.1D`

Testing begins from invariants, then attacks the System at individual, group, institutional, economic, ecological, informational, magical, training, and metaphysical scales.

Required attack families include Skill fragmentation, offer manipulation, milestone replay, delegated action, party farming, manufactured threats, dungeon industrialisation, resurrection and identity duplication, crafting reconstruction, magical perpetual motion, institutional monopoly, appraisal and privacy abuse, semantic training duplication, and deliberate self-harm as supposed development.

Every surprising result is classified as:

1. valid emergent strategy;
2. numerical imbalance;
3. presentation ambiguity;
4. local missing rule;
5. architectural contradiction;
6. invariant violation.

Repairs occur at the least disruptive valid layer and receive regression coverage.

### Layered usability and closure — `VAL1.2D`

Validated closure requires connected deliverables:

1. canonical causal specification;
2. numerical calibration annex;
3. story-facing System guide;
4. reader-facing and author-facing character-sheet schemas;
5. reference character sheets;
6. scenario validation suite;
7. contradiction and change register;
8. validated closure review.

Every scene and sheet must distinguish what is causally true, what the System can expose, what the viewpoint character can access, how the character interprets it, and what the reader needs to see.

## Implementation roadmap

The following labels are operational workstream identifiers, not new architecture decision codes.

| Workstream | Deliverable | Exit evidence |
|---|---|---|
| `CAL0` — Parameter architecture | Versioned registry of locked constants, calibratable parameters, distributions, units, constraints, dependencies, provenance, and derived metrics | Every numerical rule is represented once; missing values are explicit; units and ownership are unambiguous |
| `CAL1` — Individual engine | Deterministic life-stage, training, attribute, resource, XP, reinforcement, and assimilation model | Unit tests reproduce locked equations and conservation rules |
| `CAL2` — Reference scenarios | Calculated prenatal, childhood, civilian, combat, magical, injury, and progression cases | Repeated runs reproduce expected causal changes and readable sheets |
| `CAL3` — Cohort model | 10,000-birth seeded life-course simulation with varied households, regions, institutions, and opportunities | Stable multi-seed distributions and explainable outliers within declared envelopes |
| `ADV1` — Adversarial validation | Cross-scale exploit and institutional attack suite | No unresolved invariant violations; repairs have regression tests |
| `AUT1` — Authoring projections | Story-facing guide, character sheets, scenario library, and change register | Ordinary scene planning remains readable and canonical |
| `CLOSURE` — Validated closure | Consolidated closure review | Every closure criterion passes or residual uncertainty is classified |

### Required execution order

1. Define `CAL0`, the versioned numerical schema and parameter registry.
2. Implement natural maturation, purposeful training, attributes, resources, XP, reinforcement, and assimilation at individual scale.
3. Validate reference characters and small deterministic scenarios before population simulation.
4. Run the 10,000-birth cohort model and sensitivity analysis.
5. Attack the resulting configuration with individual and institutional adversarial suites.
6. Produce story-facing sheets, guides, and reference scenarios from the validated model.
7. Conduct the validated closure review and reopen architecture only for evidence-backed failures.

## Immediate task for the next chat: `CAL0`

The first implementation session should not invent a complete simulation or produce arbitrary demographic targets. It should create an auditable numerical foundation.

### Step 1 — Parameter inventory

Read the full specification and inventory every numeric or distribution-bearing concept. Classify each entry as:

- **locked architecture constant** — already fixed by a binding decision;
- **calibratable parameter** — requires a justified value or distribution;
- **scenario input** — chosen for a particular person, environment, or event;
- **derived value** — calculated from other registered values;
- **observable output** — reported for validation but not fitted directly;
- **calibration envelope** — a plausible range or relational condition used to judge outcomes;
- **presentation parameter** — affects display without changing the causal model.

### Step 2 — Registry schema

Propose fields sufficient to record:

- stable parameter ID and human-readable name;
- domain and owning mechanism;
- definition and causal meaning;
- scalar, vector, table, function, distribution, enum, or constraint type;
- units and reference basis;
- value, range, or unresolved state;
- locked versus calibratable status;
- valid domain and boundary behaviour;
- dependencies and derived expression;
- population, species, life-stage, environment, institution, or scenario scope;
- source decision and canonical section;
- confidence, evidence basis, and calibration rationale;
- version introduced, changed, and superseded;
- sensitivity priority and validation tests.

Do not choose a storage format merely because it is convenient. First decide what semantic information the registry must preserve. A later YAML, JSON, TOML, database, spreadsheet, or code representation should be generated from that model rather than becoming the model.

### Step 3 — Minimal deterministic reference scenarios

Define the smallest cases required to validate the registry before cohort work. At minimum include:

1. ordinary fetal growth with no formal prenatal Skill;
2. protagonist fetal growth plus accepted `Embodied Integration`;
3. differentiation and early development of `Soul Consolidation`;
4. an ordinary child gaining stats through maturation and play;
5. two people performing different physical training programmes;
6. cognitive training versus mere fact acquisition;
7. a Skill level that creates a fractional reinforcement claim and delayed assimilation;
8. a class and Skill developing from the same event without duplicated XP;
9. overtraining, injury, inadequate recovery, and diminishing returns;
10. a civilian vocation reaching a progression plateau through familiar repetition.

### Step 4 — Present only real choices

Where multiple numerical architectures remain materially viable, present explicit options with consequences, interactions, failure modes, calibration difficulty, narrative usability, game adaptability, and a recommendation. Do not manufacture A–D polls for matters already settled by the specification or for details that can remain provisional parameters.

### Expected first-session output

The preferred first output is:

1. a concise verified state statement;
2. a structured inventory of locked numerical anchors;
3. a proposed parameter taxonomy and schema;
4. a dependency map for the individual-scale model;
5. the minimal reference-scenario plan;
6. a short list of genuine decisions or missing values requiring the user's selection;
7. a recommended first calibration packet.

Stop before implementing the population model. The user should be able to inspect and challenge the schema before it becomes code.

## Writeback workflow during implementation

1. Treat the canonical specification as immutable unless a calculation exposes a concrete contradiction, ambiguity, or missing mechanism.
2. Record numerical values in a distinct calibration annex or parameter artifact rather than silently embedding every coefficient into the architecture prose.
3. Mark each value as locked, provisional, calibrated, scenario-specific, or derived.
4. Give every change a reason, source, version, and affected validation cases.
5. Preserve deterministic seeds and complete run manifests so results are reproducible.
6. When a selected numerical packet is accepted, update the calibration artifact and affected scenarios together.
7. Increment the canonical specification only for genuine specification changes, not routine calibration iterations.
8. Preserve existing file identities. Do not create numbered canonical copies.
9. Refresh this handoff when the user asks to move to another chat.

## Validation checklist before every save

- The canonical specification still reports version 0.60 unless an explicit architecture revision was made.
- The decision register contains 106 unique `DECIDED` entries.
- No architecture item has silently returned to `OPEN` or `DEFERRED`.
- Locked constants and calibratable parameters are clearly distinguished.
- Natural maturation directly changes absolute stats without XP.
- Purposeful training changes only genuinely adapted capacities and observes recovery and diminishing returns.
- Organic adaptation, Skill XP, Class XP, reinforcement, and assimilation remain separate ledgers or state processes.
- Pre-acceptance evidence does not become banked formal XP.
- One event is recorded once and cannot multiply rewards through labels, Skills, classes, parties, or scenarios.
- The attribute scale remains absolute and geometric.
- Population outputs do not recreate a hidden reward-bearing Character Level.
- Rarity, grade, power, quality, equipment, social authority, and combat readiness remain separate.
- All distributions expose their units, scope, provenance, version, and uncertainty.
- Random runs are seed-reproducible and deterministic reference scenarios remain stable.
- The protagonist is compared with ordinary and exceptional cohorts rather than inserted into the baseline population.
- Markdown tables, equations, links, and code fences remain structurally valid.

## Reasoning and style guardrails

- Lead with the numerical or causal decision and its consequences, not implementation jargon.
- Preserve decimal precision. Do not round everything to whole-number game values.
- Prefer transparent parameters, functions, and distributions over hidden fudge factors.
- Use plausible calibration envelopes to judge results; do not force exact world counts merely because a desired narrative number was imagined first.
- Explain outliers through their life histories instead of deleting them because they complicate a clean distribution.
- Keep uncertainty visible. False precision is not additional depth.
- Separate knowledge learned, capacity adapted, evidence recognised, XP awarded, threshold completed, reinforcement earned, and reinforcement assimilated.
- Remember that a high vocational Skill does not imply equal combat, magical, political, or general power.
- Keep institutions causally important through opportunity, knowledge, logistics, records, equipment, and coordination.
- Preserve the weak-to-overwhelming Mage arc without tuning the entire population around the protagonist.
- When code is eventually written, prefer inspectable deterministic components and tests over one opaque all-purpose simulation.

## What not to do next

- Do not resume `SOC`, `UI`, `WLD`, `PRO`, or `VAL` as unanswered architecture packets.
- Do not ask another fixed series of architecture questions merely to continue the previous cadence.
- Do not implement the 10,000-birth model before defining the parameter registry and deterministic individual scenarios.
- Do not assign arbitrary commoner, elite, hero, or legend level bands.
- Do not introduce a universal reward-bearing Character Level.
- Do not turn natural fetal or childhood development into automatic XP.
- Do not treat exercise, study, meditation, Skill XP, Class XP, and reinforcement as interchangeable routes to generic stat points.
- Do not grant the protagonist adult physical or cognitive stats in the womb.
- Do not pre-load every magical discipline or a fixed Archmage tree into reincarnation.
- Do not make true spawning an ordinary-world ecological mechanism.
- Do not prohibit a powerful strategy merely because it is powerful; identify the invariant or numerical envelope it actually violates.
- Do not update the canonical specification for ordinary parameter tuning.

## Successful continuation

A successful first response in the new chat will:

1. Confirm that both files were read and the canonical specification is authoritative.
2. State the verified version 0.60, 106 binding decisions, zero remaining core architecture questions, and the distinction between architecture decision closure and validated closure.
3. Confirm that `CAL0`—the numerical schema and parameter registry—is the active implementation frontier.
4. Preserve natural maturation, purposeful training, Skill XP, Class XP, reinforcement, and assimilation as distinct mechanisms.
5. Present an auditable parameter inventory and schema proposal before choosing coefficients or writing the population simulation.
6. Identify only genuine calibration choices and wait for the user's selection where those choices materially affect the model.
7. End with a clear next action toward deterministic reference scenarios and the individual-scale model.
