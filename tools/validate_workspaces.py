#!/usr/bin/env python3
"""Validate work/setting manifests, typed isolation, and static eval fixtures."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "litrpg-system/story-integration"
sys.path.insert(0, str(INTEGRATION / "validators"))
from validate import SchemaSet, load_json, semantic_work_manifest, work_identity_errors  # noqa: E402


BINDING_CANON_STATUSES = {"ACCEPTED", "PROVISIONAL", "DEFERRED"}
INVALID_FIXTURE_ROOT = INTEGRATION / "fixtures/invalid"


def normalized_scoped_path(path_value: str, root_value: str) -> Path | None:
    if "\\" in path_value or "\\" in root_value:
        return None
    path = Path(path_value)
    root = Path(root_value)
    if path.is_absolute() or root.is_absolute() or ".." in path.parts or ".." in root.parts:
        return None
    try:
        path.relative_to(root)
    except ValueError:
        return None
    if path.as_posix() != path_value or root.as_posix() != root_value:
        return None
    repository_root = ROOT.resolve()
    resolved_root = (ROOT / root).resolve()
    resolved_path = (ROOT / path).resolve()
    try:
        resolved_root.relative_to(repository_root)
        resolved_path.relative_to(resolved_root)
    except ValueError:
        return None
    return resolved_path


def markdown_fields(text: str) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["missing opening frontmatter delimiter"]
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, ["missing closing frontmatter delimiter"]
    fields: dict[str, Any] = {}
    for line_number, line in enumerate(text[4:end].splitlines(), start=2):
        if not line or line.startswith((" ", "\t")) or ":" not in line:
            errors.append(f"frontmatter line {line_number}: fields must use one-line key: value form")
            continue
        name, raw = line.split(":", 1)
        name = name.strip()
        raw = raw.strip()
        if name in fields:
            errors.append(f"frontmatter line {line_number}: duplicate field {name!r}")
            continue
        if raw in {"null", "~"}:
            value: Any = None
        elif raw.startswith(("[", "{", '"')):
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"frontmatter line {line_number}: invalid JSON value for {name!r}: {exc.msg}")
                continue
        else:
            value = raw
        fields[name] = value
    return fields, errors


def validate_pairing(
    manifest: dict[str, Any],
    manifest_path: Path,
    schema_fields: set[str],
    errors: list[str],
) -> None:
    root_value = manifest["work_root"]
    real_work = root_value.startswith("stories/")
    if not real_work:
        return
    review_path = ROOT / root_value / "work-manifest.md"
    if not review_path.is_file():
        errors.append(f"{manifest_path.relative_to(ROOT)}: real work lacks paired {review_path.relative_to(ROOT)}")
        return
    text = review_path.read_text(encoding="utf-8")
    human_fields, parse_errors = markdown_fields(text)
    errors.extend(f"{review_path.relative_to(ROOT)}: {error}" for error in parse_errors)
    unknown = set(human_fields) - schema_fields
    if unknown:
        errors.append(f"{review_path.relative_to(ROOT)}: unknown manifest fields {sorted(unknown)}")
    for field in sorted(set(manifest) | set(human_fields)):
        human = human_fields.get(field)
        machine = manifest.get(field)
        if human != machine:
            errors.append(
                f"{review_path.relative_to(ROOT)}: {field} {human!r} does not match machine authority {machine!r}"
            )


def binding_decision_errors(
    decision_uri: Any,
    accepted_on: Any,
    decisions: dict[str, dict[str, Any]],
    path: str,
) -> list[str]:
    record = decisions.get(decision_uri) if isinstance(decision_uri, str) else None
    if record is None:
        return [f"{path}: unresolved Author decision {decision_uri!r}"]
    errors: list[str] = []
    if record.get("workflow_status") != "ACCEPTED" or record.get("canon_status") not in BINDING_CANON_STATUSES:
        errors.append(f"{path}: decision is not an accepted binding governance record")
    if accepted_on is not None and record.get("accepted_on") != accepted_on:
        errors.append(f"{path}: acceptance date does not match the decision record")
    return errors


def validate_setting(
    path: Path,
    document: dict[str, Any],
    schemas: SchemaSet,
    decisions: dict[str, dict[str, Any]],
) -> list[str]:
    errors = schemas.validate(document, "setting-manifest.schema.json")
    if errors:
        return errors
    setting_id = document["setting_id"]
    slug = setting_id.removeprefix("setting://")
    root_value = document["setting_root"]
    root_path = Path(root_value)
    if root_path.name != slug:
        errors.append("$.setting_root: final directory must match the setting ID slug")
    expected_path = (ROOT / root_path / f"{slug}.setting-manifest.json").resolve()
    if path.resolve() != expected_path:
        errors.append(f"$: setting manifest must use canonical path {expected_path.relative_to(ROOT)}")
    index_path = normalized_scoped_path(document["index_path"], root_value)
    if index_path is None:
        errors.append("$.index_path: must remain within setting_root")
    elif not index_path.is_file():
        errors.append("$.index_path: setting-local index does not exist")
    workflow = document["workflow_status"]
    canon = document["canon_status"]
    allowed = (
        (workflow in {"DRAFT", "IN_REVIEW", "AWAITING_AUTHOR"} and canon == "PROPOSED")
        or (workflow == "ACCEPTED" and canon in BINDING_CANON_STATUSES)
        or (workflow == "REJECTED" and canon == "REJECTED")
        or (workflow == "SUPERSEDED" and canon == "SUPERSEDED")
    )
    if not allowed:
        errors.append("$: workflow_status and canon_status are incompatible")
    if canon in {"ACCEPTED", "PROVISIONAL"}:
        if not document.get("accepted_on") or not document.get("approval_decision_uri"):
            errors.append("$: accepted/provisional setting requires Author decision and acceptance date")
        else:
            errors.extend(
                binding_decision_errors(
                    document["approval_decision_uri"], document["accepted_on"], decisions,
                    "$.approval_decision_uri",
                )
            )
    elif document.get("accepted_on") is not None or document.get("approval_decision_uri") is not None:
        errors.append("$: nonbinding setting cannot carry Author acceptance fields")
    return errors


def validate_work_authorities(
    document: dict[str, Any],
    decisions: dict[str, dict[str, Any]],
    world_records: dict[str, dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    if document.get("canonicality") in {"ACCEPTED", "PROVISIONAL"}:
        errors.extend(
            binding_decision_errors(
                document.get("approval_decision_uri"), document.get("accepted_on"), decisions,
                "$.approval_decision_uri",
            )
        )
    seen_guardrails: set[str] = set()
    for index, adoption in enumerate(document.get("adopted_default_guardrails", [])):
        if not isinstance(adoption, dict):
            continue
        path = f"$.adopted_default_guardrails[{index}]"
        decision_uri = adoption.get("decision_uri")
        if decision_uri in seen_guardrails:
            errors.append(f"{path}.decision_uri: duplicate adopted guardrail")
        if isinstance(decision_uri, str):
            seen_guardrails.add(decision_uri)
        record = decisions.get(decision_uri)
        errors.extend(binding_decision_errors(decision_uri, None, decisions, f"{path}.decision_uri"))
        if record is not None and adoption.get("effective_revision") not in {
            record.get("id"), record.get("display_code")
        }:
            errors.append(f"{path}.effective_revision: must equal the stable decision ID")
    setting_id = document.get("shared_setting_id")
    for index, reference in enumerate(document.get("adopted_shared_world_refs", [])):
        path = f"$.adopted_shared_world_refs[{index}]"
        if isinstance(reference, str) and reference.startswith("author-decision://"):
            errors.extend(binding_decision_errors(reference, None, decisions, path))
        elif isinstance(reference, str) and reference.startswith("canon://world/"):
            record = world_records.get(reference)
            if record is None:
                errors.append(f"{path}: unresolved binding world record {reference!r}")
            else:
                approval = record.get("author_approval", {})
                errors.extend(
                    binding_decision_errors(
                        approval.get("decision_uri"), approval.get("accepted_on"), decisions,
                        f"{path}.author_approval",
                    )
                )
                if document.get("setting_scope") == "SHARED_WORLD" and record.get("setting_id") != setting_id:
                    errors.append(f"{path}: world record belongs to another setting")
        else:
            errors.append(f"{path}: must resolve to a binding world record or Author decision")
    return errors


def validate_eval(path: Path, document: dict[str, Any], schemas: SchemaSet) -> list[str]:
    errors = schemas.validate(document, "workflow-eval.schema.json")
    work_root = document.get("work_root")
    fixture_root = document.get("fixture_root")
    if not isinstance(work_root, str) or not isinstance(fixture_root, str):
        return errors
    fixture_path = normalized_scoped_path(fixture_root, work_root)
    if fixture_path is None:
        errors.append("$.fixture_root: must remain within work_root")
        return errors
    if not fixture_path.is_dir():
        errors.append("$.fixture_root: directory does not exist")
    seen_paths: set[str] = set()
    for index, artifact in enumerate(document.get("included_artifacts", [])):
        if not isinstance(artifact, dict):
            continue
        artifact_path = artifact.get("path")
        if artifact_path in seen_paths:
            errors.append(f"$.included_artifacts[{index}].path: duplicate artifact")
        if isinstance(artifact_path, str):
            seen_paths.add(artifact_path)
            resolved = normalized_scoped_path(artifact_path, fixture_root)
            if resolved is None:
                errors.append(f"$.included_artifacts[{index}].path: must remain within fixture_root")
            elif not resolved.is_file():
                errors.append(f"$.included_artifacts[{index}].path: file does not exist")
            else:
                digest = "sha256:" + hashlib.sha256(resolved.read_bytes()).hexdigest()
                if artifact.get("sha256") != digest:
                    errors.append(f"$.included_artifacts[{index}].sha256: digest mismatch")
                if resolved.name.endswith(".chapter-delta.json"):
                    delta = load_json(resolved)
                    if isinstance(delta, dict) and delta.get("status") == "ACCEPTED":
                        errors.append(f"$.included_artifacts[{index}]: evaluation delta cannot be ACCEPTED")
    finding_ids: set[str] = set()
    for index, finding in enumerate(document.get("expected_findings", [])):
        finding_id = finding.get("finding_id")
        if finding_id in finding_ids:
            errors.append(f"$.expected_findings[{index}].finding_id: duplicate finding ID")
        finding_ids.add(finding_id)
    errors.extend(work_identity_errors(document, document.get("work_id")))
    return errors


def main() -> int:
    schemas = SchemaSet(INTEGRATION / "schemas")
    errors: list[str] = []
    template_contracts = (
        (
            ROOT / "stories/templates/work-manifest.example.json",
            "work-manifest.schema.json",
            semantic_work_manifest,
        ),
        (
            ROOT / "worldbuilding/templates/setting-manifest.template.json",
            "setting-manifest.schema.json",
            lambda _document: [],
        ),
    )
    for path, schema_name, semantic_check in template_contracts:
        document = load_json(path)
        if not isinstance(document, dict):
            errors.append(f"{path.relative_to(ROOT)}: $: root must be an object")
            continue
        file_errors = schemas.validate(document, schema_name)
        file_errors.extend(semantic_check(document))
        errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in file_errors)

    decisions: dict[str, dict[str, Any]] = {}
    for path in sorted(
        set((ROOT / "governance/decisions").glob("**/*.decision.json"))
        | set((ROOT / "worldbuilding/decisions").glob("**/*.decision.json"))
        | set(ROOT.glob("worldbuilding/settings/**/decisions/**/*.decision.json"))
    ):
        document = load_json(path)
        if isinstance(document, dict) and isinstance(document.get("decision_uri"), str):
            decisions[document["decision_uri"]] = document
    world_records: dict[str, dict[str, Any]] = {}
    world_record_paths = (
        set((ROOT / "worldbuilding/canon").glob("**/*.worldbuilding.json"))
        | set((ROOT / "worldbuilding/proposals").glob("**/*.worldbuilding.json"))
        | set(ROOT.glob("worldbuilding/settings/**/canon/**/*.worldbuilding.json"))
        | set(ROOT.glob("worldbuilding/settings/**/proposals/**/*.worldbuilding.json"))
    )
    for path in sorted(world_record_paths):
        document = load_json(path)
        if isinstance(document, dict) and isinstance(document.get("record_uri"), str):
            world_records[document["record_uri"]] = document

    setting_manifests: dict[str, dict[str, Any]] = {}
    setting_paths = sorted(
        set(ROOT.glob("worldbuilding/settings/**/*.setting-manifest.json"))
        | set((INTEGRATION / "fixtures/valid/settings").glob("**/*.setting-manifest.json"))
    )
    for path in setting_paths:
        document = load_json(path)
        if not isinstance(document, dict):
            errors.append(f"{path.relative_to(ROOT)}: $: root must be an object")
            continue
        file_errors = validate_setting(path, document, schemas, decisions)
        setting_id = document.get("setting_id")
        if setting_id in setting_manifests:
            file_errors.append("$.setting_id: duplicate setting identity")
        setting_manifests[setting_id] = document
        errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in file_errors)

    work_manifests: dict[str, dict[str, Any]] = {}
    work_paths = sorted(
        set(ROOT.rglob("*.work-manifest.json")) | set(ROOT.rglob("work-manifest.json"))
    )
    for path in work_paths:
        if path.is_relative_to(INVALID_FIXTURE_ROOT):
            continue
        document = load_json(path)
        if not isinstance(document, dict):
            errors.append(f"{path.relative_to(ROOT)}: $: root must be an object")
            continue
        file_errors = schemas.validate(document, "work-manifest.schema.json")
        file_errors.extend(semantic_work_manifest(document))
        file_errors.extend(validate_work_authorities(document, decisions, world_records))
        work_id = document.get("work_id")
        if work_id in work_manifests:
            file_errors.append("$.work_id: duplicate work identity")
        work_manifests[work_id] = document
        if document.get("setting_scope") == "SHARED_WORLD":
            setting_id = document.get("shared_setting_id")
            setting = setting_manifests.get(setting_id)
            if setting is None:
                file_errors.append(f"$.shared_setting_id: unresolved setting manifest {setting_id!r}")
            elif setting.get("workflow_status") != "ACCEPTED" or setting.get("canon_status") not in {
                "ACCEPTED", "PROVISIONAL"
            }:
                file_errors.append("$.shared_setting_id: shared setting is not accepted/provisional authority")
            elif work_id not in setting.get("adopting_work_ids", []):
                file_errors.append("$.shared_setting_id: setting manifest does not list this adopting work")
        if str(document.get("work_root", "")).startswith("stories/"):
            slug = str(work_id).rsplit("/", 1)[-1]
            allowed_paths = {
                (ROOT / document["work_root"] / "work-manifest.json").resolve(),
                (ROOT / document["work_root"] / f"{slug}.work-manifest.json").resolve(),
            }
            if path.resolve() not in allowed_paths:
                file_errors.append("$: work manifest must be stored at its declared work_root")
        validate_pairing(
            document,
            path,
            set(schemas.documents["work-manifest.schema.json"]["properties"]),
            file_errors,
        )
        errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in file_errors)

    for setting_id, setting in setting_manifests.items():
        for index, work_id in enumerate(setting.get("adopting_work_ids", [])):
            work = work_manifests.get(work_id)
            path = f"setting {setting_id!r} $.adopting_work_ids[{index}]"
            if work is None:
                errors.append(f"{path}: unresolved work manifest {work_id!r}")
            elif work.get("setting_scope") != "SHARED_WORLD" or work.get("shared_setting_id") != setting_id:
                errors.append(f"{path}: work does not point back to this shared setting")

    eval_count = 0
    for path in sorted(ROOT.rglob("*.workflow-eval.json")):
        eval_count += 1
        document = load_json(path)
        if not isinstance(document, dict):
            errors.append(f"{path.relative_to(ROOT)}: $: root must be an object")
            continue
        file_errors = validate_eval(path, document, schemas)
        work = work_manifests.get(document.get("work_id"))
        if work is None:
            file_errors.append("$.work_id: evaluation has no work manifest")
        elif work.get("mode") != "EVALUATION" or work.get("promotion") != "FORBIDDEN":
            file_errors.append("$.work_id: evaluation work manifest is not evaluation/promotion-forbidden")
        elif document.get("work_root") != work.get("work_root"):
            file_errors.append("$.work_root: does not match the evaluation work manifest")
        errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in file_errors)

    invalid_eval_expectations = {
        "accepted-artifact.workflow-eval.invalid.json": "evaluation delta cannot be ACCEPTED",
    }
    for path in sorted(ROOT.rglob("*.workflow-eval.invalid.json")):
        document = load_json(path)
        file_errors = validate_eval(path, document, schemas)
        expected = invalid_eval_expectations.get(path.name)
        if expected is None:
            errors.append(f"{path.relative_to(ROOT)}: invalid eval fixture lacks targeted expectation")
        elif not any(expected in error for error in file_errors):
            errors.append(
                f"{path.relative_to(ROOT)}: expected targeted failure {expected!r}; found {file_errors}"
            )

    invalid_workspace_expectations = {
        "unresolved-guardrail.work-manifest.invalid.json": "unresolved Author decision",
        "one-way.setting-manifest.invalid.json": "unresolved work manifest",
    }
    for path in sorted(INVALID_FIXTURE_ROOT.rglob("*.work-manifest.invalid.json")):
        document = load_json(path)
        file_errors = schemas.validate(document, "work-manifest.schema.json")
        if isinstance(document, dict):
            file_errors.extend(semantic_work_manifest(document))
            file_errors.extend(validate_work_authorities(document, decisions, world_records))
        expected = invalid_workspace_expectations.get(path.name)
        if expected is None or not any(expected in error for error in file_errors):
            errors.append(
                f"{path.relative_to(ROOT)}: expected targeted failure {expected!r}; found {file_errors}"
            )
    for path in sorted(INVALID_FIXTURE_ROOT.rglob("*.setting-manifest.invalid.json")):
        document = load_json(path)
        file_errors = schemas.validate(document, "setting-manifest.schema.json")
        if isinstance(document, dict):
            work_ids = document.get("adopting_work_ids", [])
            for work_id in work_ids:
                if work_id not in work_manifests:
                    file_errors.append(f"$.adopting_work_ids: unresolved work manifest {work_id!r}")
        expected = invalid_workspace_expectations.get(path.name)
        if expected is None or not any(expected in error for error in file_errors):
            errors.append(
                f"{path.relative_to(ROOT)}: expected targeted failure {expected!r}; found {file_errors}"
            )

    if errors:
        print("workspace/evaluation validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(
        f"workspace/evaluation validation passed: {len(work_manifests)} work manifests, "
        f"{len(setting_manifests)} setting manifests, {eval_count} workflow evals, "
        f"{len(invalid_eval_expectations) + len(invalid_workspace_expectations)} rejected workspace/eval fixtures"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
