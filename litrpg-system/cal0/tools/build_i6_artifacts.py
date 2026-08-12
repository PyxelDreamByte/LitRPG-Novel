"""Materialise CAL0-I6 authoring, character, scenario, and usability artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cal0.authoring import build_i6_artifacts


TARGETS = {
    "reference_sheets": "characters/cal0-i6-reference-sheets.json",
    "projections": "authoring/cal0-i6-projection-contracts.json",
    "scenarios": "scenarios/cal0-i6-story-scenarios.json",
    "authoring_checklists": "authoring/cal0-i6-authoring-checklists.json",
    "notification_templates": "authoring/cal0-i6-notification-templates.json",
    "decision_resolution": "registries/cal0-i6-decision-resolution.json",
    "change_register": "registries/cal0-i6-change-register.json",
    "report": "reports/cal0-i6-usability-report.json",
}


def main() -> None:
    artifacts = build_i6_artifacts(ROOT)
    if not artifacts["report"]["passed"]:
        raise SystemExit("CAL0-I6 usability suite failed")
    for key, relative in TARGETS.items():
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(artifacts[key], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
