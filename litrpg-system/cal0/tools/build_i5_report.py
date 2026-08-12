"""Materialise the deterministic CAL0-I5 adversarial report."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cal0.adversarial import run_i5_adversarial_suite


def main() -> None:
    report = run_i5_adversarial_suite(ROOT)
    if not report["passed"]:
        raise SystemExit("CAL0-I5 adversarial suite failed")
    target = ROOT / "reports/cal0-i5-adversarial-report.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

