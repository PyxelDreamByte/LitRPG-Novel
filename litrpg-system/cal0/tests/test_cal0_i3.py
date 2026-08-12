from __future__ import annotations

import sys
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cal0.parameter_runtime import (
    binding_map,
    load_json,
    rehearsal_samples,
    validate_parameter_registry,
)
from cal0.scenario_runner import LEDGERS, run_i3_reference_scenarios, validate_reference_scenarios


class Cal0I3ProvisionalCalibrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.parameters = load_json(ROOT / "registries/cal0-i3-parameters.json")
        cls.scenarios = load_json(ROOT / "scenarios/cal0-i3-reference-scenarios.json")
        cls.report = run_i3_reference_scenarios(ROOT)

    def test_parameter_registry_passes_all_typed_constraints(self) -> None:
        self.assertEqual([], validate_parameter_registry(self.parameters))

    def test_every_definition_has_exactly_one_binding(self) -> None:
        definitions = {entry["parameter_id"] for entry in self.parameters["definitions"]}
        self.assertEqual(definitions, set(binding_map(self.parameters)))

    def test_unresolved_values_are_first_class_and_later_owned(self) -> None:
        unresolved = [binding for binding in self.parameters["bindings"] if binding["state"] == "UNRESOLVED"]
        self.assertEqual(6, len(unresolved))
        self.assertTrue(all("value" not in binding for binding in unresolved))
        self.assertTrue(all(binding["unresolved"]["required_stage"] in {"CAL0-I4", "CAL0-I6"} for binding in unresolved))

    def test_provisional_bindings_retain_low_confidence_and_sensitivity_flags(self) -> None:
        provisional = [binding for binding in self.parameters["bindings"] if binding["state"] == "PROVISIONAL"]
        self.assertGreater(len(provisional), 20)
        self.assertTrue(all(binding["uncertainty"]["confidence"] == "LOW" for binding in provisional))
        self.assertTrue(all(binding["uncertainty"]["sensitivity_required"] for binding in provisional))

    def test_distributions_are_finite_hard_bounded_and_rehearsal_only(self) -> None:
        for distribution in self.parameters["distributions"]:
            self.assertEqual("bounded_triangular", distribution["family"])
            self.assertEqual("hard", distribution["truncation"])
            self.assertEqual("rehearsal_only", distribution["uncertainty"]["class"])

    def test_distribution_sampling_is_replayable_and_bounded(self) -> None:
        first = rehearsal_samples(self.parameters, ("17", "83"))
        second = rehearsal_samples(self.parameters, ("17", "83"))
        self.assertEqual(first, second)
        supports = {entry["target_parameter_id"]: entry["support"] for entry in self.parameters["distributions"]}
        for sample in first.values():
            for parameter_id, value in sample.items():
                self.assertGreaterEqual(Decimal(value), Decimal(supports[parameter_id]["minimum"]))
                self.assertLessEqual(Decimal(value), Decimal(supports[parameter_id]["maximum"]))

    def test_scenario_registry_passes_topology_checks(self) -> None:
        self.assertEqual([], validate_reference_scenarios(self.scenarios, self.parameters))

    def test_reference_suite_passes_all_five_scenarios(self) -> None:
        self.assertTrue(self.report["passed"], self.report)
        self.assertEqual(5, self.report["scenario_count"])
        self.assertEqual(5, self.report["passed_count"])
        self.assertEqual(4, self.report["character_count"])

    def test_every_declared_check_is_executed_and_true(self) -> None:
        for result in self.report["results"]:
            self.assertEqual(sorted(result["expected_checks"]), sorted(result["checks"]))
            self.assertTrue(all(result["checks"].values()))

    def test_prenatal_scenario_keeps_growth_training_and_assimilation_separate(self) -> None:
        result = next(item for item in self.report["results"] if "prenatal-maturation" in item["scenario_id"])
        protagonist = result["output"]["characters"]["character://cal0/i3/protagonist-proxy@1"]
        self.assertEqual(set(LEDGERS), set(protagonist["ledgers"]))
        self.assertGreater(Decimal(protagonist["ledgers"]["natural_maturation"]["total"]), Decimal("0"))
        self.assertGreater(Decimal(protagonist["ledgers"]["skill_xp"]["total"]), Decimal("0"))
        self.assertGreater(Decimal(protagonist["ledgers"]["assimilation"]["backlog"]), Decimal("0"))

    def test_matched_training_preserves_envelopes_and_comparison_roles(self) -> None:
        result = next(item for item in self.report["results"] if "matched-training" in item["scenario_id"])
        self.assertTrue(result["checks"]["capacity_envelopes_respected"])
        self.assertTrue(result["checks"]["exceptional_starts_above_ordinary"])
        self.assertTrue(result["checks"]["natural_and_training_ledgers_separate"])

    def test_progression_keeps_skill_class_and_assimilation_contracts_distinct(self) -> None:
        result = next(item for item in self.report["results"] if "progression-and-reinforcement" in item["scenario_id"])
        self.assertNotEqual(result["output"]["skill_curve"], result["output"]["class_curve"])
        self.assertTrue(result["checks"]["blocked_xp_cannot_cascade"])
        self.assertTrue(result["checks"]["claim_budget_recipient_independent"])
        self.assertTrue(result["checks"]["fetal_backlog_exceeds_adult_backlog"])

    def test_overload_creates_harm_without_becoming_free_progress(self) -> None:
        result = next(item for item in self.report["results"] if "overload-harm" in item["scenario_id"])
        self.assertGreater(Decimal(result["output"]["overload"]["harm"]), Decimal("0"))
        self.assertLess(Decimal(result["output"]["overload"]["opportunity"]), Decimal(result["output"]["productive"]["opportunity"]))

    def test_transition_commit_is_recovery_gated_and_atomic(self) -> None:
        result = next(item for item in self.report["results"] if "structural-transition" in item["scenario_id"])
        self.assertFalse(result["output"]["failed_commit"]["committed"])
        self.assertTrue(result["output"]["successful_commit"]["committed"])

    def test_outputs_remain_reference_only_uncalibrated_and_non_cohort(self) -> None:
        self.assertEqual("REFERENCE_ONLY_NOT_STORY_CANON", self.report["canonicality"])
        self.assertEqual("PROVISIONAL", self.report["parameter_set_status"])
        self.assertEqual("UNCALIBRATED", self.report["parameter_status"])
        self.assertFalse(self.report["cohort_claims_permitted"])

    def test_report_digest_replays_exactly(self) -> None:
        second = run_i3_reference_scenarios(ROOT)
        self.assertEqual(self.report["report_digest"], second["report_digest"])


if __name__ == "__main__":
    unittest.main()
