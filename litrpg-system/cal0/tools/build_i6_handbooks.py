"""Build readable Markdown handbooks from the pinned CAL0-I6 JSON artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def text(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value).replace("|", "\\|")


def bullets(values: list[Any]) -> list[str]:
    return [f"- {text(value)}" for value in values] or ["- None."]


def build_reference_sheets() -> str:
    sheets = load("characters/cal0-i6-reference-sheets.json")["sheets"]
    lines = [
        "# CAL0-I6 reference character sheets",
        "",
        "**Specification:** 0.88  ",
        "**Calibration annex:** 2.8  ",
        "**Status:** `AUTHORING_VALIDATED_PROVISIONAL`  ",
        "**Scope:** Authoring references, not fixed plot canon.",
        "",
        "These sheets make the System usable in scenes while keeping natural maturation, training, adaptation, Skill XP, Class XP, reinforcement, and assimilation on separate causal ledgers. Exact values are planning anchors, not mandatory final-story numbers.",
        "",
    ]
    for sheet in sheets:
        identity = sheet["identity"]
        lines.extend([
            f"## {identity['label']} — {identity['milestone']}",
            "",
            sheet["author_notes"]["reader_summary"],
            "",
            "| Field | Reference |",
            "|---|---|",
            f"| Sheet ID | `{sheet['sheet_id']}` |",
            f"| Role | {identity['role']} |",
            f"| Age / life stage | {identity['age']} / {identity['life_stage']} |",
            f"| Species | {identity['species']} |",
            f"| Institution | {text(sheet['social']['institution'])} |",
            f"| Health | {sheet['resources']['health']['state']} |",
            f"| Working Mana reserve | {sheet['resources']['mana']['working_reserve']} |",
            "",
            "### Traits",
            "",
            *bullets(sheet["traits"]),
            "",
            "### Attributes",
            "",
            "| Attribute | Reference capacity | Absolute index |",
            "|---|---:|---:|",
        ])
        for name, value in sheet["attributes"].items():
            lines.append(f"| {name} | {value['reference_capacity']} | {value['absolute_index']} |")
        lines.extend(["", "### Skills and classes", "", "| Kind | Name | Level | XP | State / form |", "|---|---|---:|---:|---|"])
        for skill in sheet["progression"]["skills"]:
            lines.append(f"| Skill | {skill['name']} | {skill['level']} | {skill['xp']} | {skill['state']} |")
        for class_record in sheet["progression"]["classes"]:
            lines.append(f"| Class | {class_record['name']} | {class_record['level']} | {class_record['xp']} | {class_record['state']} / {class_record['form']} |")
        if not sheet["progression"]["skills"] and not sheet["progression"]["classes"]:
            lines.append("| — | No accepted progression | — | — | — |")
        lines.extend([
            "",
            "### Authoring constraints",
            "",
            f"- Magic methods: {', '.join(sheet['magic']['methods']) or 'none'}. Independent magic: {text(sheet['magic']['independent'])}.",
            f"- Natural maturation is separate from XP: {text(sheet['causal_ledgers']['natural_maturation']['separate_from_xp'])}.",
            f"- Reinforcement claims remain conserved: {text(sheet['causal_ledgers']['reinforcement']['claims_conserved'])}.",
            f"- Assimilation retains backlog and uses a safe governor: {text(sheet['causal_ledgers']['assimilation']['backlog_preserved'])}.",
            f"- Persistent vulnerabilities: {', '.join(sheet['author_notes']['causal_vulnerabilities_remain'])}.",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def build_scenarios() -> str:
    scenarios = load("scenarios/cal0-i6-story-scenarios.json")["scenarios"]
    lines = [
        "# CAL0-I6 worked story scenarios",
        "",
        "**Specification:** 0.88  ",
        "**Calibration annex:** 2.8  ",
        "**Scope:** Worked causal references, not fixed plot.",
        "",
        "Each scenario exposes the same seven planning layers: inputs, actor knowledge, causal sequence, state changes, interface output, reader projection, and locked checks.",
        "",
    ]
    for index, scenario in enumerate(scenarios, start=1):
        lines.extend([
            f"## {index}. {scenario['title']}",
            "",
            f"**Family:** `{scenario['family']}`  ",
            f"**Scenario ID:** `{scenario['scenario_id']}`",
            "",
            "### Inputs",
            "",
            "| Input | Value |",
            "|---|---|",
        ])
        for key, value in scenario["inputs"].items():
            lines.append(f"| {key} | {text(value)} |")
        lines.extend(["", "### What the actors know", "", *bullets(scenario["actor_knowledge"]), "", "### Causal sequence", ""])
        lines.extend(f"{step}. {value}" for step, value in enumerate(scenario["causal_sequence"], start=1))
        lines.extend(["", "### State changes", "", "| Ledger / state | Change |", "|---|---|"])
        for key, value in scenario["state_changes"].items():
            lines.append(f"| {key} | {text(value)} |")
        lines.extend([
            "",
            "### Interface output",
            "",
            *bullets(scenario["interface_outputs"]),
            "",
            "### Reader-facing projection",
            "",
            scenario["reader_facing_projection"],
            "",
            "### Locked checks",
            "",
            *bullets([f"`{value}`" for value in scenario["expected_checks"]]),
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def build_authoring_templates() -> str:
    checklists = load("authoring/cal0-i6-authoring-checklists.json")["templates"]
    notifications = load("authoring/cal0-i6-notification-templates.json")["templates"]
    changes = load("registries/cal0-i6-change-register.json")
    lines = [
        "# CAL0-I6 authoring templates and change control",
        "",
        "**Specification:** 0.88  ",
        "**Calibration annex:** 2.8",
        "",
        "Use the artifact template before drafting, the scene template immediately before prose, and the change register whenever an apparent contradiction or desired exception appears.",
        "",
        "## Artifact checklists",
        "",
    ]
    for item in checklists:
        lines.extend([
            f"### {item['artifact_type'].replace('_', ' ').title()}",
            "",
            "Required questions:",
            "",
            *bullets(item["required_questions"]),
            "",
            "Locked checks:",
            "",
            *bullets(item["locked_checks"]),
            "",
            "Type-specific checks:",
            "",
            *bullets(item["type_specific_checks"]),
            "",
        ])
    lines.extend(["## Notification templates", ""])
    for item in notifications:
        lines.extend([
            f"### {item['notification_type'].replace('_', ' ').title()}",
            "",
            f"> {item['template']}",
            "",
            f"Must not imply: {', '.join(item['must_not_imply'])}.",
            "",
        ])
    lines.extend([
        "## Change-control classifications",
        "",
        "| Classification | Use when |",
        "|---|---|",
    ])
    for classification in changes["classification_order"]:
        lines.append(f"| `{classification}` | {changes['classification_rules'][classification]} |")
    lines.extend(["", "## Closed change register", "", "| Entry | Stage | Classification | Resolution |", "|---|---|---|---|"])
    for item in changes["entries"]:
        lines.append(f"| {item['entry_id']} — {item['title']} | {item['source_stage']} | `{item['classification']}` | {text(item['resolution'])} |")
    lines.extend(["", "There are no open I6 change entries. Any future change must state its classification, affected protected facets, evidence, regression identity, migration impact, and whether architecture is being reopened.", ""])
    return "\n".join(lines)


def main() -> None:
    targets = {
        "guide/litrpg-system-reference-sheets.md": build_reference_sheets(),
        "guide/litrpg-system-worked-scenarios.md": build_scenarios(),
        "guide/litrpg-system-authoring-templates.md": build_authoring_templates(),
    }
    for relative, content in targets.items():
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
