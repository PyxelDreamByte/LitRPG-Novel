from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cal0.canonical import CanonicalisationError, canonical_bytes, semantic_digest
from cal0.validator import load_and_validate, run_fixtures, validation_report


class Cal0FoundationRegressionTests(unittest.TestCase):
    def test_active_bundle_is_complete_and_valid(self) -> None:
        docs, issues = load_and_validate(ROOT)
        self.assertEqual([], issues)
        self.assertEqual(66, len(docs["registries/model-families.json"]["entries"]))

    def test_report_exposes_i7_validated_closure_status(self) -> None:
        report = validation_report(ROOT)
        self.assertTrue(report["valid"])
        self.assertEqual("AUTHORING_VALIDATED_PROVISIONAL", report["parameter_status"])
        self.assertEqual("VALIDATED_BASELINE_WITH_BOUNDED_RESIDUALS", report["closure_status"])
        self.assertEqual("bundle://cal0/i7@0.7.0", report["bundle_id"])

    def test_all_declared_failure_fixtures_pass(self) -> None:
        results = run_fixtures(ROOT)
        self.assertEqual(48, len(results))
        self.assertTrue(all(case["passed"] for case in results), results)

    def test_canonical_mapping_order_is_irrelevant(self) -> None:
        left = {"b": ["2", "1"], "a": {"x": "3.00"}}
        right = {"a": {"x": "3.00"}, "b": ["2", "1"]}
        self.assertEqual(canonical_bytes(left), canonical_bytes(right))
        self.assertEqual(semantic_digest(left), semantic_digest(right))

    def test_sequence_order_remains_semantic(self) -> None:
        self.assertNotEqual(semantic_digest(["a", "b"]), semantic_digest(["b", "a"]))

    def test_binary_floats_are_rejected(self) -> None:
        with self.assertRaises(CanonicalisationError):
            canonical_bytes({"coefficient": 0.1})

    def test_json_float_tokens_fail_loading(self) -> None:
        source = ROOT / "registries/model-families.json"
        data = json.loads(source.read_text(encoding="utf-8"))
        data["entries"][0]["unexpected_float"] = 0.1
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "value.json"
            target.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(CanonicalisationError):
                canonical_bytes(json.loads(target.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
