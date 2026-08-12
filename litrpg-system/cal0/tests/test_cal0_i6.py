from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cal0.authoring import (
    AUTHORING_TYPES,
    CHANGE_CLASSIFICATIONS,
    COMPARISON_ROLES,
    PROTAGONIST_MILESTONES,
    REQUIRED_SCENARIO_FAMILIES,
    VIEW_KINDS,
    build_i6_artifacts,
)
from cal0.canonical import semantic_digest
from cal0.parameter_runtime import load_json


class Cal0I6AuthoringAndUsabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sheets_doc = load_json(ROOT / "characters/cal0-i6-reference-sheets.json")
        cls.projections_doc = load_json(ROOT / "authoring/cal0-i6-projection-contracts.json")
        cls.scenarios_doc = load_json(ROOT / "scenarios/cal0-i6-story-scenarios.json")
        cls.checklists_doc = load_json(ROOT / "authoring/cal0-i6-authoring-checklists.json")
        cls.notifications_doc = load_json(ROOT / "authoring/cal0-i6-notification-templates.json")
        cls.resolution = load_json(ROOT / "registries/cal0-i6-decision-resolution.json")
        cls.change_register = load_json(ROOT / "registries/cal0-i6-change-register.json")
        cls.report = load_json(ROOT / "reports/cal0-i6-usability-report.json")
        cls.parent = load_json(ROOT / "reports/cal0-i5-adversarial-report.json")

    def test_fourteen_reference_sheets_are_present(self) -> None:
        self.assertEqual(14, len(self.sheets_doc["sheets"]))
        self.assertEqual(14, self.report["sheet_count"])

    def test_all_eight_protagonist_milestones_are_present_once(self) -> None:
        actual = [item["identity"]["milestone"] for item in self.sheets_doc["sheets"] if item["identity"]["role"] == "protagonist"]
        self.assertEqual(set(PROTAGONIST_MILESTONES), set(actual))
        self.assertEqual(8, len(actual))

    def test_all_six_comparison_roles_are_present(self) -> None:
        actual = {item["identity"]["role"] for item in self.sheets_doc["sheets"]}
        self.assertTrue(set(COMPARISON_ROLES).issubset(actual))
        self.assertEqual(6, self.report["comparison_sheet_count"])

    def test_every_sheet_contains_all_eleven_attributes(self) -> None:
        expected = {"Might", "Finesse", "Alacrity", "Vitality", "Perception", "Cognition", "Focus", "Will", "Depth", "Coherence", "Resonance"}
        for sheet in self.sheets_doc["sheets"]:
            self.assertEqual(expected, set(sheet["attributes"]))

    def test_every_sheet_digest_replays(self) -> None:
        for sheet in self.sheets_doc["sheets"]:
            payload = dict(sheet)
            digest = payload.pop("sheet_digest")
            self.assertEqual(digest, semantic_digest(payload))

    def test_six_distinct_views_exist_for_every_sheet(self) -> None:
        views = self.projections_doc["views"]
        self.assertEqual(84, len(views))
        counts = {}
        for view in views:
            counts.setdefault(view["sheet_id"], set()).add(view["view_kind"])
        self.assertTrue(all(kinds == set(VIEW_KINDS) for kinds in counts.values()))

    def test_non_author_views_do_not_leak_private_backend(self) -> None:
        forbidden = {"secrets", "backend_uncertainty", "unresolved_inputs", "causal_ledgers"}
        for view in self.projections_doc["views"]:
            if view["view_kind"] not in {"private_backend", "author_facing"}:
                self.assertTrue(forbidden.isdisjoint(view))

    def test_reader_view_is_concise_and_withholds_exact_backend(self) -> None:
        for view in self.projections_doc["views"]:
            if view["view_kind"] == "reader_facing":
                self.assertTrue(view["exact_backend_withheld"])
                self.assertNotIn("attributes", view)

    def test_appraisal_view_reports_confidence_and_unknowns(self) -> None:
        for view in self.projections_doc["views"]:
            if view["view_kind"] == "appraisal_derived":
                self.assertIn("confidence", view)
                self.assertTrue(view["omissions_are_not_negative_facts"])

    def test_all_fifteen_minimum_scenarios_are_present_once(self) -> None:
        scenarios = self.scenarios_doc["scenarios"]
        self.assertEqual(15, len(scenarios))
        self.assertEqual(set(REQUIRED_SCENARIO_FAMILIES), {item["family"] for item in scenarios})

    def test_scenarios_have_complete_story_projection_records(self) -> None:
        required = {"inputs", "actor_knowledge", "causal_sequence", "state_changes", "interface_outputs", "reader_facing_projection", "expected_checks"}
        for scenario in self.scenarios_doc["scenarios"]:
            self.assertTrue(required.issubset(scenario))
            self.assertTrue(scenario["reader_facing_projection"])

    def test_every_scenario_digest_replays(self) -> None:
        for scenario in self.scenarios_doc["scenarios"]:
            payload = dict(scenario)
            digest = payload.pop("scenario_digest")
            self.assertEqual(digest, semantic_digest(payload))

    def test_natural_growth_scenario_awards_no_xp(self) -> None:
        scenario = next(item for item in self.scenarios_doc["scenarios"] if item["family"] == "natural_growth_without_xp")
        self.assertEqual("0", scenario["state_changes"]["skill_xp"])
        self.assertEqual("0", scenario["state_changes"]["class_xp"])

    def test_prenatal_reinforcement_claim_is_conserved(self) -> None:
        scenario = next(item for item in self.scenarios_doc["scenarios"] if item["family"] == "prenatal_skill_progression")
        inputs = scenario["inputs"]
        self.assertEqual("0.0015", inputs["reinforcement_claim"])
        self.assertEqual("0.0015", str(float(inputs["assimilated"]) + float(inputs["backlog"])))

    def test_party_contribution_and_reward_are_conserved(self) -> None:
        scenario = next(item for item in self.scenarios_doc["scenarios"] if item["family"] == "party_contribution_dispute")
        contribution = sum(float(value) for value in scenario["inputs"]["contributions"].values())
        rewards = sum(float(value) for key, value in scenario["state_changes"].items() if key.endswith("_reward"))
        self.assertEqual(1.0, contribution)
        self.assertEqual(100.0, rewards)

    def test_dungeon_economy_is_source_bounded(self) -> None:
        scenario = next(item for item in self.scenarios_doc["scenarios"] if item["family"] == "dungeon_spawn_economy")
        changes = scenario["state_changes"]
        self.assertEqual(float(changes["total_input"]), float(changes["total_committed"]) + float(changes["residual"]))
        self.assertEqual("0", changes["unwitnessed_restock"])

    def test_resurrection_preserves_one_identity_holder_and_no_reward_replay(self) -> None:
        scenario = next(item for item in self.scenarios_doc["scenarios"] if item["family"] == "injury_rehabilitation_resurrection")
        self.assertEqual(1, scenario["state_changes"]["continuing_identity_holders"])
        self.assertFalse(scenario["state_changes"]["reinforcement_reclaimed"])

    def test_earth_knowledge_does_not_transfer_mage_xp(self) -> None:
        scenario = next(item for item in self.scenarios_doc["scenarios"] if item["family"] == "nonmagical_knowledge_to_magic")
        self.assertEqual("0", scenario["state_changes"]["earth_knowledge_xp_transfer"])
        self.assertGreater(float(scenario["state_changes"]["local_research_skill_xp"]), 0)

    def test_all_ten_authoring_templates_are_present(self) -> None:
        templates = self.checklists_doc["templates"]
        self.assertEqual(set(AUTHORING_TYPES), {item["artifact_type"] for item in templates})
        self.assertTrue(all(item["required_questions"] and item["locked_checks"] and item["type_specific_checks"] for item in templates))

    def test_notification_templates_preserve_epistemic_limits(self) -> None:
        self.assertEqual(4, len(self.notifications_doc["templates"]))
        self.assertTrue(all(item["must_not_imply"] for item in self.notifications_doc["templates"]))

    def test_soul_multiplier_is_resolved_as_non_scalar(self) -> None:
        decision = self.resolution["resolutions"][0]
        self.assertEqual("NOT_APPLICABLE_NONSCALAR_PROFILE", decision["active_resolution"])
        self.assertFalse(decision["coefficient_changed"])
        self.assertFalse(decision["architecture_reopened"])

    def test_five_active_residuals_remain_classified(self) -> None:
        self.assertEqual(5, len(self.resolution["remaining_active_residuals"]))
        self.assertTrue(all(item["classification"] for item in self.resolution["remaining_active_residuals"]))

    def test_change_register_covers_i5_repairs_and_i6_resolution(self) -> None:
        self.assertEqual(6, self.change_register["entry_count"])
        self.assertEqual(0, self.change_register["open_entry_count"])
        self.assertEqual(
            {"CAL0-I5-R01", "CAL0-I5-R02", "CAL0-I5-R03", "CAL0-I5-R04", "CAL0-I5-R05", "CAL0-I6-C01"},
            {item["entry_id"] for item in self.change_register["entries"]},
        )
        self.assertTrue(all(item["classification"] in CHANGE_CLASSIFICATIONS for item in self.change_register["entries"]))
        payload = dict(self.change_register)
        digest = payload.pop("register_digest")
        self.assertEqual(digest, semantic_digest(payload))

    def test_story_guide_covers_ordinary_scene_planning(self) -> None:
        guide = (ROOT / "guide/litrpg-system-story-guide.md").read_text(encoding="utf-8")
        for heading in ("## Attributes", "## Skills", "## Classes", "## Training and learning", "## Magic", "## Combat", "## Items, crafting, and loot", "## Dungeons, creatures, and ecology", "## Parties and institutions", "## The protagonist", "## Scene-planning checklist"):
            self.assertIn(heading, guide)

    def test_i6_report_pins_i5_and_replays(self) -> None:
        self.assertEqual(self.parent["report_digest"], self.report["parent_i5_report_digest"])
        payload = dict(self.report)
        digest = payload.pop("report_digest")
        self.assertEqual(digest, semantic_digest(payload))
        self.assertEqual(digest, build_i6_artifacts(ROOT)["report"]["report_digest"])

    def test_every_i6_exit_check_is_true(self) -> None:
        self.assertEqual(sorted(self.report["expected_checks"]), sorted(self.report["checks"]))
        self.assertTrue(all(self.report["checks"].values()))
        self.assertTrue(self.report["passed"])


if __name__ == "__main__":
    unittest.main()
