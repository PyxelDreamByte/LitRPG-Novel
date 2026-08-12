from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cal0.authoring import VIEW_KINDS
from cal0.canonical import semantic_digest
from cal0.closure import RESIDUAL_CLASSIFICATIONS, SCENE_LAYERS, VAL12_CRITERIA, build_i7_artifacts
from cal0.parameter_runtime import load_json


class Cal0I7ValidatedClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.residuals = load_json(ROOT / "registries/cal0-i7-residual-uncertainty.json")
        cls.scene_matrix = load_json(ROOT / "authoring/cal0-i7-scene-projection-matrix.json")
        cls.change_register = load_json(ROOT / "registries/cal0-i7-change-register.json")
        cls.parent_change = load_json(ROOT / "registries/cal0-i6-change-register.json")
        cls.checklist = load_json(ROOT / "authoring/cal0-i7-character-sheet-checklist.json")
        cls.review = load_json(ROOT / "closure/cal0-i7-closure-review.json")
        cls.report = load_json(ROOT / "reports/cal0-i7-closure-report.json")
        cls.parent_report = load_json(ROOT / "reports/cal0-i6-usability-report.json")
        cls.sheet_schema = load_json(ROOT / "schemas/cal0-i7-character-sheet.schema.json")
        cls.projection_schema = load_json(ROOT / "schemas/cal0-i7-sheet-projection.schema.json")
        cls.sheets = load_json(ROOT / "characters/cal0-i6-reference-sheets.json")["sheets"]
        cls.projections = load_json(ROOT / "authoring/cal0-i6-projection-contracts.json")["views"]

    def test_all_nine_val12_criteria_pass(self) -> None:
        self.assertEqual(9, self.review["criterion_count"])
        self.assertEqual(set(VAL12_CRITERIA), {item["criterion_id"] for item in self.review["criteria"]})
        self.assertTrue(all(item["outcome"] == "PASS" and item["evidence"] for item in self.review["criteria"]))

    def test_all_nine_required_artifact_families_are_connected(self) -> None:
        self.assertEqual(9, self.review["required_artifact_count"])
        self.assertTrue(all(item["status"] == "CONNECTED" for item in self.review["required_artifacts"]))
        for item in self.review["required_artifacts"]:
            for relative in item["paths"]:
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_architecture_and_model_selection_counts_are_closed(self) -> None:
        self.assertEqual(106, self.review["architecture_decision_count"])
        self.assertEqual(106, len(set(self.review["architecture_decisions"])))
        self.assertEqual(66, self.review["cal0_model_selection_count"])

    def test_all_sixty_six_annex_residual_groups_are_registered(self) -> None:
        groups = [item for item in self.residuals["groups"] if item["source_selection_id"].startswith("CAL0-Q")]
        self.assertEqual(66, len(groups))
        self.assertEqual(300, sum(item["item_count"] for item in groups))

    def test_five_world_residuals_are_registered_separately(self) -> None:
        groups = [item for item in self.residuals["groups"] if not item["source_selection_id"].startswith("CAL0-Q")]
        self.assertEqual(5, len(groups))
        self.assertEqual(5, sum(item["item_count"] for item in groups))

    def test_all_305_residual_items_are_bounded_and_owned(self) -> None:
        self.assertEqual(71, self.residuals["group_count"])
        self.assertEqual(305, self.residuals["item_count"])
        self.assertEqual(0, self.residuals["blocking_group_count"])
        self.assertEqual(0, self.residuals["blocking_item_count"])
        for group in self.residuals["groups"]:
            self.assertIn(group["classification"], RESIDUAL_CLASSIFICATIONS)
            self.assertTrue(group["owner"] and group["boundary"] and group["activation_condition"])
            self.assertTrue(all(not item["blocking"] and item["owner"] for item in group["items"]))

    def test_residual_classification_counts_close_exactly(self) -> None:
        self.assertEqual(
            {"CALIBRATION": 109, "SETTING_CONTENT": 3, "CHARACTER_CHOICE": 0, "PLOT_CHOICE": 0, "IMPLEMENTATION": 192, "FUTURE_OPTIONAL_EXTENSION": 1},
            self.residuals["item_classification_counts"],
        )

    def test_residual_registry_digest_replays(self) -> None:
        payload = dict(self.residuals)
        digest = payload.pop("registry_digest")
        self.assertEqual(digest, semantic_digest(payload))

    def test_soul_resolution_lineage_names_both_identities(self) -> None:
        soul = self.residuals["soul_multiplier_disposition"]
        self.assertEqual("parameter://cal0/unresolved/protagonist-long-term-soul-multiplier@1", soul["historical_parameter_id"])
        self.assertEqual("parameter://cal0/protagonist/long-term-soul-multiplier@1", soul["i6_active_projection_id"])
        self.assertEqual("RESOLVES_AS_NONSCALAR_PROFILE", soul["relationship"])
        self.assertEqual("RESOLVED_NOT_A_RESIDUAL", soul["status"])

    def test_scene_matrix_has_six_layers_for_all_fifteen_scenarios(self) -> None:
        self.assertEqual(15, self.scene_matrix["scenario_count"])
        self.assertEqual(6, self.scene_matrix["layer_count"])
        self.assertEqual(90, self.scene_matrix["projection_cell_count"])
        self.assertEqual(set(SCENE_LAYERS), set(self.scene_matrix["layer_order"]))
        self.assertTrue(all(set(item["layers"]) == set(SCENE_LAYERS) for item in self.scene_matrix["entries"]))

    def test_scene_entry_and_matrix_digests_replay(self) -> None:
        for entry in self.scene_matrix["entries"]:
            payload = dict(entry)
            digest = payload.pop("entry_digest")
            self.assertEqual(digest, semantic_digest(payload))
        payload = dict(self.scene_matrix)
        digest = payload.pop("matrix_digest")
        self.assertEqual(digest, semantic_digest(payload))

    def test_successor_change_register_preserves_parent_and_closes_four_i7_corrections(self) -> None:
        self.assertEqual(self.parent_change["register_id"], self.change_register["parent_register_id"])
        self.assertEqual(self.parent_change["register_digest"], self.change_register["parent_register_digest"])
        self.assertEqual(10, self.change_register["entry_count"])
        self.assertEqual(0, self.change_register["open_entry_count"])
        i7 = [item for item in self.change_register["entries"] if item["source_stage"] == "CAL0-I7"]
        self.assertEqual(4, len(i7))
        self.assertTrue(all(item["architecture_reopened"] is False and item["status"] == "CLOSED_CLOSURE_PINNED" for item in i7))

    def test_successor_change_register_digest_replays(self) -> None:
        payload = dict(self.change_register)
        digest = payload.pop("register_digest")
        self.assertEqual(digest, semantic_digest(payload))

    def test_character_sheet_schema_requires_all_eleven_attributes(self) -> None:
        expected = {"Might", "Finesse", "Alacrity", "Vitality", "Perception", "Cognition", "Focus", "Will", "Depth", "Coherence", "Resonance"}
        self.assertEqual("schema://cal0/i7-character-sheet@1", self.sheet_schema["$id"])
        self.assertEqual(expected, set(self.sheet_schema["properties"]["attributes"]["required"]))
        self.assertTrue(all(expected == set(sheet["attributes"]) for sheet in self.sheets))

    def test_projection_schema_names_all_six_views(self) -> None:
        self.assertEqual("schema://cal0/i7-sheet-projection@1", self.projection_schema["$id"])
        self.assertEqual(set(VIEW_KINDS), set(self.projection_schema["properties"]["view_kind"]["enum"]))
        self.assertEqual(set(VIEW_KINDS), {item["view_kind"] for item in self.projections})

    def test_character_sheet_checklist_is_explicit_and_digest_stable(self) -> None:
        self.assertEqual("character_sheet", self.checklist["artifact_type"])
        self.assertEqual(set(VIEW_KINDS), set(self.checklist["required_view_kinds"]))
        payload = dict(self.checklist)
        digest = payload.pop("checklist_digest")
        self.assertEqual(digest, semantic_digest(payload))

    def test_closure_review_digest_replays(self) -> None:
        payload = dict(self.review)
        digest = payload.pop("review_digest")
        self.assertEqual(digest, semantic_digest(payload))

    def test_closure_report_pins_i6_and_every_i7_digest(self) -> None:
        self.assertEqual(self.parent_report["report_digest"], self.report["parent_i6_report_digest"])
        self.assertEqual(self.review["review_digest"], self.report["review_digest"])
        self.assertEqual(self.residuals["registry_digest"], self.report["residual_registry_digest"])
        self.assertEqual(self.change_register["register_digest"], self.report["change_register_digest"])
        self.assertEqual(self.scene_matrix["matrix_digest"], self.report["scene_matrix_digest"])

    def test_closure_report_digest_replays_and_build_is_deterministic(self) -> None:
        payload = dict(self.report)
        digest = payload.pop("report_digest")
        self.assertEqual(digest, semantic_digest(payload))
        self.assertEqual(digest, build_i7_artifacts(ROOT)["report"]["report_digest"])

    def test_every_i7_exit_check_is_true(self) -> None:
        self.assertEqual(sorted(self.report["expected_checks"]), sorted(self.report["checks"]))
        self.assertTrue(all(self.report["checks"].values()))
        self.assertTrue(self.report["passed"])

    def test_closure_preserves_parameter_uncertainty_status(self) -> None:
        self.assertEqual("VALIDATED_BASELINE_WITH_BOUNDED_RESIDUALS", self.report["closure_status"])
        self.assertEqual("AUTHORING_VALIDATED_PROVISIONAL", self.report["parameter_status"])
        self.assertEqual("AUTHORING_VALIDATED_PROVISIONAL", self.review["parameter_status_preserved"])

    def test_canonical_snapshots_name_final_versions_and_closure(self) -> None:
        specification = (ROOT / "canonical/litrpg-system-specification.md").read_text(encoding="utf-8")
        annex = (ROOT / "canonical/litrpg-system-calibration-annex.md").read_text(encoding="utf-8")
        self.assertIn("**Specification version:** 0.89", specification)
        self.assertIn("### CAL0-I7 validated-closure record", specification)
        self.assertIn("**Annex version:** 2.9", annex)
        self.assertIn("## CAL0-I7 — Validated-closure review", annex)

    def test_readable_closure_and_residual_handbooks_are_complete(self) -> None:
        closure = (ROOT / "guide/litrpg-system-validated-closure.md").read_text(encoding="utf-8")
        residuals = (ROOT / "guide/litrpg-system-residual-uncertainty-register.md").read_text(encoding="utf-8")
        for heading in ("## Closure result", "## VAL1.2D evidence matrix", "## Connected artifact set", "## I7 closure corrections", "## What closure freezes", "## What closure does not freeze"):
            self.assertIn(heading, closure)
        self.assertIn("**Items:** 305", residuals)
        self.assertIn("## Classification summary", residuals)
        self.assertIn("### CAL0-Q66B", residuals)


if __name__ == "__main__":
    unittest.main()
