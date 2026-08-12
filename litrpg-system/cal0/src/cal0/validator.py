"""Deterministic CAL0-I6 bundle, authoring, adversarial, and cohort validator."""

from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .authoring import AUTHORING_TYPES, CHANGE_CLASSIFICATIONS, COMPARISON_ROLES, PROTAGONIST_MILESTONES, REQUIRED_SCENARIO_FAMILIES, VIEW_KINDS
from .canonical import CanonicalisationError, canonical_bytes, file_digest, semantic_digest
from .closure import RESIDUAL_CLASSIFICATIONS, SCENE_LAYERS, VAL12_CRITERIA
from .cohort_runner import validate_cohort_plan
from .parameter_runtime import validate_parameter_registry
from .scenario_runner import validate_reference_scenarios


DECISION_RE = re.compile(r"^CAL0-Q([1-9]|[1-5][0-9]|6[0-6])([ABC])$")
SCHEMA_RE = re.compile(r"^schema://cal0/[a-z0-9-]+@[123456]$")
PRIMITIVE_RE = re.compile(r"^primitive://cal0/[a-z0-9-]+@1$")
SHA_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

REQUIRED_PRIMITIVES = {
    "bounded-integer",
    "enum",
    "evidence-ref",
    "exact-decimal",
    "executable-ir",
    "explicit-absence",
    "explicit-default",
    "identifier",
    "map",
    "sequence",
    "set",
    "tagged-union",
    "unit",
    "witness-ref",
}

REQUIRED_PARAMETER_RECORDS = {
    "constraint_definition",
    "distribution_definition",
    "function_definition",
    "observable_definition",
    "parameter_definition",
    "parameter_set",
    "run_manifest",
    "value_binding",
}

REQUIRED_SCHEMA_NAMES = {
    "i3-parameter-registry",
    "i3-reference-scenarios",
    "i4-cohort-plan",
    "i4-parameter-assessment",
    "canonical-primitive",
    "model-family",
    "parameter-record-type",
    "registry-envelope",
    "unresolved-value",
    "version-manifest",
    "i7-character-sheet",
    "i7-sheet-projection",
}

I5_SURFACES = {
    "individual", "institutional", "economic", "ecological", "informational",
    "magical", "training", "identity", "replay",
}


@dataclass(frozen=True, order=True)
class Issue:
    code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message}


def _issue(code: str, path: str, message: str) -> Issue:
    return Issue(code=code, path=path, message=message)


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle, parse_float=lambda value: (_ for _ in ()).throw(
            ValueError(f"binary/JSON floating-point token forbidden: {value}")
        ))


def _validate_unresolved(value: Any, path: str) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(value, dict):
        return [_issue("UNRESOLVED_TYPE", path, "unresolved marker must be an object")]
    if value.get("state") != "UNRESOLVED":
        issues.append(_issue("UNRESOLVED_STATE", f"{path}.state", "state must be UNRESOLVED"))
    if "value" in value:
        issues.append(_issue("VALUE_STATE_CONFLICT", f"{path}.value", "UNRESOLVED marker cannot contain value"))
    for field in ("reason_code", "required_stage", "owner", "provenance"):
        if field not in value:
            issues.append(_issue("UNRESOLVED_FIELD_MISSING", f"{path}.{field}", "required field missing"))
    if value.get("required_stage") not in {"CAL0-I2", "CAL0-I3", "CAL0-I4", "CAL0-I5", "CAL0-I6", "CAL0-I7"}:
        issues.append(_issue("UNRESOLVED_STAGE", f"{path}.required_stage", "unknown resolution stage"))
    if not isinstance(value.get("provenance"), list) or not value.get("provenance"):
        issues.append(_issue("UNRESOLVED_PROVENANCE", f"{path}.provenance", "at least one provenance reference is required"))
    return issues


def _validate_schemas(doc: Any) -> tuple[list[Issue], set[str]]:
    issues: list[Issue] = []
    entries = doc.get("entries", []) if isinstance(doc, dict) else []
    ids: set[str] = set()
    names: set[str] = set()
    for index, entry in enumerate(entries):
        path = f"schema_registry.entries[{index}]"
        schema_id = entry.get("schema_id") if isinstance(entry, dict) else None
        name = entry.get("name") if isinstance(entry, dict) else None
        if not isinstance(schema_id, str) or not SCHEMA_RE.fullmatch(schema_id):
            issues.append(_issue("SCHEMA_ID_INVALID", f"{path}.schema_id", "invalid schema identity"))
        elif schema_id in ids:
            issues.append(_issue("SCHEMA_ID_DUPLICATE", f"{path}.schema_id", "duplicate schema identity"))
        else:
            ids.add(schema_id)
        if isinstance(name, str):
            names.add(name)
        source = entry.get("source") if isinstance(entry, dict) else None
        if not isinstance(source, str) or not source.startswith("schemas/"):
            issues.append(_issue("SCHEMA_SOURCE_INVALID", f"{path}.source", "schema source must be package-relative"))
    missing = sorted(REQUIRED_SCHEMA_NAMES - names)
    if missing:
        issues.append(_issue("SCHEMA_REGISTRY_INCOMPLETE", "schema_registry.entries", f"missing schemas: {', '.join(missing)}"))
    return issues, ids


def _validate_schema_sources(docs: dict[str, Any], registry: Any) -> list[Issue]:
    issues: list[Issue] = []
    seen_ids: set[str] = set()
    for index, entry in enumerate(registry.get("entries", [])):
        source = entry.get("source")
        expected_id = entry.get("schema_id")
        path = f"schema_registry.entries[{index}]"
        schema = docs.get(source)
        if schema is None:
            issues.append(_issue("SCHEMA_SOURCE_MISSING", f"{path}.source", "registered schema was not loaded"))
            continue
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            issues.append(_issue("SCHEMA_DIALECT_INVALID", source, "schema must declare JSON Schema 2020-12"))
        actual_id = schema.get("$id")
        if actual_id != expected_id:
            issues.append(_issue("SCHEMA_SOURCE_ID_MISMATCH", source, "schema $id does not match registry identity"))
        if isinstance(actual_id, str) and actual_id in seen_ids:
            issues.append(_issue("SCHEMA_SOURCE_ID_DUPLICATE", source, "schema $id is duplicated"))
        elif isinstance(actual_id, str):
            seen_ids.add(actual_id)
        if schema.get("type") != "object":
            issues.append(_issue("SCHEMA_ROOT_TYPE_INVALID", source, "I1 registry schemas must have object roots"))
    return issues


def _validate_primitives(doc: Any, schema_ids: set[str]) -> list[Issue]:
    issues: list[Issue] = []
    entries = doc.get("entries", []) if isinstance(doc, dict) else []
    names: set[str] = set()
    ids: set[str] = set()
    for index, entry in enumerate(entries):
        path = f"canonical_primitives.entries[{index}]"
        primitive_id = entry.get("primitive_id") if isinstance(entry, dict) else None
        name = entry.get("name") if isinstance(entry, dict) else None
        if not isinstance(primitive_id, str) or not PRIMITIVE_RE.fullmatch(primitive_id):
            issues.append(_issue("PRIMITIVE_ID_INVALID", f"{path}.primitive_id", "invalid primitive identity"))
        elif primitive_id in ids:
            issues.append(_issue("PRIMITIVE_ID_DUPLICATE", f"{path}.primitive_id", "duplicate primitive identity"))
        else:
            ids.add(primitive_id)
        if isinstance(name, str):
            names.add(name)
        if entry.get("schema_id") not in schema_ids:
            issues.append(_issue("UNKNOWN_SCHEMA", f"{path}.schema_id", "primitive references unknown schema"))
    missing = sorted(REQUIRED_PRIMITIVES - names)
    if missing:
        issues.append(_issue("PRIMITIVE_REGISTRY_INCOMPLETE", "canonical_primitives.entries", f"missing primitives: {', '.join(missing)}"))
    return issues


def _validate_models(doc: Any, schema_ids: set[str]) -> list[Issue]:
    issues: list[Issue] = []
    entries = doc.get("entries", []) if isinstance(doc, dict) else []
    seen: dict[int, str] = {}
    identities: set[str] = set()
    for index, entry in enumerate(entries):
        path = f"model_families.entries[{index}]"
        decision_id = entry.get("decision_id") if isinstance(entry, dict) else None
        selection_id = entry.get("selection_id") if isinstance(entry, dict) else None
        match = DECISION_RE.fullmatch(selection_id or "")
        if not match:
            issues.append(_issue("MODEL_SELECTION_ID_INVALID", f"{path}.selection_id", "invalid CAL0 selection identity"))
            continue
        number = int(match.group(1))
        if decision_id != f"CAL0-Q{number}":
            issues.append(_issue("MODEL_DECISION_MISMATCH", f"{path}.decision_id", "decision and selection identities disagree"))
        if number in seen:
            issues.append(_issue("MODEL_DECISION_DUPLICATE", path, f"Q{number} also declared by {seen[number]}"))
        else:
            seen[number] = selection_id
        model_id = entry.get("model_id")
        if not isinstance(model_id, str) or model_id in identities:
            issues.append(_issue("MODEL_ID_DUPLICATE_OR_INVALID", f"{path}.model_id", "model identity must be unique"))
        else:
            identities.add(model_id)
        if entry.get("schema_id") not in schema_ids:
            issues.append(_issue("UNKNOWN_SCHEMA", f"{path}.schema_id", "model references unknown schema"))
        if entry.get("lifecycle") != "ACTIVE":
            issues.append(_issue("MODEL_NOT_ACTIVE", f"{path}.lifecycle", "selected CAL0 model must be ACTIVE"))
        issues.extend(_validate_unresolved(entry.get("parameters"), f"{path}.parameters"))
    missing = [number for number in range(1, 67) if number not in seen]
    if missing or len(entries) != 66:
        issues.append(_issue("MODEL_SEQUENCE_INCOMPLETE", "model_families.entries", f"expected Q1-Q66 exactly once; missing={missing}; count={len(entries)}"))
    return issues


def _validate_parameter_records(doc: Any, schema_ids: set[str]) -> list[Issue]:
    issues: list[Issue] = []
    entries = doc.get("entries", []) if isinstance(doc, dict) else []
    names: set[str] = set()
    for index, entry in enumerate(entries):
        path = f"parameter_record_types.entries[{index}]"
        name = entry.get("record_type") if isinstance(entry, dict) else None
        if isinstance(name, str):
            if name in names:
                issues.append(_issue("PARAMETER_RECORD_DUPLICATE", f"{path}.record_type", "duplicate record type"))
            names.add(name)
        if entry.get("schema_id") not in schema_ids:
            issues.append(_issue("UNKNOWN_SCHEMA", f"{path}.schema_id", "record type references unknown schema"))
    missing = sorted(REQUIRED_PARAMETER_RECORDS - names)
    extra = sorted(names - REQUIRED_PARAMETER_RECORDS)
    if missing or extra or len(entries) != 8:
        issues.append(_issue("PARAMETER_REGISTRY_INCOMPLETE", "parameter_record_types.entries", f"missing={missing}; extra={extra}; count={len(entries)}"))
    issues.extend(_validate_unresolved(doc.get("default_unresolved"), "parameter_record_types.default_unresolved"))
    return issues


def _validate_manifest(root: Path, manifest: Any, loaded_names: set[str], verify_digests: bool) -> list[Issue]:
    issues: list[Issue] = []
    if manifest.get("bundle_id") != "bundle://cal0/i7@0.7.0":
        issues.append(_issue("BUNDLE_ID_INVALID", "manifest.bundle_id", "unexpected I7 bundle identity"))
    if manifest.get("parameter_status") != "AUTHORING_VALIDATED_PROVISIONAL":
        issues.append(_issue("PARAMETER_STATUS_INVALID", "manifest.parameter_status", "I7 preserves the authoring-validated provisional parameter status"))
    if manifest.get("stage_status") != "COMPLETE":
        issues.append(_issue("STAGE_STATUS_INVALID", "manifest.stage_status", "I7 bundle is not complete"))
    if manifest.get("closure_status") != "VALIDATED_BASELINE_WITH_BOUNDED_RESIDUALS":
        issues.append(_issue("I7_CLOSURE_CONTRACT", "manifest.closure_status", "unexpected validated-closure status"))
    reference = manifest.get("reference_contract", {})
    if reference.get("parameter_set_id") != "parameter-set://cal0/i3-reference@1" or reference.get("parameter_set_status") != "PROVISIONAL":
        issues.append(_issue("I3_REFERENCE_CONTRACT", "manifest.reference_contract", "manifest must pin the provisional I3 reference set"))
    if reference.get("canonicality") != "REFERENCE_ONLY_NOT_STORY_CANON" or reference.get("cohort_claims_permitted") is not False:
        issues.append(_issue("I3_SCOPE_OVERCLAIM", "manifest.reference_contract", "I3 reference outputs cannot claim story canon or cohorts"))
    cohort = manifest.get("cohort_contract", {})
    if cohort.get("plan_id") != "cohort-plan://cal0/i4-human-reference@1" or cohort.get("suite_id") != "cohort-suite://cal0/i4-reference@1":
        issues.append(_issue("I4_COHORT_CONTRACT", "manifest.cohort_contract", "manifest must pin the I4 cohort plan and suite"))
    if cohort.get("births_per_seed", 0) < 10000 or cohort.get("seed_count", 0) < 3:
        issues.append(_issue("I4_COHORT_CONTRACT", "manifest.cohort_contract", "manifest cohort size or seed count is incomplete"))
    adversarial = manifest.get("adversarial_contract", {})
    if adversarial.get("suite_id") != "adversarial-suite://cal0/i5-reference@1":
        issues.append(_issue("I5_ADVERSARIAL_CONTRACT", "manifest.adversarial_contract", "manifest must pin the I5 adversarial suite"))
    if adversarial.get("attack_count", 0) < 36 or adversarial.get("repair_count", 0) < 1:
        issues.append(_issue("I5_ADVERSARIAL_CONTRACT", "manifest.adversarial_contract", "manifest attack or repair coverage is incomplete"))
    if adversarial.get("unresolved_invariant_violation_count") != 0:
        issues.append(_issue("I5_ADVERSARIAL_CONTRACT", "manifest.adversarial_contract", "manifest cannot close I5 with an unresolved invariant violation"))
    authoring = manifest.get("authoring_contract", {})
    if authoring.get("suite_id") != "authoring-suite://cal0/i6-reference@1":
        issues.append(_issue("I6_AUTHORING_CONTRACT", "manifest.authoring_contract", "manifest must pin the I6 authoring suite"))
    expected = {"sheet_count": 14, "projection_count": 84, "scenario_count": 15, "authoring_template_count": 10, "notification_template_count": 4, "change_entry_count": 6, "active_residual_count": 5}
    if any(authoring.get(key) != value for key, value in expected.items()):
        issues.append(_issue("I6_AUTHORING_CONTRACT", "manifest.authoring_contract", "manifest authoring coverage is incomplete"))
    closure = manifest.get("closure_contract", {})
    closure_expected = {
        "architecture_decision_count": 106,
        "cal0_model_selection_count": 66,
        "criterion_count": 9,
        "required_artifact_count": 9,
        "residual_group_count": 71,
        "residual_item_count": 305,
        "blocking_residual_count": 0,
        "change_entry_count": 10,
        "scene_projection_cell_count": 90,
    }
    if closure.get("suite_id") != "closure-suite://cal0/i7@1" or any(closure.get(key) != value for key, value in closure_expected.items()):
        issues.append(_issue("I7_CLOSURE_CONTRACT", "manifest.closure_contract", "manifest validated-closure coverage is incomplete"))
    artifacts = manifest.get("artifacts", [])
    paths: set[str] = set()
    for index, artifact in enumerate(artifacts if isinstance(artifacts, list) else []):
        path = f"manifest.artifacts[{index}]"
        relative = artifact.get("path") if isinstance(artifact, dict) else None
        digest = artifact.get("sha256") if isinstance(artifact, dict) else None
        if not isinstance(relative, str) or relative.startswith("/") or ".." in Path(relative).parts:
            issues.append(_issue("ARTIFACT_PATH_INVALID", f"{path}.path", "artifact path must be safe and relative"))
            continue
        if relative in paths:
            issues.append(_issue("ARTIFACT_PATH_DUPLICATE", f"{path}.path", "artifact path duplicated"))
        paths.add(relative)
        absolute = root / relative
        if not absolute.is_file():
            issues.append(_issue("ARTIFACT_MISSING", relative, "manifest artifact does not exist"))
            continue
        if not isinstance(digest, str) or not SHA_RE.fullmatch(digest):
            issues.append(_issue("ARTIFACT_DIGEST_INVALID", f"{path}.sha256", "digest must be sha256:<64 lowercase hex>"))
        elif verify_digests and file_digest(absolute) != digest:
            issues.append(_issue("ARTIFACT_DIGEST_MISMATCH", relative, "content does not match pinned digest"))
    for required in loaded_names:
        if required not in paths:
            issues.append(_issue("MANIFEST_INCOMPLETE", "manifest.artifacts", f"required executable input not pinned: {required}"))
    return issues


def _validate_i4_outputs(docs: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    report = docs["reports/cal0-i4-cohort-report.json"]
    assessment = docs["registries/cal0-i4-parameter-assessment.json"]
    if report.get("cohort_suite_id") != "cohort-suite://cal0/i4-reference@1" or report.get("parameter_status") != "COHORT_CALIBRATED_PROVISIONAL":
        issues.append(_issue("I4_REPORT_ID", "i4_report", "unexpected cohort report identity or status"))
    if report.get("passed") is not True or not all(report.get("checks", {}).values()):
        issues.append(_issue("I4_REPORT_FAILED", "i4_report.checks", "cohort report contains a failed exit check"))
    digest = report.get("report_digest")
    payload = dict(report)
    payload.pop("report_digest", None)
    if digest != semantic_digest(payload):
        issues.append(_issue("I4_REPORT_DIGEST", "i4_report.report_digest", "cohort report digest does not match its content"))
    if assessment.get("parameter_set_id") != "parameter-set://cal0/i4-reference@1" or assessment.get("status") != "COHORT_CALIBRATED_PROVISIONAL":
        issues.append(_issue("I4_ASSESSMENT_ID", "i4_assessment", "unexpected I4 assessment identity or status"))
    if assessment.get("report_digest") != digest:
        issues.append(_issue("I4_ASSESSMENT_REPORT", "i4_assessment.report_digest", "assessment does not pin the cohort report"))
    provisional = assessment.get("provisional_parameter_assessments", [])
    unresolved = assessment.get("unresolved_parameter_assessments", [])
    if len(provisional) != 39 or len({entry.get("parameter_id") for entry in provisional if isinstance(entry, dict)}) != 39:
        issues.append(_issue("I4_PROVISIONAL_COVERAGE", "i4_assessment.provisional_parameter_assessments", "all 39 provisional coefficients require unique classifications"))
    if len(unresolved) != 6 or any(entry.get("remains_unresolved") is not True for entry in unresolved if isinstance(entry, dict)):
        issues.append(_issue("I4_UNRESOLVED_COVERAGE", "i4_assessment.unresolved_parameter_assessments", "all six parent unknowns must remain explicit and classified"))
    return issues


def _validate_i5_outputs(docs: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    report = docs["reports/cal0-i5-adversarial-report.json"]
    parent = docs["reports/cal0-i4-cohort-report.json"]
    if report.get("adversarial_suite_id") != "adversarial-suite://cal0/i5-reference@1" or report.get("parameter_status") != "ADVERSARIALLY_VALIDATED_PROVISIONAL":
        issues.append(_issue("I5_REPORT_ID", "i5_report", "unexpected adversarial report identity or status"))
    if report.get("passed") is not True or not all(report.get("checks", {}).values()):
        issues.append(_issue("I5_REPORT_FAILED", "i5_report.checks", "adversarial report contains a failed exit check"))
    digest = report.get("report_digest")
    payload = dict(report)
    payload.pop("report_digest", None)
    if digest != semantic_digest(payload):
        issues.append(_issue("I5_REPORT_DIGEST", "i5_report.report_digest", "adversarial report digest does not match its content"))
    if report.get("parent_cohort_report_digest") != parent.get("report_digest"):
        issues.append(_issue("I5_PARENT_REPORT", "i5_report.parent_cohort_report_digest", "I5 report does not pin the active I4 cohort report"))
    surface_counts = report.get("surface_counts", {})
    if set(surface_counts) != I5_SURFACES or any(not isinstance(value, int) or value < 1 for value in surface_counts.values()):
        issues.append(_issue("I5_SURFACE_COVERAGE", "i5_report.surface_counts", "all nine adversarial surfaces require at least one case"))
    results = report.get("attack_results", [])
    if report.get("attack_count") != len(results) or len(results) < 36 or report.get("execution_count") != len(results) * 4:
        issues.append(_issue("I5_ATTACK_COVERAGE", "i5_report.attack_results", "attack count or four-replay execution count is incomplete"))
    if any(item.get("passed") is not True for item in results if isinstance(item, dict)):
        issues.append(_issue("I5_ATTACK_FAILED", "i5_report.attack_results", "one or more adversarial cases failed"))
    if report.get("unresolved_invariant_violations") != []:
        issues.append(_issue("I5_UNRESOLVED_INVARIANT", "i5_report.unresolved_invariant_violations", "I5 cannot close with unresolved invariant violations"))
    repairs = report.get("repairs", [])
    if not repairs or any(item.get("passed") is not True or item.get("regression_count", 0) < 1 for item in repairs if isinstance(item, dict)):
        issues.append(_issue("I5_REPAIR_COVERAGE", "i5_report.repairs", "every accepted repair requires passing regression coverage"))
    return issues


def _validate_i6_outputs(root: Path, docs: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    report = docs["reports/cal0-i6-usability-report.json"]
    parent = docs["reports/cal0-i5-adversarial-report.json"]
    sheets = docs["characters/cal0-i6-reference-sheets.json"].get("sheets", [])
    projections = docs["authoring/cal0-i6-projection-contracts.json"]
    scenarios = docs["scenarios/cal0-i6-story-scenarios.json"].get("scenarios", [])
    checklists = docs["authoring/cal0-i6-authoring-checklists.json"].get("templates", [])
    notifications = docs["authoring/cal0-i6-notification-templates.json"].get("templates", [])
    resolution = docs["registries/cal0-i6-decision-resolution.json"]
    change_register = docs["registries/cal0-i6-change-register.json"]
    if report.get("authoring_suite_id") != "authoring-suite://cal0/i6-reference@1" or report.get("parameter_status") != "AUTHORING_VALIDATED_PROVISIONAL":
        issues.append(_issue("I6_REPORT_ID", "i6_report", "unexpected I6 authoring report identity or status"))
    if report.get("passed") is not True or not all(report.get("checks", {}).values()):
        issues.append(_issue("I6_REPORT_FAILED", "i6_report.checks", "authoring report contains a failed exit check"))
    payload = dict(report)
    digest = payload.pop("report_digest", None)
    if digest != semantic_digest(payload):
        issues.append(_issue("I6_REPORT_DIGEST", "i6_report.report_digest", "authoring report digest does not match its content"))
    if report.get("parent_i5_report_digest") != parent.get("report_digest"):
        issues.append(_issue("I6_PARENT_REPORT", "i6_report.parent_i5_report_digest", "I6 report does not pin the active I5 report"))
    if len(sheets) != 14 or len({item.get("sheet_id") for item in sheets if isinstance(item, dict)}) != 14:
        issues.append(_issue("I6_SHEET_COVERAGE", "i6_sheets.sheets", "fourteen unique reference sheets are required"))
    milestones = {item.get("identity", {}).get("milestone") for item in sheets if item.get("identity", {}).get("role") == "protagonist"}
    roles = {item.get("identity", {}).get("role") for item in sheets}
    if milestones != set(PROTAGONIST_MILESTONES) or not set(COMPARISON_ROLES).issubset(roles):
        issues.append(_issue("I6_SHEET_COVERAGE", "i6_sheets.sheets", "protagonist milestones or comparison roles are incomplete"))
    sheet_ids = {item.get("sheet_id") for item in sheets}
    views = projections.get("views", [])
    view_kinds = set(projections.get("view_kinds", []))
    pairs = {(item.get("sheet_id"), item.get("view_kind")) for item in views if isinstance(item, dict)}
    expected_pairs = {(sheet_id, kind) for sheet_id in sheet_ids for kind in VIEW_KINDS}
    if view_kinds != set(VIEW_KINDS) or pairs != expected_pairs or len(views) != 84:
        issues.append(_issue("I6_PROJECTION_COVERAGE", "i6_projections.views", "every sheet requires all six projections exactly once"))
    forbidden = {"secrets", "backend_uncertainty", "unresolved_inputs", "causal_ledgers"}
    if any(forbidden.intersection(item) for item in views if item.get("view_kind") not in {"private_backend", "author_facing"}):
        issues.append(_issue("I6_PROJECTION_LEAK", "i6_projections.views", "non-author projection exposes private backend fields"))
    families = {item.get("family") for item in scenarios}
    if len(scenarios) != 15 or families != set(REQUIRED_SCENARIO_FAMILIES):
        issues.append(_issue("I6_SCENARIO_COVERAGE", "i6_scenarios.scenarios", "all fifteen required scenario families are required"))
    required_scenario = {"inputs", "actor_knowledge", "causal_sequence", "state_changes", "interface_outputs", "reader_facing_projection", "expected_checks"}
    if any(not required_scenario.issubset(item) for item in scenarios if isinstance(item, dict)):
        issues.append(_issue("I6_SCENARIO_SHAPE", "i6_scenarios.scenarios", "scenario lacks a required story-facing field"))
    if {item.get("artifact_type") for item in checklists} != set(AUTHORING_TYPES) or len(checklists) != 10:
        issues.append(_issue("I6_CHECKLIST_COVERAGE", "i6_checklists.templates", "all ten authoring template types are required"))
    if len(notifications) != 4 or any(not item.get("must_not_imply") for item in notifications if isinstance(item, dict)):
        issues.append(_issue("I6_NOTIFICATION_COVERAGE", "i6_notifications.templates", "four epistemically bounded notification templates are required"))
    resolutions = resolution.get("resolutions", [])
    if len(resolutions) != 1 or resolutions[0].get("active_resolution") != "NOT_APPLICABLE_NONSCALAR_PROFILE" or resolutions[0].get("coefficient_changed") is not False:
        issues.append(_issue("I6_SOUL_RESOLUTION", "i6_resolution.resolutions", "Soul multiplier must resolve as a non-scalar profile without a coefficient"))
    residuals = resolution.get("remaining_active_residuals", [])
    if len(residuals) != 5 or any(not item.get("classification") for item in residuals if isinstance(item, dict)):
        issues.append(_issue("I6_RESIDUAL_CLASSIFICATION", "i6_resolution.remaining_active_residuals", "five residuals require explicit classifications"))
    change_entries = change_register.get("entries", [])
    change_payload = dict(change_register)
    change_digest = change_payload.pop("register_digest", None)
    if (
        change_register.get("entry_count") != 6
        or change_register.get("open_entry_count") != 0
        or len(change_entries) != 6
        or any(item.get("classification") not in CHANGE_CLASSIFICATIONS for item in change_entries if isinstance(item, dict))
        or any(item.get("status", "").startswith("CLOSED_") is not True for item in change_entries if isinstance(item, dict))
        or change_digest != semantic_digest(change_payload)
    ):
        issues.append(_issue("I6_CHANGE_REGISTER", "i6_change_register", "change register must close and classify all five I5 repairs and the I6 decision"))
    guide = root / "guide/litrpg-system-story-guide.md"
    try:
        guide_text = guide.read_text(encoding="utf-8")
    except OSError:
        guide_text = ""
    required_headings = ("## Attributes", "## Skills", "## Classes", "## Training and learning", "## Magic", "## Combat", "## The protagonist", "## Scene-planning checklist")
    if not guide_text or any(heading not in guide_text for heading in required_headings):
        issues.append(_issue("I6_GUIDE_INCOMPLETE", "guide/litrpg-system-story-guide.md", "story guide lacks required ordinary scene-planning sections"))
    return issues


def _validate_i7_outputs(root: Path, docs: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    report = docs["reports/cal0-i7-closure-report.json"]
    parent = docs["reports/cal0-i6-usability-report.json"]
    review = docs["closure/cal0-i7-closure-review.json"]
    residuals = docs["registries/cal0-i7-residual-uncertainty.json"]
    scene_matrix = docs["authoring/cal0-i7-scene-projection-matrix.json"]
    change_register = docs["registries/cal0-i7-change-register.json"]
    parent_change = docs["registries/cal0-i6-change-register.json"]
    checklist = docs["authoring/cal0-i7-character-sheet-checklist.json"]
    sheet_schema = docs["schemas/cal0-i7-character-sheet.schema.json"]
    projection_schema = docs["schemas/cal0-i7-sheet-projection.schema.json"]

    if (
        report.get("closure_suite_id") != "closure-suite://cal0/i7@1"
        or report.get("stage") != "CAL0-I7"
        or report.get("stage_status") != "COMPLETE"
        or report.get("closure_status") != "VALIDATED_BASELINE_WITH_BOUNDED_RESIDUALS"
        or report.get("parameter_status") != "AUTHORING_VALIDATED_PROVISIONAL"
    ):
        issues.append(_issue("I7_REPORT_ID", "i7_report", "unexpected I7 closure report identity or status"))
    if report.get("passed") is not True or not all(report.get("checks", {}).values()):
        issues.append(_issue("I7_REPORT_FAILED", "i7_report.checks", "closure report contains a failed exit check"))
    report_payload = dict(report)
    report_digest = report_payload.pop("report_digest", None)
    if report_digest != semantic_digest(report_payload):
        issues.append(_issue("I7_REPORT_DIGEST", "i7_report.report_digest", "closure report digest does not match its content"))
    if report.get("parent_i6_report_digest") != parent.get("report_digest"):
        issues.append(_issue("I7_PARENT_REPORT", "i7_report.parent_i6_report_digest", "I7 report does not pin the active I6 report"))

    review_payload = dict(review)
    review_digest = review_payload.pop("review_digest", None)
    if review_digest != semantic_digest(review_payload) or report.get("review_digest") != review_digest:
        issues.append(_issue("I7_REVIEW_DIGEST", "i7_review.review_digest", "closure review digest or report pin is invalid"))
    criteria = review.get("criteria", [])
    if (
        review.get("criterion_count") != 9
        or len(criteria) != 9
        or {item.get("criterion_id") for item in criteria if isinstance(item, dict)} != set(VAL12_CRITERIA)
        or any(item.get("outcome") != "PASS" or not item.get("evidence") for item in criteria if isinstance(item, dict))
    ):
        issues.append(_issue("I7_CRITERION_COVERAGE", "i7_review.criteria", "all nine VAL1.2D criteria require passing evidence records"))
    artifacts = review.get("required_artifacts", [])
    if review.get("required_artifact_count") != 9 or len(artifacts) != 9 or any(item.get("status") != "CONNECTED" for item in artifacts if isinstance(item, dict)):
        issues.append(_issue("I7_ARTIFACT_SET", "i7_review.required_artifacts", "all nine closure artifact families must be connected"))
    elif any(not (root / relative).is_file() for item in artifacts for relative in item.get("paths", [])):
        issues.append(_issue("I7_ARTIFACT_SET", "i7_review.required_artifacts", "one or more connected artifact paths are missing"))

    residual_payload = dict(residuals)
    residual_digest = residual_payload.pop("registry_digest", None)
    if residual_digest != semantic_digest(residual_payload) or review.get("residual_registry_digest") != residual_digest or report.get("residual_registry_digest") != residual_digest:
        issues.append(_issue("I7_RESIDUAL_DIGEST", "i7_residuals.registry_digest", "residual registry digest or downstream pin is invalid"))
    groups = residuals.get("groups", [])
    q_groups = [item for item in groups if isinstance(item, dict) and str(item.get("source_selection_id", "")).startswith("CAL0-Q")]
    actual_item_count = sum(len(item.get("items", [])) for item in groups if isinstance(item, dict))
    if residuals.get("group_count") != 71 or residuals.get("item_count") != 305 or len(groups) != 71 or len(q_groups) != 66 or actual_item_count != 305:
        issues.append(_issue("I7_RESIDUAL_COVERAGE", "i7_residuals.groups", "all 66 CAL0 groups and five world residuals must expose 305 items"))
    invalid_residual = False
    for group in groups:
        if not isinstance(group, dict):
            invalid_residual = True
            continue
        if group.get("classification") not in RESIDUAL_CLASSIFICATIONS or not group.get("owner") or not group.get("boundary") or not group.get("activation_condition"):
            invalid_residual = True
        if group.get("closure_disposition") != "BOUNDED_NONBLOCKING":
            invalid_residual = True
        for item in group.get("items", []):
            if not isinstance(item, dict) or item.get("classification") not in RESIDUAL_CLASSIFICATIONS or not item.get("owner") or item.get("blocking") is not False:
                invalid_residual = True
    if residuals.get("blocking_group_count") != 0 or residuals.get("blocking_item_count") != 0 or invalid_residual:
        issues.append(_issue("I7_RESIDUAL_REGISTRY", "i7_residuals.groups", "every residual requires one permitted classification, owner, boundary, activation condition, and non-blocking disposition"))
    soul = residuals.get("soul_multiplier_disposition", {})
    if (
        soul.get("historical_parameter_id") != "parameter://cal0/unresolved/protagonist-long-term-soul-multiplier@1"
        or soul.get("i6_active_projection_id") != "parameter://cal0/protagonist/long-term-soul-multiplier@1"
        or soul.get("relationship") != "RESOLVES_AS_NONSCALAR_PROFILE"
        or soul.get("status") != "RESOLVED_NOT_A_RESIDUAL"
    ):
        issues.append(_issue("I7_SOUL_LINEAGE", "i7_residuals.soul_multiplier_disposition", "historical Soul unknown must explicitly resolve into the I6 non-scalar profile"))

    matrix_payload = dict(scene_matrix)
    matrix_digest = matrix_payload.pop("matrix_digest", None)
    if matrix_digest != semantic_digest(matrix_payload) or review.get("scene_matrix_digest") != matrix_digest or report.get("scene_matrix_digest") != matrix_digest:
        issues.append(_issue("I7_SCENE_DIGEST", "i7_scene_matrix.matrix_digest", "scene matrix digest or downstream pin is invalid"))
    scene_entries = scene_matrix.get("entries", [])
    if (
        scene_matrix.get("scenario_count") != 15
        or scene_matrix.get("layer_count") != 6
        or scene_matrix.get("projection_cell_count") != 90
        or len(scene_entries) != 15
        or set(scene_matrix.get("layer_order", [])) != set(SCENE_LAYERS)
        or any(set(item.get("layers", {})) != set(SCENE_LAYERS) for item in scene_entries if isinstance(item, dict))
    ):
        issues.append(_issue("I7_SCENE_MATRIX", "i7_scene_matrix.entries", "all fifteen scenarios require the six VAL1.2D scene-facing layers"))
    elif any((lambda payload, digest: digest != semantic_digest(payload))({key: value for key, value in item.items() if key != "entry_digest"}, item.get("entry_digest")) for item in scene_entries):
        issues.append(_issue("I7_SCENE_DIGEST", "i7_scene_matrix.entries", "one or more scene entry digests are invalid"))

    change_payload = dict(change_register)
    change_digest = change_payload.pop("register_digest", None)
    if change_digest != semantic_digest(change_payload) or review.get("change_register_digest") != change_digest or report.get("change_register_digest") != change_digest:
        issues.append(_issue("I7_CHANGE_DIGEST", "i7_change_register.register_digest", "change-register digest or downstream pin is invalid"))
    if (
        change_register.get("parent_register_id") != parent_change.get("register_id")
        or change_register.get("parent_register_digest") != parent_change.get("register_digest")
        or change_register.get("entry_count") != 10
        or len(change_register.get("entries", [])) != 10
        or change_register.get("open_entry_count") != 0
        or change_register.get("open_entries") != []
        or any(item.get("architecture_reopened") is not False for item in change_register.get("entries", []) if isinstance(item, dict))
    ):
        issues.append(_issue("I7_CHANGE_REGISTER", "i7_change_register", "I7 change register must preserve I6 and close exactly four non-architectural corrections"))

    checklist_payload = dict(checklist)
    checklist_digest = checklist_payload.pop("checklist_digest", None)
    if checklist_digest != semantic_digest(checklist_payload) or checklist.get("artifact_type") != "character_sheet" or set(checklist.get("required_view_kinds", [])) != set(VIEW_KINDS):
        issues.append(_issue("I7_SHEET_CHECKLIST", "i7_character_sheet_checklist", "explicit sheet checklist must cover all six view kinds and retain a valid digest"))
    expected_attributes = {"Might", "Finesse", "Alacrity", "Vitality", "Perception", "Cognition", "Focus", "Will", "Depth", "Coherence", "Resonance"}
    if sheet_schema.get("$id") != "schema://cal0/i7-character-sheet@1" or set(sheet_schema.get("properties", {}).get("attributes", {}).get("required", [])) != expected_attributes:
        issues.append(_issue("I7_SHEET_SCHEMA", "schemas/cal0-i7-character-sheet.schema.json", "character-sheet schema must require all eleven attributes"))
    if projection_schema.get("$id") != "schema://cal0/i7-sheet-projection@1" or set(projection_schema.get("properties", {}).get("view_kind", {}).get("enum", [])) != set(VIEW_KINDS):
        issues.append(_issue("I7_SHEET_SCHEMA", "schemas/cal0-i7-sheet-projection.schema.json", "projection schema must declare all six view kinds"))

    try:
        specification = (root / "canonical/litrpg-system-specification.md").read_text(encoding="utf-8")
        annex = (root / "canonical/litrpg-system-calibration-annex.md").read_text(encoding="utf-8")
        closure_guide = (root / "guide/litrpg-system-validated-closure.md").read_text(encoding="utf-8")
        residual_guide = (root / "guide/litrpg-system-residual-uncertainty-register.md").read_text(encoding="utf-8")
    except OSError:
        specification = annex = closure_guide = residual_guide = ""
    if "**Specification version:** 0.89" not in specification or "### CAL0-I7 validated-closure record" not in specification:
        issues.append(_issue("I7_CANONICAL_SNAPSHOT", "canonical/litrpg-system-specification.md", "canonical snapshot is not the closed 0.89 specification"))
    if "**Annex version:** 2.9" not in annex or "## CAL0-I7 — Validated-closure review" not in annex:
        issues.append(_issue("I7_CANONICAL_SNAPSHOT", "canonical/litrpg-system-calibration-annex.md", "annex snapshot is not the closed 2.9 annex"))
    if "## VAL1.2D evidence matrix" not in closure_guide or "## What closure does not freeze" not in closure_guide or "**Items:** 305" not in residual_guide:
        issues.append(_issue("I7_GUIDE_INCOMPLETE", "guide", "validated-closure or residual handbook is incomplete"))
    return issues


def validate_documents(root: Path, docs: dict[str, Any], verify_digests: bool = True) -> list[Issue]:
    issues: list[Issue] = []
    for name, doc in docs.items():
        try:
            canonical_bytes(doc)
        except CanonicalisationError as error:
            issues.append(_issue("CANONICALISATION_FAILED", name, str(error)))
    schema_issues, schema_ids = _validate_schemas(docs["registries/schema-registry.json"])
    issues.extend(schema_issues)
    issues.extend(_validate_schema_sources(docs, docs["registries/schema-registry.json"]))
    issues.extend(_validate_primitives(docs["registries/canonical-primitives.json"], schema_ids))
    issues.extend(_validate_models(docs["registries/model-families.json"], schema_ids))
    issues.extend(_validate_parameter_records(docs["registries/parameter-record-types.json"], schema_ids))
    for code, path, message in validate_parameter_registry(docs["registries/cal0-i3-parameters.json"]):
        issues.append(_issue(code, path, message))
    for code, path, message in validate_reference_scenarios(
        docs["scenarios/cal0-i3-reference-scenarios.json"],
        docs["registries/cal0-i3-parameters.json"],
    ):
        issues.append(_issue(code, path, message))
    for code, path, message in validate_cohort_plan(
        docs["scenarios/cal0-i4-cohort-plan.json"],
        docs["registries/cal0-i3-parameters.json"],
    ):
        issues.append(_issue(code, path, message))
    issues.extend(_validate_i4_outputs(docs))
    issues.extend(_validate_i5_outputs(docs))
    issues.extend(_validate_i6_outputs(root, docs))
    issues.extend(_validate_i7_outputs(root, docs))
    loaded_names = set(docs) - {"manifests/cal0-i7.bundle.json"}
    loaded_names.update({
        "canonical/litrpg-system-specification.md",
        "canonical/litrpg-system-calibration-annex.md",
        "guide/litrpg-system-story-guide.md",
        "guide/litrpg-system-reference-sheets.md",
        "guide/litrpg-system-worked-scenarios.md",
        "guide/litrpg-system-authoring-templates.md",
        "guide/litrpg-system-validated-closure.md",
        "guide/litrpg-system-residual-uncertainty-register.md",
    })
    issues.extend(_validate_manifest(root, docs["manifests/cal0-i7.bundle.json"], loaded_names, verify_digests))
    return sorted(set(issues))


def load_and_validate(root: Path, verify_digests: bool = True) -> tuple[dict[str, Any], list[Issue]]:
    manifest_path = root / "manifests/cal0-i7.bundle.json"
    try:
        manifest = _load_json(manifest_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return {}, [_issue("MANIFEST_LOAD_FAILED", str(manifest_path), str(error))]
    required = {
        "registries/schema-registry.json",
        "registries/canonical-primitives.json",
        "registries/cal0-i3-parameters.json",
        "registries/cal0-i4-parameter-assessment.json",
        "registries/model-families.json",
        "registries/parameter-record-types.json",
        "schemas/canonical-primitive.schema.json",
        "schemas/cal0-i3-parameter-registry.schema.json",
        "schemas/cal0-i3-reference-scenarios.schema.json",
        "schemas/cal0-i4-cohort-plan.schema.json",
        "schemas/cal0-i4-parameter-assessment.schema.json",
        "schemas/model-family.schema.json",
        "schemas/parameter-record-type.schema.json",
        "schemas/registry-envelope.schema.json",
        "schemas/unresolved-value.schema.json",
        "schemas/version-manifest.schema.json",
        "schemas/cal0-i7-character-sheet.schema.json",
        "schemas/cal0-i7-sheet-projection.schema.json",
        "scenarios/cal0-i3-reference-scenarios.json",
        "scenarios/cal0-i4-cohort-plan.json",
        "reports/cal0-i4-cohort-report.json",
        "reports/cal0-i5-adversarial-report.json",
        "characters/cal0-i6-reference-sheets.json",
        "authoring/cal0-i6-projection-contracts.json",
        "authoring/cal0-i6-authoring-checklists.json",
        "authoring/cal0-i6-notification-templates.json",
        "registries/cal0-i6-decision-resolution.json",
        "registries/cal0-i6-change-register.json",
        "scenarios/cal0-i6-story-scenarios.json",
        "reports/cal0-i6-usability-report.json",
        "registries/cal0-i7-residual-uncertainty.json",
        "registries/cal0-i7-change-register.json",
        "authoring/cal0-i7-scene-projection-matrix.json",
        "authoring/cal0-i7-character-sheet-checklist.json",
        "closure/cal0-i7-closure-review.json",
        "reports/cal0-i7-closure-report.json",
    }
    docs: dict[str, Any] = {"manifests/cal0-i7.bundle.json": manifest}
    load_issues: list[Issue] = []
    for relative in sorted(required):
        path = root / relative
        try:
            docs[relative] = _load_json(path)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            load_issues.append(_issue("ARTIFACT_LOAD_FAILED", relative, str(error)))
    if load_issues:
        return docs, sorted(load_issues)
    return docs, validate_documents(root, docs, verify_digests=verify_digests)


def _mutate(docs: dict[str, Any], mutation: dict[str, Any]) -> None:
    operation = mutation.get("operation")
    models = docs["registries/model-families.json"]["entries"]
    if operation == "remove_model":
        models[:] = [entry for entry in models if entry["selection_id"] != mutation["selection_id"]]
    elif operation == "duplicate_model":
        source = next(entry for entry in models if entry["selection_id"] == mutation["selection_id"])
        models.append(copy.deepcopy(source))
    elif operation == "unknown_schema":
        models[0]["schema_id"] = mutation["schema_id"]
    elif operation == "unresolved_contains_value":
        models[0]["parameters"]["value"] = mutation.get("value", "1")
    elif operation == "manifest_remove_artifact":
        target = mutation["path"]
        artifacts = docs["manifests/cal0-i7.bundle.json"]["artifacts"]
        artifacts[:] = [artifact for artifact in artifacts if artifact["path"] != target]
    elif operation == "remove_i3_binding":
        target = mutation["parameter_id"]
        bindings = docs["registries/cal0-i3-parameters.json"]["bindings"]
        bindings[:] = [binding for binding in bindings if binding["parameter_id"] != target]
    elif operation == "i3_value_out_of_domain":
        target = mutation["parameter_id"]
        binding = next(binding for binding in docs["registries/cal0-i3-parameters.json"]["bindings"] if binding["parameter_id"] == target)
        binding["value"] = mutation["value"]
    elif operation == "i3_distribution_unbounded":
        docs["registries/cal0-i3-parameters.json"]["distributions"][0]["truncation"] = "none"
    elif operation == "i3_dependence_non_psd":
        matrix = docs["registries/cal0-i3-parameters.json"]["dependence_blocks"][0]["correlation_matrix"]
        matrix[0][1] = mutation.get("correlation", "1.20")
        matrix[1][0] = mutation.get("correlation", "1.20")
    elif operation == "i3_unresolved_contains_value":
        binding = next(binding for binding in docs["registries/cal0-i3-parameters.json"]["bindings"] if binding["state"] == "UNRESOLVED")
        binding["value"] = mutation.get("value", "1")
    elif operation == "i3_unknown_character":
        docs["scenarios/cal0-i3-reference-scenarios.json"]["scenarios"][0]["characters"].append(mutation.get("character_id", "character://cal0/i3/unknown@1"))
    elif operation == "i4_cohort_too_small":
        docs["scenarios/cal0-i4-cohort-plan.json"]["births_per_seed"] = mutation.get("births_per_seed", 9999)
    elif operation == "i4_duplicate_seed":
        seeds = docs["scenarios/cal0-i4-cohort-plan.json"]["seeds"]
        seeds[-1] = seeds[0]
    elif operation == "i4_environment_weight":
        docs["scenarios/cal0-i4-cohort-plan.json"]["environments"][0]["weight"] = mutation.get("weight", "0.31")
    elif operation == "i4_trial_resolves_parent":
        docs["scenarios/cal0-i4-cohort-plan.json"]["trial_inputs"]["may_resolve_parent_unresolved_bindings"] = True
    elif operation == "i4_broken_iteration_lineage":
        docs["scenarios/cal0-i4-cohort-plan.json"]["calibration_iterations"][1]["parent"] = "calibration-iteration://cal0/i4/unknown@1"
    elif operation == "i4_protagonist_population":
        comparison = next(item for item in docs["scenarios/cal0-i4-cohort-plan.json"]["comparison_ensembles"] if "protagonist" in item["ensemble_id"])
        comparison["kind"] = "population"
    elif operation == "i5_report_failed":
        docs["reports/cal0-i5-adversarial-report.json"]["checks"]["catalog_valid"] = False
    elif operation == "i5_parent_digest_drift":
        docs["reports/cal0-i5-adversarial-report.json"]["parent_cohort_report_digest"] = "sha256:" + "0" * 64
    elif operation == "i5_remove_surface":
        docs["reports/cal0-i5-adversarial-report.json"]["surface_counts"].pop("ecological", None)
    elif operation == "i5_unresolved_invariant":
        docs["reports/cal0-i5-adversarial-report.json"]["unresolved_invariant_violations"] = ["synthetic-fixture"]
    elif operation == "i5_repair_uncovered":
        docs["reports/cal0-i5-adversarial-report.json"]["repairs"][0]["regression_count"] = 0
    elif operation == "i5_report_digest_drift":
        docs["reports/cal0-i5-adversarial-report.json"]["report_digest"] = "sha256:" + "0" * 64
    elif operation == "i6_report_failed":
        docs["reports/cal0-i6-usability-report.json"]["checks"]["six_views_per_sheet"] = False
    elif operation == "i6_parent_digest_drift":
        docs["reports/cal0-i6-usability-report.json"]["parent_i5_report_digest"] = "sha256:" + "0" * 64
    elif operation == "i6_remove_sheet":
        docs["characters/cal0-i6-reference-sheets.json"]["sheets"].pop()
    elif operation == "i6_remove_projection":
        docs["authoring/cal0-i6-projection-contracts.json"]["views"].pop()
    elif operation == "i6_projection_leak":
        target = next(item for item in docs["authoring/cal0-i6-projection-contracts.json"]["views"] if item["view_kind"] == "reader_facing")
        target["secrets"] = ["synthetic leak"]
    elif operation == "i6_remove_scenario":
        docs["scenarios/cal0-i6-story-scenarios.json"]["scenarios"].pop()
    elif operation == "i6_scalar_soul_resolution":
        decision = docs["registries/cal0-i6-decision-resolution.json"]["resolutions"][0]
        decision["active_resolution"] = "SCALAR_MULTIPLIER"
        decision["coefficient_changed"] = True
    elif operation == "i6_unclassified_residual":
        docs["registries/cal0-i6-decision-resolution.json"]["remaining_active_residuals"][0]["classification"] = ""
    elif operation == "i6_unclassified_change":
        docs["registries/cal0-i6-change-register.json"]["entries"][0]["classification"] = ""
    elif operation == "i6_report_digest_drift":
        docs["reports/cal0-i6-usability-report.json"]["report_digest"] = "sha256:" + "0" * 64
    elif operation == "i7_report_failed":
        docs["reports/cal0-i7-closure-report.json"]["checks"]["all_nine_val12_criteria_pass"] = False
    elif operation == "i7_parent_digest_drift":
        docs["reports/cal0-i7-closure-report.json"]["parent_i6_report_digest"] = "sha256:" + "0" * 64
    elif operation == "i7_remove_criterion":
        docs["closure/cal0-i7-closure-review.json"]["criteria"].pop()
    elif operation == "i7_unclassified_residual":
        docs["registries/cal0-i7-residual-uncertainty.json"]["groups"][0]["classification"] = ""
    elif operation == "i7_ownerless_residual":
        docs["registries/cal0-i7-residual-uncertainty.json"]["groups"][0]["owner"] = ""
    elif operation == "i7_blocking_residual":
        docs["registries/cal0-i7-residual-uncertainty.json"]["groups"][0]["items"][0]["blocking"] = True
    elif operation == "i7_remove_residual_group":
        docs["registries/cal0-i7-residual-uncertainty.json"]["groups"].pop(0)
    elif operation == "i7_break_soul_lineage":
        docs["registries/cal0-i7-residual-uncertainty.json"]["soul_multiplier_disposition"]["relationship"] = "UNRELATED"
    elif operation == "i7_remove_scene_layer":
        docs["authoring/cal0-i7-scene-projection-matrix.json"]["entries"][0]["layers"].pop("reader_need")
    elif operation == "i7_open_change":
        register = docs["registries/cal0-i7-change-register.json"]
        register["open_entry_count"] = 1
        register["open_entries"] = ["synthetic-fixture"]
    elif operation == "i7_disconnect_artifact":
        docs["closure/cal0-i7-closure-review.json"]["required_artifacts"][0]["status"] = "DISCONNECTED"
    elif operation == "i7_incomplete_sheet_schema":
        docs["schemas/cal0-i7-character-sheet.schema.json"]["properties"]["attributes"]["required"].remove("Resonance")
    elif operation == "i7_remove_checklist_view":
        docs["authoring/cal0-i7-character-sheet-checklist.json"]["required_view_kinds"].pop()
    elif operation == "i7_report_digest_drift":
        docs["reports/cal0-i7-closure-report.json"]["report_digest"] = "sha256:" + "0" * 64
    elif operation is None:
        return
    else:
        raise ValueError(f"unknown fixture mutation: {operation}")
    if isinstance(operation, str) and operation.startswith("i5_") and operation != "i5_report_digest_drift":
        report = docs["reports/cal0-i5-adversarial-report.json"]
        payload = dict(report)
        payload.pop("report_digest", None)
        report["report_digest"] = semantic_digest(payload)
    if isinstance(operation, str) and operation.startswith("i5_"):
        i6_report = docs["reports/cal0-i6-usability-report.json"]
        i6_report["parent_i5_report_digest"] = docs["reports/cal0-i5-adversarial-report.json"]["report_digest"]
        payload = dict(i6_report)
        payload.pop("report_digest", None)
        i6_report["report_digest"] = semantic_digest(payload)
    if isinstance(operation, str) and operation.startswith("i6_") and operation not in {"i6_report_digest_drift", "i6_remove_sheet", "i6_remove_projection", "i6_projection_leak", "i6_remove_scenario", "i6_scalar_soul_resolution", "i6_unclassified_residual"}:
        report = docs["reports/cal0-i6-usability-report.json"]
        payload = dict(report)
        payload.pop("report_digest", None)
        report["report_digest"] = semantic_digest(payload)
    if isinstance(operation, str) and (operation.startswith("i5_") or operation.startswith("i6_")):
        i7_report = docs["reports/cal0-i7-closure-report.json"]
        i7_report["parent_i6_report_digest"] = docs["reports/cal0-i6-usability-report.json"]["report_digest"]
        payload = dict(i7_report)
        payload.pop("report_digest", None)
        i7_report["report_digest"] = semantic_digest(payload)
    if isinstance(operation, str) and operation.startswith("i7_") and operation != "i7_report_digest_drift":
        residuals = docs["registries/cal0-i7-residual-uncertainty.json"]
        payload = dict(residuals)
        payload.pop("registry_digest", None)
        residuals["registry_digest"] = semantic_digest(payload)
        matrix = docs["authoring/cal0-i7-scene-projection-matrix.json"]
        for entry in matrix["entries"]:
            payload = dict(entry)
            payload.pop("entry_digest", None)
            entry["entry_digest"] = semantic_digest(payload)
        payload = dict(matrix)
        payload.pop("matrix_digest", None)
        matrix["matrix_digest"] = semantic_digest(payload)
        change = docs["registries/cal0-i7-change-register.json"]
        payload = dict(change)
        payload.pop("register_digest", None)
        change["register_digest"] = semantic_digest(payload)
        checklist = docs["authoring/cal0-i7-character-sheet-checklist.json"]
        payload = dict(checklist)
        payload.pop("checklist_digest", None)
        checklist["checklist_digest"] = semantic_digest(payload)
        review = docs["closure/cal0-i7-closure-review.json"]
        review["residual_registry_digest"] = residuals["registry_digest"]
        review["change_register_digest"] = change["register_digest"]
        review["scene_matrix_digest"] = matrix["matrix_digest"]
        payload = dict(review)
        payload.pop("review_digest", None)
        review["review_digest"] = semantic_digest(payload)
        report = docs["reports/cal0-i7-closure-report.json"]
        report["review_digest"] = review["review_digest"]
        report["residual_registry_digest"] = residuals["registry_digest"]
        report["change_register_digest"] = change["register_digest"]
        report["scene_matrix_digest"] = matrix["matrix_digest"]
        payload = dict(report)
        payload.pop("report_digest", None)
        report["report_digest"] = semantic_digest(payload)


def run_fixtures(root: Path) -> list[dict[str, Any]]:
    docs, baseline_issues = load_and_validate(root)
    if baseline_issues:
        return [{"case_id": "baseline", "passed": False, "actual_codes": sorted({issue.code for issue in baseline_issues}), "expected_codes": []}]
    fixture_documents = [
        _load_json(root / "fixtures/cal0-i1-fixtures.json"),
        _load_json(root / "fixtures/cal0-i3-parameter-fixtures.json"),
        _load_json(root / "fixtures/cal0-i4-fixtures.json"),
        _load_json(root / "fixtures/cal0-i5-fixtures.json"),
        _load_json(root / "fixtures/cal0-i6-fixtures.json"),
        _load_json(root / "fixtures/cal0-i7-fixtures.json"),
    ]
    results: list[dict[str, Any]] = []
    for case in [case for document in fixture_documents for case in document["cases"]]:
        candidate = copy.deepcopy(docs)
        _mutate(candidate, case.get("mutation", {}))
        issues = validate_documents(root, candidate, verify_digests=False)
        actual = sorted({issue.code for issue in issues})
        expected = sorted(case["expected_codes"])
        results.append({"case_id": case["case_id"], "passed": actual == expected, "actual_codes": actual, "expected_codes": expected})
    return results


def validation_report(root: Path) -> dict[str, Any]:
    docs, issues = load_and_validate(root)
    models = docs.get("registries/model-families.json", {}).get("entries", [])
    report = {
        "bundle_id": docs.get("manifests/cal0-i7.bundle.json", {}).get("bundle_id"),
        "canonical_digest": semantic_digest(docs) if docs else None,
        "issue_count": len(issues),
        "issues": [issue.as_dict() for issue in issues],
        "model_count": len(models),
        "parameter_status": docs.get("manifests/cal0-i7.bundle.json", {}).get("parameter_status"),
        "closure_status": docs.get("manifests/cal0-i7.bundle.json", {}).get("closure_status"),
        "provisional_binding_count": sum(
            1 for binding in docs.get("registries/cal0-i3-parameters.json", {}).get("bindings", [])
            if binding.get("state") == "PROVISIONAL"
        ),
        "unresolved_binding_count": sum(
            1 for binding in docs.get("registries/cal0-i3-parameters.json", {}).get("bindings", [])
            if binding.get("state") == "UNRESOLVED"
        ),
        "valid": not issues,
    }
    return report
