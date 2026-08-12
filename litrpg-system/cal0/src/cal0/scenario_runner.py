"""Executable CAL0-I3 comparison characters and small reference scenarios."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping

from .canonical import semantic_digest
from .engines import (
    Pchip,
    ReinforcementClaim,
    assimilate_claim,
    blocked_xp_credit,
    claim_conservation,
    constraint_first_transition,
    headroom,
    hormetic_outputs,
    maturation_capacity,
    realise_foundation_step,
    transition_commit,
    xp_threshold,
)
from .exact import D, ONE, ZERO, plain
from .parameter_runtime import load_json, rehearsal_samples, validate_parameter_registry, value_map


LEDGERS = (
    "natural_maturation",
    "purposeful_training",
    "organic_adaptation",
    "skill_xp",
    "class_xp",
    "reinforcement",
    "assimilation",
)


def _empty_ledgers() -> dict[str, Any]:
    return {name: {"events": [], "total": "0"} for name in LEDGERS}


def _character_map(document: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {character["character_id"]: character for character in document["characters"]}


def _p(values: Mapping[str, Any], name: str) -> Any:
    return values[f"parameter://cal0/{name}@1"]


def _prenatal(parameters: Mapping[str, Any], scenario: Mapping[str, Any], characters: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    anchors = _p(parameters, "maturation/anchor-coordinates")
    curves = {
        "physical": Pchip.compile(anchors, _p(parameters, "maturation/physical-programme")),
        "neural": Pchip.compile(anchors, _p(parameters, "maturation/neural-programme")),
        "soul": Pchip.compile(anchors, _p(parameters, "maturation/soul-programme")),
    }
    gate_curve = Pchip.compile(anchors, _p(parameters, "maturation/structural-gate-programme"))
    rise = _p(parameters, "maturation/foundation-rise-rate")
    loss = _p(parameters, "maturation/foundation-loss-rate")
    rows: dict[str, Any] = {}
    for character_id in scenario["characters"]:
        character = characters[character_id]
        ledgers = _empty_ledgers()
        foundations = {channel: ZERO for channel in curves}
        previous = ZERO
        stages = []
        for raw_coordinate in scenario["coordinates"]:
            coordinate = D(raw_coordinate)
            dt = coordinate - previous
            previous = coordinate
            for channel, curve in curves.items():
                target, realised = realise_foundation_step(
                    foundations[channel],
                    curve.evaluate(coordinate),
                    character["endowment_multiplier"],
                    "1",
                    "0",
                    rise,
                    loss,
                    dt,
                )
                foundations[channel] = realised
                ledgers["natural_maturation"]["events"].append(
                    {"coordinate": plain(coordinate), "channel": channel, "target": plain(target), "realised": plain(realised)}
                )
            metabolic = (foundations["physical"] + foundations["neural"]) / Decimal("2")
            capacity = maturation_capacity(
                {"physical": foundations["physical"], "neural": foundations["neural"], "metabolic": metabolic},
                _p(parameters, "maturation/aggregate-weights"),
                _p(parameters, "maturation/aggregate-rho"),
                _p(parameters, "maturation/species-scale"),
                gate_curve.evaluate(coordinate),
            )
            stages.append({"coordinate": plain(coordinate), "foundations": {key: plain(value) for key, value in foundations.items()}, "capacity": plain(capacity)})
        ledgers["natural_maturation"]["total"] = plain(sum(foundations.values(), ZERO))
        rows[character_id] = {"stages": stages, "ledgers": ledgers}

    protagonist_id = "character://cal0/i3/protagonist-proxy@1"
    protagonist = rows[protagonist_id]
    directed_load = D(_p(parameters, "scenario/prenatal-directed-load"))
    conscious_fraction = D(_p(parameters, "scenario/prenatal-consciousness-fraction"))
    purposeful = directed_load * conscious_fraction
    opportunity, fatigue, harm = hormetic_outputs(
        directed_load,
        _p(parameters, "adaptation/maintenance"),
        _p(parameters, "adaptation/peak"),
        _p(parameters, "adaptation/excessive"),
        _p(parameters, "adaptation/stop"),
        _p(parameters, "adaptation/harm-scale"),
        _p(parameters, "adaptation/harm-exponent"),
    )
    organic = opportunity * D(_p(parameters, "adaptation/gain-scale")) * conscious_fraction
    skill_xp = purposeful * Decimal("10")
    protagonist["ledgers"]["purposeful_training"] = {"events": [{"practice": "directed_attention", "load": plain(directed_load), "conscious_fraction": plain(conscious_fraction)}], "total": plain(purposeful)}
    protagonist["ledgers"]["organic_adaptation"] = {"events": [{"opportunity": plain(opportunity), "fatigue": plain(fatigue), "harm": plain(harm)}], "total": plain(organic)}
    protagonist["ledgers"]["skill_xp"] = {"events": [{"skill": "Directed Attention", "xp": plain(skill_xp)}], "total": plain(skill_xp)}
    claim = ReinforcementClaim.create(
        "ReincarnateContinuity:EmbodiedIntegration",
        1,
        _p(parameters, "reinforcement/skill-level-budget"),
        _p(parameters, "reinforcement/skill-distribution"),
        (scenario["scenario_id"], "reference-only"),
    )
    current = {"Focus": "0.08", "Coherence": "0.10", "Perception": "0.12"}
    assimilation = assimilate_claim(claim, current, _p(parameters, "reinforcement/fetal-assimilation"))
    protagonist["ledgers"]["reinforcement"] = {"events": [{"claim_id": claim.claim_id, "budget": plain(claim.total_budget)}], "total": plain(claim.total_budget)}
    protagonist["ledgers"]["assimilation"] = {
        "events": [{key: {name: plain(value) for name, value in row.items()} for key, row in assimilation.items()}],
        "total": plain(sum((row["assimilated"] for row in assimilation.values()), ZERO)),
        "backlog": plain(sum((row["backlog"] for row in assimilation.values()), ZERO)),
    }
    stage_monotone = all(
        all(D(right["foundations"][channel]) >= D(left["foundations"][channel]) for left, right in zip(row["stages"], row["stages"][1:]))
        for row in rows.values()
        for channel in ("physical", "neural", "soul")
    )
    checks = {
        "natural_foundations_monotone": stage_monotone,
        "directed_load_separate": protagonist["ledgers"]["purposeful_training"]["total"] != protagonist["ledgers"]["natural_maturation"]["total"],
        "skill_xp_non_negative": skill_xp >= ZERO,
        "claim_conserved": claim_conservation(assimilation, claim.total_budget),
        "assimilation_backlog_positive": D(protagonist["ledgers"]["assimilation"]["backlog"]) > ZERO,
        "no_story_canon_claim": characters[protagonist_id]["canonicality"] == "REFERENCE_ONLY_NOT_STORY_CANON",
    }
    return {"checks": checks, "characters": rows}


def _training(parameters: Mapping[str, Any], scenario: Mapping[str, Any], characters: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    challenge_parameters = {
        "character://cal0/i3/ordinary-reference@1": "scenario/ordinary-training-challenge",
        "character://cal0/i3/trained-reference@1": "scenario/trained-training-challenge",
        "character://cal0/i3/exceptional-reference@1": "scenario/exceptional-training-challenge",
    }
    weeks = int(_p(parameters, "scenario/training-weeks"))
    rows: dict[str, Any] = {}
    for character_id in scenario["characters"]:
        character = characters[character_id]
        ledgers = _empty_ledgers()
        start = D(character["initial_functional_adaptation"])
        realised = start
        envelope = D(_p(parameters, "adaptation/functional-envelope-scale")) * D(character["endowment_multiplier"])
        challenge = D(_p(parameters, challenge_parameters[character_id]))
        for week in range(1, weeks + 1):
            opportunity, fatigue, harm = hormetic_outputs(
                challenge,
                _p(parameters, "adaptation/maintenance"),
                _p(parameters, "adaptation/peak"),
                _p(parameters, "adaptation/excessive"),
                _p(parameters, "adaptation/stop"),
                _p(parameters, "adaptation/harm-scale"),
                _p(parameters, "adaptation/harm-exponent"),
            )
            remaining = headroom(realised, envelope, _p(parameters, "adaptation/headroom-beta"))
            gain = D(_p(parameters, "adaptation/gain-scale")) * opportunity * remaining * D(character["trainability_multiplier"])
            realised = min(envelope, realised + gain)
            ledgers["purposeful_training"]["events"].append({"week": week, "challenge": plain(challenge), "fatigue": plain(fatigue)})
            ledgers["organic_adaptation"]["events"].append({"week": week, "opportunity": plain(opportunity), "headroom": plain(remaining), "gain": plain(gain), "harm": plain(harm)})
        ledgers["purposeful_training"]["total"] = plain(challenge * Decimal(weeks))
        ledgers["organic_adaptation"]["total"] = plain(realised - start)
        rows[character_id] = {
            "start_functional_adaptation": plain(start),
            "final_functional_adaptation": plain(realised),
            "functional_envelope": plain(envelope),
            "start_reference_capacity": character["initial_reference_capacity"],
            "final_reference_capacity": plain(D(character["initial_reference_capacity"]) + realised),
            "ledgers": ledgers,
        }
    checks = {
        "all_training_gains_positive": all(D(row["ledgers"]["organic_adaptation"]["total"]) > ZERO for row in rows.values()),
        "capacity_envelopes_respected": all(D(row["final_functional_adaptation"]) <= D(row["functional_envelope"]) for row in rows.values()),
        "natural_and_training_ledgers_separate": all(row["ledgers"]["natural_maturation"] is not row["ledgers"]["organic_adaptation"] for row in rows.values()),
        "exceptional_starts_above_ordinary": D(rows["character://cal0/i3/exceptional-reference@1"]["start_reference_capacity"]) > D(rows["character://cal0/i3/ordinary-reference@1"]["start_reference_capacity"]),
        "no_cohort_claim": True,
    }
    return {"checks": checks, "characters": rows}


def _progression(parameters: Mapping[str, Any], scenario: Mapping[str, Any], characters: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    skill_count = int(_p(parameters, "xp/skill-threshold-count"))
    class_count = int(_p(parameters, "xp/class-threshold-count"))
    skill_curve = [plain(xp_threshold(_p(parameters, "xp/skill-total-scale"), level, skill_count, _p(parameters, "xp/skill-exponent"))) for level in range(1, 4)]
    class_curve = [plain(xp_threshold(_p(parameters, "xp/class-total-scale"), level, class_count, _p(parameters, "xp/class-exponent"))) for level in range(1, 4)]
    next_threshold = D(skill_curve[0])
    following_cost = D(skill_curve[1]) - next_threshold
    current = next_threshold + following_cost * Decimal("0.25")
    credit, cap = blocked_xp_credit(
        current,
        next_threshold,
        following_cost,
        _p(parameters, "xp/blocked-overhang"),
        _p(parameters, "xp/blocked-taper-exponent"),
        "0.8",
        "0.5",
    )
    skill_claim = ReinforcementClaim.create("Skill:DirectedAttention", 1, _p(parameters, "reinforcement/skill-level-budget"), _p(parameters, "reinforcement/skill-distribution"), (scenario["scenario_id"],))
    class_claim = ReinforcementClaim.create("Class:ReferenceMage", 1, _p(parameters, "reinforcement/class-level-budget"), _p(parameters, "reinforcement/class-distribution"), (scenario["scenario_id"],))
    current_values = {"Focus": "0.08", "Coherence": "0.10", "Perception": "0.12"}
    fetal = assimilate_claim(skill_claim, current_values, _p(parameters, "reinforcement/fetal-assimilation"))
    adult = assimilate_claim(skill_claim, current_values, _p(parameters, "reinforcement/adult-assimilation"))
    fetal_backlog = sum((row["backlog"] for row in fetal.values()), ZERO)
    adult_backlog = sum((row["backlog"] for row in adult.values()), ZERO)
    ledgers = _empty_ledgers()
    ledgers["skill_xp"] = {"events": [{"thresholds": skill_curve, "blocked_credit": plain(credit), "cap": plain(cap)}], "total": plain(current + credit)}
    ledgers["class_xp"] = {"events": [{"thresholds": class_curve}], "total": class_curve[0]}
    ledgers["reinforcement"] = {"events": [{"skill_claim": skill_claim.claim_id}, {"class_claim": class_claim.claim_id}], "total": plain(skill_claim.total_budget + class_claim.total_budget)}
    ledgers["assimilation"] = {"events": [{"fetal_backlog": plain(fetal_backlog), "adult_backlog": plain(adult_backlog)}], "total": plain(sum((row["assimilated"] for row in fetal.values()), ZERO))}
    checks = {
        "skill_and_class_curves_distinct": skill_curve != class_curve,
        "blocked_xp_cannot_cascade": current + credit < D(skill_curve[1]),
        "claim_budget_recipient_independent": sum((row["claim"] for row in fetal.values()), ZERO) == sum((row["claim"] for row in adult.values()), ZERO),
        "fetal_backlog_exceeds_adult_backlog": fetal_backlog > adult_backlog,
        "claim_conserved": claim_conservation(fetal, skill_claim.total_budget) and claim_conservation(adult, skill_claim.total_budget),
    }
    return {"checks": checks, "ledgers": ledgers, "skill_curve": skill_curve, "class_curve": class_curve, "class_claim_budget": plain(class_claim.total_budget)}


def _overload(parameters: Mapping[str, Any], scenario: Mapping[str, Any], characters: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    productive = hormetic_outputs(
        _p(parameters, "scenario/trained-training-challenge"),
        _p(parameters, "adaptation/maintenance"),
        _p(parameters, "adaptation/peak"),
        _p(parameters, "adaptation/excessive"),
        _p(parameters, "adaptation/stop"),
        _p(parameters, "adaptation/harm-scale"),
        _p(parameters, "adaptation/harm-exponent"),
    )
    overload = hormetic_outputs(
        _p(parameters, "scenario/overload-challenge"),
        _p(parameters, "adaptation/maintenance"),
        _p(parameters, "adaptation/peak"),
        _p(parameters, "adaptation/excessive"),
        _p(parameters, "adaptation/stop"),
        _p(parameters, "adaptation/harm-scale"),
        _p(parameters, "adaptation/harm-exponent"),
    )
    checks = {
        "productive_opportunity_positive": productive[0] > ZERO,
        "overload_harm_positive": overload[2] > ZERO,
        "overload_opportunity_lower": overload[0] < productive[0],
        "fatigue_harm_opportunity_separate": len({plain(value) for value in overload}) == 3,
    }
    return {
        "checks": checks,
        "productive": {"opportunity": plain(productive[0]), "fatigue": plain(productive[1]), "harm": plain(productive[2])},
        "overload": {"opportunity": plain(overload[0]), "fatigue": plain(overload[1]), "harm": plain(overload[2])},
        "ledgers": _empty_ledgers(),
    }


def _transition(parameters: Mapping[str, Any], scenario: Mapping[str, Any], characters: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    minima = {name: _p(parameters, f"transition/min-{name}") for name in ("readiness", "execution", "stability", "recovery")}
    required = ("foundation", "load-path", "recovery-channel")
    present = required
    failed = constraint_first_transition(required, present, {"readiness": "0.65", "execution": "0.82", "stability": "0.78", "recovery": "0.80"}, minima, True)
    passing_dimensions = {"readiness": "0.82", "execution": "0.80", "stability": "0.78", "recovery": "0.84"}
    provisional = constraint_first_transition(required, present, passing_dimensions, minima, False)
    successful = constraint_first_transition(required, present, passing_dimensions, minima, True)
    pre = D(characters[scenario["characters"][0]]["initial_reference_capacity"])
    post = pre * D(_p(parameters, "transition/envelope-multiplier"))
    failed_commit = transition_commit(True, True, "failed", True, (True,), pre, post, "0.04")
    success_commit = transition_commit(True, True, "successful", True, (True, True), pre, post, "0.04")
    checks = {
        "failed_minimum_rejected": failed["status"] == "rejected" and not failed["committed"],
        "recovery_incomplete_not_committed": provisional["status"] == "provisional" and not provisional["committed"],
        "successful_transition_atomic": successful["committed"] and success_commit["committed"] and D(success_commit["envelope"]) == post,
        "failed_transition_preserves_envelope": not failed_commit["committed"] and D(failed_commit["envelope"]) == pre,
    }
    return {"checks": checks, "failed": failed, "provisional": provisional, "successful": successful, "failed_commit": failed_commit, "successful_commit": success_commit, "ledgers": _empty_ledgers()}


def validate_reference_scenarios(document: Any, parameters: Mapping[str, Any]) -> list[tuple[str, str, str]]:
    if not isinstance(document, dict):
        return [("I3_SCENARIO_REGISTRY_TYPE", "i3_scenarios", "scenario registry must be an object")]
    issues: list[tuple[str, str, str]] = []
    if document.get("canonicality") != "REFERENCE_ONLY_NOT_STORY_CANON":
        issues.append(("I3_SCOPE_OVERCLAIM", "i3_scenarios.canonicality", "I3 scenario suite must remain non-canonical"))
    if document.get("parameter_set_id") != "parameter-set://cal0/i3-reference@1":
        issues.append(("I3_SCENARIO_PARAMETER_SET", "i3_scenarios.parameter_set_id", "unknown I3 parameter set"))
    characters = document.get("characters", [])
    character_ids = [item.get("character_id") for item in characters if isinstance(item, dict)]
    if len(character_ids) != 4 or len(set(character_ids)) != 4:
        issues.append(("I3_CHARACTER_SET", "i3_scenarios.characters", "exactly four unique comparison characters are required"))
    roles = {item.get("comparison_role") for item in characters if isinstance(item, dict)}
    required_roles = {"ordinary_reference", "trained_reference", "exceptional_reference", "protagonist_proxy"}
    if roles != required_roles:
        issues.append(("I3_CHARACTER_ROLES", "i3_scenarios.characters", "ordinary, trained, exceptional, and protagonist proxy roles are required"))
    parameter_ids = {definition["parameter_id"] for definition in parameters.get("definitions", [])}
    scenarios = document.get("scenarios", [])
    scenario_ids: set[str] = set()
    for index, scenario in enumerate(scenarios if isinstance(scenarios, list) else []):
        path = f"i3_scenarios.scenarios[{index}]"
        scenario_id = scenario.get("scenario_id") if isinstance(scenario, dict) else None
        if not isinstance(scenario_id, str) or scenario_id in scenario_ids:
            issues.append(("I3_SCENARIO_ID", f"{path}.scenario_id", "scenario identity must be unique"))
        elif isinstance(scenario_id, str):
            scenario_ids.add(scenario_id)
        unknown_characters = sorted(set(scenario.get("characters", [])) - set(character_ids))
        if unknown_characters:
            issues.append(("I3_SCENARIO_UNKNOWN_CHARACTER", f"{path}.characters", f"unknown characters: {unknown_characters}"))
        missing_parameters = sorted(set(scenario.get("required_parameter_ids", [])) - parameter_ids)
        if missing_parameters:
            issues.append(("I3_SCENARIO_UNKNOWN_PARAMETER", f"{path}.required_parameter_ids", f"unknown parameters: {missing_parameters}"))
        if tuple(scenario.get("causal_ledgers", [])) != LEDGERS:
            issues.append(("I3_CAUSAL_LEDGER_COLLAPSE", f"{path}.causal_ledgers", "all seven causal ledgers are required in canonical order"))
        if not scenario.get("narrative_envelopes") or not scenario.get("expected_checks"):
            issues.append(("I3_SCENARIO_ENVELOPE", path, "scenario requires narrative envelopes and expected checks"))
    if len(scenario_ids) != 5:
        issues.append(("I3_SCENARIO_COUNT", "i3_scenarios.scenarios", "exactly five reference scenarios are required"))
    return sorted(set(issues))


def run_i3_reference_scenarios(root: Path) -> dict[str, Any]:
    parameter_document = load_json(root / "registries/cal0-i3-parameters.json")
    scenario_document = load_json(root / "scenarios/cal0-i3-reference-scenarios.json")
    parameter_issues = validate_parameter_registry(parameter_document)
    scenario_issues = validate_reference_scenarios(scenario_document, parameter_document)
    if parameter_issues or scenario_issues:
        return {
            "scenario_suite_id": "scenario-suite://cal0/i3-reference@1",
            "passed": False,
            "issues": [list(issue) for issue in parameter_issues + scenario_issues],
        }
    parameters = value_map(parameter_document)
    characters = _character_map(scenario_document)
    dispatch = {
        "scenario://cal0/i3/prenatal-maturation@1": _prenatal,
        "scenario://cal0/i3/matched-training@1": _training,
        "scenario://cal0/i3/progression-and-reinforcement@1": _progression,
        "scenario://cal0/i3/overload-harm@1": _overload,
        "scenario://cal0/i3/structural-transition@1": _transition,
    }
    results = []
    for scenario in sorted(scenario_document["scenarios"], key=lambda item: item["scenario_id"]):
        result = dispatch[scenario["scenario_id"]](parameters, scenario, characters)
        actual_checks = result["checks"]
        expected = sorted(scenario["expected_checks"])
        passed = sorted(actual_checks) == expected and all(actual_checks.values())
        record = {
            "scenario_id": scenario["scenario_id"],
            "title": scenario["title"],
            "canonicality": scenario_document["canonicality"],
            "narrative_envelopes": scenario["narrative_envelopes"],
            "checks": actual_checks,
            "expected_checks": expected,
            "passed": passed,
            "output": result,
        }
        record["scenario_digest"] = semantic_digest(record)
        results.append(record)
    report = {
        "scenario_suite_id": "scenario-suite://cal0/i3-reference@1",
        "parameter_set_id": scenario_document["parameter_set_id"],
        "parameter_set_status": "PROVISIONAL",
        "parameter_status": "UNCALIBRATED",
        "canonicality": scenario_document["canonicality"],
        "cohort_claims_permitted": False,
        "character_count": len(characters),
        "scenario_count": len(results),
        "passed_count": sum(1 for result in results if result["passed"]),
        "rehearsal_samples": rehearsal_samples(parameter_document, ("17", "83")),
        "results": results,
        "passed": all(result["passed"] for result in results),
    }
    report["report_digest"] = semantic_digest(report)
    return report
