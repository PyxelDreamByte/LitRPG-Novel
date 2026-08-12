#!/usr/bin/env python3
"""Build deterministic routing indexes for the monolithic CAL0 specification."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = REPOSITORY_ROOT / "litrpg-system/cal0/canonical/litrpg-system-specification.md"
MANIFEST_PATH = REPOSITORY_ROOT / "litrpg-system/cal0/manifests/cal0-i7.bundle.json"
OUTPUT_ROOT = REPOSITORY_ROOT / "litrpg-system/indices"

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
SECTION_CODE_RE = re.compile(r"^([A-Z][A-Z0-9]*(?:\.[0-9]+)*)\s+—\s+(.+)$")
SELECTED_RE = re.compile(r"^\*\*Selected option:\s+(.+?)\s+—\s+(.+?)\*\*\s*$")
STATUS_RE = re.compile(r"^\*\*Status:\s+(.+?)\*\*\s*$")
VERSION_RE = re.compile(r"^\*\*Specification version:\*\*\s+(.+?)\s*$")

TOPICS = (
    ("attributes", "Attributes, growth, reinforcement, and life stages", ("ATR",)),
    ("resources", "Resources, condition, action, Soul, and checks", ("RES",)),
    ("skills", "Skill identity, progression, evolution, and transmission", ("SKL",)),
    ("traits", "Traits, ancestry, bloodlines, and alterations", ("TRT",)),
    ("classes", "Class offers, advancement, rewards, and evolution", ("CLS",)),
    ("progression", "XP, achievements, titles, quests, and rarity", ("PRG",)),
    ("magic", "Spells, casting, magical research, and distributed systems", ("MAG",)),
    ("items", "Items, equipment, storage, crafting, and loot", ("ITM",)),
    ("society", "Parties, companions, factions, and reputation", ("SOC",)),
    ("interface", "Interface, notifications, information, and privacy", ("UI",)),
    ("world", "Awakening, creatures, exceptional places, and ecology", ("WLD",)),
    ("protagonist", "Protagonist continuity, prenatal access, and Mage trajectory", ("PRO",)),
    ("validation", "Calibration, adversarial validation, and closure", ("VAL",)),
)


@dataclass
class Heading:
    level: int
    title: str
    anchor: str
    line_start: int
    line_end: int = 0
    section_code: str | None = None
    section_title: str | None = None
    parent_anchors: tuple[str, ...] = ()


def github_anchor(title: str, seen: dict[str, int]) -> str:
    value = title.strip().lower()
    value = re.sub(r"[^\w\- ]", "", value, flags=re.UNICODE)
    value = value.replace(" ", "-")
    count = seen.get(value, 0)
    seen[value] = count + 1
    return value if count == 0 else f"{value}-{count}"


def parse_specification(text: str) -> tuple[list[Heading], list[dict[str, object]], str]:
    lines = text.splitlines()
    seen: dict[str, int] = {}
    headings: list[Heading] = []
    stack: list[Heading] = []
    version = "UNKNOWN"

    for number, line in enumerate(lines, start=1):
        version_match = VERSION_RE.match(line)
        if version_match:
            version = version_match.group(1)
        match = HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        title = match.group(2)
        while stack and stack[-1].level >= level:
            stack.pop()
        section_match = SECTION_CODE_RE.match(title)
        heading = Heading(
            level=level,
            title=title,
            anchor=github_anchor(title, seen),
            line_start=number,
            section_code=section_match.group(1) if section_match else None,
            section_title=section_match.group(2) if section_match else None,
            parent_anchors=tuple(parent.anchor for parent in stack),
        )
        headings.append(heading)
        stack.append(heading)

    for index, heading in enumerate(headings):
        heading.line_end = len(lines)
        for candidate in headings[index + 1 :]:
            if candidate.level <= heading.level:
                heading.line_end = candidate.line_start - 1
                break

    decisions: list[dict[str, object]] = []
    heading_index = 0
    active_heading: Heading | None = None
    active_status = "UNSPECIFIED"
    for number, line in enumerate(lines, start=1):
        while heading_index < len(headings) and headings[heading_index].line_start == number:
            active_heading = headings[heading_index]
            active_status = "UNSPECIFIED"
            heading_index += 1
        status_match = STATUS_RE.match(line)
        if status_match:
            active_status = status_match.group(1)
        selected_match = SELECTED_RE.match(line)
        if not selected_match:
            continue
        if active_heading is None or active_heading.section_code is None:
            raise ValueError(f"selected option at line {number} has no coded section heading")
        decisions.append(
            {
                "decision_id": active_heading.section_code,
                "decision_title": active_heading.section_title,
                "status": active_status,
                "selected_option_id": selected_match.group(1),
                "selected_option_title": selected_match.group(2),
                "heading_anchor": active_heading.anchor,
                "line_start": active_heading.line_start,
                "selection_line": number,
            }
        )

    if len(decisions) != 106:
        raise ValueError(f"expected 106 architecture decisions, found {len(decisions)}")
    return headings, decisions, version


def make_outputs() -> dict[str, str]:
    spec_bytes = SPEC_PATH.read_bytes()
    text = spec_bytes.decode("utf-8")
    digest = "sha256:" + hashlib.sha256(spec_bytes).hexdigest()
    headings, decisions, version = parse_specification(text)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    manifest_spec = next(
        artifact for artifact in manifest["artifacts"]
        if artifact["path"] == "canonical/litrpg-system-specification.md"
    )
    if manifest_spec["sha256"] != digest:
        raise ValueError("canonical specification digest does not match the CAL0 manifest")

    heading_records = [
        {
            "level": heading.level,
            "title": heading.title,
            "anchor": heading.anchor,
            "line_start": heading.line_start,
            "line_end": heading.line_end,
            "section_code": heading.section_code,
            "parent_anchors": list(heading.parent_anchors),
        }
        for heading in headings
    ]
    heading_document = {
        "index_version": "1.0.0",
        "generated_from": "litrpg-system/cal0/canonical/litrpg-system-specification.md",
        "source_sha256": digest,
        "specification_version": version,
        "heading_count": len(heading_records),
        "headings": heading_records,
    }
    decision_document = {
        "index_version": "1.0.0",
        "generated_from": "litrpg-system/cal0/canonical/litrpg-system-specification.md",
        "source_sha256": digest,
        "specification_version": version,
        "decision_count": len(decisions),
        "decisions": decisions,
    }

    routes: list[dict[str, object]] = []
    for key, title, prefixes in TOPICS:
        sections = [
            {
                "section_code": heading.section_code,
                "title": heading.section_title,
                "anchor": heading.anchor,
                "line_start": heading.line_start,
                "line_end": heading.line_end,
            }
            for heading in headings
            if heading.level == 2
            and heading.section_code
            and heading.section_code.startswith(prefixes)
        ]
        route_decisions = [
            decision["selected_option_id"]
            for decision in decisions
            if str(decision["decision_id"]).startswith(prefixes)
        ]
        routes.append(
            {
                "topic": key,
                "description": title,
                "specification_sections": sections,
                "decision_refs": route_decisions,
                "context_order": [
                    "litrpg-system/cal0/guide/litrpg-system-story-guide.md",
                    "litrpg-system/cal0/guide/litrpg-system-worked-scenarios.md",
                    "the specification sections listed in this route",
                    "litrpg-system/cal0/canonical/litrpg-system-calibration-annex.md",
                    "litrpg-system/cal0/registries/ and executable code when exact behaviour matters"
                ],
            }
        )
    routing_document = {
        "index_version": "1.0.0",
        "generated_from": "litrpg-system/cal0/canonical/litrpg-system-specification.md",
        "source_sha256": digest,
        "cal0_bundle_id": manifest["bundle_id"],
        "rule": "Load the smallest sufficient authoritative context; generated routes never override canonical sources.",
        "topics": routes,
    }

    markdown_lines = [
        "# Generated CAL0 routing index",
        "",
        "> Generated by `tools/build_system_indexes.py`; do not edit by hand.",
        "",
        f"- Specification: `{version}`",
        f"- Source digest: `{digest}`",
        f"- Indexed headings: `{len(headings)}`",
        f"- Architecture decisions: `{len(decisions)}`",
        "",
        "| Topic | Specification sections | Decisions |",
        "|---|---:|---:|",
    ]
    for route in routes:
        section_links = ", ".join(
            f"[`{section['section_code']}`](../cal0/canonical/litrpg-system-specification.md#{section['anchor']})"
            for section in route["specification_sections"]
        )
        markdown_lines.append(
            f"| {route['description']} | {section_links} | {len(route['decision_refs'])} |"
        )
    markdown_lines.extend(
        [
            "",
            "Use `topic-routing.json` for machine routing, `architecture-decisions.json` for exact selected-option lookup, and `specification-headings.json` for bounded section retrieval.",
            "",
        ]
    )

    def render_json(value: object) -> str:
        return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n"

    return {
        "specification-headings.json": render_json(heading_document),
        "architecture-decisions.json": render_json(decision_document),
        "topic-routing.json": render_json(routing_document),
        "INDEX.md": "\n".join(markdown_lines),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if committed indexes are stale")
    args = parser.parse_args()
    outputs = make_outputs()
    stale: list[str] = []
    for name, expected in outputs.items():
        path = OUTPUT_ROOT / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != expected:
                stale.append(str(path.relative_to(REPOSITORY_ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8", newline="\n")
    if stale:
        print("stale generated System indexes:", file=sys.stderr)
        for path in stale:
            print(f"  - {path}", file=sys.stderr)
        print("run: python3 tools/build_system_indexes.py", file=sys.stderr)
        return 1
    action = "verified" if args.check else "generated"
    print(f"{action} {len(outputs)} deterministic System indexes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

