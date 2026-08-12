"""Mechanically rebuild the content-pinned CAL0-I7 bundle manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "manifests/cal0-i7.bundle.json"


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def role(relative: str) -> str:
    if relative == "README.md":
        return "documentation"
    if relative.startswith("schemas/"):
        return "schema"
    if relative.startswith("registries/"):
        return "registry"
    if relative.startswith("fixtures/"):
        return "fixture"
    if relative.startswith("scenarios/"):
        return "fixture"
    if relative.startswith("reports/"):
        return "fixture"
    if relative.startswith("closure/"):
        return "fixture"
    if relative.startswith("canonical/") or relative.startswith("guide/"):
        return "documentation"
    if relative.startswith("tests/"):
        return "test"
    if relative.startswith("src/cal0/"):
        return "validator" if relative.endswith(("validator.py", "canonical.py", "cli.py")) else "engine"
    return "bootstrap"


def main() -> None:
    paths = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path == TARGET:
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative.endswith((".pyc", ".zip")):
            continue
        paths.append(relative)
    artifacts = [{"path": item, "role": role(item), "sha256": digest(ROOT / item)} for item in sorted(paths)]
    report = json.loads((ROOT / "reports/cal0-i4-cohort-report.json").read_text(encoding="utf-8"))
    adversarial = json.loads((ROOT / "reports/cal0-i5-adversarial-report.json").read_text(encoding="utf-8"))
    authoring = json.loads((ROOT / "reports/cal0-i6-usability-report.json").read_text(encoding="utf-8"))
    closure = json.loads((ROOT / "reports/cal0-i7-closure-report.json").read_text(encoding="utf-8"))
    manifest = {
        "bundle_id": "bundle://cal0/i7@0.7.0",
        "package_version": "0.7.0",
        "stage": "CAL0-I7",
        "stage_status": "COMPLETE",
        "parameter_status": "AUTHORING_VALIDATED_PROVISIONAL",
        "closure_status": "VALIDATED_BASELINE_WITH_BOUNDED_RESIDUALS",
        "canonical_specification": "0.89",
        "calibration_annex": "2.9",
        "numerical_environment": {
            "language": "Python",
            "minimum_version": "3.11",
            "decimal_policy": "exact decimal strings until explicitly parsed",
            "float_policy": "forbidden in canonical records",
            "canonical_json": "UTF-8, sorted keys, compact separators, no NaN/Infinity"
        },
        "fixture_contract": {
            "suite_id": "fixture-suite://cal0/i2-reference@1",
            "case_count": 66,
            "seed_set": [17, 83],
            "traversal_set": ["forward", "reverse"],
            "synthetic_only": True
        },
        "reference_contract": {
            "parameter_set_id": "parameter-set://cal0/i3-reference@1",
            "parameter_set_status": "PROVISIONAL",
            "scenario_suite_id": "scenario-suite://cal0/i3-reference@1",
            "character_count": 4,
            "scenario_count": 5,
            "canonicality": "REFERENCE_ONLY_NOT_STORY_CANON",
            "cohort_claims_permitted": False
        },
        "cohort_contract": {
            "plan_id": "cohort-plan://cal0/i4-human-reference@1",
            "suite_id": "cohort-suite://cal0/i4-reference@1",
            "successor_parameter_set_id": "parameter-set://cal0/i4-reference@1",
            "births_per_seed": report["births_per_seed"],
            "seed_count": report["seed_count"],
            "iteration_count": len(report["calibration_iterations"]),
            "comparison_ensemble_count": len(report["comparison_ensembles"]),
            "report_digest": report["report_digest"],
            "canonicality": report["canonicality"]
        },
        "adversarial_contract": {
            "suite_id": adversarial["adversarial_suite_id"],
            "attack_count": adversarial["attack_count"],
            "execution_count": adversarial["execution_count"],
            "surface_count": len(adversarial["surface_counts"]),
            "repair_count": adversarial["repair_count"],
            "unresolved_invariant_violation_count": len(adversarial["unresolved_invariant_violations"]),
            "report_digest": adversarial["report_digest"],
            "canonicality": adversarial["canonicality"]
        },
        "authoring_contract": {
            "suite_id": authoring["authoring_suite_id"],
            "sheet_count": authoring["sheet_count"],
            "projection_count": authoring["projection_count"],
            "scenario_count": authoring["scenario_count"],
            "authoring_template_count": authoring["authoring_template_count"],
            "notification_template_count": authoring["notification_template_count"],
            "change_entry_count": authoring["change_entry_count"],
            "active_residual_count": authoring["active_residual_count"],
            "report_digest": authoring["report_digest"],
            "canonicality": authoring["canonicality"]
        },
        "closure_contract": {
            "suite_id": closure["closure_suite_id"],
            "architecture_decision_count": closure["architecture_decision_count"],
            "cal0_model_selection_count": closure["cal0_model_selection_count"],
            "criterion_count": closure["criterion_count"],
            "required_artifact_count": closure["required_artifact_count"],
            "residual_group_count": closure["residual_group_count"],
            "residual_item_count": closure["residual_item_count"],
            "blocking_residual_count": closure["blocking_residual_count"],
            "change_entry_count": closure["change_entry_count"],
            "scene_projection_cell_count": closure["scene_projection_cell_count"],
            "report_digest": closure["report_digest"],
            "closure_status": closure["closure_status"]
        },
        "artifacts": artifacts,
    }
    TARGET.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
