# LitRPG System residual-uncertainty register

**Closure status:** `VALIDATED_BASELINE_WITH_BOUNDED_RESIDUALS`  
**Groups:** 71  
**Items:** 305  
**Blocking items:** 0

A residual is not a concealed System rule. It names information that must be supplied only when a declared setting, population, character, plot, implementation, or optional extension needs it. Every entry below has an owner, activation condition, and failure boundary.

## Classification summary

| Classification | Groups | Items | Meaning |
|---|---:|---:|---|
| `CALIBRATION` | 19 | 109 | A coefficient, distribution, threshold, tolerance, or quantitative model must be pinned for a named scope before that scope is claimed. |
| `SETTING_CONTENT` | 3 | 3 | The world must author a contingent fact; the System architecture does not determine it. |
| `CHARACTER_CHOICE` | 0 | 0 | A person must choose within causal possibilities; no universal outcome should be specified. |
| `PLOT_CHOICE` | 0 | 0 | A later narrative event must select among valid possibilities without changing the System rule. |
| `IMPLEMENTATION` | 48 | 192 | A schema, algorithm, policy, witness, or optimisation is required only when a future implementation exercises that branch. |
| `FUTURE_OPTIONAL_EXTENSION` | 1 | 1 | The current baseline excludes this scope and does not depend upon it. |

## Registered residuals

### CAL0-Q1B

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q1b/01@1` — component inventory and cross-attribute mapping;
- `residual://cal0/i7/cal0-q1b/02@1` — milestone locations and anchor values for each developmental component;
- `residual://cal0/i7/cal0-q1b/03@1` — inherited endowment distributions and correlations;
- `residual://cal0/i7/cal0-q1b/04@1` — support, deprivation, disease, injury, catch-up, rehabilitation, and ageing functions;
- `residual://cal0/i7/cal0-q1b/05@1` — structural gates, aggregation weights, bottleneck exponents, and species scales;
- `residual://cal0/i7/cal0-q1b/06@1` — prenatal maternal–fetal resource coupling and recovery constraints;
- `residual://cal0/i7/cal0-q1b/07@1` — ordinary and exceptional variation envelopes.

### CAL0-Q4B

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q4b/01@1` — species baseline event timings, coordinate values, and chronological-time interpolation;
- `residual://cal0/i7/cal0-q4b/02@1` — the canonical milestone vocabulary and which components require distinct prenatal anchors;
- `residual://cal0/i7/cal0-q4b/03@1` — anchor timings, target values, turning points, and boundary policies;
- `residual://cal0/i7/cal0-q4b/04@1` — allowed individual timing variation and cross-component synchronisation;
- `residual://cal0/i7/cal0-q4b/05@1` — which anchor changes are ordinary calibration versus transformation or injury events.

### CAL0-Q7B

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q7b/01@1` — the canonical event vocabulary and coordinate values for the human reference programme;
- `residual://cal0/i7/cal0-q7b/02@1` — component-specific advance, lag, synchronisation, and prerequisite bounds;
- `residual://cal0/i7/cal0-q7b/03@1` — correlated inherited timing distributions and their separation from environmental timing effects;
- `residual://cal0/i7/cal0-q7b/04@1` — (Z^+), (Z^-), \(\eta^+\), \(\eta^-\), and resynchronisation functions;
- `residual://cal0/i7/cal0-q7b/05@1` — rules for variable gestation, premature birth, delayed transitions, catch-up, magical development, and transformation;
- `residual://cal0/i7/cal0-q7b/06@1` — coordinate precision, update cadence, and cross-species homologous-event mappings.

### CAL0-Q10B

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q10b/01@1` — factor vocabulary, component loadings, covariance matrices, and residual scales by species and population scope;
- `residual://cal0/i7/cal0-q10b/02@1` — distribution families, tail treatment, truncation, and ordered-event projection method;
- `residual://cal0/i7/cal0-q10b/03@1` — inheritance, maternal or gestational, environmental, and Soul-factor separation;
- `residual://cal0/i7/cal0-q10b/04@1` — event-family coupling across prenatal, childhood, adolescent, mature, and ageing transitions;
- `residual://cal0/i7/cal0-q10b/05@1` — calibration targets for within-person coherence, population dispersion, and rare but ordinary outliers;
- `residual://cal0/i7/cal0-q10b/06@1` — sensitivity and identifiability tests required before any factor receives a causal interpretation.

### CAL0-Q13B

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q13b/01@1` — bounded marginal families and parameters for each shared factor and residual;
- `residual://cal0/i7/cal0-q13b/02@1` — correlation matrices, permitted structural zeros, and any justified conditional dependence by scope;
- `residual://cal0/i7/cal0-q13b/03@1` — positive-semidefinite validation, repair policy, inverse-CDF precision, and sampling order;
- `residual://cal0/i7/cal0-q13b/04@1` — cohort diagnostics for marginal recovery, rank dependence, transformed Pearson dependence, and boundary accumulation;
- `residual://cal0/i7/cal0-q13b/05@1` — treatment of missing observations, selection, mortality, and uncertain population targets;
- `residual://cal0/i7/cal0-q13b/06@1` — sensitivity thresholds at which conclusions must be reported as dependence-model contingent.

### CAL0-Q16B

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q16b/01@1` — block vocabulary, membership, loading signs, loading bounds, and allowed cross-domain blocks by scope;
- `residual://cal0/i7/cal0-q16b/02@1` — residual-variance floors, permitted residual graph, and maximum residual-link density;
- `residual://cal0/i7/cal0-q16b/03@1` — identifiability conventions, sign orientation, and equivalent-factor-rotation policy;
- `residual://cal0/i7/cal0-q16b/04@1` — parameter-set rejection tolerances and diagnostics for near-singular covariance;
- `residual://cal0/i7/cal0-q16b/05@1` — cohort targets for within-block, cross-block, and residual rank dependence;
- `residual://cal0/i7/cal0-q16b/06@1` — escalation criteria for replacing the Gaussian copula if validated asymmetric or tail dependence cannot be represented.

### CAL0-Q2C

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q2c/01@1` — channel reference demands, dose-field units, and response kernels;
- `residual://cal0/i7/cal0-q2c/02@1` — gains, thresholds, nonlinear damage exponents, and recovery time constants;
- `residual://cal0/i7/cal0-q2c/03@1` — novelty, feedback, technique, and transfer functions;
- `residual://cal0/i7/cal0-q2c/04@1` — cross-channel interference and cooperation matrices;
- `residual://cal0/i7/cal0-q2c/05@1` — age, development, health, resource, and foundation modifiers;
- `residual://cal0/i7/cal0-q2c/06@1` — consolidation success, maladaptation, envelope motion, maintenance, and detraining;
- `residual://cal0/i7/cal0-q2c/07@1` — relationship between organic adaptation load and the already locked assimilation scheduler.

### CAL0-Q8B

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q8b/01@1` — channel-specific absolute-demand units, references, exposure integrals, and task-conditioned capacity functions;
- `residual://cal0/i7/cal0-q8b/02@1` — measurement and inference rules for technique, novelty, feedback, and structure loading;
- `residual://cal0/i7/cal0-q8b/03@1` — productive, fatigue, and harm response surfaces over absolute and relative challenge;
- `residual://cal0/i7/cal0-q8b/04@1` — interaction terms, uncertainty propagation, and dose aggregation across interrupted or compound episodes;
- `residual://cal0/i7/cal0-q8b/05@1` — maintenance-dose, minimum-effective-dose, saturation, overload, and recovery-spacing behaviour;
- `residual://cal0/i7/cal0-q8b/06@1` — cross-channel transfer rules for complex activities and mixed physical, cognitive, magical, or Soul practice.

### CAL0-Q11B

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q11b/01@1` — challenge-coordinate functions and window boundaries for each physical, cognitive, perceptual, magical, and Soul channel;
- `residual://cal0/i7/cal0-q11b/02@1` — shape functions, minimum effective doses, maintenance responses, and peak widths;
- `residual://cal0/i7/cal0-q11b/03@1` — fatigue and harm functions, exponents, protective inhibition, and stop conditions;
- `residual://cal0/i7/cal0-q11b/04@1` — effects of novelty, technique, feedback, recovery, development, health, equipment, and assistance on each window;
- `residual://cal0/i7/cal0-q11b/05@1` — session aggregation, spacing, repeated-bout effects, and cross-channel interference;
- `residual://cal0/i7/cal0-q11b/06@1` — calibration observables distinguishing productive overload from survivorship bias and hidden injury.

### CAL0-Q14B

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q14b/01@1` — maintenance and stop boundaries, modes, concentrations, and excessive-load boundaries by channel;
- `residual://cal0/i7/cal0-q14b/02@1` — bounded modifiers for development, health, recovery, technique, novelty, equipment, Mana stability, and Soul stability;
- `residual://cal0/i7/cal0-q14b/03@1` — minimum reporting precision and log-domain numerical tolerances;
- `residual://cal0/i7/cal0-q14b/04@1` — separate fatigue and harm functions and their coupling to the same challenge coordinate;
- `residual://cal0/i7/cal0-q14b/05@1` — calibration targets for peak location, productive width, asymmetry, overload reversal, and session spacing;
- `residual://cal0/i7/cal0-q14b/06@1` — cross-channel constraints preventing implausibly narrow or broad windows from being used as hidden balance multipliers.

### CAL0-Q17B

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q17b/01@1` — permitted effect masks and transform families for recovery, illness, injury, technique, novelty, feedback, equipment, assistance, development, Mana stability, and Soul stability;
- `residual://cal0/i7/cal0-q17b/02@1` — composition order, interaction terms, saturation rules, and projection-versus-rejection tolerances;
- `residual://cal0/i7/cal0-q17b/03@1` — bounds on interval width, mode movement, concentration, attainable height, fatigue, and harm;
- `residual://cal0/i7/cal0-q17b/04@1` — cross-channel load-routing and conservation rules;
- `residual://cal0/i7/cal0-q17b/05@1` — condition observables and uncertainty when the actor cannot measure the latent transform inputs;
- `residual://cal0/i7/cal0-q17b/06@1` — fixtures and cohort diagnostics for continuity, monotonic safety effects, and non-interchangeability.

### CAL0-Q9B

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q9b/01@1` — layer units, routing fractions, integration functions, and diminishing-return exponents;
- `residual://cal0/i7/cal0-q9b/02@1` — channel-specific envelope target functions and foundation bottlenecks;
- `residual://cal0/i7/cal0-q9b/03@1` — timescale ordering, fill rates, motion rates, maintenance demand, and detraining constants;
- `residual://cal0/i7/cal0-q9b/04@1` — chronic-load history, recovery, interference, and injury effects on envelope movement;
- `residual://cal0/i7/cal0-q9b/05@1` — rules for plateaus, catch-up, breakthroughs, transformation, and post-transformation conserved adaptation;
- `residual://cal0/i7/cal0-q9b/06@1` — interaction between organic adaptation, natural maturation, temporary effects, and reinforcement assimilation.

### CAL0-Q12B

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q12b/01@1` — which structural reorganisations justify phase transitions rather than continuous remodelling;
- `residual://cal0/i7/cal0-q12b/02@1` — prerequisite schemas, evidence sufficiency, attempt definitions, and outcome-resolution families;
- `residual://cal0/i7/cal0-q12b/03@1` — recovery, stabilisation, validation, relapse, partial-success, and maladaptation rules;
- `residual://cal0/i7/cal0-q12b/04@1` — state-transfer maps, conservation requirements, new maintenance costs, and post-transition detraining;
- `residual://cal0/i7/cal0-q12b/05@1` — interaction with age, developmental windows, injury, support, reinforcement assimilation, Skill evolution, and class evolution;
- `residual://cal0/i7/cal0-q12b/06@1` — story-facing visibility of eligibility, uncertainty, failed attempts, and validated completion.

### CAL0-Q15B

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q15b/01@1` — latent readiness, execution, stability, and incompatibility variables for each transition family;
- `residual://cal0/i7/cal0-q15b/02@1` — deterministic decision surfaces and rules for failed, partial, successful, and maladaptive outcomes;
- `residual://cal0/i7/cal0-q15b/03@1` — attempt-identity construction, solver seeding, version migration, and replay guarantees;
- `residual://cal0/i7/cal0-q15b/04@1` — observer models, evidence channels, forecast granularity, calibration error, and System-facing visibility;
- `residual://cal0/i7/cal0-q15b/05@1` — minimum material-change requirements for a genuinely new attempt;
- `residual://cal0/i7/cal0-q15b/06@1` — recovery and validation evidence capable of revising provisional classification without changing causal history.

### CAL0-Q18B

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q18b/01@1` — hard-constraint schemas, incompatibility vocabulary, and non-compensable minima by transition family;
- `residual://cal0/i7/cal0-q18b/02@1` — dimension definitions, bounds, vetoes, allowed trade-offs, and outcome surfaces;
- `residual://cal0/i7/cal0-q18b/03@1` — causal definitions of partial change, failure, and maladaptation;
- `residual://cal0/i7/cal0-q18b/04@1` — recovery and validation criteria for committing or revising provisional outcomes;
- `residual://cal0/i7/cal0-q18b/05@1` — observer-visible explanations and forecast limits without exposing omniscient hidden state;
- `residual://cal0/i7/cal0-q18b/06@1` — cross-family consistency tests and minimum material-change requirements for a new attempt.

### CAL0-Q3A

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q3a/01@1` — visible XP unit and baseline \(K_s\) for Skill and class forms;
- `residual://cal0/i7/cal0-q3a/02@1` — steepness exponent \(p_s\) and whether it is shared or family-specific;
- `residual://cal0/i7/cal0-q3a/03@1` — exact evolutionary-grade multiplier functions for Skills and classes;
- `residual://cal0/i7/cal0-q3a/04@1` — exact evidence-to-XP recognition scales by lineage family;
- `residual://cal0/i7/cal0-q3a/05@1` — qualitative-gate profiles and milestone cadence;
- `residual://cal0/i7/cal0-q3a/06@1` — taper exponent, relevance weighting, and overhang fraction while an attestation gate is blocked;
- `residual://cal0/i7/cal0-q3a/07@1` — cap, deferral, evolution, and display rounding behaviour in numerical implementation.

### CAL0-Q5B

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q5b/01@1` — grade-0 cumulative XP totals for standard Skill and class forms;
- `residual://cal0/i7/cal0-q5b/02@1` — whether Skills and classes use different geometric grade multipliers;
- `residual://cal0/i7/cal0-q5b/03@1` — the maximum grade for which a geometric multiplier remains plausible;
- `residual://cal0/i7/cal0-q5b/04@1` — whether the exponent \(p_s\) is type-specific while remaining smooth;
- `residual://cal0/i7/cal0-q5b/05@1` — display-unit scaling and rounding without loss of exact ledger values.

### CAL0-Q6C

**Classification:** `CALIBRATION`  
**Owner:** Calibration parameter-set authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q6c/01@1` — the overhang fraction \(\omega_s\) by Skill or class type and grade;
- `residual://cal0/i7/cal0-q6c/02@1` — taper exponent \(q_s\) and whether it varies by lineage family;
- `residual://cal0/i7/cal0-q6c/03@1` — the deterministic relevance rubric used to calculate \(r_{s,e}\);
- `residual://cal0/i7/cal0-q6c/04@1` — terminal-threshold behaviour and the relationship to successor offers;
- `residual://cal0/i7/cal0-q6c/05@1` — UI disclosure of blocked XP, capped XP, missing evidence, and uncertainty.

### CAL0-Q19B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q19b/01@1` — loading bounds and minimum identifiable energy by block family;
- `residual://cal0/i7/cal0-q19b/02@1` — permitted sign patterns and whether any block admits mixed signs;
- `residual://cal0/i7/cal0-q19b/03@1` — component-level overlap-energy ceilings;
- `residual://cal0/i7/cal0-q19b/04@1` — stability tolerances across fitted parameter versions.

### CAL0-Q20B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q20b/01@1` — complete stage graph and registered field operators;
- `residual://cal0/i7/cal0-q20b/02@1` — authorised within-stage and cross-condition interaction families;
- `residual://cal0/i7/cal0-q20b/03@1` — projection tolerances and invalid-parameter thresholds;
- `residual://cal0/i7/cal0-q20b/04@1` — provenance granularity for compound equipment, technique, illness, and support effects.

### CAL0-Q21B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q21b/01@1` — the canonical structural-delta schema and dependency vocabulary;
- `residual://cal0/i7/cal0-q21b/02@1` — which provisional functions, if any, are safe to express;
- `residual://cal0/i7/cal0-q21b/03@1` — recovery, validation, rollback, and repair policies by transition family;
- `residual://cal0/i7/cal0-q21b/04@1` — projection rules for reader-facing aggregate outcome labels.

### CAL0-Q22B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q22b/01@1` — component-energy ceilings and primary-block reservations by family;
- `residual://cal0/i7/cal0-q22b/02@1` — the residual-correlation accounting convention and safety margin;
- `residual://cal0/i7/cal0-q22b/03@1` — evidence required to add, enlarge, split, or remove an overlap;
- `residual://cal0/i7/cal0-q22b/04@1` — ablation and sensitivity thresholds that retire an unjustified bridge.

### CAL0-Q23B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q23b/01@1` — field scales and total interaction budgets by stage and mechanism family;
- `residual://cal0/i7/cal0-q23b/02@1` — permitted interaction arity and whether any justified term may span adjacent stages;
- `residual://cal0/i7/cal0-q23b/03@1` — compatibility predicates, conflict handling, and numerical tolerances;
- `residual://cal0/i7/cal0-q23b/04@1` — minimum materiality and ablation evidence for retaining a term.

### CAL0-Q24B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q24b/01@1` — deterministic selection policy when several maximal safe subsets compete;
- `residual://cal0/i7/cal0-q24b/02@1` — whether independent safe components share one transaction or several linked atomic commits;
- `residual://cal0/i7/cal0-q24b/03@1` — concurrency, rollback, recovery-validation, and stale-proposal rules;
- `residual://cal0/i7/cal0-q24b/04@1` — event-ledger representation for rejected and superseded proposals.

### CAL0-Q25B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q25b/01@1` — minimum primary and residual reservations by component family;
- `residual://cal0/i7/cal0-q25b/02@1` — maximum number, energy share, and cumulative share of secondary allocations;
- `residual://cal0/i7/cal0-q25b/03@1` — evidence and sensitivity thresholds for creating or enlarging an allocation;
- `residual://cal0/i7/cal0-q25b/04@1` — versioning and migration rules when an allocation is reduced, retired, or reclassified as primary.

### CAL0-Q26B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q26b/01@1` — registered loss and materiality measures by mechanism and scenario family;
- `residual://cal0/i7/cal0-q26b/02@1` — minimum scenario coverage, stability, and out-of-sample evidence for retention;
- `residual://cal0/i7/cal0-q26b/03@1` — review intervals, grace rules, and protected-boundary tolerances;
- `residual://cal0/i7/cal0-q26b/04@1` — whether a retired interaction may be reinstated or must receive a new identity.

### CAL0-Q27B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q27b/01@1` — the objective vocabulary, type-specific comparison operators, and equality tolerances;
- `residual://cal0/i7/cal0-q27b/02@1` — permitted transition-family overrides and governance for changing objective order;
- `residual://cal0/i7/cal0-q27b/03@1` — treatment of genuinely incomparable objective values before deterministic tie-breaking;
- `residual://cal0/i7/cal0-q27b/04@1` — canonical subset-identity construction and cross-version replay rules.

### CAL0-Q28B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q28b/01@1` — minimum evidence duration, scenario coverage, and ablation stability before a transfer may be proposed;
- `residual://cal0/i7/cal0-q28b/02@1` — minimum primary and residual reservations by component family after reallocation;
- `residual://cal0/i7/cal0-q28b/03@1` — maximum transfer magnitude and frequency per version lineage;
- `residual://cal0/i7/cal0-q28b/04@1` — compatibility, migration-reporting, and deprecation rules for successor parameter sets.

### CAL0-Q29B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q29b/01@1` — exact scope-lattice precedence where population, life-stage, condition, and scenario refinements intersect;
- `residual://cal0/i7/cal0-q29b/02@1` — minimum shared evidence required before a parent binding may be inherited;
- `residual://cal0/i7/cal0-q29b/03@1` — partial-pooling rules, uncertainty widening, and multiple-comparison controls;
- `residual://cal0/i7/cal0-q29b/04@1` — conflict resolution when two incomparable scope bindings both cover one request.

### CAL0-Q30B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q30b/01@1` — initial objective vocabulary and type-specific comparison/equality semantics;
- `residual://cal0/i7/cal0-q30b/02@1` — permitted family templates and the governance threshold for refinements;
- `residual://cal0/i7/cal0-q30b/03@1` — handling of incomparable typed values without collapsing them into scalar utility;
- `residual://cal0/i7/cal0-q30b/04@1` — cross-version replay, deprecation, and migration rules for template changes.

### CAL0-Q31B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q31b/01@1` — stable node, edge, branch, and merge identity construction;
- `residual://cal0/i7/cal0-q31b/02@1` — compatibility dimensions, directions, tolerances, and protected observables;
- `residual://cal0/i7/cal0-q31b/03@1` — common-ancestor selection and typed conflict resolution where several ancestors exist;
- `residual://cal0/i7/cal0-q31b/04@1` — branch activation, review, convergence, deprecation, and orphan-handling rules.

### CAL0-Q32B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q32b/01@1` — support-distance topology, path composition, and attenuation functions by scope dimension;
- `residual://cal0/i7/cal0-q32b/02@1` — transfer-variance floors, per-source and total effective-sample caps, and uncertainty coverage targets;
- `residual://cal0/i7/cal0-q32b/03@1` — conflict tests, multiple-source reconciliation, deduplication, and protected-boundary tolerances;
- `residual://cal0/i7/cal0-q32b/04@1` — minimum local evidence required before borrowed evidence may influence an active binding.

### CAL0-Q33B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q33b/01@1` — initial typed comparison relations, equivalence tolerances, and incomparability reasons;
- `residual://cal0/i7/cal0-q33b/02@1` — admissible family-resolution rule forms, ordering, invariance requirements, and review governance;
- `residual://cal0/i7/cal0-q33b/03@1` — treatment of uncertainty intervals, set-valued objectives, and partially observed values;
- `residual://cal0/i7/cal0-q33b/04@1` — canonical tie-break identity and cross-version replay when comparison semantics change.

### CAL0-Q34B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q34b/01@1` — the minimum protected outputs, mappings, tolerances, and witness suites for each compatibility dimension;
- `residual://cal0/i7/cal0-q34b/02@1` — which changes invalidate a claim immediately, place it under review, or remain outside its dependency set;
- `residual://cal0/i7/cal0-q34b/03@1` — admissible composition and transitivity proofs, if any, and their maximum scope;
- `residual://cal0/i7/cal0-q34b/04@1` — claim expiry, revalidation, and presentation rules for authors and validation tooling.

### CAL0-Q35B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q35b/01@1` — edge attenuation, transfer-variance, effective-sample ceilings, and maximum path lengths by observable and scope dimension;
- `residual://cal0/i7/cal0-q35b/02@1` — canonical edge decomposition and equivalence rules that prevent path-length or path-splitting exploits;
- `residual://cal0/i7/cal0-q35b/03@1` — boundary and conflict tests, including whether any protected edge forces a stronger terminal status than `unsupported`;
- `residual://cal0/i7/cal0-q35b/04@1` — governed selection and aggregation when several non-dominated admissible paths connect the same source and target.

### CAL0-Q36B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q36b/01@1` — the first registered predicate vocabulary, permitted input types, and transition-family templates;
- `residual://cal0/i7/cal0-q36b/02@1` — non-emptiness, monotonicity, renaming, unit, perturbation, and lower-priority invariance fixtures;
- `residual://cal0/i7/cal0-q36b/03@1` — handling of partially observed predicate inputs and observer-specific uncertainty without changing the latent outcome;
- `residual://cal0/i7/cal0-q36b/04@1` — review, retirement, and migration rules when a predicate or cascade version fails validation.

### CAL0-Q37B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q37b/01@1` — the typed dependency vocabulary, transitive-closure rules, and semantic fingerprint construction;
- `residual://cal0/i7/cal0-q37b/02@1` — which change classes make each dependency unaffected, stale, or immediately invalid;
- `residual://cal0/i7/cal0-q37b/03@1` — revalidation witness coverage, expiry, review, and failure-to-verdict rules by compatibility dimension;
- `residual://cal0/i7/cal0-q37b/04@1` — presentation rules distinguishing current evidence, stale evidence, invalidated semantics, incompatibility, and lack of support.

### CAL0-Q38B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q38b/01@1` — path-dominance relations, canonical route equivalence, and maximum retained-path budgets by observable;
- `residual://cal0/i7/cal0-q38b/02@1` — event, source, edge, witness, and causal-ancestor overlap representation;
- `residual://cal0/i7/cal0-q38b/03@1` — conservative dependence aggregation, corroboration credit, uncertainty widening, and effective-sample ceilings;
- `residual://cal0/i7/cal0-q38b/04@1` — conflict propagation, pre-outcome path freezing, and sensitivity tests against graph densification or edge splitting.

### CAL0-Q39B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q39b/01@1` — the initial predicate type vocabulary, registry namespaces, and authorised transition-family templates;
- `residual://cal0/i7/cal0-q39b/02@1` — formal non-emptiness, monotonicity, perturbation, liveness, and cross-predicate composition fixtures;
- `residual://cal0/i7/cal0-q39b/03@1` — governance thresholds for registration, restriction, retirement, replacement, and family-template evolution;
- `residual://cal0/i7/cal0-q39b/04@1` — behavioural compatibility and replay rules across predicate and template versions.

### CAL0-Q40B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q40b/01@1` — the first semantic-facet, dependency-edge, and successor-change vocabularies;
- `residual://cal0/i7/cal0-q40b/02@1` — canonical projection, fingerprint, equivalence, and atomic-bundle rules;
- `residual://cal0/i7/cal0-q40b/03@1` — the complete typed impact table and cross-edge composition witnesses;
- `residual://cal0/i7/cal0-q40b/04@1` — claim-specific revalidation planning, explanation presentation, and change-set review thresholds.

### CAL0-Q41B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q41b/01@1` — the first provenance-node types, equivalence rules, and graph-construction contracts;
- `residual://cal0/i7/cal0-q41b/02@1` — overlap-to-bound compilation, unknown-dependence defaults, and PSD-feasibility rules;
- `residual://cal0/i7/cal0-q41b/03@1` — path-weight, source-cap, structural-uncertainty, and effective-support policies;
- `residual://cal0/i7/cal0-q41b/04@1` — solver precision, worst-case dependence search, and graph-densification sensitivity fixtures.

### CAL0-Q42B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q42b/01@1` — the initial behavioural-compatibility dimensions, allowed implications, and scope vocabulary;
- `residual://cal0/i7/cal0-q42b/02@1` — mandatory regression, boundary, metamorphic, differential, and composition witness suites;
- `residual://cal0/i7/cal0-q42b/03@1` — activation, restriction, retirement, invalidation, rollback, and replacement authority thresholds;
- `residual://cal0/i7/cal0-q42b/04@1` — template-upgrade, deprecation-window, diagnostic migration, and long-term replay-retention rules.

### CAL0-Q43B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q43b/01@1` — the initial typed schema and facet-projection registry, including ordered, unordered, absent, default, unit, decimal, and executable representations;
- `residual://cal0/i7/cal0-q43b/02@1` — digest algorithms, canonical encodings, collision response, independent canonicalisation witnesses, and algorithm-migration rules;
- `residual://cal0/i7/cal0-q43b/03@1` — typed cross-version facet-equivalence contracts and when a changed facet is stale, invalid, or behaviour-preserving;
- `residual://cal0/i7/cal0-q43b/04@1` — authoring views, explanation granularity, storage policy, and historical retention for semantic and representation fingerprints.

### CAL0-Q44B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q44b/01@1` — the initial overlap taxonomy, typed rule grammar, precedence, interval-composition semantics, and conservative unknown-dependence defaults;
- `residual://cal0/i7/cal0-q44b/02@1` — evidence standards and bounds for event, cohort, process, instrument, institution, witness, mechanism, and ancestry relationships;
- `residual://cal0/i7/cal0-q44b/03@1` — PSD-feasibility solver, precision, conflict-core extraction, worst-case optimisation, and numerical reproducibility contracts;
- `residual://cal0/i7/cal0-q44b/04@1` — registry review, scope restriction, successor-version, graph-refactoring, and sensitivity requirements.

### CAL0-Q45B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q45b/01@1` — the exact behavioural dimensions, subdimensions, scope language, verdict predicates, and protected inputs, outputs, traces, and diagnostics;
- `residual://cal0/i7/cal0-q45b/02@1` — the first registered implication and composition rules, including proof obligations and prohibited inferences;
- `residual://cal0/i7/cal0-q45b/03@1` — conflict, restriction, staleness, invalidity, expiry, revalidation, and presentation rules for profile cells;
- `residual://cal0/i7/cal0-q45b/04@1` — witness coverage, boundary partitions, tolerance semantics, manifest bindings, and long-term executable replay retention.

### CAL0-Q46B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q46b/01@1` — the first schema language, primitive-type registry, semantic-role vocabulary, facet-assignment rules, and domain-override boundaries;
- `residual://cal0/i7/cal0-q46b/02@1` — compiler determinism, totality, independent implementation, golden-vector, fuzz, and cross-platform conformance suites;
- `residual://cal0/i7/cal0-q46b/03@1` — equivalence-migration direction, invertibility, round-trip, loss, scope, and facet-specific evidence standards;
- `residual://cal0/i7/cal0-q46b/04@1` — schema, primitive, compiler, and migration activation, restriction, retirement, invalidation, and replay-retention governance.

### CAL0-Q47B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q47b/01@1` — the complete atomic constraint language, canonical expansion rules, variable mappings, and semantic equivalence treatment;
- `residual://cal0/i7/cal0-q47b/02@1` — certified feasibility, PSD, interval, precision, residual, solver-independence, and cross-platform reproducibility contracts;
- `residual://cal0/i7/cal0-q47b/03@1` — irreducible and bounded conflict-core extraction, deterministic core ranking, explanation, and authoring diagnostics;
- `residual://cal0/i7/cal0-q47b/04@1` — conservative-refinement proofs and the governance of withdrawal, weakening, rescoping, correction, replacement, and sensitivity reruns.

### CAL0-Q48B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q48b/01@1` — the first admissible implication and composition constructors for each behavioural dimension and direction;
- `residual://cal0/i7/cal0-q48b/02@1` — scope intersection, restriction, exclusion, tolerance, counterexample, evidence-strength, and lifecycle propagation laws;
- `residual://cal0/i7/cal0-q48b/03@1` — proof-DAG canonicalisation, cycle rejection, minimal explanation, cache invalidation, and manifest-binding rules;
- `residual://cal0/i7/cal0-q48b/04@1` — rule registration, differential and composition witness coverage, algebra-version compatibility, retirement, and long-term proof replay.

### CAL0-Q49B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q49b/01@1` — the evolution-node types, impact classes, facet-dependency vocabulary, closure algorithm, and unknown-impact failure policy;
- `residual://cal0/i7/cal0-q49b/02@1` — conformance-contract grammar, admitted bundle combinations, independent compiler witnesses, and cross-platform reproducibility requirements;
- `residual://cal0/i7/cal0-q49b/03@1` — single- and multi-parent proposal, conflict-resolution, atomic activation, restriction, retirement, rollback, and invalidation governance;
- `residual://cal0/i7/cal0-q49b/04@1` — migration-obligation matrices, historical executable retention, graph compaction, and long-term replay support.

### CAL0-Q50B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q50b/01@1` — type-specific evidence standards, authority thresholds, review roles, and correction-versus-relaxation classification tests;
- `residual://cal0/i7/cal0-q50b/02@1` — feasible-set mapping, set-difference approximation, worst-case output, effective-support, factor-identity, and uncertainty-delta methods;
- `residual://cal0/i7/cal0-q50b/03@1` — split and rescope exhaustiveness, overlap, boundary, fallback, and ungoverned-gap rules;
- `residual://cal0/i7/cal0-q50b/04@1` — competing-repair comparison, activation, appeal, supersession, model-rejection, and historical-retention governance.

### CAL0-Q51B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q51b/01@1` — proof-object schema, canonical DAG identity, semantic deduplication, minimal explanation, and direct-versus-derived evidence presentation;
- `residual://cal0/i7/cal0-q51b/02@1` — dimension-specific strength partial orders, corroboration ceilings, shared-evidence treatment, and tolerance-composition laws;
- `residual://cal0/i7/cal0-q51b/03@1` — dependency-impact, stale, invalid, conflicted, restricted, superseded, revalidated, and retired lifecycle propagation;
- `residual://cal0/i7/cal0-q51b/04@1` — proof storage, incremental revalidation, manifest binding, executable replay retention, and governed compaction.

### CAL0-Q52B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q52b/01@1` — maximal-common-base discovery, facet-specific comparison-base selection, criss-cross ancestry, and canonical virtual-base rules;
- `residual://cal0/i7/cal0-q52b/02@1` — conflict classes, interaction promotion, resolution types, authority, evidence thresholds, and exhaustive scope-partition tests;
- `residual://cal0/i7/cal0-q52b/03@1` — merged impact-closure compilation, bundle witness matrices, atomic activation, rollback, and failed-merge retention;
- `residual://cal0/i7/cal0-q52b/04@1` — convergence identity, compatibility claims to each parent, repeated merges, graph compaction, and long-term branch replay.

### CAL0-Q53B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q53b/01@1` — non-compensable gate vocabularies, evidence cutoffs, protected-meaning thresholds, disclosure standards, and missing-data policy;
- `residual://cal0/i7/cal0-q53b/02@1` — repair-type comparison constructors, dominance witnesses, incomparable dimensions, canonical frontier identity, and perturbation tests;
- `residual://cal0/i7/cal0-q53b/03@1` — selection authority, mandate, rationale schema, conflict-of-interest controls, appeal, reconsideration, and successor-decision governance;
- `residual://cal0/i7/cal0-q53b/04@1` — counterfactual retention, downstream monitoring, manifest binding, frontier compaction, and long-term audit presentation.

### CAL0-Q54B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q54b/01@1` — semantic change-batch schema, snapshot isolation, impact closure, minimal-frontier construction, topological scheduling, and cycle policy;
- `residual://cal0/i7/cal0-q54b/02@1` — content-addressed subproof identity, context equality, lifecycle admissibility, deduplication, and proof-reuse eligibility;
- `residual://cal0/i7/cal0-q54b/03@1` — staged successor creation, atomic dependency-closed commit, interruption recovery, concurrent batches, and supersession topology;
- `residual://cal0/i7/cal0-q54b/04@1` — revalidation budgets, prioritisation, failed-batch retention, manifest migration, graph compaction, and replay-service requirements.

### CAL0-Q55B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q55b/01@1` — typed maximal-common-ancestor discovery, criss-cross graph validation, missing-history policy, and canonical graph-snapshot identity;
- `residual://cal0/i7/cal0-q55b/02@1` — facet-state antichain representation, equivalence and subsumption witnesses, scope projection, restrictions, and conflict classification;
- `residual://cal0/i7/cal0-q55b/03@1` — multi-base delta compilation, interaction promotion, virtual-base lifecycle, invalidation, succession, and reuse eligibility;
- `residual://cal0/i7/cal0-q55b/04@1` — comparison-artifact storage, explanation, compaction, manifest binding, and long-term convergence replay.

### CAL0-Q56B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q56b/01@1` — standing, grounds, materiality, evidence-admission, mandate, timeliness, conflict-of-interest, and emergency-suspension rules;
- `residual://cal0/i7/cal0-q56b/02@1` — successor-frontier compilation, candidate carry-forward, corrected-evidence treatment, comparison-law changes, and differential witnesses;
- `residual://cal0/i7/cal0-q56b/03@1` — affirm, supersede, narrow, suspend, remand, and reject effects; effective-scope and effective-time semantics;
- `residual://cal0/i7/cal0-q56b/04@1` — concurrent appeals, episode-lineage topology, manifest migration, notification, retention, compaction, and historical replay.

### CAL0-Q57B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q57b/01@1` — snapshot and graph-root schema, isolation level, dependency and registry guards, read visibility, and manifest-admission boundary;
- `residual://cal0/i7/cal0-q57b/02@1` — staging namespace, obligation closure, worker scheduling, witness caching, resource budgets, and failed-stage retention;
- `residual://cal0/i7/cal0-q57b/03@1` — atomic publication mechanism, idempotency key, crash recovery, audit log, garbage collection, rollback, and supersession indexing;
- `residual://cal0/i7/cal0-q57b/04@1` — overlapping and disjoint concurrent batches, conflict detection, serialisation, deterministic rebase, starvation, and long-term replay service.

### CAL0-Q58B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q58b/01@1` — protected comparison-query vocabularies, typed answer equivalence, boundary completeness, subsumption, and multi-state coverage rules;
- `residual://cal0/i7/cal0-q58b/02@1` — canonical reduction selection, partial compaction, minimum useful reduction, proof search budgets, and denial-of-service limits;
- `residual://cal0/i7/cal0-q58b/03@1` — reversible recovery maps, content retention, certificate composition, lifecycle propagation, revalidation, and successor topology;
- `residual://cal0/i7/cal0-q58b/04@1` — explanation expansion, audit presentation, storage compaction, manifest binding, long-term availability, and garbage-collection prohibitions.

### CAL0-Q59B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q59b/01@1` — standing classes, represented interests, authority credentials, jurisdiction, mandate, timeliness, waiver, and conflict-of-interest rules;
- `residual://cal0/i7/cal0-q59b/02@1` — typed grounds, provenance thresholds, materiality witnesses, protected dimensions, duplicate identity, and abuse controls;
- `residual://cal0/i7/cal0-q59b/03@1` — affirmance, supersession, narrowing, suspension, remand, rejection, dismissal, withdrawal, and emergency-effect semantics;
- `residual://cal0/i7/cal0-q59b/04@1` — concurrent and consolidated requests, notice, participation, deadlines, effective boundaries, manifest admission, and historical-use review.

### CAL0-Q60B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q60b/01@1` — semantic read/write/guard key schema, dependency closure, alias normalisation, scope intersection, and conservative unknown handling;
- `residual://cal0/i7/cal0-q60b/02@1` — admission index, lock or certification mechanism, disjointness witnesses, deadlock avoidance, fairness, starvation, priority, and resource budgets;
- `residual://cal0/i7/cal0-q60b/03@1` — intervening-delta calculation, deterministic rebase identity, reusable-stage eligibility, obligation replay, and order-invariant root composition;
- `residual://cal0/i7/cal0-q60b/04@1` — conflict retention, retry limits, crash recovery, monitoring, manifest admission, distributed implementation, and long-term serialisability witnesses.

### CAL0-Q61B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q61b/01@1` — certificate-node and composition-edge schemas, canonical DAG identity, facet compatibility, path normalisation, cycle detection, and duplicate-route handling;
- `residual://cal0/i7/cal0-q61b/02@1` — protected-query closure, scope intersection, weakest-authority and evidence ceilings, restriction accumulation, recovery composition, and conflict semantics;
- `residual://cal0/i7/cal0-q61b/03@1` — checkpoint admission thresholds, independent end-to-end witness suites, checkpoint placement, refresh, succession, invalidation, and replay budgets;
- `residual://cal0/i7/cal0-q61b/04@1` — premise retention, recovery service, explanation expansion, dependency indexing, DAG compaction, denial-of-service controls, and long-term availability.

### CAL0-Q62B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q62b/01@1` — appeal semantic identity, participant retention, evidence deduplication, relation vocabulary, dependency closure, component identity, and frozen-snapshot rules;
- `residual://cal0/i7/cal0-q62b/02@1` — compatible, competing, and conflicting remedy algebra; scope, time, mandate, jurisdiction, authority, and participation-right intersections;
- `residual://cal0/i7/cal0-q62b/03@1` — consolidation, severance, coordinated review, remand, adjudication, atomic publication, deadlines, stays, fairness, and starvation controls;
- `residual://cal0/i7/cal0-q62b/04@1` — late requests, successor dockets, notice, explanation, manifest-admission boundaries, historical-use review, retention, and long-term procedural replay.

### CAL0-Q63B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q63b/01@1` — base-access vocabulary, semantic-root and facet atom schema, access modes, negative obligations, alias closure, and transitive policy closure;
- `residual://cal0/i7/cal0-q63b/02@1` — scope algebra, intersection certificates, conservative unknown atoms, conflict indexing, canonical explanations, and deterministic digest construction;
- `residual://cal0/i7/cal0-q63b/03@1` — compiler soundness, completeness envelopes, monotone-conservatism, metamorphic refactoring, known-conflict corpora, liveness metrics, and performance budgets;
- `residual://cal0/i7/cal0-q63b/04@1` — compiler evolution, compatibility and differential witnesses, staged-batch invalidation, guard-index migration, distributed admission, audit, and historical replay.

### CAL0-Q64B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q64b/01@1` — workload-manifest schema, benchmark isolation, cost dimensions, confidence rules, minimum-benefit frontiers, placement candidates, and stopping boundaries;
- `residual://cal0/i7/cal0-q64b/02@1` — end-to-end protected-query closure, non-loss corpus, explanation and recovery equivalence, perturbation coverage, and adversarial reference implementations;
- `residual://cal0/i7/cal0-q64b/03@1` — facet-impact mapping, lifecycle states, renewal frontier, unaffected-subproof reuse, successor identity, expiry, retirement, and historical replay;
- `residual://cal0/i7/cal0-q64b/04@1` — checkpoint index, admission cadence, storage and compute budgets, eviction, denial-of-service controls, observability, and long-term dependency availability.

### CAL0-Q65B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q65b/01@1` — authority-source, standing, mandate, jurisdiction, delegation, concurrence, recusal, conflict, participation, and remedy schemas;
- `residual://cal0/i7/cal0-q65b/02@1` — dimension-specific lattice relations, implication and composition rules, scope and time algebra, unknown handling, and deterministic conflict classification;
- `residual://cal0/i7/cal0-q65b/03@1` — coordination, severance, remand, interim protection, review, adjudicator admission, dissent, deadlock, fairness, deadline, and starvation controls;
- `residual://cal0/i7/cal0-q65b/04@1` — mandate evolution, succession, notice, historical-use review, explanation, registry governance, audit, retention, and procedural replay.

### CAL0-Q66B

**Classification:** `IMPLEMENTATION`  
**Owner:** Executable implementation and version-governance authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch.

**Activation:** A successor manifest expands the active reference scope or claims the unresolved surface.

- `residual://cal0/i7/cal0-q66b/01@1` — quotient-class and compound-atom schemas, typed equivalence envelopes, operation interaction tables, scope-cover proofs, reverse expansion, and canonical identity;
- `residual://cal0/i7/cal0-q66b/02@1` — reference conflict compiler, protected explanation equivalence, finite and generated witness corpora, unknown boundaries, and completeness claims;
- `residual://cal0/i7/cal0-q66b/03@1` — quotient search, certificate construction, incremental invalidation, fallback, staged-batch handling, index migration, and distributed admission;
- `residual://cal0/i7/cal0-q66b/04@1` — liveness and compression metrics, performance budgets, adversarial collision generation, monitoring, retention, audit, and historical explanation replay.

### parameter://cal0/unresolved/rare-soul-prevalence@1

**Classification:** `SETTING_CONTENT`  
**Owner:** Setting design  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** No population claim may infer this prevalence from generated outliers. A setting version must author it before a world population uses it.

**Activation:** A story, population model, or institution requires a numerical prevalence.

- `residual://cal0/i7/rare-soul-prevalence@1` — Rare-Soul prevalence

### parameter://cal0/unresolved/prenatal-consciousness-distribution@1

**Classification:** `SETTING_CONTENT`  
**Owner:** Setting design  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The protagonist's reincarnate continuity remains a separate scenario mechanism. Ordinary cohorts assume no directed prenatal System practice unless a setting version states otherwise.

**Activation:** Ordinary prenatal awareness becomes relevant to a plot, culture, or population model.

- `residual://cal0/i7/ordinary-prenatal-consciousness@1` — Ordinary prenatal-consciousness distribution

### parameter://cal0/unresolved/cross-species-scale@1

**Classification:** `FUTURE_OPTIONAL_EXTENSION`  
**Owner:** Species-extension design  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** Human-reference values cannot be extrapolated into a nonhuman species. A species-specific extension must declare morphology, life course, anchors, and comparison evidence.

**Activation:** A nonhuman species requires numerical sheets or population calibration.

- `residual://cal0/i7/cross-species-scale@1` — Cross-species absolute-capacity scale

### parameter://cal0/unresolved/injury-incidence@1

**Classification:** `CALIBRATION`  
**Owner:** Population-calibration authors  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** The I4 rate is a sensitivity-tested trial input, not an empirical world estimate. New populations must pin their own exposure model and rerun survivorship envelopes.

**Activation:** A setting population makes quantitative injury, disability, or survivorship claims.

- `residual://cal0/i7/injury-incidence@1` — World injury incidence

### parameter://cal0/unresolved/rarity-distribution@1

**Classification:** `SETTING_CONTENT`  
**Owner:** Setting design, consumed by population calibration  
**Disposition:** `BOUNDED_NONBLOCKING`

**Boundary:** Rarity labels remain typed and scope-specific. A setting version must author eligible denominators and evidence before a population distribution is claimed.

**Activation:** The story or a population model needs numerical rarity proportions.

- `residual://cal0/i7/rarity-distribution@1` — Rarity distribution

## Resolved Soul question

`parameter://cal0/unresolved/protagonist-long-term-soul-multiplier@1` is `RESOLVED_NOT_A_RESIDUAL` through `RESOLVES_AS_NONSCALAR_PROFILE`. The active resolution is `NOT_APPLICABLE_NONSCALAR_PROFILE`; it is not counted among the 305 residual items.

Registry digest: `sha256:1d3a7db6206ef6f25aa7636cc2e7044580738aab89dd4270b04977cf28eb795b`.
