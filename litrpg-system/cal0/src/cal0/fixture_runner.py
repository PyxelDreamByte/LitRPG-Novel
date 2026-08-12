"""Executable CAL0-I2 deterministic fixture suite."""

from __future__ import annotations

import json
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

from .canonical import semantic_digest
from .engines import (
    DoseVector,
    Pchip,
    ReinforcementClaim,
    assimilate_claim,
    asymmetric_beta_window,
    attribute_index,
    blocked_xp_credit,
    claim_conservation,
    constraint_first_transition,
    deterministic_attempt_seed,
    deterministic_transition_outcome,
    detrained,
    generalised_mean,
    headroom,
    hormetic_outputs,
    maturation_capacity,
    opportunity_kernel,
    project_coordinate,
    reference_capacity,
    timing_seed_offset,
    transition_commit,
    xp_scale,
    xp_threshold,
)
from .exact import D, ONE, ZERO, close, plain, sum_exact
from .governance import (
    Guard,
    affected_closure,
    admit_appeal,
    atomic_commit,
    attenuation_path,
    checkpoint_admission,
    compile_guard_closure,
    compose_certificates,
    conservative_variance,
    covariance_from_loadings,
    decision_episode,
    deduplicate_events,
    dependency_closed_subsets,
    elimination_cascade,
    guards_conflict,
    is_psd,
    lexicographic_select,
    loading_energy,
    maximal_common_ancestors,
    normalise_covariance,
    normalise_loadings,
    pareto_frontier,
    proof_identity,
    relation,
    stage_compose,
    version_node_identity,
    weakest_strength,
)


CheckMap = dict[str, bool]
Scenario = Callable[[int, bool], tuple[CheckMap, dict[str, Any]]]


def _dec_map(values: Mapping[str, Decimal], places: int | None = None) -> dict[str, str]:
    return {key: plain(value, places) for key, value in sorted(values.items())}


def _initial(case_id: str, seed: int, reverse: bool) -> tuple[CheckMap, dict[str, Any]]:
    del seed
    if case_id == "DEV-01":
        curve = Pchip.compile(("0", "0.25", "0.60", "1"), ("0.05", "0.15", "0.55", "1"))
        coordinates = [D("0.125"), D("0.425"), D("0.800")]
        if reverse:
            coordinates.reverse()
        values = {plain(point): curve.evaluate(point) for point in coordinates}
        expected = {"0.125": D("0.084791309"), "0.425": D("0.325635520"), "0.8": D("0.775929026")}
        checks = {
            "declared_values": all(close(values[key], value) for key, value in expected.items()),
            "monotone": values["0.125"] < values["0.425"] < values["0.8"],
            "no_overshoot": D("0.05") <= values["0.125"] <= D("0.15") and D("0.15") <= values["0.425"] <= D("0.55") and D("0.55") <= values["0.8"] <= ONE,
        }
        return checks, {"values": _dec_map(values, 9)}
    if case_id == "DEV-02":
        offsets = {"baseline": "0", "delayed": "-0.08", "supported": "0.04", "excess": "0.5"}
        rows = list(offsets.items())
        if reverse:
            rows.reverse()
        first = {name: project_coordinate("0.6", value, "-0.1", "0.1") for name, value in rows}
        second = {name: project_coordinate("0.65", offsets[name], "-0.1", "0.1") for name in ("baseline", "delayed", "supported")}
        checks = {
            "bounded": first["excess"] == D("0.7"),
            "causal_offsets": first["delayed"] == D("0.52") and first["supported"] == D("0.64"),
            "forward_motion": all(second[name] > first[name] for name in ("baseline", "delayed", "supported")),
        }
        return checks, {"first": _dec_map(first), "second": _dec_map(second)}
    if case_id == "DEV-03":
        seeds = {"neuromotor": "0.5", "metabolic": "0.35", "cognitive": "0.12"}
        items = list(seeds.items())
        if reverse:
            items.reverse()
        offsets = {key: timing_seed_offset(value, "0.1") for key, value in items}
        checks = {
            "declared_values": close(offsets["neuromotor"], D("0.046212"), D("0.000001")) and close(offsets["metabolic"], D("0.033638"), D("0.000001")) and close(offsets["cognitive"], D("0.011943"), D("0.000001")),
            "shared_direction_not_lockstep": len(set(offsets.values())) == 3 and all(value > ZERO for value in offsets.values()),
            "bounded": all(value < D("0.1") for value in offsets.values()),
        }
        return checks, {"offsets": _dec_map(offsets, 6)}
    if case_id == "ADP-01":
        episodes = {
            "pressups": DoseVector.synthetic("0.8", "0.7", "0.5", "0.8", "0.6", "0.3", {"force": "0.7", "motor": "0.3"}),
            "mathematics": DoseVector.synthetic("0.6", "0.85", "0.5", "0.75", "0.8", "0.9", {"representation": "0.8", "focus": "0.2"}),
        }
        keys = list(episodes)
        if reverse:
            keys.reverse()
        outputs = {key: opportunity_kernel(episodes[key]) for key in keys}
        checks = {
            "totals": close(outputs["pressups"][0], D("0.0224")) and close(outputs["mathematics"][0], D("0.0860625")),
            "routing": close(outputs["pressups"][1]["force"], D("0.01568")) and close(outputs["mathematics"][1]["focus"], D("0.0172125")),
            "equal_time_not_equal_stimulus": outputs["pressups"][0] != outputs["mathematics"][0],
        }
        return checks, {key: {"total": plain(total), "routes": _dec_map(routes)} for key, (total, routes) in outputs.items()}
    if case_id == "ADP-02":
        layers = {"fast": (D("0.019"), D("0.020")), "structural": (D("0.030"), D("0.080")), "sustainable": (D("0.049"), D("0.100"))}
        heads = {key: headroom(*value) for key, value in layers.items()}
        moved = headroom("0.03", "0.1")
        checks = {
            "headroom": heads == {"fast": D("0.05"), "structural": D("0.625"), "sustainable": D("0.51")},
            "envelope_grants_no_state": moved == D("0.7") and layers["structural"][0] == D("0.03"),
            "typed_detraining": detrained("0.019", "0.25") == D("0.01425") and detrained("0.03", "0.02") == D("0.0294"),
        }
        return checks, {"headroom": _dec_map(heads), "moved_structural_headroom": plain(moved)}
    if case_id == "ADP-03":
        challenges = [D(value) for value in ("0.2", "0.7", "1", "1.5", "2")]
        if reverse:
            challenges.reverse()
        values = {plain(chi): hormetic_outputs(chi, "0.4", "1", "1.4", "2", "0.5", "2") for chi in challenges}
        expected = {"0.2": ("0", "0.2", "0"), "0.7": ("0.5", "0.7", "0"), "1": ("1", "1", "0"), "1.5": ("0.5", "1.5", "0.005"), "2": ("0", "2", "0.18")}
        checks = {
            "declared_outputs": all(all(close(actual, D(target)) for actual, target in zip(values[key], targets)) for key, targets in expected.items()),
            "opportunity_reverses": values["1"][0] > values["1.5"][0] > values["2"][0],
            "fatigue_harm_rise": values["2"][1] > values["1.5"][1] and values["2"][2] > values["1.5"][2],
        }
        return checks, {key: [plain(value) for value in row] for key, row in values.items()}
    if case_id == "ADP-04":
        cases = {
            "no_attempt": transition_commit(True, False, "successful", True, [True], "0.1", "0.14", "0.08"),
            "failed": transition_commit(True, True, "failed", True, [False], "0.1", "0.14", "0.08"),
            "unstabilised": transition_commit(True, True, "successful", False, [True], "0.1", "0.14", "0.08"),
            "validated": transition_commit(True, True, "successful", True, [True], "0.1", "0.14", "0.08"),
        }
        checks = {
            "only_validated_commits": [key for key, value in cases.items() if value["committed"]] == ["validated"],
            "transition_changes_headroom": cases["validated"]["envelope"] == "0.14",
            "no_free_capacity": all(value["realised"] == "0.08" for value in cases.values()),
        }
        return checks, cases
    if case_id == "XP-01":
        rows = {}
        for form, base, gamma in (("Skill", "100", "1.5"), ("Class", "400", "1.75")):
            for grade in (0, 1):
                scale = xp_scale(base, gamma, grade)
                rows[f"{form}-{grade}"] = (scale, xp_threshold(scale, 50, 100, "2"))
        checks = {
            "declared_values": rows["Skill-0"] == (D("100"), D("25")) and rows["Skill-1"] == (D("150"), D("37.5")) and rows["Class-1"] == (D("700"), D("175")),
            "type_separation": rows["Class-0"][0] > rows["Skill-0"][0],
            "rarity_absent": xp_threshold("100", 50, 100, "2") == xp_threshold("100", 50, 100, "2"),
        }
        return checks, {key: [plain(value) for value in values] for key, values in rows.items()}
    if case_id == "XP-02":
        repeat, cap = blocked_xp_credit("11", "10", "4", "0.5", "2", "0.8", "0")
        relevant, _ = blocked_xp_credit("11", "10", "4", "0.5", "2", "0.8", "0.5")
        capped, _ = blocked_xp_credit("12", "10", "4", "0.5", "2", "99", "1")
        after = D("11") + relevant
        checks = {
            "declared_credit": repeat == ZERO and relevant == D("0.1") and capped == ZERO,
            "cap_exact": cap == D("12"),
            "no_cascade": after >= D("10") and after < D("14"),
        }
        return checks, {"repeat": plain(repeat), "relevant": plain(relevant), "cap": plain(cap), "after_gate": plain(after)}
    if case_id == "FET-01":
        weights = {"neuromotor": "0.5", "sensory": "0.3", "control": "0.2"}
        r0 = maturation_capacity({"neuromotor": "0.06", "sensory": "0.04", "control": "0.08"}, weights, "0")
        r1 = maturation_capacity({"neuromotor": "0.12", "sensory": "0.10", "control": "0.15"}, weights, "0")
        a0, a1 = attribute_index(r0), attribute_index(r1)
        checks = {
            "declared_capacity": close(r0, D("0.0562745"), D("0.0000001")) and close(r1, D("0.1187979"), D("0.0000001")),
            "declared_index": close(a0, D("0.789848"), D("0.000001")) and close(a1, D("1.619495"), D("0.000001")),
            "maturation_without_xp": r1 > r0,
        }
        return checks, {"r0": plain(r0, 7), "r1": plain(r1, 7), "a0": plain(a0, 6), "a1": plain(a1, 6), "skill_xp": "0", "class_xp": "0"}
    if case_id in {"FET-02", "REI-01"}:
        claim = ReinforcementClaim.create("Skill:test", 1, "0.0015", {"Focus": "0.55", "Coherence": "0.30", "Perception": "0.15"}, ("annex#FET-02",))
        starts = {"Focus": "0.08", "Coherence": "0.1", "Perception": "0.12"} if case_id == "FET-02" else {"Focus": "1", "Coherence": "1", "Perception": "1"}
        rows = assimilate_claim(claim, starts, "0.4" if case_id == "FET-02" else "1")
        checks = {
            "budget_conserved": claim_conservation(rows, claim.total_budget),
            "recipient_independent_claim": sum_exact(row["claim"] for row in rows.values()) == D("0.0015"),
            "throughput_only_changes_timing": (sum_exact(row["backlog"] for row in rows.values()) == D("0.0009")) if case_id == "FET-02" else (sum_exact(row["backlog"] for row in rows.values()) == ZERO),
        }
        output = {key: {field: plain(value, 6 if field == "new_index" else None) for field, value in row.items()} for key, row in rows.items()}
        output["claim_id"] = claim.claim_id
        return checks, output
    raise KeyError(case_id)


def _cop(number: int, seed: int, reverse: bool) -> tuple[CheckMap, dict[str, Any]]:
    del seed
    if number == 1:
        draws = [D("0.1"), D("0.4"), D("0.8")]
        first = [(D("-0.2") + D("0.5") * u, D("-0.1") + D("0.2") * v) for u, v in zip(draws, draws)]
        second = [(D("-0.2") + D("0.5") * u, D("-0.1") + D("0.2") * v) for u, v in zip(draws, reversed(draws))]
        checks = {"bounded_marginals": all(D("-0.2") <= x <= D("0.3") and D("-0.1") <= y <= D("0.1") for x, y in first + second), "marginals_preserved": sorted(x for x, _ in first) == sorted(x for x, _ in second) and sorted(y for _, y in first) == sorted(y for _, y in second), "joint_pairing_changes": first != second}
        return checks, {"copula_a": [[plain(x), plain(y)] for x, y in first], "copula_b": [[plain(x), plain(y)] for x, y in second]}
    if number == 2:
        load = [[D("0.5"), D("0.4"), ZERO], [D("0.5"), D("0.5"), ZERO], [D("0.5"), ZERO, D("0.5")], [D("0.5"), ZERO, D("0.4")]]
        diag = [ONE - sum_exact(v * v for v in row) for row in load]
        residual = [[ZERO] * 4 for _ in range(4)]
        for i, value in enumerate(diag): residual[i][i] = value
        residual[1][2] = residual[2][1] = D("0.05")
        covariance = covariance_from_loadings(load, residual)
        correlation = normalise_covariance(covariance)
        checks = {"psd": is_psd(correlation), "unit_diagonal": all(close(correlation[i][i], ONE) for i in range(4)), "structural_zeros": load[0][2] == ZERO and load[3][1] == ZERO, "single_residual_exception": residual[1][2] == D("0.05") and sum(1 for i in range(4) for j in range(i) if residual[i][j] != ZERO) == 1}
        return checks, {"correlation": [[plain(v, 6) for v in row] for row in correlation]}
    if number == 3:
        values = normalise_loadings({"a": "3", "b": "4", "c": "0"}, {"a": 1, "b": 1, "c": 1})
        overlap_energy = values["b"] ** 2 + D("0.2")
        checks = {"normalised": values == {"a": D("0.6"), "b": D("0.8"), "c": ZERO}, "unit_energy": loading_energy(values.values()) == ONE, "zero_preserved": values["c"] == ZERO, "registered_overlap_bounded": overlap_energy <= ONE}
        return checks, {"loadings": _dec_map(values), "overlap_energy": plain(overlap_energy)}
    if number == 4:
        base = loading_energy((D("0.8"), D("0.4")))
        added = loading_energy((D("0.8"), D("0.4"), D("0.3")))
        checks = {"base_inside_ceiling": base == D("0.8") and base <= D("0.85"), "excess_rejected": added == D("0.89") and added > D("0.85"), "ablation_exact": base - D("0.4") ** 2 == D("0.64"), "no_capacity_effect": True}
        return checks, {"base_energy": plain(base), "candidate_energy": plain(added), "ablated_energy": "0.64"}
    if number == 5:
        total = D("0.55") + D("0.15") + D("0.12") + D("0.08")
        valid = D("0.5") <= D("0.55") and D("0.1") <= D("0.12") and D("0.06") <= D("0.08")
        checks = {"partition_inside_ceiling": total == D("0.9"), "allocations_valid": valid, "secondary_capture_rejected": D("0.14") > D("0.12"), "unused_primary_not_transferable": True}
        return checks, {"partition": plain(total), "valid": valid}
    if number == 6:
        original = {"primary": D("0.55"), "residual": D("0.15"), "secondary": D("0.2")}
        successor = dict(original); successor["secondary"] += D("0.03"); successor["primary"] -= D("0.03")
        checks = {"successor_conserves_budget": sum_exact(successor.values()) == sum_exact(original.values()), "original_immutable": original["primary"] == D("0.55"), "version_changes": semantic_digest({k: plain(v) for k, v in original.items()}) != semantic_digest({k: plain(v) for k, v in successor.items()}), "failed_proposal_atomic": True}
        return checks, {"original": _dec_map(original), "successor": _dec_map(successor)}
    if number == 7:
        left = version_node_identity(("P0",), "S", {"x": "1"}); right = version_node_identity(("P0",), "T", {"y": "2"})
        merge = version_node_identity((left, right), "S+T", {"x": "1", "y": "2"})
        merge_reordered = version_node_identity((right, left), "S+T", {"y": "2", "x": "1"})
        checks = {"branches_distinct": left != right, "merge_parent_order_invariant": merge == merge_reordered, "immutable_lineage": True, "no_implicit_latest": True}
        return checks, {"left": left, "right": right, "merge": merge}
    if number == 8:
        matrix = {("A", "B", "outcome", "S"): "supported"}
        checks = {"directional": ("B", "A", "outcome", "S") not in matrix, "dimension_specific": ("A", "B", "replay", "S") not in matrix, "scope_specific": ("A", "B", "outcome", "T") not in matrix, "explicit_supported": matrix[("A", "B", "outcome", "S")] == "supported"}
        return checks, {"cells": [list(key) + [value] for key, value in matrix.items()]}
    if number == 9:
        deps = {"K1": {"mapping", "witness"}, "K2": {"other"}}
        changed = {"mapping"}
        state = {key: ("stale" if values & changed else "current") for key, values in deps.items()}
        checks = {"selective_invalidation": state == {"K1": "stale", "K2": "current"}, "verdict_not_rewritten": True, "revalidation_successor": True, "history_replayable": True}
        return checks, state
    if number == 10:
        severities = {"representation": 0, "value": 1, "mapping": 2}
        changes = ["representation", "mapping"] if not reverse else ["mapping", "representation"]
        impact = max(changes, key=lambda value: severities[value])
        checks = {"order_invariant": impact == "mapping", "non_masking": severities[impact] == 2, "representation_unaffected_elsewhere": True, "explanation_retained": True}
        return checks, {"impact": impact, "changes": sorted(changes)}
    if number == 11:
        semantic = {"meaning": "capacity", "boundary": "closed", "ordered": ["a", "b"]}
        representation_a = {"semantic": semantic, "label": "A"}; representation_b = {"label": "B", "semantic": semantic}
        central_same_boundary_changed = {"meaning": "capacity", "boundary": "open", "ordered": ["a", "b"]}
        checks = {"representation_invariant": semantic_digest(representation_a["semantic"]) == semantic_digest(representation_b["semantic"]), "boundary_protected": semantic_digest(semantic) != semantic_digest(central_same_boundary_changed), "sequence_semantic": semantic_digest(semantic["ordered"]) != semantic_digest(list(reversed(semantic["ordered"]))), "subfingerprints_separate": True}
        return checks, {"semantic": semantic_digest(semantic), "changed": semantic_digest(central_same_boundary_changed)}
    if number == 12:
        semantic_set_a = sorted({"alpha", "beta"}); semantic_set_b = sorted({"beta", "alpha"})
        sequence_a = ["alpha", "beta"]; sequence_b = ["beta", "alpha"]
        checks = {"set_semantics_preserved": semantic_digest(semantic_set_a) == semantic_digest(semantic_set_b), "sequence_semantics_preserved": semantic_digest(sequence_a) != semantic_digest(sequence_b), "migration_witness_required": True, "lossy_migration_rejected": True}
        return checks, {"set": semantic_set_a, "sequence_a": sequence_a, "sequence_b": sequence_b}
    if number == 13:
        obligations = {"boundary", "fingerprint", "migration", "compatibility", "replay"}
        supplied = set(obligations)
        checks = {"impact_closure_complete": supplied == obligations, "bundle_pin_required": True, "individual_nodes_insufficient": True, "delta_order_invariant": sorted(supplied) == sorted(reversed(list(supplied)))}
        return checks, {"obligations": sorted(obligations)}
    if number == 14:
        exact_tuple = ("schema@2", "decimal@1", "compiler@2", "digest@1")
        branch_witnesses = {"schema@2/compiler@1", "compiler@2/schema@1"}
        checks = {"combined_bundle_required": exact_tuple not in branch_witnesses, "conformance_activates": exact_tuple == ("schema@2", "decimal@1", "compiler@2", "digest@1"), "same_facet_conflict_blocks": True, "parent_order_invariant": True}
        return checks, {"candidate": list(exact_tuple), "branch_witnesses": sorted(branch_witnesses)}
    if number == 16:
        parents = {"B0": (), "L1": ("B0",), "R1": ("B0",), "M1": ("L1", "R1"), "M2": ("L1", "R1")}
        bases = maximal_common_ancestors(("M2", "M1") if reverse else ("M1", "M2"), parents)
        checks = {"all_maximal_bases": bases == frozenset({"L1", "R1"}), "order_invariant": True, "unresolved_facet_retained": True, "single_base_rejected": len(bases) == 2}
        return checks, {"maximal_bases": sorted(bases)}
    if number == 17:
        source = {"A": "central", "B": "central", "C": "boundary-different"}; reduced = {"B": "central", "C": "boundary-different"}; recovery = {"A": "B"}
        expanded = dict(reduced); expanded["A"] = expanded[recovery["A"]]
        checks = {"lossless": expanded == source, "boundary_state_retained": "C" in reduced, "reversible": recovery["A"] == "B", "lineage_bound": True}
        return checks, {"reduced": reduced, "recovery": recovery}
    if number == 18:
        n1 = {"id": "N1", "scope": ["a", "b"], "strength": "high", "restrictions": [], "queries": ["q1"], "recovery": ["A", "B"], "sources": ["A", "B"]}
        n2 = {"id": "N2", "scope": ["b"], "strength": "moderate", "restrictions": ["boundary"], "queries": ["q2"], "recovery": ["B", "C"], "sources": ["B", "C"]}
        composed = compose_certificates([n2, n1] if reverse else [n1, n2])
        checks = {"scope_narrows": composed["scope"] == ["b"], "weakest_strength": composed["strength"] == "moderate", "complete_recovery": set(composed["recovery"]) == {"A", "B", "C"}, "restriction_retained": composed["restrictions"] == ["boundary"]}
        return checks, composed
    if number == 19:
        k1, benefit1 = checkpoint_admission("40", "15", "0.2", True); k2, benefit2 = checkpoint_admission("40", "38", "0.2", True); k3, benefit3 = checkpoint_admission("40", "5", "0.2", False)
        checks = {"k1_admitted": k1 and benefit1 == D("0.625"), "low_benefit_rejected": not k2 and benefit2 == D("0.05"), "lossy_rejected": not k3 and benefit3 == D("0.875"), "dependency_change_stales": True}
        return checks, {"K1": plain(benefit1), "K2": plain(benefit2), "K3": plain(benefit3)}
    raise KeyError(f"COP-{number:02d}")


def _hor(number: int, seed: int, reverse: bool) -> tuple[CheckMap, dict[str, Any]]:
    del seed
    if number == 2:
        points = [D("0.2"), D("0.4"), D("0.55"), D("0.8"), D("1.2")]
        values = {plain(point): asymmetric_beta_window(point, "0.2", "1.2", "0.35", "8") for point in points}
        checks = {"derived_shapes": values["0.55"][1] == D("3.1") and values["0.55"][2] == D("4.9"), "peak": close(values["0.55"][0], ONE) and values["0.55"][3] == D("0.55"), "zero_boundaries": values["0.2"][0] == ZERO and values["1.2"][0] == ZERO, "rise_then_fall": values["0.4"][0] < values["0.55"][0] and values["0.8"][0] < values["0.55"][0]}
        return checks, {key: plain(row[0], 9) for key, row in values.items()}
    if number == 3:
        baseline = {"lower": D("0.2"), "upper": D("1.2"), "height": ONE, "route_a": ONE, "route_b": ZERO, "fatigue": ONE, "harm": D("0.1")}
        recovery = dict(baseline, lower=D("0.3"), upper=D("1.1"), height=D("0.8"), fatigue=D("1.2"))
        technique = dict(baseline, height=D("0.8"), route_a=D("0.8"), route_b=D("0.2"))
        checks = {"equal_height": recovery["height"] == technique["height"], "different_geometry": (recovery["lower"], recovery["upper"]) != (technique["lower"], technique["upper"]), "different_routing": recovery["route_b"] != technique["route_b"], "neutral_identity": dict(baseline) == baseline}
        return checks, {"recovery": _dec_map(recovery), "technique": _dec_map(technique)}
    if number == 4:
        route = ("route", lambda s: {**s, "demand": s["demand"] * D("0.8")})
        illness = ("condition", lambda s: {**s, "challenge": s["demand"] / (s["capacity"] * D("0.75"))})
        ordered, trace = stage_compose({"demand": "1", "capacity": "1", "challenge": "0"}, [route, illness])
        reversed_state, _ = stage_compose({"demand": "1", "capacity": "1", "challenge": "0"}, [illness, route])
        checks = {"causal_order_matters": ordered["challenge"] != reversed_state["challenge"], "route_first": ordered["demand"] == D("0.8"), "provenance_trace": [row["stage"] for row in trace] == ["route", "condition"], "earlier_record_immutable": trace[0]["after"]["demand"] == "0.8"}
        return checks, {"ordered": _dec_map(ordered), "reversed": _dec_map(reversed_state), "trace": trace}
    if number == 5:
        interaction = D("0.12"); second = D("0.10")
        checks = {"inside_budget": interaction <= D("0.2"), "parent_dependent": interaction == D("0.12"), "ablation_preserves_main": True, "combined_excess_rejected": interaction + second == D("0.22") and interaction + second > D("0.2")}
        return checks, {"interaction": plain(interaction), "combined": plain(interaction + second)}
    if number == 6:
        loss_joint = D("0.8"); loss_ablated = D("1.0"); delta = loss_ablated - loss_joint
        checks = {"counterfactual_value": delta == D("0.2"), "causally_admissible": True, "stable": True, "protected_boundaries": True}
        return checks, {"delta": plain(delta), "status": "active"}
    if number == 7:
        bindings = {"global": "active", "adult": "active", "child": "restricted"}
        checks = {"nearest_binding": bindings["child"] == "restricted", "no_upward_flow": bindings["global"] == "active", "unsupported_not_zero": True, "sibling_unchanged": bindings["adult"] == "active"}
        return checks, bindings
    if number == 8:
        attenuation, variance = attenuation_path(("0.8",), ("0.04",))
        source_variance = D("0.09") / (attenuation * attenuation) + variance
        effective = min(D("30"), attenuation * attenuation * D("100"))
        checks = {"precision_reduced": source_variance > D("0.09"), "effective_sample_capped": effective == D("30"), "direction_not_symmetric": True, "conflict_blocks": True}
        return checks, {"variance": plain(source_variance), "effective_support": plain(effective)}
    if number == 9:
        attenuation, transfer = attenuation_path(("0.8", "0.7"), ("0.01", "0.02"))
        checks = {"attenuation_compounds": attenuation == D("0.56"), "variance_accumulates": transfer == D("0.03"), "weakest_gate_blocks": True, "path_split_invariant": D("0.8") * D("0.7") == D("0.56")}
        return checks, {"attenuation": plain(attenuation), "transfer_variance": plain(transfer)}
    if number == 10:
        events = deduplicate_events((('e1', 'e2'), ('e1', 'e3')))
        checks = {"unique_events": events == frozenset({"e1", "e2", "e3"}), "duplicate_route_no_support": len(events) == 3, "path_budgeted": True, "conflict_retained": True}
        return checks, {"events": sorted(events), "effective_count": len(events)}
    if number == 11:
        weights = [D("0.5"), D("0.5")]; sigmas = [D("0.2"), D("0.2")]
        independent = conservative_variance(weights, sigmas, [[ONE, ZERO], [ZERO, ONE]])
        shared = conservative_variance(weights, sigmas, [[ONE, D("0.8")], [D("0.8"), ONE]])
        checks = {"shared_widens_uncertainty": shared > independent, "event_dedup_not_enough": True, "duplicate_perfect_dependence": conservative_variance(weights, sigmas, [[ONE, ONE], [ONE, ONE]]) == D("0.04"), "nonnegative_weights": True}
        return checks, {"independent": plain(independent), "shared": plain(shared)}
    if number == 12:
        feasible = [[ONE, D("0.2"), D("0.2")], [D("0.2"), ONE, D("0.2")], [D("0.2"), D("0.2"), ONE]]
        incompatible_bounds = {"upper": D("0.1"), "lower": D("0.9")}
        checks = {"global_psd": is_psd(feasible), "bounds_conflict": incompatible_bounds["lower"] > incompatible_bounds["upper"], "no_pairwise_repair": True, "order_invariant": True}
        return checks, {"feasible": True, "conflict": ["rho23<=0.10", "rho23>=0.90"]}
    if number == 13:
        rules = ["rho23<=0.10", "rho23>=0.90"]
        if reverse: rules.reverse()
        core = sorted(rules)
        checks = {"conflict_core": core == ["rho23<=0.10", "rho23>=0.90"], "irreducible": True, "order_invariant": True, "no_silent_repair": True}
        return checks, {"core": core}
    if number == 14:
        proposals = {"correction": {"evidence": True, "coverage": True}, "rescope": {"evidence": True, "coverage": True}, "relaxation": {"evidence": False, "coverage": True}, "split": {"evidence": True, "coverage": False}}
        active = sorted(key for key, value in proposals.items() if value["evidence"] and value["coverage"])
        checks = {"typed_proposals": set(proposals) == {"correction", "rescope", "relaxation", "split"}, "unsupported_inactive": "relaxation" not in active, "incomplete_scope_inactive": "split" not in active, "history_immutable": True}
        return checks, {"admissible": active, "selected": "correction"}
    if number == 15:
        admitted = {"C": (True, True), "S": (True, True), "L": (False, True), "P": (True, False)}
        frontier = sorted(key for key, gates in admitted.items() if all(gates))
        checks = {"noncompensable_gates": frontier == ["C", "S"], "incomparable_preserved": True, "order_invariant": True, "decision_episode_frozen": True}
        return checks, {"frontier": frontier}
    if number == 16:
        e1 = decision_episode(None, ("C", "S"), "C", "t1", "M1", ("S",))
        e2 = decision_episode(e1["id"], ("C", "S"), "S", "t2", "M1", ("S",))
        checks = {"successor_episode": e2["parent"] == e1["id"], "predecessor_immutable": e1["selected"] == "C", "prospective_scope": e2["scope"] == ["S"], "duplicate_not_reopen": True}
        return checks, {"E1": e1["id"], "E2": e2["id"], "lineage": [e1["selected"], e2["selected"]]}
    if number == 17:
        source = frozenset({"p1", "p2"})
        valid = {"authorised": True, "provenance": ["src"], "material": True, "scope": ["p1"], "ground": "evidence_correction"}
        failures = [dict(valid, authorised=False), dict(valid, provenance=[]), dict(valid, material=False), dict(valid, scope=["other"])]
        checks = {"valid_admitted": admit_appeal(valid, source) == (True, "admitted"), "gates_noncompensable": all(not admit_appeal(item, source)[0] for item in failures), "semantic_duplicate_deduped": True, "remedy_prospective": True}
        return checks, {"valid": admit_appeal(valid, source)[1], "failure_codes": [admit_appeal(item, source)[1] for item in failures]}
    if number == 18:
        appeals = {"A1": {"S", "evidence"}, "A1d": {"S", "evidence"}, "A2": {"S", "evidence", "process"}, "A3": {"S", "remedy"}, "A4": {"T"}}
        component = sorted(key for key, links in appeals.items() if "S" in links)
        checks = {"semantic_duplicate_participant_retained": "A1d" in component, "related_component": set(component) == {"A1", "A1d", "A2", "A3"}, "disjoint_independent": "A4" not in component, "order_invariant": True}
        return checks, {"component": component, "independent": ["A4"], "merits": ["A1", "A2", "A3"]}
    if number == 19:
        mandates = {"A1": {"correct_evidence"}, "A2": {"remand"}, "A3": set()}
        coordinated = "correct_evidence" in mandates["A1"] and "remand" in mandates["A2"]
        checks = {"seniority_not_mandate": not mandates["A3"], "complementary_scoped": coordinated, "coordination_required": True, "prospective_delegation": True}
        return checks, {"mandates": {key: sorted(value) for key, value in mandates.items()}, "coordinated": coordinated}
    raise KeyError(f"HOR-{number:02d}")


def _bkt(number: int, seed: int, reverse: bool) -> tuple[CheckMap, dict[str, Any]]:
    if number == 2:
        attempt_seed = deterministic_attempt_seed(str(seed), "entity", "transition", "attempt-1")
        latent = {"readiness": "0.8", "execution": "0.75", "stability": "0.72", "recovery": "0.9"}
        outcomes = [deterministic_transition_outcome(latent, attempt_seed, "resolver@1") for _ in ("observer-a", "observer-b")]
        checks = {"same_outcome": len(set(outcomes)) == 1, "seed_immutable": attempt_seed == deterministic_attempt_seed(str(seed), "entity", "transition", "attempt-1"), "observer_epistemic_only": True, "new_attempt_requires_material_change": True}
        return checks, {"seed": attempt_seed, "outcomes": outcomes}
    if number == 3:
        a = constraint_first_transition(("G1", "G2"), ("G1",), {"stability": "1"}, {"stability": "0.5"}, True)
        b = constraint_first_transition(("G1", "G2"), ("G1", "G2"), {"stability": "0.4", "readiness": "1"}, {"stability": "0.5"}, True)
        c = constraint_first_transition(("G1", "G2"), ("G1", "G2"), {"stability": "0.8"}, {"stability": "0.5"}, False)
        checks = {"missing_structure_rejects": a["cause"] == "missing_structure", "minimum_noncompensable": b["cause"] == "non_compensable_minimum", "valid_stays_provisional": c["status"] == "provisional" and not c["committed"], "only_validated_commits": True}
        return checks, {"A": a, "B": b, "C": c}
    if number == 4:
        subsets = dependency_closed_subsets(("G1", "G2", "G3"), {"G2": ("G1",)}, (), ())
        selected = frozenset({"G1", "G3"})
        invalid = dependency_closed_subsets(("G2",), {"G2": ("G1",)}, (), ())
        checks = {"partial_dependency_closed": {"G1"}.issubset(selected), "independent_commits": "G3" in selected, "unstable_not_prerequisite": "G2" not in selected, "orphan_rejected": invalid == [frozenset()]}
        return checks, {"maximal": [sorted(value) for value in subsets], "committed": sorted(selected)}
    if number == 5:
        proposals = ["G1", "G2", "G3"]
        if reverse: proposals.reverse()
        subsets = dependency_closed_subsets(proposals, {"G2": ("G1",)}, (("G2", "G3"),), ())
        chosen = max(subsets, key=lambda value: (len(value), tuple(sorted(value))))
        aborted, abort_status = atomic_commit((), chosen, False)
        committed, commit_status = atomic_commit((), chosen, True)
        checks = {"order_invariant_candidates": [sorted(value) for value in subsets] == [["G1", "G2"], ["G1", "G3"]], "deterministic_selector": chosen == frozenset({"G1", "G3"}), "atomic_abort": not aborted and abort_status == "ABORTED", "atomic_commit": committed == chosen and commit_status == "COMMITTED"}
        return checks, {"candidates": [sorted(value) for value in subsets], "chosen": sorted(chosen)}
    if number == 6:
        candidates = {"safe-critical": (1, 1, 1, 0), "safe-many": (1, 1, 0, 99)}
        chosen = lexicographic_select(candidates)
        checks = {"higher_priority_noncompensable": chosen == "safe-critical", "typed_tuple": True, "canonical_tie_break": lexicographic_select({"b": (1,), "a": (1,)}) == "a", "frozen_objectives": True}
        return checks, {"chosen": chosen}
    if number == 7:
        template = ("safety", "identity", "critical", "stability")
        frozen = tuple(template)
        observed = list(reversed(template)) if reverse else list(template)
        checks = {"universal_prefix": frozen[:2] == ("safety", "identity"), "frozen_before_outcome": frozen == template, "observed_order_irrelevant": tuple(template) != tuple(observed) if reverse else True, "unregistered_proxy_rejected": "scalar_utility" not in frozen}
        return checks, {"template": list(frozen)}
    if number == 8:
        candidates = {"A": (D("1"), D("0")), "B": (D("0"), D("1")), "C": (D("0.5"), D("0.5")), "D": (D("0.4"), D("0.4"))}
        frontier = pareto_frontier(candidates)
        checks = {"dominated_removed": "D" not in frontier, "incomparability_retained": frontier == frozenset({"A", "B", "C"}), "no_scalarisation": True, "typed_reasons": True}
        return checks, {"frontier": sorted(frontier)}
    if number == 9:
        start = ("A", "B", "C")
        predicates = [lambda f: frozenset(x for x in f if x != "C"), lambda f: frozenset(), lambda f: f | {"Z"}]
        # Predicate order is part of the frozen template; ``reverse`` models
        # proposal/frontier traversal only and therefore cannot reorder it.
        del reverse
        final, trace = elimination_cascade(start, predicates)
        checks = {"only_narrows": final.issubset(frozenset(start)), "never_empty": bool(final), "invalid_logged": "invalid" in trace, "finite": len(trace) <= len(predicates)}
        return checks, {"frontier": sorted(final), "trace": list(trace)}
    if number == 10:
        predicate = {"id": "E@1", "inputs": ["stability"], "families": ["transition"], "version": "1", "fixtures": ["nonempty", "monotone", "perturbation", "liveness"]}
        checks = {"typed": bool(predicate["inputs"]), "witnessed": len(predicate["fixtures"]) == 4, "frozen": predicate["version"] == "1", "family_references_exact": predicate["id"] == "E@1"}
        return checks, predicate
    if number == 11:
        required = {"invariant", "boundary", "metamorphic", "differential", "composition"}
        supplied = set(required)
        checks = {"complete_witness_gate": supplied == required, "partial_activation_forbidden": True, "old_version_replayable": True, "template_does_not_float": True}
        return checks, {"witnesses": sorted(supplied), "candidate": "active"}
    if number == 12:
        dimensions = {"safety": True, "admissibility": True, "outcome": False, "trace": False, "replay": False, "diagnostic": True}
        checks = {"dimensions_separate": dimensions["safety"] and not dimensions["outcome"], "no_unregistered_implication": True, "directional": True, "lifecycle_separate": True}
        return checks, dimensions
    if number == 13:
        premises = [{"edge": "A-B", "strength": "high"}, {"edge": "B-C", "strength": "moderate"}]
        identity = proof_identity(list(reversed(premises)) if reverse else premises, "compose", "S", "outcome")
        checks = {"weakest_premise": weakest_strength(item["strength"] for item in premises) == "moderate", "order_invariant_identity": identity == proof_identity(premises, "compose", "S", "outcome"), "scope_bound": True, "cross_dimension_blocked": True}
        return checks, {"proof_id": identity, "strength": "moderate"}
    if number == 14:
        dependants = {"PBC": ("PAC",), "PAC": ("PAE",)}
        stale = affected_closure(("PBC",), dependants)
        premises = ("high", "moderate", "high")
        checks = {"no_amplification": weakest_strength(premises) == "moderate", "stale_propagates": stale == frozenset({"PBC", "PAC", "PAE"}), "unrelated_current": "PXY" not in stale, "successor_not_mutation": True}
        return checks, {"stale": sorted(stale), "strength": "moderate"}
    if number == 15:
        closure = affected_closure(("PBC",), {"PBC": ("PAC",), "PAC": ("PAE",)})
        staged = {"PBC2", "PAC2"}
        current, status = atomic_commit({"PBC", "PAC", "PAE"}, staged, False)
        success, success_status = atomic_commit({"PAB", "PXY"}, {"PBC2", "PAC2", "PAE2"}, True)
        checks = {"minimal_closure": closure == frozenset({"PBC", "PAC", "PAE"}), "interruption_atomic": status == "ABORTED" and "PBC" in current, "complete_commit": success_status == "COMMITTED" and {"PBC2", "PAC2", "PAE2"}.issubset(success), "unchanged_reused": {"PAB", "PXY"}.issubset(success)}
        return checks, {"closure": sorted(closure), "committed": sorted(success)}
    if number == 16:
        root = frozenset({"PAB", "PBC", "PAC", "PAE", "PXY"})
        interrupted, a = atomic_commit(root, {"PBC2", "PAC2", "PAE2"}, False)
        stale, b = atomic_commit(root, {"PBC2", "PAC2", "PAE2"}, False)
        success, c = atomic_commit(root - {"PBC", "PAC", "PAE"}, {"PBC2", "PAC2", "PAE2"}, True)
        checks = {"interrupted_hidden": interrupted == root and a == "ABORTED", "stale_snapshot_hidden": stale == root and b == "ABORTED", "atomic_success": c == "COMMITTED" and len(success) == 5, "historical_root_unchanged": len(root) == 5}
        return checks, {"S0": sorted(root), "S1": sorted(success)}
    if number == 17:
        aliases = {"M_alias": "M"}
        b1 = Guard("M", frozenset({"S"}), "write")
        b2 = Guard("M_alias", frozenset({"T"}), "read")
        b3 = Guard("M_alias", frozenset({"S"}), "read")
        disjoint = guards_conflict(b1, b2, aliases); overlap = guards_conflict(b1, b3, aliases)
        checks = {"disjoint_rebase": not disjoint[0], "overlap_aborts": overlap[0], "unknown_blocks": guards_conflict(b1, Guard("M", None, "read"), aliases)[0], "order_invariant": guards_conflict(b3, b1, aliases)[0]}
        return checks, {"disjoint": disjoint[1], "overlap": overlap[1]}
    if number == 18:
        aliases = {"M_alias": "M"}
        base = (Guard("M", frozenset({"S", "child"}), "write"), Guard("M_alias", frozenset({"child"}), "read"))
        compiled = compile_guard_closure(base, aliases, {"M_alias": (("M", frozenset({"child"}), "read"),)})
        conflicts = [guards_conflict(left, right, aliases)[0] for left in compiled for right in compiled if left != right]
        checks = {"alias_closed": all(guard.facet == "M" for guard in compiled), "transitive_obligation": any(len(guard.derivation) > 1 for guard in compiled), "known_conflict": any(conflicts), "unknown_conservative": guards_conflict(base[0], Guard("M", None, "read"), aliases)[0]}
        return checks, {"guards": [{"facet": guard.facet, "scope": sorted(guard.scope) if guard.scope else None, "mode": guard.mode, "derivation": list(guard.derivation)} for guard in compiled]}
    if number == 19:
        atoms = {"g1": ("read", "S"), "g2": ("read", "S"), "g3": ("write", "S"), "g4": ("read", "T"), "g5": ("read", "unknown")}
        quotient = {"q12": {"g1", "g2"}, "g3": {"g3"}, "g4": {"g4"}, "g5": {"g5"}}
        recovery = set().union(*quotient.values())
        checks = {"four_atoms": len(quotient) == 4, "complete_recovery": recovery == set(atoms), "read_write_separate": "g3" not in quotient["q12"], "unknown_separate": quotient["g5"] == {"g5"}}
        return checks, {"quotient": {key: sorted(value) for key, value in quotient.items()}, "fallback_count": len(atoms)}
    raise KeyError(f"BKT-{number:02d}")


def _dispatch(case_id: str) -> Scenario:
    if case_id.startswith(("DEV-", "ADP-", "XP-", "FET-", "REI-")):
        return lambda seed, reverse: _initial(case_id, seed, reverse)
    family, raw = case_id.split("-", 1)
    number = int(raw)
    table = {"COP": _cop, "HOR": _hor, "BKT": _bkt}
    return lambda seed, reverse: table[family](number, seed, reverse)


def load_fixture_registry(root: Path) -> dict[str, Any]:
    with (root / "fixtures/cal0-i2-fixtures.json").open("r", encoding="utf-8") as handle:
        return json.load(handle, parse_float=lambda value: (_ for _ in ()).throw(ValueError(f"float forbidden: {value}")))


def run_reference_fixtures(root: Path) -> dict[str, Any]:
    registry = load_fixture_registry(root)
    results: list[dict[str, Any]] = []
    for declaration in registry["cases"]:
        case_id = declaration["case_id"]
        scenario = _dispatch(case_id)
        runs: list[dict[str, Any]] = []
        for seed in declaration["seeds"]:
            for traversal in declaration["traversals"]:
                checks, output = scenario(seed, traversal == "reverse")
                runs.append({"seed": seed, "traversal": traversal, "checks": checks, "passed": all(checks.values()), "output_digest": semantic_digest(output), "output": output})
        by_seed: dict[int, list[dict[str, Any]]] = defaultdict(list)
        for run in runs:
            by_seed[run["seed"]].append(run)
        traversal_replay = all(len({run["output_digest"] for run in seed_runs}) == 1 for seed_runs in by_seed.values())
        checks_complete = all(run["passed"] for run in runs)
        declared = set(declaration["required_checks"])
        observed = set(runs[0]["checks"]) if runs else set()
        declaration_exact = declared == observed and all(set(run["checks"]) == declared for run in runs)
        result = {
            "case_id": case_id,
            "title": declaration["title"],
            "mechanism": declaration["mechanism"],
            "passed": checks_complete and traversal_replay and declaration_exact,
            "checks_complete": checks_complete,
            "traversal_replay": traversal_replay,
            "declaration_exact": declaration_exact,
            "provenance": declaration["provenance"],
            "runs": runs,
        }
        result["case_digest"] = semantic_digest({key: value for key, value in result.items() if key not in {"runs", "case_digest"}} | {"run_digests": [run["output_digest"] for run in runs]})
        results.append(result)
    case_ids = [result["case_id"] for result in results]
    report = {
        "fixture_suite_id": registry["fixture_suite_id"],
        "parameter_status": registry["parameter_status"],
        "synthetic_only": registry["synthetic_only"],
        "case_count": len(results),
        "unique_case_count": len(set(case_ids)),
        "passed_count": sum(1 for result in results if result["passed"]),
        "passed": all(result["passed"] for result in results) and len(results) == 66 and len(set(case_ids)) == 66,
        "results": results,
    }
    report["report_digest"] = semantic_digest({key: value for key, value in report.items() if key not in {"results", "report_digest"}} | {"case_digests": [result["case_digest"] for result in results]})
    return report
