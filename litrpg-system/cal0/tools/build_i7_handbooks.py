"""Build readable CAL0-I7 closure and residual handbooks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def closure_handbook() -> str:
    review = load("closure/cal0-i7-closure-review.json")
    report = load("reports/cal0-i7-closure-report.json")
    changes = load("registries/cal0-i7-change-register.json")
    lines = [
        "# LitRPG System validated-closure review",
        "",
        "**Canonical specification:** 0.89  ",
        "**Calibration annex:** 2.9  ",
        "**Stage:** `CAL0-I7 — COMPLETE`  ",
        "**Closure status:** `VALIDATED_BASELINE_WITH_BOUNDED_RESIDUALS`  ",
        "**Parameter status:** `AUTHORING_VALIDATED_PROVISIONAL`",
        "",
        "Validated closure means the connected architecture, numerical, adversarial, scenario, sheet, authoring, and change-control baseline has passed every VAL1.2D criterion. It does not turn provisional coefficients into empirical facts or pre-decide setting, character, or plot content.",
        "",
        "## Closure result",
        "",
        "| Measure | Result |",
        "|---|---:|",
        f"| Binding architecture decisions | {review['architecture_decision_count']} |",
        f"| CAL0 model-family selections | {review['cal0_model_selection_count']} |",
        f"| Required connected artifact families | {review['required_artifact_count']} |",
        f"| VAL1.2D closure criteria | {review['criterion_count']} passed |",
        f"| Residual groups | {report['residual_group_count']} |",
        f"| Explicit residual items | {report['residual_item_count']} |",
        f"| Blocking residuals | {report['blocking_residual_count']} |",
        f"| Change-register entries | {report['change_entry_count']} closed |",
        f"| Six-layer scenario projection cells | {report['scene_projection_cell_count']} |",
        "",
        "## VAL1.2D evidence matrix",
        "",
        "| Criterion | Outcome | Finding |",
        "|---|---|---|",
    ]
    for criterion in review["criteria"]:
        lines.append(f"| `{criterion['criterion_id']}` | {criterion['outcome']} | {criterion['finding']} |")
    lines.extend(["", "## Connected artifact set", "", "| Artifact family | Status | Files |", "|---|---|---|"])
    for artifact in review["required_artifacts"]:
        files = "<br>".join(f"`{path}`" for path in artifact["paths"])
        lines.append(f"| {artifact['artifact'].replace('_', ' ')} | {artifact['status']} | {files} |")
    lines.extend([
        "",
        "## I7 closure corrections",
        "",
        "The review found four packaging or projection gaps. Each is closed below the architecture layer:",
        "",
        "| Entry | Classification | Resolution |",
        "|---|---|---|",
    ])
    for entry in changes["entries"]:
        if entry["source_stage"] == "CAL0-I7":
            lines.append(f"| `{entry['entry_id']}` — {entry['title']} | `{entry['classification']}` | {entry['resolution']} |")
    lines.extend([
        "",
        "## Soul-resolution lineage",
        "",
        "The historical I3 unknown `parameter://cal0/unresolved/protagonist-long-term-soul-multiplier@1` remains immutable. Its I6 story-facing successor is explicitly joined to it as `RESOLVES_AS_NONSCALAR_PROFILE`. No universal multiplier or replacement coefficient exists: unusual development remains facet-specific across Depth, Coherence, Resonance, boundary integrity, coupling, recovery, and safe assimilation.",
        "",
        "## What closure freezes",
        "",
        "- The 106 architecture decisions and 66 CAL0 model-family selections.",
        "- The reference parameter lineage, cohort evidence, adversarial findings, I5 repairs, I6 projections, and I7 closure evidence.",
        "- The rule that projections never create facts, capability, access, authority, ownership, identity, resources, or progression.",
        "- The requirement that future changes are prospective, classified, evidenced, migration-aware, and regression-tested.",
        "",
        "## What closure does not freeze",
        "",
        "- Setting-specific prevalence, injury, rarity, culture, or population values not yet authored for a named scope.",
        "- Character decisions, plot outcomes, local opportunities, opposition, or final story-sheet numbers.",
        "- Optional nonhuman numerical extensions and advanced implementation branches not used by the active baseline.",
        "- Provisional coefficients as empirical claims.",
        "",
        "## Maintenance rule",
        "",
        review["governance_boundary"],
        "",
        f"Closure report digest: `{report['report_digest']}`.",
        "",
    ])
    return "\n".join(lines)


def residual_handbook() -> str:
    registry = load("registries/cal0-i7-residual-uncertainty.json")
    lines = [
        "# LitRPG System residual-uncertainty register",
        "",
        "**Closure status:** `VALIDATED_BASELINE_WITH_BOUNDED_RESIDUALS`  ",
        f"**Groups:** {registry['group_count']}  ",
        f"**Items:** {registry['item_count']}  ",
        f"**Blocking items:** {registry['blocking_item_count']}",
        "",
        "A residual is not a concealed System rule. It names information that must be supplied only when a declared setting, population, character, plot, implementation, or optional extension needs it. Every entry below has an owner, activation condition, and failure boundary.",
        "",
        "## Classification summary",
        "",
        "| Classification | Groups | Items | Meaning |",
        "|---|---:|---:|---|",
    ]
    for classification in registry["allowed_classifications"]:
        lines.append(
            f"| `{classification}` | {registry['group_classification_counts'][classification]} | {registry['item_classification_counts'][classification]} | {registry['classification_definitions'][classification]} |"
        )
    lines.extend(["", "## Registered residuals", ""])
    for group in registry["groups"]:
        lines.extend([
            f"### {group['source_selection_id']}",
            "",
            f"**Classification:** `{group['classification']}`  ",
            f"**Owner:** {group['owner']}  ",
            f"**Disposition:** `{group['closure_disposition']}`",
            "",
            f"**Boundary:** {group['boundary']}",
            "",
            f"**Activation:** {group['activation_condition']}",
            "",
        ])
        for item in group["items"]:
            lines.append(f"- `{item['item_id']}` — {item['text']}")
        lines.append("")
    soul = registry["soul_multiplier_disposition"]
    lines.extend([
        "## Resolved Soul question",
        "",
        f"`{soul['historical_parameter_id']}` is `{soul['status']}` through `{soul['relationship']}`. The active resolution is `{soul['active_resolution']}`; it is not counted among the 305 residual items.",
        "",
        f"Registry digest: `{registry['registry_digest']}`.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    outputs = {
        "guide/litrpg-system-validated-closure.md": closure_handbook(),
        "guide/litrpg-system-residual-uncertainty-register.md": residual_handbook(),
    }
    for relative, content in outputs.items():
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
