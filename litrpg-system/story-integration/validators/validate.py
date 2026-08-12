#!/usr/bin/env python3
"""Dependency-free schema and cross-record validation for story integration."""

from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
INTEGRATION_ROOT = REPOSITORY_ROOT / "litrpg-system/story-integration"
SCHEMA_ROOT = INTEGRATION_ROOT / "schemas"
FIXTURE_ROOT = INTEGRATION_ROOT / "fixtures"
DECISION_INDEX = REPOSITORY_ROOT / "litrpg-system/indices/architecture-decisions.json"
I3_PARAMETER_REGISTRY = REPOSITORY_ROOT / "litrpg-system/cal0/registries/cal0-i3-parameters.json"
I4_PARAMETER_ASSESSMENT = REPOSITORY_ROOT / "litrpg-system/cal0/registries/cal0-i4-parameter-assessment.json"

INVALID_EXPECTATIONS = {
    "duplicate-and-inexact.chapter-delta.json": "JSON floating-point value",
    "duplicate-record-identifiers.chapter-delta.json": "duplicate change ID",
    "wrong-canon-review.chapter-delta.json": "requires CHAPTER_ACCEPTANCE",
    "shared-author-decision.chapter-delta.json": "decision distinct from chapter-delta acceptance",
    "manuscript-digest-mismatch.chapter-delta.json": "digest does not match bound manuscript bytes",
    "manuscript-path-traversal.chapter-delta.json": "paths are forbidden",
    "accepted-open-major.chapter-delta.json": "cannot retain major findings",
    "accepted-unresolved-system-change.chapter-delta.json": "cannot retain an unresolved proposed System change",
    "unknown-parameter-set.chapter-delta.json": "unknown CAL0 parameter set",
}


class SchemaSet:
    def __init__(self, root: Path):
        self.root = root
        self.documents: dict[str, dict[str, Any]] = {}
        for path in sorted(root.glob("*.schema.json")):
            self.documents[path.name] = load_json(path)

    def resolve(self, reference: str, current_name: str) -> tuple[Any, str]:
        file_part, separator, fragment = reference.partition("#")
        target_name = Path(file_part).name if file_part else current_name
        if target_name not in self.documents:
            raise KeyError(f"unknown schema document {target_name!r}")
        target: Any = self.documents[target_name]
        if separator and fragment:
            if not fragment.startswith("/"):
                raise KeyError(f"unsupported schema fragment #{fragment}")
            for token in fragment[1:].split("/"):
                token = token.replace("~1", "/").replace("~0", "~")
                target = target[token]
        return target, target_name

    def validate(self, value: Any, schema_name: str) -> list[str]:
        errors: list[str] = []
        self._validate(value, self.documents[schema_name], schema_name, "$", errors)
        return errors

    def _validate(
        self,
        value: Any,
        schema: Any,
        schema_name: str,
        path: str,
        errors: list[str],
    ) -> None:
        if schema is True:
            return
        if schema is False:
            errors.append(f"{path}: forbidden by schema")
            return
        if not isinstance(schema, dict):
            errors.append(f"{path}: invalid schema node")
            return
        if "$ref" in schema:
            try:
                target, target_name = self.resolve(schema["$ref"], schema_name)
            except (KeyError, TypeError) as exc:
                errors.append(f"{path}: invalid schema reference {schema['$ref']!r}: {exc}")
                return
            self._validate(value, target, target_name, path, errors)
            return
        if "const" in schema and value != schema["const"]:
            errors.append(f"{path}: must equal {schema['const']!r}")
        if "enum" in schema and value not in schema["enum"]:
            errors.append(f"{path}: {value!r} is not an allowed value")

        expected_type = schema.get("type")
        matches_type = {
            "object": isinstance(value, dict),
            "array": isinstance(value, list),
            "string": isinstance(value, str),
            "integer": isinstance(value, int) and not isinstance(value, bool),
            "boolean": isinstance(value, bool),
            "null": value is None,
        }.get(expected_type, True)
        if not matches_type:
            errors.append(f"{path}: expected {expected_type}, found {type(value).__name__}")
            return

        if isinstance(value, dict):
            required = schema.get("required", [])
            for name in required:
                if name not in value:
                    errors.append(f"{path}: missing required property {name!r}")
            properties = schema.get("properties", {})
            additional = schema.get("additionalProperties", True)
            for name, item in value.items():
                item_path = f"{path}.{name}"
                if name in properties:
                    self._validate(item, properties[name], schema_name, item_path, errors)
                elif additional is False:
                    errors.append(f"{item_path}: additional property is forbidden")
                elif isinstance(additional, dict):
                    self._validate(item, additional, schema_name, item_path, errors)
        elif isinstance(value, list):
            if len(value) < schema.get("minItems", 0):
                errors.append(f"{path}: requires at least {schema['minItems']} items")
            if schema.get("uniqueItems"):
                keys = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
                if len(keys) != len(set(keys)):
                    errors.append(f"{path}: items must be unique")
            if "items" in schema:
                for index, item in enumerate(value):
                    self._validate(item, schema["items"], schema_name, f"{path}[{index}]", errors)
        elif isinstance(value, str):
            if len(value) < schema.get("minLength", 0):
                errors.append(f"{path}: string is too short")
            if "pattern" in schema and re.search(schema["pattern"], value) is None:
                errors.append(f"{path}: {value!r} does not match {schema['pattern']!r}")
        elif isinstance(value, int) and not isinstance(value, bool):
            if "minimum" in schema and value < schema["minimum"]:
                errors.append(f"{path}: must be at least {schema['minimum']}")

        if "allOf" in schema:
            for subschema in schema["allOf"]:
                self._validate(value, subschema, schema_name, path, errors)
        if "anyOf" in schema:
            attempts = []
            for subschema in schema["anyOf"]:
                attempt: list[str] = []
                self._validate(value, subschema, schema_name, path, attempt)
                attempts.append(attempt)
            if all(attempts):
                errors.append(f"{path}: does not satisfy any allowed schema")
        if "oneOf" in schema:
            passing = 0
            for subschema in schema["oneOf"]:
                attempt: list[str] = []
                self._validate(value, subschema, schema_name, path, attempt)
                passing += not attempt
            if passing != 1:
                errors.append(f"{path}: must satisfy exactly one allowed schema")


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle, parse_float=lambda value: ("__JSON_FLOAT__", value))


def locate_encoded_floats(value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(value, tuple) and len(value) == 2 and value[0] == "__JSON_FLOAT__":
        return [f"{path}: JSON floating-point value {value[1]} is forbidden; use a plain decimal string"]
    if isinstance(value, dict):
        for key, item in value.items():
            errors.extend(locate_encoded_floats(item, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(locate_encoded_floats(item, f"{path}[{index}]"))
    return errors


def exact(value: Any, path: str, errors: list[str]) -> Decimal | None:
    if not isinstance(value, str):
        errors.append(f"{path}: exact decimal must be a string")
        return None
    if re.fullmatch(r"-?(0|[1-9][0-9]*)(\.[0-9]+)?", value) is None:
        errors.append(f"{path}: invalid plain exact-decimal string {value!r}")
        return None
    try:
        result = Decimal(value)
    except InvalidOperation:
        errors.append(f"{path}: invalid decimal {value!r}")
        return None
    if not result.is_finite():
        errors.append(f"{path}: non-finite decimal is forbidden")
        return None
    return result


def reference_errors(values: list[str], event_ids: set[str], path: str) -> list[str]:
    return [f"{path}: unknown causal event {value!r}" for value in values if value not in event_ids]


def semantic_delta(
    document: dict[str, Any],
    decision_ids: set[str],
    parameter_set_ids: set[str],
) -> list[str]:
    errors = locate_encoded_floats(document)
    events = document.get("events", [])
    chapter_id = document.get("chapter_id")
    event_ids: set[str] = set()
    sequences: list[int] = []
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            continue
        event_id = event.get("event_id")
        if event_id in event_ids:
            errors.append(f"$.events[{index}].event_id: duplicate event ID {event_id!r}")
        if isinstance(event_id, str):
            event_ids.add(event_id)
        if event.get("chapter_id") != chapter_id:
            errors.append(f"$.events[{index}].chapter_id: does not match delta chapter_id")
        sequence = event.get("sequence")
        if isinstance(sequence, int) and not isinstance(sequence, bool):
            sequences.append(sequence)
    if sequences != list(range(1, len(sequences) + 1)):
        errors.append("$.events: sequence values must be contiguous, unique, ordered, and start at 1")

    claim_ids: set[str] = set()
    progression_ids: set[str] = set()
    for index, progression in enumerate(document.get("progression_events", [])):
        if not isinstance(progression, dict):
            continue
        path = f"$.progression_events[{index}]"
        if progression.get("chapter_id") != chapter_id:
            errors.append(f"{path}.chapter_id: does not match delta chapter_id")
        progression_id = progression.get("progression_event_id")
        if progression_id in progression_ids:
            errors.append(f"{path}.progression_event_id: duplicate progression event ID")
        if isinstance(progression_id, str):
            progression_ids.add(progression_id)
        source_event_id = progression.get("source_event_id")
        if source_event_id not in event_ids:
            errors.append(f"{path}.source_event_id: unknown causal event {source_event_id!r}")
        provenance = progression.get("provenance", {})
        errors.extend(reference_errors(provenance.get("source_event_ids", []), event_ids, f"{path}.provenance.source_event_ids"))
        claim_id = provenance.get("reward_claim_id")
        if claim_id in claim_ids:
            errors.append(f"{path}.provenance.reward_claim_id: duplicate reward claim {claim_id!r}")
        if isinstance(claim_id, str):
            claim_ids.add(claim_id)
        mechanism_refs = set(provenance.get("mechanism_decision_refs", []))
        authority_refs = set(progression.get("cal0_authority", {}).get("decision_refs", []))
        parameter_set_id = progression.get("cal0_authority", {}).get("parameter_set_id")
        if parameter_set_id not in parameter_set_ids:
            errors.append(f"{path}.cal0_authority.parameter_set_id: unknown CAL0 parameter set {parameter_set_id!r}")
        for decision_ref in mechanism_refs | authority_refs:
            if decision_ref not in decision_ids:
                errors.append(f"{path}: unknown CAL0 selected-option reference {decision_ref!r}")
        if not mechanism_refs.issubset(authority_refs):
            errors.append(f"{path}: provenance decisions must be included in cal0_authority.decision_refs")
        if progression.get("retrospective_reclassification") is not False:
            errors.append(f"{path}.retrospective_reclassification: retrospective relabelling is forbidden")
        operation = progression.get("operation")
        track_kind = progression.get("track", {}).get("kind")
        if operation == "XP_GAIN" and track_kind in {"SKILL", "CLASS"}:
            eligibility = progression.get("eligibility", {})
            if not isinstance(eligibility, dict) or not eligibility.get("prior_state_ref"):
                errors.append(f"{path}.eligibility: Skill/Class XP requires prior accepted-state evidence")
            elif eligibility.get("prior_state_ref") not in document.get("base_snapshot_ids", []):
                errors.append(f"{path}.eligibility.prior_state_ref: must name a base snapshot of this delta")
            if eligibility.get("accepted_lineage_id") != progression.get("track", {}).get("lineage_id"):
                errors.append(f"{path}.eligibility.accepted_lineage_id: must match the awarded track lineage")
        if operation == "NATURAL_MATURATION" and track_kind in {"SKILL", "CLASS"}:
            errors.append(f"{path}: natural maturation cannot award Skill or Class progression")
        if operation == "ATTRIBUTE_ADAPTATION" and track_kind != "ATTRIBUTE":
            errors.append(f"{path}: attribute adaptation must use an ATTRIBUTE track")
        before = exact(progression.get("before_value"), f"{path}.before_value", errors)
        amount = exact(progression.get("amount"), f"{path}.amount", errors)
        after = exact(progression.get("after_value"), f"{path}.after_value", errors)
        additive_operations = {
            "XP_GAIN",
            "REINFORCEMENT_CLAIMED",
            "ASSIMILATION_PROGRESS",
            "NATURAL_MATURATION",
            "ATTRIBUTE_ADAPTATION",
            "RESOURCE_CHANGE",
        }
        if (
            operation in additive_operations
            and before is not None
            and amount is not None
            and after is not None
            and before + amount != after
        ):
            errors.append(f"{path}: before_value + amount must equal after_value exactly")
        if "attribution_share" in provenance:
            share = exact(provenance["attribution_share"], f"{path}.provenance.attribution_share", errors)
            if share is not None and not Decimal("0") <= share <= Decimal("1"):
                errors.append(f"{path}.provenance.attribution_share: must be between 0 and 1")

    seen_change_ids: set[str] = set()
    for index, change in enumerate(document.get("character_changes", [])):
        if not isinstance(change, dict):
            continue
        change_id = change.get("change_id")
        if change_id in seen_change_ids:
            errors.append(f"$.character_changes[{index}].change_id: duplicate change ID {change_id!r}")
        if isinstance(change_id, str):
            seen_change_ids.add(change_id)

    seen_proposal_ids: set[str] = set()
    for index, proposal in enumerate(document.get("canon_proposals", [])):
        if not isinstance(proposal, dict):
            continue
        proposal_id = proposal.get("proposal_id")
        if proposal_id in seen_proposal_ids:
            errors.append(f"$.canon_proposals[{index}].proposal_id: duplicate canon proposal ID {proposal_id!r}")
        if isinstance(proposal_id, str):
            seen_proposal_ids.add(proposal_id)

    for collection_name in ("character_changes", "thread_changes", "canon_proposals"):
        for index, record in enumerate(document.get(collection_name, [])):
            if isinstance(record, dict):
                errors.extend(reference_errors(record.get("source_event_ids", []), event_ids, f"$.{collection_name}[{index}].source_event_ids"))
                if collection_name == "character_changes" and record.get("value_type") == "EXACT_DECIMAL":
                    if "before" in record:
                        exact(record["before"], f"$.{collection_name}[{index}].before", errors)
                    if "after" in record:
                        exact(record["after"], f"$.{collection_name}[{index}].after", errors)
                if collection_name == "canon_proposals" and record.get("chapter_id") != chapter_id:
                    errors.append(f"$.{collection_name}[{index}].chapter_id: does not match delta chapter_id")

    required_reviews = {
        "LOCAL_COLOUR": "CHAPTER_ACCEPTANCE",
        "SETTING_EXTENSION": "WORLDBUILDING_REVIEW",
        "CHARACTER_STATE_CHANGE": "CONTINUITY_REVIEW",
        "SYSTEM_APPLICATION": "CAL0_MECHANICS_REVIEW",
        "SYSTEM_CHANGE": "AUTHOR_DECISION_REQUIRED",
        "CONTRADICTION_OR_RETCON": "AUTHOR_DECISION_REQUIRED",
    }
    delta_approval_id = document.get("author_approval", {}).get("decision_id")
    for index, proposal in enumerate(document.get("canon_proposals", [])):
        if not isinstance(proposal, dict):
            continue
        path = f"$.canon_proposals[{index}]"
        classification = proposal.get("classification")
        expected_review = required_reviews.get(classification)
        if expected_review is not None and proposal.get("required_review") != expected_review:
            errors.append(
                f"{path}.required_review: {classification} requires {expected_review}"
            )
        if proposal.get("classification") in {"SYSTEM_CHANGE", "CONTRADICTION_OR_RETCON"}:
            if proposal.get("status") == "ACCEPTED":
                approval = proposal.get("author_approval", {})
                if approval.get("decision") != "ACCEPT":
                    errors.append(f"{path}: accepted System change or retcon lacks separate Author acceptance")
                if document.get("status") == "ACCEPTED" and approval.get("decision_id") == delta_approval_id:
                    errors.append(
                        f"{path}.author_approval.decision_id: System change or retcon must use "
                        "a decision distinct from chapter-delta acceptance"
                    )
        if proposal.get("status") == "ACCEPTED" and proposal.get("author_approval", {}).get("decision") != "ACCEPT":
            errors.append(f"{path}: accepted proposal lacks Author acceptance")

    if document.get("status") == "ACCEPTED":
        approval = document.get("author_approval", {})
        if approval.get("decision") != "ACCEPT":
            errors.append("$.author_approval: accepted delta lacks Author acceptance")
        manuscript = document.get("manuscript")
        if not isinstance(manuscript, dict):
            errors.append("$.manuscript: accepted delta requires a manuscript binding")
        else:
            manuscript_path = manuscript.get("path")
            if not isinstance(manuscript_path, str):
                errors.append("$.manuscript.path: accepted delta requires a repository-relative path")
            elif (
                "\\" in manuscript_path
                or Path(manuscript_path).is_absolute()
                or re.match(r"^[A-Za-z]:/", manuscript_path) is not None
                or Path(manuscript_path).as_posix() != manuscript_path
                or any(part in {"", ".", ".."} for part in Path(manuscript_path).parts)
            ):
                errors.append("$.manuscript.path: absolute, traversal, empty, and non-normalized paths are forbidden")
            else:
                candidate = (REPOSITORY_ROOT / manuscript_path).resolve()
                try:
                    candidate.relative_to(REPOSITORY_ROOT.resolve())
                except ValueError:
                    errors.append("$.manuscript.path: path resolves outside the repository")
                else:
                    if not candidate.is_file():
                        errors.append(f"$.manuscript.path: bound manuscript does not exist: {manuscript_path!r}")
                    else:
                        digest = "sha256:" + hashlib.sha256(candidate.read_bytes()).hexdigest()
                        if manuscript.get("sha256") != digest:
                            errors.append("$.manuscript.sha256: digest does not match bound manuscript bytes")
        if document.get("review", {}).get("blocking_findings"):
            errors.append("$.review.blocking_findings: accepted delta cannot retain blocking findings")
        if document.get("review", {}).get("major_findings"):
            errors.append("$.review.major_findings: accepted delta cannot retain major findings")
        for index, proposal in enumerate(document.get("canon_proposals", [])):
            if (
                isinstance(proposal, dict)
                and proposal.get("classification") in {"SYSTEM_CHANGE", "CONTRADICTION_OR_RETCON"}
                and proposal.get("status") == "PROPOSED"
            ):
                errors.append(
                    f"$.canon_proposals[{index}]: accepted delta cannot retain an unresolved proposed "
                    "System change or retcon"
                )
    return errors


def semantic_character_state(document: dict[str, Any]) -> list[str]:
    errors = locate_encoded_floats(document)
    for resource_id, resource in document.get("resources", {}).items():
        if not isinstance(resource, dict):
            continue
        current = exact(resource.get("current"), f"$.resources.{resource_id}.current", errors)
        capacity = exact(resource.get("capacity"), f"$.resources.{resource_id}.capacity", errors)
        if current is not None and capacity is not None and current > capacity:
            errors.append(f"$.resources.{resource_id}: current exceeds capacity")
    seen_tracks: set[tuple[Any, Any]] = set()
    for index, track in enumerate(document.get("progression", [])):
        if not isinstance(track, dict):
            continue
        key = (track.get("kind"), track.get("track_id"))
        if key in seen_tracks:
            errors.append(f"$.progression[{index}]: duplicate progression track {key!r}")
        seen_tracks.add(key)
    for index, condition in enumerate(document.get("conditions", [])):
        if not isinstance(condition, dict):
            continue
        severity = exact(condition.get("severity"), f"$.conditions[{index}].severity", errors)
        if severity is not None and not Decimal("0") <= severity <= Decimal("1"):
            errors.append(f"$.conditions[{index}].severity: must be between 0 and 1")
    return errors


def schema_health(schemas: SchemaSet) -> list[str]:
    errors: list[str] = []
    ids: set[str] = set()

    def walk(value: Any, schema_name: str, path: str) -> None:
        if isinstance(value, tuple):
            errors.append(f"{schema_name}:{path}: JSON float is forbidden in schema documents")
        elif isinstance(value, dict):
            if "$ref" in value:
                try:
                    schemas.resolve(value["$ref"], schema_name)
                except (KeyError, TypeError) as exc:
                    errors.append(f"{schema_name}:{path}: unresolved $ref: {exc}")
            if "required" in value and "properties" in value:
                missing = set(value["required"]) - set(value["properties"])
                if missing:
                    errors.append(f"{schema_name}:{path}: required properties not declared: {sorted(missing)}")
            for name, item in value.items():
                walk(item, schema_name, f"{path}/{name}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                walk(item, schema_name, f"{path}/{index}")

    for name, document in schemas.documents.items():
        if document.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{name}: unsupported or missing $schema")
        schema_id = document.get("$id")
        if not isinstance(schema_id, str) or schema_id in ids:
            errors.append(f"{name}: missing or duplicate $id")
        else:
            ids.add(schema_id)
        walk(document, name, "#")
    return errors


def validate_file(
    path: Path,
    schemas: SchemaSet,
    decision_ids: set[str],
    parameter_set_ids: set[str],
) -> list[str]:
    document = load_json(path)
    errors = locate_encoded_floats(document)
    if path.name.endswith(".chapter-delta.json"):
        schema_name = "chapter-delta.schema.json"
        errors.extend(schemas.validate(document, schema_name))
        if isinstance(document, dict):
            errors.extend(semantic_delta(document, decision_ids, parameter_set_ids))
    elif path.name.endswith(".character-state.json"):
        schema_name = "character-state.schema.json"
        errors.extend(schemas.validate(document, schema_name))
        if isinstance(document, dict):
            errors.extend(semantic_character_state(document))
    elif path.name.endswith(".chapter-event.json"):
        errors.extend(schemas.validate(document, "chapter-event.schema.json"))
    elif path.name.endswith(".progression-event.json"):
        errors.extend(schemas.validate(document, "progression-event.schema.json"))
    elif path.name.endswith(".canon-proposal.json"):
        errors.extend(schemas.validate(document, "canon-proposal.schema.json"))
    else:
        errors.append(f"unsupported integration-document suffix: {path.name}")
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path, help="specific story-integration JSON documents")
    args = parser.parse_args()
    schemas = SchemaSet(SCHEMA_ROOT)
    errors = schema_health(schemas)
    if not DECISION_INDEX.exists():
        errors.append("generated architecture-decision index is missing")
        decision_ids: set[str] = set()
    else:
        decision_document = load_json(DECISION_INDEX)
        decision_ids = {item["selected_option_id"] for item in decision_document["decisions"]}
    parameter_set_ids: set[str] = set()
    try:
        i3_registry = load_json(I3_PARAMETER_REGISTRY)
        parameter_set_ids.update(
            item["parameter_set_id"] for item in i3_registry["parameter_sets"]
        )
        i4_assessment = load_json(I4_PARAMETER_ASSESSMENT)
        parameter_set_ids.add(i4_assessment["parameter_set_id"])
        parameter_set_ids.add(i4_assessment["parent_parameter_set_id"])
    except (KeyError, OSError, json.JSONDecodeError) as exc:
        errors.append(f"could not load CAL0 parameter-set authorities: {exc}")

    if args.paths:
        for path in args.paths:
            file_errors = validate_file(path, schemas, decision_ids, parameter_set_ids)
            errors.extend(f"{path}: {error}" for error in file_errors)
        expected_valid = len(args.paths)
        expected_invalid = 0
    else:
        valid_paths = sorted((FIXTURE_ROOT / "valid").glob("*.json"))
        invalid_paths = sorted((FIXTURE_ROOT / "invalid").glob("*.json"))
        expected_valid = len(valid_paths)
        expected_invalid = len(invalid_paths)
        for path in valid_paths:
            file_errors = validate_file(path, schemas, decision_ids, parameter_set_ids)
            errors.extend(f"{path.relative_to(REPOSITORY_ROOT)}: {error}" for error in file_errors)
        for path in invalid_paths:
            file_errors = validate_file(path, schemas, decision_ids, parameter_set_ids)
            if not file_errors:
                errors.append(f"{path.relative_to(REPOSITORY_ROOT)}: invalid fixture unexpectedly passed")
                continue
            expected = INVALID_EXPECTATIONS.get(path.name)
            if expected is None:
                errors.append(f"{path.relative_to(REPOSITORY_ROOT)}: invalid fixture lacks a targeted expectation")
            elif not any(expected in error for error in file_errors):
                errors.append(
                    f"{path.relative_to(REPOSITORY_ROOT)}: expected failure containing {expected!r}; "
                    f"found {file_errors}"
                )

    if errors:
        print("story-integration validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(
        f"story-integration validation passed: {len(schemas.documents)} schemas, "
        f"{expected_valid} valid fixture(s), {expected_invalid} rejected fixture(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
