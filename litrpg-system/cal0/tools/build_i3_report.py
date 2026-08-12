"""Materialise the deterministic CAL0-I3 reference-scenario report."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cal0.scenario_runner import run_i3_reference_scenarios


def main() -> None:
    report = run_i3_reference_scenarios(ROOT)
    if not report.get("passed"):
        raise SystemExit(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    target = ROOT / "reports/cal0-i3-reference-report.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(report["report_digest"])


if __name__ == "__main__":
    main()
