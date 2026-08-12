from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cal0.adversarial import ATTACKS, REQUIRED_FAMILY_TAGS, REPAIRS, SURFACES, run_i5_adversarial_suite, validate_attack_catalog
from cal0.canonical import semantic_digest
from cal0.engines import ResourceLedger
from cal0.parameter_runtime import load_json


class Cal0I5AdversarialValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = load_json(ROOT / "reports/cal0-i5-adversarial-report.json")
        cls.parent = load_json(ROOT / "reports/cal0-i4-cohort-report.json")

    def test_attack_catalog_is_complete_and_valid(self) -> None:
        self.assertEqual([], validate_attack_catalog())
        self.assertEqual(42, len(ATTACKS))

    def test_all_nine_attack_surfaces_are_covered(self) -> None:
        self.assertEqual(SURFACES, {case["surface"] for case in ATTACKS})
        self.assertTrue(all(self.report["surface_counts"][surface] > 0 for surface in SURFACES))

    def test_all_required_val1_attack_families_are_covered(self) -> None:
        actual = {tag for case in ATTACKS for tag in case["family_tags"]}
        self.assertTrue(REQUIRED_FAMILY_TAGS.issubset(actual))

    def test_every_attack_has_four_order_invariant_replays(self) -> None:
        for result in self.report["attack_results"]:
            self.assertEqual(4, len(result["replays"]))
            self.assertEqual(1, len({item["outcome_digest"] for item in result["replays"]}))

    def test_every_validation_record_retains_required_context(self) -> None:
        required = {"preconditions", "actor_knowledge", "available_resources", "action_sequence", "predicted_result", "observed_result", "affected_invariants", "subsystems", "exploit_classification", "regression_test", "record_digest"}
        for result in self.report["attack_results"]:
            self.assertTrue(required.issubset(result))

    def test_valid_optimisation_and_blocked_exploits_both_remain_visible(self) -> None:
        self.assertEqual(15, self.report["allowed_strategy_count"])
        self.assertEqual(27, self.report["denied_exploit_count"])

    def test_academy_and_industry_are_not_misclassified_as_exploits(self) -> None:
        results = {item["case_id"]: item for item in self.report["attack_results"]}
        for case_id in ("I5-A05", "I5-A08", "I5-A09", "I5-A12", "I5-A24", "I5-A27"):
            self.assertEqual("ALLOWED", results[case_id]["observed_result"])

    def test_semantic_replay_and_provenance_free_value_are_denied(self) -> None:
        results = {item["case_id"]: item for item in self.report["attack_results"]}
        for case_id in ("I5-A01", "I5-A10", "I5-A25", "I5-A37", "I5-A38", "I5-A39", "I5-A40", "I5-A41"):
            self.assertEqual("DENIED", results[case_id]["observed_result"])

    def test_resource_recovery_requires_a_bounded_source_witness(self) -> None:
        exhausted = ResourceLedger.create("mana", "10", "0")
        with self.assertRaises(ValueError):
            exhausted.recover("5", "event:rest", "5", "")
        bounded = exhausted.recover("8", "event:rest", "3", "source:ambient-mana")
        self.assertEqual("3", str(bounded.available))

    def test_identity_continuation_is_exclusive_but_derived_people_remain_possible(self) -> None:
        results = {item["case_id"]: item for item in self.report["attack_results"]}
        self.assertEqual("DENIED", results["I5-A31"]["observed_result"])
        self.assertEqual("DENIED", results["I5-A34"]["observed_result"])
        self.assertEqual("ALLOWED", results["I5-A32"]["observed_result"])
        self.assertEqual("ALLOWED", results["I5-A35"]["observed_result"])

    def test_all_five_repairs_have_passing_regressions(self) -> None:
        self.assertEqual(5, len(REPAIRS))
        self.assertEqual(5, len(self.report["repairs"]))
        self.assertTrue(all(item["regression_count"] > 0 and item["passed"] for item in self.report["repairs"]))

    def test_no_unresolved_invariant_violation_remains(self) -> None:
        self.assertEqual([], self.report["unresolved_invariant_violations"])
        self.assertTrue(self.report["checks"]["no_unresolved_invariant_violation"])

    def test_i4_cohort_evidence_is_pinned_without_becoming_empirical_truth(self) -> None:
        self.assertEqual(self.parent["report_digest"], self.report["parent_cohort_report_digest"])
        self.assertEqual("INTERNAL_SYSTEM_VALIDATION_NOT_EMPIRICAL_FACT_OR_STORY_CANON", self.report["canonicality"])

    def test_parameter_status_advances_without_resolving_deferred_unknowns(self) -> None:
        self.assertEqual("ADVERSARIALLY_VALIDATED_PROVISIONAL", self.report["parameter_status"])
        assessment = load_json(ROOT / "registries/cal0-i4-parameter-assessment.json")
        self.assertEqual(6, len(assessment["unresolved_parameter_assessments"]))
        self.assertTrue(all(item["remains_unresolved"] for item in assessment["unresolved_parameter_assessments"]))

    def test_report_digest_is_content_stable(self) -> None:
        payload = dict(self.report)
        digest = payload.pop("report_digest")
        self.assertEqual(digest, semantic_digest(payload))
        self.assertEqual(digest, run_i5_adversarial_suite(ROOT)["report_digest"])

    def test_every_exit_check_is_true(self) -> None:
        self.assertEqual(sorted(self.report["expected_checks"]), sorted(self.report["checks"]))
        self.assertTrue(all(self.report["checks"].values()))
        self.assertTrue(self.report["passed"])


if __name__ == "__main__":
    unittest.main()
