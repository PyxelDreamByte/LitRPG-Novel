"""Command-line entry point for CAL0-I7 validation and replay."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .adversarial import run_i5_adversarial_suite
from .authoring import build_i6_artifacts
from .cohort_runner import run_i4_calibration
from .closure import build_i7_artifacts
from .fixture_runner import run_reference_fixtures
from .parameter_runtime import load_json
from .scenario_runner import run_i3_reference_scenarios
from .validator import run_fixtures, validation_report


def _print(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(prog="cal0-validate")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("validate", "fixtures", "reference-fixtures", "reference-summary", "i3-scenarios", "i3-summary", "i4-calibrate", "i4-summary", "i5-adversarial", "i5-summary", "i6-authoring", "i6-summary", "i7-close", "i7-summary"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if args.command == "validate":
        report = validation_report(root)
        _print(report)
        return 0 if report["valid"] else 1
    if args.command == "fixtures":
        results = run_fixtures(root)
        report = {"case_count": len(results), "passed": all(case["passed"] for case in results), "results": results}
        _print(report)
        return 0 if report["passed"] else 1
    if args.command in {"i3-scenarios", "i3-summary"}:
        report = run_i3_reference_scenarios(root)
        if args.command == "i3-summary" and report.get("passed"):
            report = {
                "scenario_suite_id": report["scenario_suite_id"],
                "parameter_set_id": report["parameter_set_id"],
                "parameter_set_status": report["parameter_set_status"],
                "parameter_status": report["parameter_status"],
                "canonicality": report["canonicality"],
                "character_count": report["character_count"],
                "scenario_count": report["scenario_count"],
                "passed_count": report["passed_count"],
                "report_digest": report["report_digest"],
                "passed": report["passed"],
            }
        _print(report)
        return 0 if report.get("passed") else 1
    if args.command == "i4-calibrate":
        report = run_i4_calibration(root)
        _print(report)
        return 0 if report.get("passed") else 1
    if args.command == "i4-summary":
        report = load_json(root / "reports/cal0-i4-cohort-report.json")
        final = report["calibration_iterations"][-1]
        _print({
            "cohort_suite_id": report["cohort_suite_id"],
            "parameter_status": report["parameter_status"],
            "births_per_seed": report["births_per_seed"],
            "seed_count": report["seed_count"],
            "total_reference_births_per_iteration": report["total_reference_births_per_iteration"],
            "iteration_count": len(report["calibration_iterations"]),
            "comparison_ensemble_count": len(report["comparison_ensembles"]),
            "final_metrics": final["aggregate_metrics"],
            "failed_envelopes": final["failed_envelopes"],
            "report_digest": report["report_digest"],
            "passed": report["passed"],
        })
        return 0 if report.get("passed") else 1
    if args.command in {"i5-adversarial", "i5-summary"}:
        report = run_i5_adversarial_suite(root) if args.command == "i5-adversarial" else load_json(root / "reports/cal0-i5-adversarial-report.json")
        if args.command == "i5-summary":
            report = {
                "adversarial_suite_id": report["adversarial_suite_id"],
                "parameter_status": report["parameter_status"],
                "attack_count": report["attack_count"],
                "execution_count": report["execution_count"],
                "allowed_strategy_count": report["allowed_strategy_count"],
                "denied_exploit_count": report["denied_exploit_count"],
                "repair_count": report["repair_count"],
                "unresolved_invariant_violation_count": len(report["unresolved_invariant_violations"]),
                "report_digest": report["report_digest"],
                "passed": report["passed"],
            }
        _print(report)
        return 0 if report.get("passed") else 1
    if args.command in {"i6-authoring", "i6-summary"}:
        report = build_i6_artifacts(root)["report"] if args.command == "i6-authoring" else load_json(root / "reports/cal0-i6-usability-report.json")
        if args.command == "i6-summary":
            report = {
                "authoring_suite_id": report["authoring_suite_id"],
                "parameter_status": report["parameter_status"],
                "sheet_count": report["sheet_count"],
                "protagonist_milestone_count": report["protagonist_milestone_count"],
                "comparison_sheet_count": report["comparison_sheet_count"],
                "projection_count": report["projection_count"],
                "scenario_count": report["scenario_count"],
                "authoring_template_count": report["authoring_template_count"],
                "notification_template_count": report["notification_template_count"],
                "change_entry_count": report["change_entry_count"],
                "active_residual_count": report["active_residual_count"],
                "report_digest": report["report_digest"],
                "passed": report["passed"],
            }
        _print(report)
        return 0 if report.get("passed") else 1
    if args.command in {"i7-close", "i7-summary"}:
        report = build_i7_artifacts(root)["report"] if args.command == "i7-close" else load_json(root / "reports/cal0-i7-closure-report.json")
        if args.command == "i7-summary":
            report = {
                "closure_suite_id": report["closure_suite_id"],
                "stage_status": report["stage_status"],
                "closure_status": report["closure_status"],
                "parameter_status": report["parameter_status"],
                "architecture_decision_count": report["architecture_decision_count"],
                "cal0_model_selection_count": report["cal0_model_selection_count"],
                "criterion_count": report["criterion_count"],
                "required_artifact_count": report["required_artifact_count"],
                "residual_group_count": report["residual_group_count"],
                "residual_item_count": report["residual_item_count"],
                "blocking_residual_count": report["blocking_residual_count"],
                "change_entry_count": report["change_entry_count"],
                "scene_projection_cell_count": report["scene_projection_cell_count"],
                "report_digest": report["report_digest"],
                "passed": report["passed"],
            }
        _print(report)
        return 0 if report.get("passed") else 1
    report = run_reference_fixtures(root)
    if args.command == "reference-summary":
        report = {
            "fixture_suite_id": report["fixture_suite_id"],
            "parameter_status": report["parameter_status"],
            "synthetic_only": report["synthetic_only"],
            "case_count": report["case_count"],
            "unique_case_count": report["unique_case_count"],
            "passed_count": report["passed_count"],
            "report_digest": report["report_digest"],
            "passed": report["passed"],
        }
    _print(report)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
