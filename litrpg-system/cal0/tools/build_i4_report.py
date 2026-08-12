"""Build the deterministic I4 cohort report and successor assessment registry."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cal0.canonical import semantic_digest
from cal0.cohort_runner import run_i4_calibration


def main() -> None:
    report = run_i4_calibration(ROOT)
    if not report.get("passed"):
        raise SystemExit(json.dumps({"passed": False, "checks": report.get("checks"), "issues": report.get("issues")}, sort_keys=True))
    report_path = ROOT / "reports/cal0-i4-cohort-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    sensitivity = report["sensitivity_and_identifiability"]
    final_iteration = report["calibration_iterations"][-1]
    assessment = {
        "parameter_set_id": report["successor_parameter_set_id"],
        "parent_parameter_set_id": report["parameter_parent"],
        "status": report["parameter_status"],
        "canonicality": report["canonicality"],
        "final_iteration_id": final_iteration["iteration_id"],
        "final_overrides": final_iteration["overrides"],
        "provisional_parameter_assessments": sensitivity["provisional_parameter_assessments"],
        "unresolved_parameter_assessments": sensitivity["unresolved_parameter_assessments"],
        "report_digest": report["report_digest"],
        "assessment_digest": semantic_digest({
            "provisional": sensitivity["provisional_parameter_assessments"],
            "unresolved": sensitivity["unresolved_parameter_assessments"],
            "overrides": final_iteration["overrides"],
        }),
        "provenance": [
            "litrpg-system-specification.md#VAL1.0",
            "litrpg-system-calibration-annex.md#CAL0-I4",
            report["cohort_plan_id"]
        ]
    }
    assessment_path = ROOT / "registries/cal0-i4-parameter-assessment.json"
    assessment_path.write_text(json.dumps(assessment, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "passed": True,
        "report_digest": report["report_digest"],
        "assessment_digest": assessment["assessment_digest"],
        "reference_births_per_iteration": report["total_reference_births_per_iteration"],
        "iteration_count": len(report["calibration_iterations"])
    }, sort_keys=True))


if __name__ == "__main__":
    main()
