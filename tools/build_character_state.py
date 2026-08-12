#!/usr/bin/env python3
"""Deterministically derive a bounded character snapshot from one accepted delta."""

from __future__ import annotations

import argparse
from copy import deepcopy
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STORY_VALIDATOR = ROOT / "litrpg-system/story-integration/validators/validate.py"
CAL0_SRC = ROOT / "litrpg-system/cal0/src"
I3_PARAMETERS = ROOT / "litrpg-system/cal0/registries/cal0-i3-parameters.json"
I4_ASSESSMENT = ROOT / "litrpg-system/cal0/registries/cal0-i4-parameter-assessment.json"
sys.path.insert(0, str(CAL0_SRC))
from cal0.engines import xp_threshold  # noqa: E402


class DerivationError(ValueError):
    pass


def load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(
            handle,
            parse_float=lambda raw: (_ for _ in ()).throw(
                DerivationError(f"{path}: JSON floats are forbidden; use exact-decimal strings")
            ),
        )
    if not isinstance(value, dict):
        raise DerivationError(f"{path}: root must be an object")
    return value


def exact(value: Any, label: str) -> Decimal:
    if not isinstance(value, str):
        raise DerivationError(f"{label}: exact decimal must be a string")
    try:
        decimal = Decimal(value)
    except InvalidOperation as exc:
        raise DerivationError(f"{label}: invalid decimal {value!r}") from exc
    if not decimal.is_finite() or format(decimal, "f") != value:
        raise DerivationError(f"{label}: decimal must use plain canonical notation")
    return decimal


def plain(value: Decimal) -> str:
    rendered = format(value, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return "0" if rendered in {"", "-0"} else rendered


def require_new_snapshot_identity(snapshot_id: Any, work_id: Any, base_snapshot_id: Any) -> None:
    """Require a new typed snapshot URI in the exact namespace of the work."""
    if not isinstance(work_id, str):
        raise DerivationError("work_id must be a typed work URI")
    match = re.fullmatch(
        r"work://(series|standalone-novel|novella|short-story|experiment)/"
        r"([a-z0-9]+(?:-[a-z0-9]+)*)",
        work_id,
    )
    if match is None:
        raise DerivationError("work_id must use work://<type>/<slug> without extra scope segments")
    work_type, slug = match.groups()
    expected = rf"snapshot://{re.escape(work_type)}/{re.escape(slug)}/"
    local_path = r"[a-z0-9]+(?:-[a-z0-9]+)*(?:/[a-z0-9]+(?:-[a-z0-9]+)*)*"
    if not isinstance(snapshot_id, str) or re.fullmatch(expected + local_path, snapshot_id) is None:
        raise DerivationError(
            f"new snapshot_id must be a snapshot URI in the same work namespace {work_id!r}"
        )
    if snapshot_id == base_snapshot_id:
        raise DerivationError("new snapshot_id must differ from the base snapshot_id")


def validate_contract_files(*paths: Path, label: str) -> None:
    """Run the canonical schema/semantic gate for reducer inputs or output."""
    result = subprocess.run(
        [sys.executable, str(STORY_VALIDATOR), *(str(path) for path in paths)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "validator returned no detail"
        raise DerivationError(f"{label} contract validation failed:\n{detail}")


def next_xp_threshold(event: dict[str, Any], record: dict[str, Any]) -> Decimal:
    parameter_set_id = event["cal0_authority"]["parameter_set_id"]
    registry = load(I3_PARAMETERS)
    values = {
        binding["parameter_id"]: binding["value"]
        for binding in registry["bindings"]
        if "value" in binding
    }
    if parameter_set_id == "parameter-set://cal0/i4-reference@1":
        values.update(load(I4_ASSESSMENT)["final_overrides"])
    elif parameter_set_id != "parameter-set://cal0/i3-reference@1":
        raise DerivationError(f"unsupported CAL0 parameter set {parameter_set_id!r}")
    prefix = "skill" if record["kind"] == "SKILL" else "class"
    level = exact(record["level"], f"{event['progression_event_id']}.prior_level")
    if level < 0 or level != level.to_integral_value():
        raise DerivationError(f"{event['progression_event_id']}: bounded XP reducer requires an integral level")
    threshold = int(level) + 1
    count = values[f"parameter://cal0/xp/{prefix}-threshold-count@1"]
    if not isinstance(count, int) or threshold > count:
        raise DerivationError(
            f"{event['progression_event_id']}: XP at the form boundary requires a typed evolution reducer"
        )
    total = exact(str(values[f"parameter://cal0/xp/{prefix}-total-scale@1"]), "CAL0 total scale")
    exponent = exact(str(values[f"parameter://cal0/xp/{prefix}-exponent@1"]), "CAL0 XP exponent")
    return xp_threshold(total, threshold, count, exponent)


def pointer_target(document: dict[str, Any], pointer: str) -> tuple[dict[str, Any], str]:
    if not pointer.startswith("/") or pointer.endswith("/"):
        raise DerivationError(f"unsupported state path {pointer!r}: canonical JSON pointer required")
    tokens = [token.replace("~1", "/").replace("~0", "~") for token in pointer[1:].split("/")]
    allowed = (
        len(tokens) == 2 and tokens[0] == "attributes"
    ) or (
        len(tokens) == 3 and tokens[0] == "resources" and tokens[2] in {"current", "capacity"}
    ) or tokens == ["location_id"]
    if not allowed:
        raise DerivationError(f"unsupported state path {pointer!r} in bounded reducer")
    target: Any = document
    for token in tokens[:-1]:
        if not isinstance(target, dict) or token not in target:
            raise DerivationError(f"state path {pointer!r} does not exist in the base snapshot")
        target = target[token]
    if not isinstance(target, dict):
        raise DerivationError(f"state path {pointer!r} has a non-object parent")
    return target, tokens[-1]


def apply_character_change(state: dict[str, Any], change: dict[str, Any]) -> None:
    target, key = pointer_target(state, change["path"])
    if key not in target:
        raise DerivationError(f"state path {change['path']!r} does not exist in the base snapshot")
    if target[key] != change.get("before"):
        raise DerivationError(f"{change['change_id']}: declared before value does not match base state")
    operation = change["operation"]
    value_type = change["value_type"]
    if operation == "ADD":
        if value_type != "EXACT_DECIMAL":
            raise DerivationError(f"{change['change_id']}: ADD is supported only for exact decimals")
        before = exact(change["before"], f"{change['change_id']}.before")
        after = exact(change["after"], f"{change['change_id']}.after")
        # The delta records the resulting value, not a second unrecorded amount.
        if after < before:
            raise DerivationError(f"{change['change_id']}: bounded ADD cannot reduce a value")
        target[key] = plain(after)
    elif operation == "SET":
        if value_type == "EXACT_DECIMAL":
            exact(change["after"], f"{change['change_id']}.after")
        target[key] = deepcopy(change["after"])
    else:
        raise DerivationError(f"{change['change_id']}: unsupported reducer operation {operation}")


def apply_xp(state: dict[str, Any], event: dict[str, Any]) -> None:
    if event["operation"] != "XP_GAIN" or event["track"]["kind"] not in {"SKILL", "CLASS"}:
        raise DerivationError(
            f"{event['progression_event_id']}: bounded reducer supports only Skill/Class XP_GAIN; "
            "other accepted operations require a typed reducer extension"
        )
    track = event["track"]
    candidates = [
        record for record in state["progression"]
        if record["kind"] == track["kind"] and record["track_id"] == track["track_id"]
    ]
    if len(candidates) != 1:
        raise DerivationError(f"{event['progression_event_id']}: expected exactly one prior progression track")
    record = candidates[0]
    if record.get("lineage_id") != track.get("lineage_id"):
        raise DerivationError(f"{event['progression_event_id']}: lineage differs from prior state")
    before = exact(event["before_value"], f"{event['progression_event_id']}.before_value")
    amount = exact(event["amount"], f"{event['progression_event_id']}.amount")
    after = exact(event["after_value"], f"{event['progression_event_id']}.after_value")
    if exact(record["xp"], f"{event['progression_event_id']}.prior_xp") != before:
        raise DerivationError(f"{event['progression_event_id']}: prior XP does not match base snapshot")
    if before + amount != after:
        raise DerivationError(f"{event['progression_event_id']}: exact XP arithmetic failed")
    if amount <= 0:
        raise DerivationError(f"{event['progression_event_id']}: XP_GAIN amount must be positive")
    threshold = next_xp_threshold(event, record)
    if before >= threshold or after >= threshold:
        raise DerivationError(
            f"{event['progression_event_id']}: XP crosses the next CAL0 threshold; "
            "level and reinforcement require a typed reducer extension"
        )
    record["xp"] = plain(after)
    provenance_refs = record.setdefault("provenance_refs", [])
    for reference in (
        event["progression_event_id"],
        event["provenance"]["provenance_id"],
        event["provenance"]["reward_claim_id"],
    ):
        if reference not in provenance_refs:
            provenance_refs.append(reference)


def derive(base: dict[str, Any], delta: dict[str, Any], snapshot_id: str) -> dict[str, Any]:
    if delta.get("status") != "ACCEPTED":
        raise DerivationError("only accepted deltas may produce authoritative snapshots")
    if delta.get("author_approval", {}).get("decision") != "ACCEPT":
        raise DerivationError("accepted delta lacks an explicit Author acceptance decision")
    review = delta.get("review", {})
    if review.get("blocking_findings") or review.get("major_findings"):
        raise DerivationError("accepted delta retains blocking or major findings")
    if not isinstance(delta.get("manuscript"), dict):
        raise DerivationError("accepted delta lacks an immutable manuscript binding")
    if base.get("work_id") != delta.get("work_id"):
        raise DerivationError("base snapshot and delta belong to different works")
    require_new_snapshot_identity(snapshot_id, base.get("work_id"), base.get("snapshot_id"))
    if base.get("snapshot_id") not in delta.get("base_snapshot_ids", []):
        raise DerivationError("delta does not name the supplied base snapshot")
    character_ids = {change.get("character_id") for change in delta.get("character_changes", [])}
    character_ids.update(event.get("actor_id") for event in delta.get("progression_events", []))
    if character_ids - {base.get("character_id")}:
        raise DerivationError("delta includes changes for a different character")

    state = deepcopy(base)
    for change in delta.get("character_changes", []):
        apply_character_change(state, change)
    for event in delta.get("progression_events", []):
        apply_xp(state, event)
    state["snapshot_id"] = snapshot_id
    state["as_of_chapter_id"] = delta["chapter_id"]
    state["as_of_event_sequence"] = max(event["sequence"] for event in delta["events"])
    state["derived_from_delta_ids"] = [*base["derived_from_delta_ids"], delta["delta_id"]]
    return state


def rendered(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--delta", type=Path, required=True)
    parser.add_argument("--snapshot-id", required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path, help="compare derived output with an existing snapshot")
    args = parser.parse_args()
    try:
        validate_contract_files(args.base, args.delta, label="input")
        result = derive(load(args.base), load(args.delta), args.snapshot_id)
        output = rendered(result)
        with tempfile.TemporaryDirectory(prefix="character-state-validation-") as temporary:
            validation_path = Path(temporary) / "derived.character-state.json"
            validation_path.write_text(output, encoding="utf-8", newline="\n")
            validate_contract_files(validation_path, label="derived snapshot")
    except (OSError, json.JSONDecodeError, KeyError, DerivationError) as exc:
        print(f"state derivation failed: {exc}", file=sys.stderr)
        return 1
    if args.check:
        if not args.check.is_file() or args.check.read_text(encoding="utf-8") != output:
            print(f"derived state differs from {args.check}", file=sys.stderr)
            return 1
        print(f"verified deterministic state derivation against {args.check}")
    elif args.output:
        args.output.write_text(output, encoding="utf-8", newline="\n")
        print(f"wrote {args.output}")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
