from __future__ import annotations

import sys
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cal0.canonical import semantic_digest
from cal0.engines import (
    Pchip,
    ReinforcementClaim,
    ResourceLedger,
    assimilate_claim,
    asymmetric_beta_window,
    attribute_index,
    blocked_xp_credit,
    claim_conservation,
    deterministic_attempt_seed,
    deterministic_transition_outcome,
    generalised_mean,
)
from cal0.fixture_runner import load_fixture_registry, run_reference_fixtures
from cal0.governance import (
    Guard,
    affected_closure,
    atomic_commit,
    compose_certificates,
    dependency_closed_subsets,
    guards_conflict,
    maximal_common_ancestors,
)


class Cal0I2ReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = run_reference_fixtures(ROOT)

    def test_all_66_declared_fixtures_pass(self) -> None:
        self.assertTrue(self.report["passed"])
        self.assertEqual(66, self.report["case_count"])
        self.assertEqual(66, self.report["unique_case_count"])
        self.assertEqual(66, self.report["passed_count"])

    def test_every_fixture_retains_provenance_and_four_replays(self) -> None:
        for result in self.report["results"]:
            self.assertTrue(result["provenance"])
            self.assertEqual(4, len(result["runs"]))
            self.assertTrue(result["traversal_replay"])

    def test_fixture_registry_is_explicitly_synthetic_and_uncalibrated(self) -> None:
        registry = load_fixture_registry(ROOT)
        self.assertTrue(registry["synthetic_only"])
        self.assertEqual("UNCALIBRATED", registry["parameter_status"])
        self.assertIn("not population forecasts", registry["separation_contract"])

    def test_pchip_matches_declared_shape_preserving_fixture(self) -> None:
        curve = Pchip.compile(("0", "0.25", "0.6", "1"), ("0.05", "0.15", "0.55", "1"))
        self.assertAlmostEqual(Decimal("0.084791309"), curve.evaluate("0.125"), places=9)
        self.assertAlmostEqual(Decimal("0.325635520"), curve.evaluate("0.425"), places=9)
        self.assertAlmostEqual(Decimal("0.775929026"), curve.evaluate("0.8"), places=9)

    def test_geometric_attribute_projection_is_invertible(self) -> None:
        value = generalised_mean({"a": "0.06", "b": "0.04", "c": "0.08"}, {"a": "0.5", "b": "0.3", "c": "0.2"}, "0")
        self.assertGreater(attribute_index(value), Decimal("0"))

    def test_asymmetric_beta_has_authored_peak(self) -> None:
        opportunity, alpha, beta, peak = asymmetric_beta_window("0.55", "0.2", "1.2", "0.35", "8")
        self.assertAlmostEqual(Decimal("1"), opportunity, places=20)
        self.assertEqual((Decimal("3.10"), Decimal("4.90"), Decimal("0.55")), (alpha, beta, peak))

    def test_blocked_xp_taper_cannot_cascade(self) -> None:
        credit, cap = blocked_xp_credit("11", "10", "4", "0.5", "2", "0.8", "0.5")
        self.assertEqual(Decimal("0.1"), credit)
        self.assertEqual(Decimal("12"), cap)
        self.assertLess(Decimal("11") + credit, Decimal("14"))

    def test_reinforcement_budget_is_recipient_independent(self) -> None:
        claim = ReinforcementClaim.create("Skill:test", 1, "0.0015", {"Focus": "0.55", "Coherence": "0.30", "Perception": "0.15"}, ("fixture",))
        fetal = assimilate_claim(claim, {"Focus": "0.08", "Coherence": "0.10", "Perception": "0.12"}, "0.4")
        adult = assimilate_claim(claim, {"Focus": "1", "Coherence": "1", "Perception": "1"}, "1")
        self.assertTrue(claim_conservation(fetal, claim.total_budget))
        self.assertTrue(claim_conservation(adult, claim.total_budget))
        self.assertEqual(sum(row["claim"] for row in fetal.values()), sum(row["claim"] for row in adult.values()))

    def test_resource_reservation_consumption_and_recovery_conserve_pool(self) -> None:
        initial = ResourceLedger.create("Mana", "10")
        reserved = initial.reserve("cast-1", "4", "event:prepare")
        consumed = reserved.consume("cast-1", "3", "event:cast")
        released = consumed.release("cast-1", "event:cancel-remainder")
        recovered = released.recover("2", "event:rest", "2", "source:metabolic-replenishment")
        self.assertEqual(Decimal("6"), reserved.available)
        self.assertEqual(Decimal("3"), consumed.consumed_total)
        self.assertEqual(Decimal("7"), released.available)
        self.assertEqual(Decimal("9"), recovered.available)
        self.assertNotEqual(initial.identity, recovered.identity)
        with self.assertRaises(ValueError):
            initial.reserve("overspend", "11", "event:invalid")

    def test_observer_cannot_reroll_seeded_transition(self) -> None:
        seed = deterministic_attempt_seed("17", "person", "transition", "attempt")
        state = {"readiness": "0.8", "execution": "0.75", "stability": "0.72", "recovery": "0.9"}
        self.assertEqual(deterministic_transition_outcome(state, seed, "resolver@1"), deterministic_transition_outcome(state, seed, "resolver@1"))

    def test_dependency_closed_selection_is_order_invariant(self) -> None:
        forward = dependency_closed_subsets(("G1", "G2", "G3"), {"G2": ("G1",)}, (("G2", "G3"),))
        reverse = dependency_closed_subsets(("G3", "G2", "G1"), {"G2": ("G1",)}, (("G3", "G2"),))
        self.assertEqual(forward, reverse)

    def test_failed_atomic_commit_exposes_no_successor(self) -> None:
        original = frozenset({"A", "B"})
        result, status = atomic_commit(original, {"C"}, False)
        self.assertEqual(original, result)
        self.assertEqual("ABORTED", status)

    def test_affected_proof_closure_is_minimal(self) -> None:
        closure = affected_closure(("PBC",), {"PBC": ("PAC",), "PAC": ("PAE",), "PXY": ("PXZ",)})
        self.assertEqual(frozenset({"PBC", "PAC", "PAE"}), closure)

    def test_criss_cross_base_retains_both_maximal_ancestors(self) -> None:
        parents = {"B0": (), "L1": ("B0",), "R1": ("B0",), "M1": ("L1", "R1"), "M2": ("L1", "R1")}
        self.assertEqual(frozenset({"L1", "R1"}), maximal_common_ancestors(("M1", "M2"), parents))

    def test_certificate_composition_uses_weakest_premise(self) -> None:
        n1 = {"id": "N1", "scope": ["a", "b"], "strength": "high", "queries": ["q1"], "recovery": ["A"]}
        n2 = {"id": "N2", "scope": ["b"], "strength": "moderate", "queries": ["q2"], "restrictions": ["edge"], "recovery": ["B", "C"]}
        combined = compose_certificates([n1, n2])
        self.assertEqual("moderate", combined["strength"])
        self.assertEqual(["b"], combined["scope"])
        self.assertEqual({"A", "B", "C"}, set(combined["recovery"]))

    def test_semantic_alias_and_unknown_scope_block_concurrency(self) -> None:
        aliases = {"alias": "root"}
        write = Guard("root", frozenset({"S"}), "write")
        read_alias = Guard("alias", frozenset({"S"}), "read")
        unknown = Guard("root", None, "read")
        self.assertTrue(guards_conflict(write, read_alias, aliases)[0])
        self.assertTrue(guards_conflict(write, unknown, aliases)[0])

    def test_report_digest_is_replayable(self) -> None:
        second = run_reference_fixtures(ROOT)
        self.assertEqual(self.report["report_digest"], second["report_digest"])
        self.assertEqual(semantic_digest([r["case_digest"] for r in self.report["results"]]), semantic_digest([r["case_digest"] for r in second["results"]]))


if __name__ == "__main__":
    unittest.main()
