# CAL0 reference implementation

**Package version:** 0.7.0  
**Implements:** CAL0-I1 through CAL0-I7  
**Canonical specification:** 0.89  
**Calibration annex:** 2.9  
**Parameter status:** `AUTHORING_VALIDATED_PROVISIONAL`
**Closure status:** `VALIDATED_BASELINE_WITH_BOUNDED_RESIDUALS`

This dependency-free Python package implements the closed CAL0 model-family
topology, deterministic reference engines, typed provisional parameters, small
reference scenarios, the I4 life-course calibration model, the I5
invariant-led adversarial network, the I6 authoring layer, and the I7
validated-closure evidence chain. It does not claim to estimate real human
biology, convert provisional inputs into empirical facts, or freeze
plot-specific character values.

## CAL0-I7 deliverables

- a nine-criterion `VAL1.2D` evidence matrix connecting all required artifacts;
- a 71-group, 305-item residual-uncertainty register covering every unresolved
  CAL0-Q1–Q66 parameter surface plus five world-level residuals, with zero
  blocking entries;
- explicit JSON Schemas for complete character sheets and all six projection
  views;
- an independently named character-sheet checklist and a ninety-cell scene
  matrix that separates causal truth, source record, viewpoint access,
  interpretation, presentation, and reader need for all fifteen scenarios;
- a ten-entry successor change register preserving the six I5/I6 entries and
  closing four I7 implementation or presentation corrections;
- an explicit lineage joining the historical protagonist Soul unknown to its
  non-scalar I6 resolution without inventing a coefficient;
- readable validated-closure and residual-uncertainty handbooks.

## CAL0-I6 deliverables

- 14 complete reference sheets: eight protagonist milestones and six ordinary,
  professional, institutional, military, creature, and exceptional comparisons;
- six separate projections for every sheet—private backend, author-facing,
  character-accessible, appraisal-derived, institutional, and reader-facing—
  for 84 validated views without private-field leakage;
- 15 worked story scenarios covering the minimum growth, progression, training,
  institution, dungeon, research, craft, injury, conflict, and knowledge-transfer
  families;
- authoring checklists for ten artifact types and four epistemically bounded
  System-notification templates;
- a concise story-facing guide and readable reference-sheet, worked-scenario,
  and authoring-template handbooks;
- a controlled six-entry change register covering all five I5 repairs and the
  I6 protagonist-Soul decision;
- a non-scalar protagonist Soul profile: unusual development is expressed
  through Depth, Coherence, Resonance, boundary integrity, coupling, recovery,
  and safe assimilation, not a universal multiplier.

## CAL0-I5 deliverables

- 42 adversarial cases across individual, institutional, economic, ecological,
  informational, magical, training, identity, and replay surfaces;
- two pinned seeds and forward/reverse traversal for every case, producing 168
  order-invariant executions;
- complete attack records containing preconditions, actor knowledge, bounded
  resources, action sequence, predicted and observed results, affected
  invariants, subsystem scope, classification, repair, and regression identity;
- 15 causally funded strategies retained as valid emergent optimisation and 27
  provenance-free, duplicating, retrospective, or unsupported attempts denied;
- five least-disruptive repairs covering semantic event identity,
  source-bounded renewal, projection/authority separation, exclusive identity
  continuation, and training-stimulus deduplication with harm gating;
- zero unresolved invariant violations and regression coverage for every
  accepted repair.

## CAL0-I4 deliverables

- three immutable calibration iterations, each containing five seeded runs of
  10,000 births;
- four deliberately different social environments in every reference cohort;
- late-prenatal, newborn, child, adult, and ageing projections with separate
  maturation, purposeful-training, organic-adaptation, reinforcement,
  assimilation, and injury contributions;
- Skill and class offers, choices, XP, levels, form completion, later-grade
  feasibility, magical contact, independent capability, representative
  vocational/combat/coordination performances, and survivorship outcomes;
- ordinary-household, talented, institutional, early-magic, and two separate
  protagonist scenario ensembles;
- one-at-a-time sensitivity and identifiability classifications for all 39 I3
  provisional coefficients, plus dependence-model sensitivity;
- explicit classifications for all six unresolved parent values without
  inventing estimates or hiding them in defaults;
- causal histories for exceptional performance and injury-tail outliers;
- a content-addressed successor assessment and replay-stable cohort report.

The final reference successor changes only four I3 coefficients: adaptation
gain scale, Skill XP total scale, Class XP total scale, and Class XP exponent.
The original I3 set and the over-braked intermediate I4 iteration remain
immutable and replayable alongside the final successor.

## Interpretation boundary

`AUTHORING_VALIDATED_PROVISIONAL` still means the cohort-calibrated and adversarially
validated reference configuration can be used for ordinary story planning
through the declared I6 projections, sheets, scenarios, templates, and guide.
`VALIDATED_BASELINE_WITH_BOUNDED_RESIDUALS` additionally means every VAL1.2D
closure criterion has passing evidence and all outstanding uncertainty is
classified, owned, bounded, and non-blocking for the active reference scope.
Neither status means the input distributions were empirically estimated or that
reference sheets are fixed plot canon. Rare-Soul prevalence, ordinary prenatal
consciousness, cross-species scaling, injury incidence, and rarity proportions
remain classified inputs or future extensions. The earlier protagonist Soul
multiplier question is resolved as inapplicable: the active model is non-scalar.

## Inherited engine and fixture families

- milestone-anchored PCHIP maturation and generalised-mean capacity mapping;
- typed adaptation, hormetic load, headroom, detraining, and transition gates;
- Skill and Class XP curves, grade scaling, attestation taper, and threshold
  isolation;
- resource conservation, immutable reinforcement claims, safe assimilation,
  and protected backlog;
- dependence, overlap, provenance, transition, proof, appeal, semantic-guard,
  checkpoint, and atomic-publication governance;
- the exact 66-case I2 fixture suite, five I3 reference scenarios, twelve I1/I3
  malformed-input cases, six I4 cohort-plan failure fixtures, six I5
  adversarial-report failure fixtures, ten I6 usability failure fixtures, and
  fourteen I7 closure failure fixtures.

## Run

From this directory:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m cal0.cli validate .
PYTHONPATH=src python3 -m cal0.cli fixtures .
PYTHONPATH=src python3 -m cal0.cli reference-summary .
PYTHONPATH=src python3 -m cal0.cli i3-summary .
PYTHONPATH=src python3 -m cal0.cli i4-summary .
PYTHONPATH=src python3 -m cal0.cli i5-summary .
PYTHONPATH=src python3 -m cal0.cli i6-summary .
PYTHONPATH=src python3 -m cal0.cli i7-summary .
```

`i4-summary`, `i5-summary`, `i6-summary`, and `i7-summary` read their pinned materialised reports. Deliberate
full replays are:

```bash
PYTHONPATH=src python3 -m cal0.cli i4-calibrate .
PYTHONPATH=src python3 -m cal0.cli i5-adversarial .
PYTHONPATH=src python3 -m cal0.cli i6-authoring .
PYTHONPATH=src python3 -m cal0.cli i7-close .
```

The package uses only the Python standard library. Canonical JSON rejects
binary floating-point values, non-finite values, and ambiguous map keys. Exact
decimal strings are parsed only inside numerical engines and serialised back to
plain decimal strings before entering replay records.

## Stage boundary

CAL0-I7 is complete because all nine VAL1.2D criteria pass, the standard
artifact set is connected, every residual uncertainty has a permitted
classification and owner, no blocking residual remains, and the complete
I1–I7 evidence chain replays from a content-pinned archive. Further work is
controlled maintenance or setting/story development, not another scheduled
CAL0 architecture or execution stage.
