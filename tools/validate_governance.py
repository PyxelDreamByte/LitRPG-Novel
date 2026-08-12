#!/usr/bin/env python3
"""Validate structured governance records with dependency-free semantics."""

from __future__ import annotations

import hashlib
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "litrpg-system/story-integration"
FIXTURE_ROOT = INTEGRATION / "fixtures/governance"
sys.path.insert(0, str(INTEGRATION / "validators"))
from validate import SchemaSet, load_json  # noqa: E402


BINDING = {"ACCEPTED", "PROVISIONAL", "DEFERRED"}
COMPATIBLE = {
    "DRAFT": {"PROPOSED"},
    "IN_REVIEW": {"PROPOSED"},
    "AWAITING_AUTHOR": {"PROPOSED"},
    "ACCEPTED": {"ACCEPTED", "PROVISIONAL", "DEFERRED"},
    "REJECTED": {"REJECTED"},
    "SUPERSEDED": {"SUPERSEDED"},
}


def record_kind(path: Path) -> str | None:
    if path.name.endswith(".decision.json"):
        return "decision"
    if path.name.endswith(".worldbuilding.json"):
        return "worldbuilding"
    if path.name.endswith(".workflow-evidence.json"):
        return "evidence"
    return None


def semantic_record(document: dict[str, Any], kind: str) -> list[str]:
    errors: list[str] = []
    workflow = document.get("workflow_status")
    canon = document.get("canon_status")
    if kind in {"decision", "worldbuilding"}:
        allowed = COMPATIBLE.get(workflow, set())
        if canon not in allowed:
            errors.append(
                f"$: incompatible workflow/canon status pair {workflow!r}/{canon!r}"
            )
        if canon in BINDING:
            if workflow != "ACCEPTED":
                errors.append("$: binding canon status requires ACCEPTED workflow status")
            if kind == "decision":
                for field in ("accepted_on", "accepted_by", "approval_evidence"):
                    if not document.get(field):
                        errors.append(f"$.{field}: binding decision requires Author evidence")
                if document.get("accepted_by") != "Author":
                    errors.append("$.accepted_by: binding decision must be accepted by Author")
            else:
                approval = document.get("author_approval")
                if not isinstance(approval, dict):
                    errors.append("$.author_approval: binding world record requires Author evidence")
                elif approval.get("accepted_by") != "Author" or not approval.get("evidence"):
                    errors.append("$.author_approval: binding world record requires Author evidence")
    return errors


def repository_file(path_value: Any, label: str) -> tuple[Path | None, list[str]]:
    """Resolve one content-pinned evidence path without permitting repository escape."""
    if not isinstance(path_value, str) or not path_value or "\\" in path_value:
        return None, [f"{label}: must be a normalized repository-relative path"]
    relative = Path(path_value)
    if relative.is_absolute() or ".." in relative.parts or relative.as_posix() != path_value:
        return None, [f"{label}: must be a normalized repository-relative path"]
    repository_root = ROOT.resolve()
    resolved = (ROOT / relative).resolve()
    try:
        resolved.relative_to(repository_root)
    except ValueError:
        return None, [f"{label}: resolves outside the repository"]
    if not resolved.is_file():
        return None, [f"{label}: file does not exist"]
    return resolved, []


def evidence_file_errors(document: dict[str, Any], record_path: Path) -> list[str]:
    """Verify retained live/accepted evidence against the exact bytes it names."""
    errors: list[str] = []
    references: list[tuple[str, Any]] = []
    for field in ("source_manifest", "target_artifacts"):
        for index, reference in enumerate(document.get(field, [])):
            references.append((f"$.{field}[{index}]", reference))
    if isinstance(document.get("raw_output"), dict):
        references.append(("$.raw_output", document["raw_output"]))

    for label, reference in references:
        if not isinstance(reference, dict):
            continue
        resolved, path_errors = repository_file(reference.get("path"), f"{label}.path")
        errors.extend(path_errors)
        if resolved is not None:
            digest = "sha256:" + hashlib.sha256(resolved.read_bytes()).hexdigest()
            if reference.get("sha256") != digest:
                errors.append(f"{label}.sha256: digest mismatch")

    retained = document.get("retained_files", [])
    for index, path_value in enumerate(retained):
        resolved, path_errors = repository_file(path_value, f"$.retained_files[{index}]")
        errors.extend(path_errors)
        if resolved is not None:
            try:
                resolved.relative_to(record_path.parent.resolve())
            except ValueError:
                errors.append(
                    f"$.retained_files[{index}]: retained file must stay beside its evidence manifest"
                )
    if document.get("evidence_kind") == "LIVE_NONCANONICAL_EVALUATION":
        raw_path = document.get("raw_output", {}).get("path")
        if raw_path not in retained:
            errors.append("$.raw_output.path: raw output must also be listed in retained_files")
    return errors


def real_paths() -> list[Path]:
    paths: set[Path] = set()
    for pattern in (
        "governance/decisions/**/*.decision.json",
        "governance/evidence/**/*.workflow-evidence.json",
        "worldbuilding/canon/**/*.worldbuilding.json",
        "worldbuilding/proposals/**/*.worldbuilding.json",
        "worldbuilding/decisions/**/*.decision.json",
    ):
        paths.update(ROOT.glob(pattern))
    return sorted(paths)


def validate_set(paths: list[Path], schemas: SchemaSet, fixture: bool = False) -> tuple[list[str], dict[str, dict[str, Any]]]:
    errors: list[str] = []
    records: dict[str, dict[str, Any]] = {}
    for path in paths:
        kind = record_kind(path)
        if kind is None:
            continue
        document = load_json(path)
        schema_name = {
            "decision": "decision-record.schema.json",
            "worldbuilding": "worldbuilding-record.schema.json",
            "evidence": "workflow-evidence-manifest.schema.json",
        }[kind]
        schema_value = document.pop("$schema", None)
        file_errors = [] if schema_value is None or isinstance(schema_value, str) else [
            "$.$schema: schema annotation must be a string"
        ]
        file_errors.extend(schemas.validate(document, schema_name))
        file_errors.extend(semantic_record(document, kind))
        if kind == "evidence":
            file_errors.extend(evidence_file_errors(document, path))
        identity = document.get("decision_uri") or document.get("record_uri") or document.get("run_id")
        if identity in records:
            file_errors.append(f"$: duplicate governance identity {identity!r}")
        if isinstance(identity, str):
            records[identity] = {"kind": kind, "path": path, "document": document}
        errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in file_errors)
    return errors, records


def cross_links(records: dict[str, dict[str, Any]], require_indexes: bool) -> list[str]:
    errors: list[str] = []
    decisions = {key for key, value in records.items() if value["kind"] == "decision"}
    world_index_path = ROOT / "worldbuilding/INDEX.md"
    world_index = world_index_path.read_text(encoding="utf-8") if world_index_path.is_file() else ""
    repository_index_path = ROOT / "governance/decisions/README.md"
    repository_index = (
        repository_index_path.read_text(encoding="utf-8")
        if repository_index_path.is_file()
        else ""
    )
    for identity, record in records.items():
        document = record["document"]
        path = record["path"]
        if record["kind"] == "worldbuilding" and document.get("canon_status") in BINDING:
            decision_uri = document.get("author_approval", {}).get("decision_uri")
            if decision_uri not in decisions:
                errors.append(f"{path.relative_to(ROOT)}: unresolved Author decision {decision_uri!r}")
        if require_indexes and document.get("canon_status") in BINDING:
            if record["kind"] == "decision":
                review_path = path.with_name(path.name.removesuffix(".decision.json") + ".md")
                review = review_path.read_text(encoding="utf-8") if review_path.is_file() else ""
                if document.get("id") not in review or identity not in review:
                    errors.append(
                        f"{path.relative_to(ROOT)}: binding decision lacks an identity-matched human review/index surface"
                    )
                if identity.startswith("author-decision://world/") and (
                    document.get("id") not in world_index or identity not in world_index
                ):
                    errors.append(
                        f"{path.relative_to(ROOT)}: binding world decision is absent from worldbuilding/INDEX.md"
                    )
                if identity.startswith("author-decision://repository/") and (
                    document.get("id") not in repository_index or identity not in repository_index
                ):
                    errors.append(
                        f"{path.relative_to(ROOT)}: binding repository decision is absent from governance/decisions/README.md"
                    )
            elif record["kind"] == "worldbuilding":
                if document.get("id") not in world_index and identity not in world_index:
                    errors.append(f"{path.relative_to(ROOT)}: binding world record is absent from worldbuilding/INDEX.md")
    return errors


def main() -> int:
    schemas = SchemaSet(ROOT / "governance/schemas")
    errors, real_records = validate_set(real_paths(), schemas)
    errors.extend(cross_links(real_records, require_indexes=True))

    valid_paths = sorted((FIXTURE_ROOT / "valid").glob("*.json"))
    fixture_errors, fixture_records = validate_set(valid_paths, schemas, fixture=True)
    fixture_errors.extend(cross_links(fixture_records, require_indexes=False))
    errors.extend(fixture_errors)
    invalid_expectations = {
        "live-evaluation-digest-mismatch.workflow-evidence.json": "digest mismatch",
        "live-evaluation-with-approval.workflow-evidence.json": "must satisfy exactly one allowed schema",
        "missing-author-evidence.decision.json": "binding decision requires Author evidence",
        "unindexed-world-decision.decision.json": "binding world decision is absent from worldbuilding/INDEX.md",
        "unresolved-world-decision.worldbuilding.json": "unresolved Author decision",
    }
    for path in sorted((FIXTURE_ROOT / "invalid").glob("*.json")):
        file_errors, records = validate_set([path], schemas, fixture=True)
        file_errors.extend(
            cross_links(
                records,
                require_indexes=path.name == "unindexed-world-decision.decision.json",
            )
        )
        expected = invalid_expectations.get(path.name)
        if expected is None:
            errors.append(f"{path.relative_to(ROOT)}: invalid fixture lacks targeted expectation")
        elif not any(expected in error for error in file_errors):
            errors.append(f"{path.relative_to(ROOT)}: expected targeted failure {expected!r}; found {file_errors}")

    if errors:
        print("governance validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(
        f"governance validation passed: {len(real_records)} repository records, "
        f"{len(valid_paths)} valid fixtures, {len(invalid_expectations)} rejected fixtures"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
