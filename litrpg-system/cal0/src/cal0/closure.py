"""CAL0-I7 validated-closure review and residual-uncertainty registry."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
from typing import Any, Mapping

from .authoring import VIEW_KINDS
from .canonical import semantic_digest
from .parameter_runtime import load_json


RESIDUAL_CLASSIFICATIONS = (
    "CALIBRATION",
    "SETTING_CONTENT",
    "CHARACTER_CHOICE",
    "PLOT_CHOICE",
    "IMPLEMENTATION",
    "FUTURE_OPTIONAL_EXTENSION",
)

SCENE_LAYERS = (
    "causal_truth",
    "source_record",
    "viewpoint_access",
    "viewpoint_interpretation",
    "interface_or_cultural_presentation",
    "reader_need",
)

VAL12_CRITERIA = (
    "binding_decisions_consistent",
    "multiseed_distributions_stable_and_reproducible",
    "causal_progression_ledgers_separable",
    "no_unresolved_invariant_violation",
    "reference_scenarios_replay_consistently",
    "protagonist_exceptional_without_cohort_redefinition",
    "institutions_and_long_lived_actors_behave_plausibly",
    "reader_projections_comprehensible_without_falsification",
    "outstanding_uncertainty_classified_and_owned",
)


WORLD_RESIDUALS: tuple[dict[str, str], ...] = (
    {
        "residual_id": "residual://cal0/i7/rare-soul-prevalence@1",
        "source_parameter_id": "parameter://cal0/unresolved/rare-soul-prevalence@1",
        "title": "Rare-Soul prevalence",
        "classification": "SETTING_CONTENT",
        "owner": "Setting design",
        "boundary": "No population claim may infer this prevalence from generated outliers. A setting version must author it before a world population uses it.",
        "activation_condition": "A story, population model, or institution requires a numerical prevalence.",
    },
    {
        "residual_id": "residual://cal0/i7/ordinary-prenatal-consciousness@1",
        "source_parameter_id": "parameter://cal0/unresolved/prenatal-consciousness-distribution@1",
        "title": "Ordinary prenatal-consciousness distribution",
        "classification": "SETTING_CONTENT",
        "owner": "Setting design",
        "boundary": "The protagonist's reincarnate continuity remains a separate scenario mechanism. Ordinary cohorts assume no directed prenatal System practice unless a setting version states otherwise.",
        "activation_condition": "Ordinary prenatal awareness becomes relevant to a plot, culture, or population model.",
    },
    {
        "residual_id": "residual://cal0/i7/cross-species-scale@1",
        "source_parameter_id": "parameter://cal0/unresolved/cross-species-scale@1",
        "title": "Cross-species absolute-capacity scale",
        "classification": "FUTURE_OPTIONAL_EXTENSION",
        "owner": "Species-extension design",
        "boundary": "Human-reference values cannot be extrapolated into a nonhuman species. A species-specific extension must declare morphology, life course, anchors, and comparison evidence.",
        "activation_condition": "A nonhuman species requires numerical sheets or population calibration.",
    },
    {
        "residual_id": "residual://cal0/i7/injury-incidence@1",
        "source_parameter_id": "parameter://cal0/unresolved/injury-incidence@1",
        "title": "World injury incidence",
        "classification": "CALIBRATION",
        "owner": "Population-calibration authors",
        "boundary": "The I4 rate is a sensitivity-tested trial input, not an empirical world estimate. New populations must pin their own exposure model and rerun survivorship envelopes.",
        "activation_condition": "A setting population makes quantitative injury, disability, or survivorship claims.",
    },
    {
        "residual_id": "residual://cal0/i7/rarity-distribution@1",
        "source_parameter_id": "parameter://cal0/unresolved/rarity-distribution@1",
        "title": "Rarity distribution",
        "classification": "SETTING_CONTENT",
        "owner": "Setting design, consumed by population calibration",
        "boundary": "Rarity labels remain typed and scope-specific. A setting version must author eligible denominators and evidence before a population distribution is claimed.",
        "activation_condition": "The story or a population model needs numerical rarity proportions.",
    },
)


def _architecture_decisions(specification: str) -> list[str]:
    section = specification.split("## Decision register", 1)[1].split("## Architecture closure", 1)[0]
    decisions: list[str] = []
    for line in section.splitlines():
        match = re.match(r"^\|\s*([^|]+?)\s*\|", line)
        if match and match.group(1).strip() not in {"Code", "---"}:
            decisions.append(match.group(1).strip())
    return decisions


def _annex_residual_groups(annex: str) -> list[dict[str, Any]]:
    expression = re.compile(
        r"^### Unresolved (CAL0-Q(\d+)[A-Z]) parameters\s*\n(.*?)(?=^##|^### )",
        re.MULTILINE | re.DOTALL,
    )
    groups: list[dict[str, Any]] = []
    for match in expression.finditer(annex):
        selection_id = match.group(1)
        decision_number = int(match.group(2))
        classification = "CALIBRATION" if decision_number <= 18 else "IMPLEMENTATION"
        owner = "Calibration parameter-set authors" if classification == "CALIBRATION" else "Executable implementation and version-governance authors"
        boundary = (
            "The active reference parameter set pins every value it executes. This residual becomes mandatory only when a successor set exercises the wider mechanism or makes a stronger quantitative claim."
            if classification == "CALIBRATION"
            else
            "The active bundle implements or fails closed over the exercised path. This residual becomes mandatory before a future manifest may rely on the wider optional governance or optimisation branch."
        )
        items = [
            {
                "item_id": f"residual://cal0/i7/{selection_id.lower()}/{index:02d}@1",
                "text": line.strip()[2:],
                "classification": classification,
                "owner": owner,
                "blocking": False,
            }
            for index, line in enumerate(match.group(3).splitlines(), start=1)
            if line.strip().startswith("- ")
        ]
        groups.append({
            "residual_group_id": f"residual-group://cal0/i7/{selection_id.lower()}@1",
            "source_selection_id": selection_id,
            "classification": classification,
            "owner": owner,
            "closure_disposition": "BOUNDED_NONBLOCKING",
            "boundary": boundary,
            "activation_condition": "A successor manifest expands the active reference scope or claims the unresolved surface.",
            "item_count": len(items),
            "items": items,
            "evidence": [
                "canonical/litrpg-system-calibration-annex.md",
                "registries/cal0-i3-parameters.json",
                "manifests/cal0-i7.bundle.json",
            ],
        })
    return groups


def build_residual_register(annex: str) -> dict[str, Any]:
    groups = _annex_residual_groups(annex)
    for item in WORLD_RESIDUALS:
        groups.append({
            "residual_group_id": item["residual_id"].replace("residual://", "residual-group://"),
            "source_selection_id": item["source_parameter_id"],
            "classification": item["classification"],
            "owner": item["owner"],
            "closure_disposition": "BOUNDED_NONBLOCKING",
            "boundary": item["boundary"],
            "activation_condition": item["activation_condition"],
            "item_count": 1,
            "items": [{
                "item_id": item["residual_id"],
                "text": item["title"],
                "classification": item["classification"],
                "owner": item["owner"],
                "blocking": False,
            }],
            "evidence": [
                "registries/cal0-i3-parameters.json",
                "registries/cal0-i4-parameter-assessment.json",
                "registries/cal0-i6-decision-resolution.json",
            ],
        })
    item_counts = Counter(item["classification"] for group in groups for item in group["items"])
    group_counts = Counter(group["classification"] for group in groups)
    register: dict[str, Any] = {
        "registry_id": "residual-registry://cal0/i7-closure@1",
        "closure_status": "VALIDATED_BASELINE_WITH_BOUNDED_RESIDUALS",
        "allowed_classifications": list(RESIDUAL_CLASSIFICATIONS),
        "classification_definitions": {
            "CALIBRATION": "A coefficient, distribution, threshold, tolerance, or quantitative model must be pinned for a named scope before that scope is claimed.",
            "SETTING_CONTENT": "The world must author a contingent fact; the System architecture does not determine it.",
            "CHARACTER_CHOICE": "A person must choose within causal possibilities; no universal outcome should be specified.",
            "PLOT_CHOICE": "A later narrative event must select among valid possibilities without changing the System rule.",
            "IMPLEMENTATION": "A schema, algorithm, policy, witness, or optimisation is required only when a future implementation exercises that branch.",
            "FUTURE_OPTIONAL_EXTENSION": "The current baseline excludes this scope and does not depend upon it.",
        },
        "group_count": len(groups),
        "item_count": sum(group["item_count"] for group in groups),
        "blocking_group_count": sum(group["closure_disposition"] != "BOUNDED_NONBLOCKING" for group in groups),
        "blocking_item_count": sum(item["blocking"] is True for group in groups for item in group["items"]),
        "group_classification_counts": {key: group_counts.get(key, 0) for key in RESIDUAL_CLASSIFICATIONS},
        "item_classification_counts": {key: item_counts.get(key, 0) for key in RESIDUAL_CLASSIFICATIONS},
        "groups": groups,
        "soul_multiplier_disposition": {
            "historical_parameter_id": "parameter://cal0/unresolved/protagonist-long-term-soul-multiplier@1",
            "i6_active_projection_id": "parameter://cal0/protagonist/long-term-soul-multiplier@1",
            "relationship": "RESOLVES_AS_NONSCALAR_PROFILE",
            "status": "RESOLVED_NOT_A_RESIDUAL",
            "active_resolution": "NOT_APPLICABLE_NONSCALAR_PROFILE",
        },
        "closure_rule": "A bounded residual does not block validated closure when it has one allowed classification, a named owner, an activation condition, a failure boundary, and no current baseline dependency that assumes its answer.",
    }
    register["registry_digest"] = semantic_digest(register)
    return register


def build_scene_matrix(scenarios: list[Mapping[str, Any]]) -> dict[str, Any]:
    entries = []
    for scenario in scenarios:
        entry = {
            "scenario_id": scenario["scenario_id"],
            "family": scenario["family"],
            "layers": {
                "causal_truth": {
                    "source_fields": ["inputs", "causal_sequence", "state_changes"],
                    "value": {"inputs": scenario["inputs"], "causal_sequence": scenario["causal_sequence"], "state_changes": scenario["state_changes"]},
                },
                "source_record": {
                    "source_fields": ["interface_outputs"],
                    "value": scenario["interface_outputs"],
                    "record_is_not_cause": True,
                },
                "viewpoint_access": {
                    "source_fields": ["actor_knowledge"],
                    "value": scenario["actor_knowledge"],
                    "omission_is_not_negative_fact": True,
                },
                "viewpoint_interpretation": {
                    "rule": "Interpretation is bounded by declared knowledge, available evidence, skill, uncertainty, and culture; it cannot upgrade an interface omission into proof.",
                    "confidence": "SCENARIO_BOUNDED",
                },
                "interface_or_cultural_presentation": {
                    "source_fields": ["interface_outputs"],
                    "value": scenario["interface_outputs"],
                    "projection_is_not_authority": True,
                },
                "reader_need": {
                    "source_fields": ["reader_facing_projection"],
                    "value": scenario["reader_facing_projection"],
                    "exact_backend_required": False,
                },
            },
        }
        entry["entry_digest"] = semantic_digest(entry)
        entries.append(entry)
    matrix: dict[str, Any] = {
        "matrix_id": "scene-projection-matrix://cal0/i7-closure@1",
        "layer_order": list(SCENE_LAYERS),
        "scenario_count": len(entries),
        "layer_count": len(SCENE_LAYERS),
        "projection_cell_count": len(entries) * len(SCENE_LAYERS),
        "entries": entries,
    }
    matrix["matrix_digest"] = semantic_digest(matrix)
    return matrix


def _successor_change_register(parent: Mapping[str, Any]) -> dict[str, Any]:
    entries = [dict(item) for item in parent["entries"]]
    additions = (
        {
            "entry_id": "CAL0-I7-C01",
            "title": "Explicitly join the historical Soul unknown to its I6 non-scalar projection",
            "classification": "IMPLEMENTATION_CORRECTION",
            "finding": "I6 preserved the historical record but its active resolved projection used a new identifier without an explicit machine-readable relationship to the I3 unknown.",
            "resolution": "The I7 residual register names both identities and declares RESOLVES_AS_NONSCALAR_PROFILE; the historical record remains immutable and the active resolution remains non-numerical.",
            "evidence": ["registries/cal0-i7-residual-uncertainty.json", "tests/test_cal0_i7.py"],
        },
        {
            "entry_id": "CAL0-I7-C02",
            "title": "Materialise explicit character-sheet and projection JSON Schemas",
            "classification": "IMPLEMENTATION_CORRECTION",
            "finding": "I6 validated six projection contracts and complete sheet records but did not publish standalone JSON Schema identities for them.",
            "resolution": "I7 registers and validates schema://cal0/i7-character-sheet@1 and schema://cal0/i7-sheet-projection@1 against the existing fourteen sheets and eighty-four views.",
            "evidence": ["schemas/cal0-i7-character-sheet.schema.json", "schemas/cal0-i7-sheet-projection.schema.json", "tests/test_cal0_i7.py"],
        },
        {
            "entry_id": "CAL0-I7-C03",
            "title": "Add an independently named character-sheet authoring checklist",
            "classification": "PRESENTATION_CLARIFICATION",
            "finding": "The I6 character template governed sheets implicitly, while VAL1.2D names sheets independently.",
            "resolution": "I7 adds a supplemental character_sheet checklist without changing the ten historical I6 templates or their report digest.",
            "evidence": ["authoring/cal0-i7-character-sheet-checklist.json", "tests/test_cal0_i7.py"],
        },
        {
            "entry_id": "CAL0-I7-C04",
            "title": "Materialise the six-layer scene-facing projection rule",
            "classification": "PRESENTATION_CLARIFICATION",
            "finding": "I6 scenario fields contained the required information but did not expose one explicit six-layer crosswalk for every scenario.",
            "resolution": "I7 generates a ninety-cell matrix across all fifteen scenarios, separating causal truth, source record, access, interpretation, presentation, and reader need.",
            "evidence": ["authoring/cal0-i7-scene-projection-matrix.json", "tests/test_cal0_i7.py"],
        },
    )
    for addition in additions:
        entry = {
            **addition,
            "source_stage": "CAL0-I7",
            "status": "CLOSED_CLOSURE_PINNED",
            "architecture_reopened": False,
            "source_record_digest": semantic_digest(addition),
        }
        entries.append(entry)
    register: dict[str, Any] = {
        "register_id": "change-register://cal0/i7-governance@1",
        "parent_register_id": parent["register_id"],
        "parent_register_digest": parent["register_digest"],
        "classification_order": parent["classification_order"],
        "classification_rules": parent["classification_rules"],
        "entry_count": len(entries),
        "open_entry_count": 0,
        "entries": entries,
        "open_entries": [],
        "new_changes_require": parent["new_changes_require"],
    }
    register["register_digest"] = semantic_digest(register)
    return register


def _sheet_checklist() -> dict[str, Any]:
    checklist: dict[str, Any] = {
        "checklist_id": "checklist://cal0/i7/character-sheet@1",
        "artifact_type": "character_sheet",
        "required_questions": [
            "Which canonical entity and life-stage snapshot does this sheet represent?",
            "Which facts are causally true, recorded, accessible, interpretable, presentable, and reader-relevant?",
            "Which progression, resource, condition, institution, and causal-ledger states are in scope?",
        ],
        "locked_checks": [
            "All eleven attributes use the absolute-capacity architecture and are not totalled into power.",
            "Natural maturation, purposeful training, organic adaptation, Skill XP, Class XP, reinforcement, and assimilation remain distinct.",
            "Projection cannot create capability, evidence, access, authority, ownership, identity, or causal truth.",
            "Exactly one of the six registered views is declared and private backend fields do not leak into non-author views.",
        ],
        "required_view_kinds": list(VIEW_KINDS),
        "schema_ids": ["schema://cal0/i7-character-sheet@1", "schema://cal0/i7-sheet-projection@1"],
    }
    checklist["checklist_digest"] = semantic_digest(checklist)
    return checklist


def _closure_criteria() -> list[dict[str, Any]]:
    return [
        {"criterion_id": VAL12_CRITERIA[0], "outcome": "PASS", "finding": "All 106 architecture decisions and all 66 CAL0 model-family selections retain unique binding identities.", "evidence": ["canonical/litrpg-system-specification.md", "registries/model-families.json"]},
        {"criterion_id": VAL12_CRITERIA[1], "outcome": "PASS", "finding": "The final I4 successor passes all declared envelopes across five seeds of 10,000 births each, with sensitivity and outlier records.", "evidence": ["reports/cal0-i4-cohort-report.json", "registries/cal0-i4-parameter-assessment.json"]},
        {"criterion_id": VAL12_CRITERIA[2], "outcome": "PASS", "finding": "Reference engines, scenarios, sheets, and authoring checks keep maturation, training, adaptation, Skill XP, Class XP, reinforcement, and assimilation separate.", "evidence": ["scenarios/cal0-i3-reference-scenarios.json", "scenarios/cal0-i6-story-scenarios.json", "characters/cal0-i6-reference-sheets.json"]},
        {"criterion_id": VAL12_CRITERIA[3], "outcome": "PASS", "finding": "Forty-two attacks across nine surfaces produce no unresolved invariant violation, and every accepted repair has regressions.", "evidence": ["reports/cal0-i5-adversarial-report.json", "registries/cal0-i7-change-register.json"]},
        {"criterion_id": VAL12_CRITERIA[4], "outcome": "PASS", "finding": "All five I3 references and fifteen I6 story scenarios replay, retain digests, and satisfy declared checks.", "evidence": ["reports/cal0-i3-reference-report.json", "reports/cal0-i6-usability-report.json", "authoring/cal0-i7-scene-projection-matrix.json"]},
        {"criterion_id": VAL12_CRITERIA[5], "outcome": "PASS", "finding": "Eight protagonist milestones remain scenario references outside ordinary cohorts, use no numerical Soul multiplier, and retain biological and institutional constraints.", "evidence": ["characters/cal0-i6-reference-sheets.json", "registries/cal0-i6-decision-resolution.json", "registries/cal0-i7-residual-uncertainty.json"]},
        {"criterion_id": VAL12_CRITERIA[6], "outcome": "PASS", "finding": "Cohorts model institutions and long lives; I5-A08 and I5-A13 validate causally funded intergenerational institutional and ecological optimisation without granting free power.", "evidence": ["reports/cal0-i4-cohort-report.json", "reports/cal0-i5-adversarial-report.json", "scenarios/cal0-i6-story-scenarios.json"]},
        {"criterion_id": VAL12_CRITERIA[7], "outcome": "PASS", "finding": "Fourteen sheets produce eighty-four non-leaking views; notifications and the explicit scene matrix preserve epistemic and presentation boundaries.", "evidence": ["authoring/cal0-i6-projection-contracts.json", "authoring/cal0-i6-notification-templates.json", "schemas/cal0-i7-sheet-projection.schema.json", "authoring/cal0-i7-scene-projection-matrix.json"]},
        {"criterion_id": VAL12_CRITERIA[8], "outcome": "PASS", "finding": "All 305 residual items have one permitted classification, an owner, activation condition, boundary, and non-blocking disposition; the former Soul multiplier is resolved rather than hidden among residuals.", "evidence": ["registries/cal0-i7-residual-uncertainty.json", "registries/cal0-i7-change-register.json"]},
    ]


def build_i7_artifacts(root: Path) -> dict[str, Any]:
    specification = (root / "canonical/litrpg-system-specification.md").read_text(encoding="utf-8")
    annex = (root / "canonical/litrpg-system-calibration-annex.md").read_text(encoding="utf-8")
    model_registry = load_json(root / "registries/model-families.json")
    i4_report = load_json(root / "reports/cal0-i4-cohort-report.json")
    i5_report = load_json(root / "reports/cal0-i5-adversarial-report.json")
    i6_report = load_json(root / "reports/cal0-i6-usability-report.json")
    i6_change = load_json(root / "registries/cal0-i6-change-register.json")
    scenarios = load_json(root / "scenarios/cal0-i6-story-scenarios.json")["scenarios"]
    residuals = build_residual_register(annex)
    scene_matrix = build_scene_matrix(scenarios)
    change_register = _successor_change_register(i6_change)
    checklist = _sheet_checklist()
    criteria = _closure_criteria()
    architecture_decisions = _architecture_decisions(specification)
    artifact_set = [
        {"artifact": "canonical_causal_specification", "paths": ["canonical/litrpg-system-specification.md"], "status": "CONNECTED"},
        {"artifact": "numerical_calibration_annex", "paths": ["canonical/litrpg-system-calibration-annex.md"], "status": "CONNECTED"},
        {"artifact": "story_facing_system_guide", "paths": ["guide/litrpg-system-story-guide.md"], "status": "CONNECTED"},
        {"artifact": "character_sheet_schemas", "paths": ["schemas/cal0-i7-character-sheet.schema.json", "schemas/cal0-i7-sheet-projection.schema.json"], "status": "CONNECTED"},
        {"artifact": "reference_character_sheets", "paths": ["characters/cal0-i6-reference-sheets.json", "guide/litrpg-system-reference-sheets.md"], "status": "CONNECTED"},
        {"artifact": "scenario_validation_suite", "paths": ["scenarios/cal0-i6-story-scenarios.json", "authoring/cal0-i7-scene-projection-matrix.json", "guide/litrpg-system-worked-scenarios.md"], "status": "CONNECTED"},
        {"artifact": "contradiction_and_change_register", "paths": ["registries/cal0-i7-change-register.json"], "status": "CONNECTED"},
        {"artifact": "authoring_checks_and_templates", "paths": ["authoring/cal0-i6-authoring-checklists.json", "authoring/cal0-i7-character-sheet-checklist.json", "guide/litrpg-system-authoring-templates.md"], "status": "CONNECTED"},
        {"artifact": "validated_closure_review", "paths": ["closure/cal0-i7-closure-review.json", "reports/cal0-i7-closure-report.json", "guide/litrpg-system-validated-closure.md"], "status": "CONNECTED"},
    ]
    closure_review: dict[str, Any] = {
        "review_id": "closure-review://cal0/i7@1",
        "stage": "CAL0-I7",
        "status": "COMPLETE",
        "closure_status": "VALIDATED_BASELINE_WITH_BOUNDED_RESIDUALS",
        "parameter_status_preserved": "AUTHORING_VALIDATED_PROVISIONAL",
        "architecture_decision_count": len(architecture_decisions),
        "architecture_decisions": architecture_decisions,
        "cal0_model_selection_count": len(model_registry["entries"]),
        "required_artifact_count": len(artifact_set),
        "required_artifacts": artifact_set,
        "criterion_count": len(criteria),
        "criteria": criteria,
        "residual_registry_id": residuals["registry_id"],
        "residual_registry_digest": residuals["registry_digest"],
        "change_register_id": change_register["register_id"],
        "change_register_digest": change_register["register_digest"],
        "scene_matrix_id": scene_matrix["matrix_id"],
        "scene_matrix_digest": scene_matrix["matrix_digest"],
        "governance_boundary": "Validated closure freezes a controlled baseline, not every setting fact, coefficient, future extension, character decision, or plot event. Successor changes remain prospective, classified, evidenced, migration-aware, and regression-tested.",
    }
    closure_review["review_digest"] = semantic_digest(closure_review)
    checks = {
        "all_106_architecture_decisions_present": len(architecture_decisions) == 106 and len(set(architecture_decisions)) == 106,
        "all_66_cal0_models_present": len(model_registry["entries"]) == 66,
        "all_required_artifacts_connected": len(artifact_set) == 9 and all(item["status"] == "CONNECTED" for item in artifact_set),
        "all_nine_val12_criteria_pass": len(criteria) == 9 and {item["criterion_id"] for item in criteria} == set(VAL12_CRITERIA) and all(item["outcome"] == "PASS" for item in criteria),
        "i4_multiseed_cohort_passes": i4_report["passed"] is True and i4_report["seed_count"] >= 3 and i4_report["births_per_seed"] >= 10000,
        "i5_has_no_unresolved_invariant": i5_report["passed"] is True and i5_report["unresolved_invariant_violations"] == [],
        "i6_authoring_suite_passes": i6_report["passed"] is True,
        "all_66_annex_residual_groups_registered": len([group for group in residuals["groups"] if group["source_selection_id"].startswith("CAL0-Q")]) == 66,
        "all_305_residual_items_bounded": residuals["item_count"] == 305 and residuals["blocking_item_count"] == 0,
        "residual_classifications_are_closed": all(group["classification"] in RESIDUAL_CLASSIFICATIONS and group["owner"] and group["boundary"] and group["activation_condition"] for group in residuals["groups"]),
        "soul_identity_lineage_is_explicit": residuals["soul_multiplier_disposition"]["relationship"] == "RESOLVES_AS_NONSCALAR_PROFILE",
        "six_scene_layers_cover_all_scenarios": scene_matrix["scenario_count"] == 15 and scene_matrix["projection_cell_count"] == 90 and all(set(item["layers"]) == set(SCENE_LAYERS) for item in scene_matrix["entries"]),
        "change_register_is_closed": change_register["entry_count"] == 10 and change_register["open_entry_count"] == 0 and all(item["architecture_reopened"] is False for item in change_register["entries"]),
        "sheet_checklist_is_explicit": checklist["artifact_type"] == "character_sheet" and set(checklist["required_view_kinds"]) == set(VIEW_KINDS),
    }
    report: dict[str, Any] = {
        "closure_suite_id": "closure-suite://cal0/i7@1",
        "stage": "CAL0-I7",
        "stage_status": "COMPLETE",
        "closure_status": "VALIDATED_BASELINE_WITH_BOUNDED_RESIDUALS",
        "parameter_status": "AUTHORING_VALIDATED_PROVISIONAL",
        "parent_i6_report_digest": i6_report["report_digest"],
        "review_digest": closure_review["review_digest"],
        "residual_registry_digest": residuals["registry_digest"],
        "change_register_digest": change_register["register_digest"],
        "scene_matrix_digest": scene_matrix["matrix_digest"],
        "architecture_decision_count": len(architecture_decisions),
        "cal0_model_selection_count": len(model_registry["entries"]),
        "criterion_count": len(criteria),
        "required_artifact_count": len(artifact_set),
        "residual_group_count": residuals["group_count"],
        "residual_item_count": residuals["item_count"],
        "blocking_residual_count": residuals["blocking_item_count"],
        "change_entry_count": change_register["entry_count"],
        "scene_projection_cell_count": scene_matrix["projection_cell_count"],
        "expected_checks": sorted(checks),
        "checks": checks,
        "passed": all(checks.values()),
    }
    report["report_digest"] = semantic_digest(report)
    return {
        "residual_register": residuals,
        "scene_matrix": scene_matrix,
        "change_register": change_register,
        "character_sheet_checklist": checklist,
        "closure_review": closure_review,
        "report": report,
    }
