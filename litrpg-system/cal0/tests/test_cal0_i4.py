from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cal0.canonical import semantic_digest
from cal0.cohort_runner import validate_cohort_plan
from cal0.parameter_runtime import load_json


class Cal0I4CohortCalibrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.parameters = load_json(ROOT / "registries/cal0-i3-parameters.json")
        cls.plan = load_json(ROOT / "scenarios/cal0-i4-cohort-plan.json")
        cls.report = load_json(ROOT / "reports/cal0-i4-cohort-report.json")
        cls.assessment = load_json(ROOT / "registries/cal0-i4-parameter-assessment.json")

    def test_plan_passes_topology_and_scope_validation(self) -> None:
        self.assertEqual([], validate_cohort_plan(self.plan, self.parameters))

    def test_every_reference_seed_contains_at_least_ten_thousand_births(self) -> None:
        final = self.report["calibration_iterations"][-1]
        self.assertGreaterEqual(len(final["seed_summaries"]), 3)
        self.assertTrue(all(item["birth_count"] >= 10000 for item in final["seed_summaries"]))

    def test_all_declared_social_environments_are_present(self) -> None:
        expected = {entry["environment_id"] for entry in self.plan["environments"]}
        for summary in self.report["calibration_iterations"][-1]["seed_summaries"]:
            self.assertEqual(expected, set(summary["environments"]))

    def test_complete_life_course_is_reported(self) -> None:
        expected = {"late_prenatal", "newborn", "child", "adult", "ageing"}
        for summary in self.report["calibration_iterations"][-1]["seed_summaries"]:
            self.assertEqual(expected, set(summary["life_stage_capacity"]))

    def test_causal_contributions_remain_separate(self) -> None:
        required = {"natural_maturation", "purposeful_training_load", "organic_training_adaptation", "reinforcement_expressed", "injury_loss"}
        for summary in self.report["calibration_iterations"][-1]["seed_summaries"]:
            self.assertTrue(required.issubset(summary["causal_contributions"]))

    def test_outliers_retain_causal_histories_and_ledgers(self) -> None:
        for summary in self.report["calibration_iterations"][-1]["seed_summaries"]:
            self.assertTrue(summary["causal_outliers"])
            self.assertTrue(all("causal_history" in item and "ledger_contributions" in item for item in summary["causal_outliers"]))

    def test_calibration_lineage_preserves_overbraked_intermediate_attempt(self) -> None:
        iterations = self.report["calibration_iterations"]
        self.assertEqual(3, len(iterations))
        self.assertEqual([], iterations[0]["failed_envelopes"])
        self.assertTrue(iterations[1]["failed_envelopes"])
        self.assertEqual([], iterations[-1]["failed_envelopes"])

    def test_final_iteration_passes_every_envelope(self) -> None:
        final = self.report["calibration_iterations"][-1]
        self.assertTrue(all(item["passed"] for item in final["envelopes"]))
        self.assertEqual(len(self.plan["envelopes"]), final["passed_envelope_count"])

    def test_every_provisional_parameter_has_an_identifiability_class(self) -> None:
        entries = self.assessment["provisional_parameter_assessments"]
        self.assertEqual(39, len(entries))
        self.assertEqual(39, len({item["parameter_id"] for item in entries}))

    def test_all_six_unknowns_remain_explicit_and_classified(self) -> None:
        entries = self.assessment["unresolved_parameter_assessments"]
        self.assertEqual(6, len(entries))
        self.assertTrue(all(item["remains_unresolved"] for item in entries))

    def test_protagonist_soul_multiplier_remains_deferred(self) -> None:
        entry = next(item for item in self.assessment["unresolved_parameter_assessments"] if "protagonist-long-term-soul" in item["parameter_id"])
        self.assertEqual("DEFERRED_STORY_DECISION", entry["classification"])
        self.assertEqual("CAL0-I6", entry["required_stage"])

    def test_protagonist_comparisons_are_scenario_ensembles(self) -> None:
        protagonist = [item for item in self.report["comparison_ensembles"] if "protagonist" in item["ensemble_id"]]
        self.assertEqual(2, len(protagonist))
        self.assertTrue(all(item["kind"] == "scenario_ensemble_not_population" for item in protagonist))
        self.assertTrue(all(item["ordinary_population_contamination"] is False for item in protagonist))

    def test_dependency_variants_are_all_executed(self) -> None:
        variants = {item["variant"] for item in self.report["sensitivity_and_identifiability"]["dependence_sensitivity"]}
        self.assertEqual({"independent", "provisional", "strong-shared"}, variants)

    def test_report_scope_is_internal_not_empirical_or_story_canon(self) -> None:
        self.assertEqual("INTERNAL_WORLD_CALIBRATION_NOT_EMPIRICAL_FACT", self.report["canonicality"])
        self.assertEqual("COHORT_CALIBRATED_PROVISIONAL", self.report["parameter_status"])
        self.assertIn("do not become empirical estimates", self.report["trial_input_warning"])

    def test_report_digest_is_content_stable(self) -> None:
        payload = dict(self.report)
        digest = payload.pop("report_digest")
        self.assertEqual(digest, semantic_digest(payload))
        self.assertEqual(digest, self.assessment["report_digest"])

    def test_suite_checks_are_complete_and_true(self) -> None:
        self.assertTrue(self.report["passed"])
        self.assertEqual(sorted(self.report["expected_checks"]), sorted(self.report["checks"]))
        self.assertTrue(all(self.report["checks"].values()))


if __name__ == "__main__":
    unittest.main()
