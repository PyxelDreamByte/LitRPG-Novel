"""Materialise the deterministic CAL0-I2 fixture report for the bundle."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cal0.fixture_runner import run_reference_fixtures


def main() -> None:
    report = run_reference_fixtures(ROOT)
    target = ROOT / "reports/cal0-i2-fixture-report.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
