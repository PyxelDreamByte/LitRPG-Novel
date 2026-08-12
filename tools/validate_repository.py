#!/usr/bin/env python3
"""Dependency-free validation entrypoint for repository structure and content."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return {}, [f"{path.relative_to(ROOT)}: missing opening YAML frontmatter delimiter"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, [f"{path.relative_to(ROOT)}: missing closing YAML frontmatter delimiter"]
    values: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([A-Za-z][A-Za-z0-9_-]*):\s*(.*?)\s*", line)
        if match is None:
            errors.append(f"{path.relative_to(ROOT)}:{line_number}: unsupported frontmatter syntax")
            continue
        key, raw = match.groups()
        if key in values:
            errors.append(f"{path.relative_to(ROOT)}:{line_number}: duplicate frontmatter key {key!r}")
            continue
        if raw.startswith(('"', "'")):
            if raw.startswith('"'):
                try:
                    value = json.loads(raw)
                except json.JSONDecodeError as exc:
                    errors.append(f"{path.relative_to(ROOT)}:{line_number}: invalid quoted scalar: {exc.msg}")
                    continue
            elif raw.endswith("'"):
                value = raw[1:-1].replace("''", "'")
            else:
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: unterminated quoted scalar")
                continue
        else:
            value = raw
        if not isinstance(value, str):
            errors.append(f"{path.relative_to(ROOT)}:{line_number}: frontmatter values must be strings")
            continue
        values[key] = value
    return values, errors


def validate_skills() -> tuple[list[str], int]:
    errors: list[str] = []
    skills_root = ROOT / ".agents/skills"
    if not skills_root.is_dir():
        return [".agents/skills: directory is missing"], 0
    directories = sorted(path for path in skills_root.iterdir() if path.is_dir())
    skill_files = sorted(skills_root.glob("*/SKILL.md"))
    for directory in directories:
        if not (directory / "SKILL.md").is_file():
            errors.append(f"{directory.relative_to(ROOT)}: skill directory lacks SKILL.md")
    for path in skill_files:
        frontmatter, parse_errors = parse_frontmatter(path)
        errors.extend(parse_errors)
        expected_name = path.parent.name
        if frontmatter.get("name") != expected_name:
            errors.append(
                f"{path.relative_to(ROOT)}: frontmatter name {frontmatter.get('name')!r} "
                f"does not match directory {expected_name!r}"
            )
        if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", expected_name) is None:
            errors.append(f"{path.relative_to(ROOT)}: skill directory is not a lowercase hyphenated name")
        if not frontmatter.get("description", "").strip():
            errors.append(f"{path.relative_to(ROOT)}: frontmatter description is required")
    return errors, len(skill_files)


def find_model_pins(value: Any, path: str = "$") -> list[str]:
    pins: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            item_path = f"{path}.{key}"
            if key == "model" or key.startswith("model_"):
                pins.append(item_path)
            pins.extend(find_model_pins(item, item_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            pins.extend(find_model_pins(item, f"{path}[{index}]"))
    return pins


def validate_codex_configuration() -> tuple[list[str], int]:
    errors: list[str] = []
    config_path = ROOT / ".codex/config.toml"
    if not config_path.is_file():
        errors.append(".codex/config.toml: file is missing")
    else:
        try:
            config = tomllib.loads(config_path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            errors.append(f".codex/config.toml: invalid TOML: {exc}")
            config = {}
        thread_count = config.get("agents", {}).get("max_concurrent_threads_per_session")
        if not isinstance(thread_count, int) or isinstance(thread_count, bool) or thread_count < 1:
            errors.append(".codex/config.toml: agents.max_concurrent_threads_per_session must be a positive integer")
        for pin in find_model_pins(config):
            errors.append(f".codex/config.toml:{pin}: repository model pins are forbidden")

    agents_root = ROOT / ".codex/agents"
    if not agents_root.is_dir():
        return errors + [".codex/agents: directory is missing"], 0
    agent_files = sorted(agents_root.glob("*.toml"))
    for path in agent_files:
        relative = path.relative_to(ROOT)
        try:
            document = tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            errors.append(f"{relative}: invalid TOML: {exc}")
            continue
        for field in ("name", "description", "developer_instructions"):
            if not isinstance(document.get(field), str) or not document[field].strip():
                errors.append(f"{relative}: required non-empty string field {field!r} is missing")
        name = document.get("name")
        if isinstance(name, str) and name != path.stem:
            errors.append(f"{relative}: agent name {name!r} does not match filename {path.stem!r}")
        for pin in find_model_pins(document):
            errors.append(f"{relative}:{pin}: repository model pins are forbidden")
        description = str(document.get("description", "")).lower()
        reviewer = (
            isinstance(name, str)
            and (
                name.endswith("-auditor")
                or name in {"story-architect", "prose-editor"}
                or "read-only" in description
            )
        )
        if reviewer and document.get("sandbox_mode") != "read-only":
            errors.append(f"{relative}: reviewer/auditor agents must set sandbox_mode = \"read-only\"")
    return errors, len(agent_files)


def reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def validate_non_cal0_json() -> tuple[list[str], int]:
    errors: list[str] = []
    count = 0
    for path in sorted(ROOT.rglob("*.json")):
        relative = path.relative_to(ROOT)
        if relative.parts[:2] == ("litrpg-system", "cal0"):
            continue
        count += 1
        try:
            json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_json_keys)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{relative}: invalid JSON: {exc}")
    return errors, count


def main() -> int:
    errors: list[str] = []
    skill_errors, skill_count = validate_skills()
    agent_errors, agent_count = validate_codex_configuration()
    json_errors, json_count = validate_non_cal0_json()
    errors.extend(skill_errors)
    errors.extend(agent_errors)
    errors.extend(json_errors)
    if errors:
        print("repository structure validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(
        f"repository structure passed: {skill_count} skills, {agent_count} custom agents, "
        f"{json_count} non-CAL0 JSON files",
        flush=True,
    )
    try:
        subprocess.run([sys.executable, "tools/validate_system.py"], cwd=ROOT, check=True)
    except subprocess.CalledProcessError as exc:
        return exc.returncode or 1
    print("\nComplete repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
