"""Materialise CAL0-I7 validated-closure artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cal0.closure import build_i7_artifacts


TARGETS = {
    "residual_register": "registries/cal0-i7-residual-uncertainty.json",
    "scene_matrix": "authoring/cal0-i7-scene-projection-matrix.json",
    "change_register": "registries/cal0-i7-change-register.json",
    "character_sheet_checklist": "authoring/cal0-i7-character-sheet-checklist.json",
    "closure_review": "closure/cal0-i7-closure-review.json",
    "report": "reports/cal0-i7-closure-report.json",
}


def main() -> None:
    artifacts = build_i7_artifacts(ROOT)
    if not artifacts["report"]["passed"]:
        raise SystemExit("CAL0-I7 closure suite failed")
    for key, relative in TARGETS.items():
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(artifacts[key], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
