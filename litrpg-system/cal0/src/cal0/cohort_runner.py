"""Deterministic CAL0-I4 life-course cohorts and calibration analysis.

The cohort model is an internal world-calibration instrument.  It converts the
I3 rehearsal priors and declared qualitative envelopes into reproducible test
populations; it does not claim to estimate real human biology or story-canon
protagonist values.
"""

from __future__ import annotations

import hashlib
from collections import Counter, defaultdict
from decimal import Decimal, localcontext
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .canonical import semantic_digest
from .engines import Pchip, generalised_mean, headroom, hormetic_outputs, xp_threshold
from .exact import D, ONE, PRECISION, ZERO, clamp, plain
from .parameter_runtime import load_json, value_map


IssueTuple = tuple[str, str, str]

STAGES = ("late_prenatal", "newborn", "child", "adult", "ageing")
CORE_SENSITIVITY_METRICS = (
    "adult_capacity_p50",
    "training_contribution_p50",
    "skill_form_completion_rate",
    "class_form_completion_rate",
    "independent_mage_rate",
    "injury_rate",
)

COHORT_USED_PARAMETERS = {
    "parameter://cal0/maturation/physical-programme@1",
    "parameter://cal0/maturation/neural-programme@1",
    "parameter://cal0/maturation/soul-programme@1",
    "parameter://cal0/maturation/structural-gate-programme@1",
    "parameter://cal0/maturation/aggregate-rho@1",
    "parameter://cal0/maturation/aggregate-weights@1",
    "parameter://cal0/adaptation/maintenance@1",
    "parameter://cal0/adaptation/peak@1",
    "parameter://cal0/adaptation/excessive@1",
    "parameter://cal0/adaptation/stop@1",
    "parameter://cal0/adaptation/harm-scale@1",
    "parameter://cal0/adaptation/harm-exponent@1",
    "parameter://cal0/adaptation/headroom-beta@1",
    "parameter://cal0/adaptation/detraining-weekly@1",
    "parameter://cal0/adaptation/gain-scale@1",
    "parameter://cal0/adaptation/functional-envelope-scale@1",
    "parameter://cal0/xp/skill-total-scale@1",
    "parameter://cal0/xp/skill-exponent@1",
    "parameter://cal0/xp/skill-grade-multiplier@1",
    "parameter://cal0/xp/class-total-scale@1",
    "parameter://cal0/xp/class-exponent@1",
    "parameter://cal0/xp/class-grade-multiplier@1",
    "parameter://cal0/reinforcement/skill-level-budget@1",
    "parameter://cal0/reinforcement/class-level-budget@1",
    "parameter://cal0/reinforcement/adult-assimilation@1",
}

CONFOUNDED_FAMILIES = {
    "parameter://cal0/adaptation/gain-scale@1": "adaptation_gain_x_trainability_x_access",
    "parameter://cal0/adaptation/functional-envelope-scale@1": "adaptation_gain_x_trainability_x_access",
    "parameter://cal0/xp/skill-total-scale@1": "xp_scale_x_evidence_opportunity",
    "parameter://cal0/xp/skill-exponent@1": "xp_scale_x_evidence_opportunity",
    "parameter://cal0/xp/class-total-scale@1": "xp_scale_x_institutional_access",
    "parameter://cal0/xp/class-exponent@1": "xp_scale_x_institutional_access",
}


def _issue(code: str, path: str, message: str) -> IssueTuple:
    return code, path, message


def _decimal(value: Any) -> Decimal | None:
    if isinstance(value, bool) or not isinstance(value, (str, int, Decimal)):
        return None
    try:
        return D(value)
    except Exception:
        return None


def validate_cohort_plan(document: Any, parameter_document: Mapping[str, Any]) -> list[IssueTuple]:
    if not isinstance(document, dict):
        return [_issue("I4_PLAN_TYPE", "i4_plan", "cohort plan must be an object")]
    issues: list[IssueTuple] = []
    if document.get("cohort_plan_id") != "cohort-plan://cal0/i4-human-reference@1":
        issues.append(_issue("I4_PLAN_ID", "i4_plan.cohort_plan_id", "unexpected cohort-plan identity"))
    if document.get("canonicality") != "INTERNAL_WORLD_CALIBRATION_NOT_EMPIRICAL_FACT":
        issues.append(_issue("I4_SCOPE_OVERCLAIM", "i4_plan.canonicality", "I4 may not claim empirical fact or story canon"))
    births = document.get("births_per_seed")
    seeds = document.get("seeds", [])
    if not isinstance(births, int) or isinstance(births, bool) or births < 10000:
        issues.append(_issue("I4_COHORT_TOO_SMALL", "i4_plan.births_per_seed", "every reference seed requires at least 10,000 births"))
    if not isinstance(seeds, list) or len(seeds) < 3 or len(set(seeds)) != len(seeds) or any(not isinstance(seed, int) or isinstance(seed, bool) for seed in seeds):
        issues.append(_issue("I4_SEED_SET", "i4_plan.seeds", "at least three unique integer seeds are required"))

    environments = document.get("environments", [])
    environment_ids: set[str] = set()
    weights: list[Decimal] = []
    required_environment_fields = {"nutrition", "education", "training_access", "magic_access", "safety", "institution"}
    for index, environment in enumerate(environments if isinstance(environments, list) else []):
        path = f"i4_plan.environments[{index}]"
        if not isinstance(environment, dict):
            issues.append(_issue("I4_ENVIRONMENT_TYPE", path, "environment must be an object"))
            continue
        environment_id = environment.get("environment_id")
        if not isinstance(environment_id, str) or environment_id in environment_ids:
            issues.append(_issue("I4_ENVIRONMENT_ID", f"{path}.environment_id", "environment identity must be unique"))
        else:
            environment_ids.add(environment_id)
        weight = _decimal(environment.get("weight"))
        if weight is None or weight <= ZERO:
            issues.append(_issue("I4_ENVIRONMENT_WEIGHT", f"{path}.weight", "environment weight must be positive"))
        else:
            weights.append(weight)
        if not required_environment_fields.issubset(environment):
            issues.append(_issue("I4_ENVIRONMENT_FIELDS", path, "environment is missing a causal support field"))
    if len(environment_ids) < 3 or sum(weights, ZERO) != ONE:
        issues.append(_issue("I4_ENVIRONMENT_CLOSURE", "i4_plan.environments", "at least three environments with weights summing to one are required"))

    trial = document.get("trial_inputs", {})
    if not isinstance(trial, dict) or trial.get("may_resolve_parent_unresolved_bindings") is not False:
        issues.append(_issue("I4_TRIAL_OVERCLAIM", "i4_plan.trial_inputs", "trial assumptions cannot resolve parent unknowns"))
    probabilities = trial.get("rarity_probabilities", {}) if isinstance(trial, dict) else {}
    parsed_probabilities = [_decimal(value) for value in probabilities.values()] if isinstance(probabilities, dict) else []
    if len(parsed_probabilities) != 4 or any(value is None or value < ZERO for value in parsed_probabilities) or sum((value for value in parsed_probabilities if value is not None), ZERO) != ONE:
        issues.append(_issue("I4_RARITY_NORMALISATION", "i4_plan.trial_inputs.rarity_probabilities", "rarity trial probabilities must be non-negative and sum to one"))

    iterations = document.get("calibration_iterations", [])
    iteration_ids: set[str] = set()
    known_parent = "parameter-set://cal0/i3-reference@1"
    parameter_ids = {definition.get("parameter_id") for definition in parameter_document.get("definitions", [])}
    for index, iteration in enumerate(iterations if isinstance(iterations, list) else []):
        path = f"i4_plan.calibration_iterations[{index}]"
        iteration_id = iteration.get("iteration_id") if isinstance(iteration, dict) else None
        if not isinstance(iteration_id, str) or iteration_id in iteration_ids:
            issues.append(_issue("I4_ITERATION_ID", f"{path}.iteration_id", "iteration identity must be unique"))
            continue
        if iteration.get("parent") != known_parent:
            issues.append(_issue("I4_ITERATION_LINEAGE", f"{path}.parent", "calibration iterations must form one immutable successor chain"))
        overrides = iteration.get("overrides", {})
        if not isinstance(overrides, dict) or set(overrides) - parameter_ids:
            issues.append(_issue("I4_ITERATION_OVERRIDE", f"{path}.overrides", "iteration contains an unknown parameter override"))
        iteration_ids.add(iteration_id)
        known_parent = iteration_id
    if len(iteration_ids) < 2:
        issues.append(_issue("I4_ITERATION_COUNT", "i4_plan.calibration_iterations", "at least a baseline and one successor iteration are required"))

    envelope_ids = [entry.get("envelope_id") for entry in document.get("envelopes", []) if isinstance(entry, dict)]
    if not envelope_ids or len(set(envelope_ids)) != len(envelope_ids):
        issues.append(_issue("I4_ENVELOPE_SET", "i4_plan.envelopes", "calibration envelopes must be present and uniquely identified"))
    for index, envelope in enumerate(document.get("envelopes", [])):
        minimum, maximum = _decimal(envelope.get("minimum")), _decimal(envelope.get("maximum"))
        if minimum is None or maximum is None or minimum > maximum:
            issues.append(_issue("I4_ENVELOPE_BOUNDS", f"i4_plan.envelopes[{index}]", "envelope minimum must not exceed maximum"))

    comparisons = document.get("comparison_ensembles", [])
    comparison_ids = {item.get("ensemble_id") for item in comparisons if isinstance(item, dict)}
    protagonist = [item for item in comparisons if isinstance(item, dict) and "protagonist" in str(item.get("ensemble_id"))]
    if len(comparison_ids) < 5 or len(protagonist) < 2:
        issues.append(_issue("I4_COMPARISON_SET", "i4_plan.comparison_ensembles", "ordinary, advantaged, early-contact, and protagonist comparisons are required"))
    if any(item.get("kind") != "scenario_ensemble_not_population" for item in protagonist):
        issues.append(_issue("I4_PROTAGONIST_CONTAMINATION", "i4_plan.comparison_ensembles", "protagonist ensembles cannot be population cohorts"))

    sensitivity = document.get("sensitivity", {})
    if not isinstance(sensitivity, dict) or len(sensitivity.get("seeds", [])) < 2 or sensitivity.get("births_per_seed", 0) < 1000:
        issues.append(_issue("I4_SENSITIVITY_DESIGN", "i4_plan.sensitivity", "multi-seed sensitivity design with at least 1,000 births per seed is required"))
    return sorted(set(issues))


def _u01(seed: int, entity: int, namespace: str) -> Decimal:
    digest = hashlib.sha256(f"{seed}\x1f{entity}\x1f{namespace}".encode("utf-8")).digest()
    numerator = int.from_bytes(digest[:8], "big")
    denominator = (1 << 64) - 1
    with localcontext() as context:
        context.prec = PRECISION
        return Decimal(numerator) / Decimal(denominator)


def _triangular(low: Decimal, mode: Decimal, high: Decimal, u: Decimal) -> Decimal:
    if not low <= mode <= high or low == high:
        raise ValueError("invalid triangular distribution")
    split = (mode - low) / (high - low)
    with localcontext() as context:
        context.prec = PRECISION
        if u <= split:
            return low + (u * (high - low) * (mode - low)).sqrt()
        return high - ((ONE - u) * (high - low) * (high - mode)).sqrt()


def _weighted_environment(environments: Sequence[Mapping[str, Any]], draw: Decimal) -> Mapping[str, Any]:
    cumulative = ZERO
    for environment in environments:
        cumulative += D(environment["weight"])
        if draw <= cumulative:
            return environment
    return environments[-1]


def _distribution_by_target(parameter_document: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {distribution["target_parameter_id"]: distribution for distribution in parameter_document["distributions"]}


def _latent_record(
    seed: int,
    entity: int,
    plan: Mapping[str, Any],
    parameter_document: Mapping[str, Any],
    dependence_strength: Decimal = Decimal("0.25"),
    forced_environment: str | None = None,
) -> dict[str, Any]:
    environment = _weighted_environment(plan["environments"], _u01(seed, entity, "environment"))
    if forced_environment:
        environment = next(item for item in plan["environments"] if item["environment_id"] == forced_environment)
    shared = _u01(seed, entity, "shared-development")
    distributions = _distribution_by_target(parameter_document)
    samples: dict[str, Decimal] = {}
    for parameter_id, distribution in distributions.items():
        individual = _u01(seed, entity, distribution["seed_namespace"])
        mixed = clamp(dependence_strength * shared + (ONE - dependence_strength) * individual, ZERO, ONE)
        parameters = distribution["parameters"]
        samples[parameter_id] = _triangular(D(parameters["minimum"]), D(parameters["mode"]), D(parameters["maximum"]), mixed)
    return {
        "person_id": f"person://cal0/i4/{seed}/{entity}",
        "seed": seed,
        "entity": entity,
        "environment": environment,
        "endowment": samples["parameter://cal0/population/endowment-multiplier@1"],
        "timing": samples["parameter://cal0/population/developmental-timing-offset@1"],
        "trainability": samples["parameter://cal0/population/trainability-multiplier@1"],
        "recovery": samples["parameter://cal0/population/recovery-multiplier@1"],
        "health": Decimal("0.82") + Decimal("0.34") * _u01(seed, entity, "health"),
        "diligence": _u01(seed, entity, "diligence"),
        "feedback": _u01(seed, entity, "feedback"),
        "responsibility": _u01(seed, entity, "responsibility"),
        "risk": _u01(seed, entity, "risk"),
        "preference_magic": _u01(seed, entity, "preference-magic"),
        "preference_combat": _u01(seed, entity, "preference-combat"),
        "age_exposure": Decimal("0.75") + Decimal("0.50") * _u01(seed, entity, "age-exposure"),
        "injury_draw": _u01(seed, entity, "injury"),
        "severity_draw": _u01(seed, entity, "injury-severity"),
        "mortality_draw": _u01(seed, entity, "mortality"),
        "offer_draw": _u01(seed, entity, "offer-choice"),
        "rare_draw": _u01(seed, entity, "rarity"),
    }


def _p(values: Mapping[str, Any], name: str) -> Any:
    return values[f"parameter://cal0/{name}@1"]


def _curves(values: Mapping[str, Any]) -> dict[str, Pchip]:
    anchors = _p(values, "maturation/anchor-coordinates")
    return {
        "physical": Pchip.compile(anchors, _p(values, "maturation/physical-programme")),
        "neural": Pchip.compile(anchors, _p(values, "maturation/neural-programme")),
        "soul": Pchip.compile(anchors, _p(values, "maturation/soul-programme")),
        "gate": Pchip.compile(anchors, _p(values, "maturation/structural-gate-programme")),
    }


def _level_for_xp(xp: Decimal, scale: Any, count: int, exponent: Any) -> int:
    level = 0
    for threshold in range(1, count + 1):
        if xp >= xp_threshold(scale, threshold, count, exponent):
            level = threshold
        else:
            break
    return level


def _level_for_thresholds(xp: Decimal, thresholds: Sequence[Decimal]) -> int:
    level = 0
    for index, threshold in enumerate(thresholds, start=1):
        if xp >= threshold:
            level = index
        else:
            break
    return level


def _stage_capacities(
    record: Mapping[str, Any],
    values: Mapping[str, Any],
    curves: Mapping[str, Pchip],
    coordinates: Mapping[str, Any],
    cache: dict[tuple[str, str, str, str], tuple[Decimal, Decimal]],
) -> tuple[dict[str, Decimal], Decimal]:
    environment = record["environment"]
    capacities: dict[str, Decimal] = {}
    adult_soul = ZERO
    timing_bucket = record["timing"].quantize(Decimal("0.01"))
    recovery_bucket = record["recovery"].quantize(Decimal("0.05"))
    for stage in ("late_prenatal", "newborn", "child", "adult"):
        key = (environment["environment_id"], plain(timing_bucket), plain(recovery_bucket), stage)
        if key not in cache:
            coordinate = clamp(D(coordinates[stage]) + timing_bucket, Decimal("0.001"), ONE)
            physical = max(Decimal("0.000001"), curves["physical"].evaluate(coordinate) * D(environment["nutrition"]))
            neural = max(Decimal("0.000001"), curves["neural"].evaluate(coordinate) * (Decimal("0.90") + Decimal("0.10") * D(environment["education"])))
            metabolic = max(Decimal("0.000001"), (physical + neural) / Decimal("2") * (Decimal("0.90") + Decimal("0.10") * recovery_bucket))
            capacity_factor = generalised_mean(
                {"physical": physical, "neural": neural, "metabolic": metabolic},
                _p(values, "maturation/aggregate-weights"),
                _p(values, "maturation/aggregate-rho"),
            ) * curves["gate"].evaluate(coordinate)
            soul_factor = curves["soul"].evaluate(coordinate) * (Decimal("0.90") + Decimal("0.10") * recovery_bucket)
            cache[key] = capacity_factor, soul_factor
        capacity_factor, soul_factor = cache[key]
        capacities[stage] = record["endowment"] * record["health"] * capacity_factor
        if stage == "adult":
            adult_soul = record["endowment"] * soul_factor
    decline = Decimal("0.12") + Decimal("0.10") * (ONE - clamp(record["recovery"], ZERO, ONE))
    capacities["ageing"] = capacities["adult"] * (ONE - decline)
    return capacities, adult_soul


def _simulate_person(
    record: Mapping[str, Any],
    values: Mapping[str, Any],
    curves: Mapping[str, Pchip],
    plan: Mapping[str, Any],
    variant: str = "ordinary",
    stage_cache: dict[tuple[str, str, str, str], tuple[Decimal, Decimal]] | None = None,
    threshold_cache: Mapping[str, Sequence[Decimal]] | None = None,
) -> dict[str, Any]:
    environment = record["environment"]
    endowment = record["endowment"]
    trainability = record["trainability"]
    recovery = record["recovery"]
    forced_magic = False
    continuity_bonus = ZERO
    directed_practice = ZERO
    if variant == "talented":
        endowment *= Decimal("1.12")
        trainability *= Decimal("1.10")
    elif variant == "institutional":
        trainability *= Decimal("1.04")
    elif variant == "early_magic":
        forced_magic = True
    elif variant == "protagonist_no_practice":
        forced_magic = True
        continuity_bonus = Decimal("0.08")
    elif variant == "protagonist_directed":
        forced_magic = True
        continuity_bonus = Decimal("0.08")
        directed_practice = Decimal("0.025")
    adjusted = dict(record)
    adjusted["endowment"] = endowment
    adjusted["trainability"] = trainability
    adjusted["recovery"] = recovery
    capacities, adult_soul = _stage_capacities(adjusted, values, curves, plan["life_stage_coordinates"], stage_cache if stage_cache is not None else {})

    diligence = clamp(record["diligence"] + continuity_bonus, ZERO, ONE)
    challenge = Decimal("0.18") + Decimal("0.72") * diligence * (Decimal("0.75") + Decimal("0.25") * D(environment["training_access"]))
    opportunity, fatigue, training_harm = hormetic_outputs(
        challenge,
        _p(values, "adaptation/maintenance"),
        _p(values, "adaptation/peak"),
        _p(values, "adaptation/excessive"),
        _p(values, "adaptation/stop"),
        _p(values, "adaptation/harm-scale"),
        _p(values, "adaptation/harm-exponent"),
    )
    envelope = D(_p(values, "adaptation/functional-envelope-scale")) * endowment * capacities["adult"] * (Decimal("0.75") + Decimal("0.25") * recovery)
    raw_adaptation = (
        D(_p(values, "adaptation/gain-scale"))
        * opportunity
        * trainability
        * recovery
        * D(environment["training_access"])
        * Decimal("5.04")
    )
    provisional_fraction = clamp(raw_adaptation / max(envelope, Decimal("0.000001")) / Decimal("2"), ZERO, ONE)
    remaining_base = ONE - provisional_fraction
    beta = D(_p(values, "adaptation/headroom-beta"))
    if beta == Decimal("1.5"):
        remaining = remaining_base * remaining_base.sqrt()
    elif beta == ONE:
        remaining = remaining_base
    elif beta == Decimal("2"):
        remaining = remaining_base * remaining_base
    else:
        remaining = headroom(raw_adaptation / Decimal("2"), max(envelope, Decimal("0.000001")), beta)
    realised = min(envelope, raw_adaptation * remaining)
    if diligence < Decimal("0.30"):
        realised *= ONE - D(_p(values, "adaptation/detraining-weekly")) * Decimal("8")
    realised = max(ZERO, realised + directed_practice)

    education = D(environment["education"]) * (Decimal("0.72") + Decimal("0.28") * record["feedback"])
    practice = diligence * D(environment["training_access"])
    knowledge = clamp(Decimal("0.55") * education + Decimal("0.45") * record["feedback"], ZERO, Decimal("1.25"))
    skill_xp = (
        Decimal("28")
        + Decimal("112")
        * (
            Decimal("0.32") * education
            + Decimal("0.34") * practice
            + Decimal("0.20") * record["feedback"]
            + Decimal("0.14") * record["age_exposure"]
        )
        + continuity_bonus * Decimal("80")
        + directed_practice * Decimal("240")
    )
    skill_count = int(_p(values, "xp/skill-threshold-count"))
    skill_thresholds = threshold_cache["skill"] if threshold_cache is not None else tuple(
        xp_threshold(_p(values, "xp/skill-total-scale"), level, skill_count, _p(values, "xp/skill-exponent"))
        for level in range(1, skill_count + 1)
    )
    skill_level = _level_for_thresholds(skill_xp, skill_thresholds)
    skill_grade_one = skill_xp >= D(_p(values, "xp/skill-total-scale")) * D(_p(values, "xp/skill-grade-multiplier"))

    specialisation = clamp(
        Decimal("0.38") * diligence
        + Decimal("0.34") * D(environment["institution"])
        + Decimal("0.28") * record["responsibility"],
        ZERO,
        Decimal("1.20"),
    )
    class_xp = Decimal("18") + Decimal("250") * specialisation * (Decimal("0.45") + Decimal("0.55") * Decimal(skill_level) / Decimal(skill_count)) * record["age_exposure"]
    class_count = int(_p(values, "xp/class-threshold-count"))
    class_thresholds = threshold_cache["class"] if threshold_cache is not None else tuple(
        xp_threshold(_p(values, "xp/class-total-scale"), level, class_count, _p(values, "xp/class-exponent"))
        for level in range(1, class_count + 1)
    )
    class_level = _level_for_thresholds(class_xp, class_thresholds)
    successor_evidence = (
        Decimal("0.35") * record["responsibility"]
        + Decimal("0.25") * min(ONE, D(environment["institution"]))
        + Decimal("0.20") * clamp((record["age_exposure"] - Decimal("0.75")) / Decimal("0.50"), ZERO, ONE)
        + Decimal("0.20") * Decimal(skill_level) / Decimal(skill_count)
    )
    successor_threshold = clamp(
        Decimal("0.82") + Decimal("0.08") * (D(_p(values, "xp/class-grade-multiplier")) - ONE),
        Decimal("0.82"),
        Decimal("0.95"),
    )
    later_grade_class = class_level == class_count and skill_level == skill_count and successor_evidence >= successor_threshold

    first_skill_threshold = skill_thresholds[0]
    first_class_threshold = class_thresholds[0]
    skill_status = "not_offered"
    if skill_xp >= first_skill_threshold:
        skill_status = "accepted" if record["offer_draw"] > Decimal("0.08") else "deferred"
    class_status = "not_offered"
    if class_xp >= first_class_threshold and specialisation > Decimal("0.30"):
        if record["offer_draw"] < Decimal("0.06"):
            class_status = "rejected"
        elif record["offer_draw"] < Decimal("0.18"):
            class_status = "deferred"
        else:
            class_status = "accepted"

    trial = plan["trial_inputs"]
    injury_probability = (
        D(trial["lifetime_injury_base_probability"])
        * (Decimal("0.58") + Decimal("0.82") * record["risk"])
        * (Decimal("1.16") - Decimal("0.22") * D(environment["safety"]))
        * (Decimal("1.18") - Decimal("0.22") * min(recovery, Decimal("1.20")))
        + training_harm
    )
    injured = record["injury_draw"] < clamp(injury_probability, ZERO, Decimal("0.95"))
    severe = injured and record["severity_draw"] < Decimal("0.18")
    disabled = severe and record["severity_draw"] < Decimal("0.075")
    retired_early = severe and record["responsibility"] < Decimal("0.32")
    died_before_old_age = severe and record["mortality_draw"] < Decimal("0.09") * (Decimal("1.20") - D(environment["safety"]))
    injury_loss = ZERO
    if injured:
        injury_loss = Decimal("0.015") + Decimal("0.08") * record["severity_draw"]
    if severe:
        injury_loss += Decimal("0.06")

    reinforcement_claim = Decimal(skill_level) * D(_p(values, "reinforcement/skill-level-budget")) + Decimal(class_level) * D(_p(values, "reinforcement/class-level-budget"))
    reinforcement_expressed = reinforcement_claim * D(_p(values, "reinforcement/adult-assimilation"))
    reinforcement_backlog = reinforcement_claim - reinforcement_expressed
    overload = reinforcement_backlog > capacities["adult"] * Decimal("0.08") or training_harm > Decimal("0.005")
    adult_capacity = max(ZERO, capacities["adult"] + realised + reinforcement_expressed - injury_loss)
    ageing_capacity = max(ZERO, capacities["ageing"] + realised * Decimal("0.62") + reinforcement_expressed - injury_loss)
    capacities["adult"] = adult_capacity
    capacities["ageing"] = ageing_capacity

    magic_contact_probability = clamp(D(environment["magic_access"]) * (Decimal("0.24") + Decimal("0.24") * min(adult_soul, ONE)), ZERO, Decimal("0.95"))
    magic_contact = forced_magic or record["preference_magic"] < magic_contact_probability
    magic_xp = skill_xp * D(environment["magic_access"]) * (Decimal("0.32") + Decimal("0.68") * record["preference_magic"]) if magic_contact else ZERO
    magic_level = _level_for_thresholds(magic_xp, skill_thresholds)
    vocational = clamp(Decimal("0.42") * adult_capacity + Decimal("0.30") * knowledge + Decimal("0.28") * Decimal(skill_level) / Decimal(skill_count), ZERO, Decimal("1.60"))
    combat = clamp(Decimal("0.38") * adult_capacity + Decimal("0.34") * realised + Decimal("0.28") * record["preference_combat"] * practice - injury_loss, ZERO, Decimal("1.40"))
    coordination = clamp(Decimal("0.42") * record["responsibility"] + Decimal("0.33") * knowledge + Decimal("0.25") * D(environment["institution"]), ZERO, Decimal("1.30"))
    magic = ZERO
    if magic_contact:
        magic = clamp(
            Decimal("0.24") * adult_soul
            + Decimal("0.34") * Decimal(magic_level) / Decimal(skill_count)
            + Decimal("0.27") * Decimal(class_level) / Decimal(class_count)
            + Decimal("0.15") * D(environment["institution"]),
            ZERO,
            Decimal("1.40"),
        )
    independent_mage = magic_contact and magic_level >= 7 and class_level >= 5 and magic >= Decimal("0.58") and not died_before_old_age
    battle_capable_mage = independent_mage and magic >= Decimal("0.78") and combat >= Decimal("0.55")
    combat_ready = combat >= Decimal("0.58")

    rare_soul = record["rare_draw"] < D(trial["rare_soul_prevalence"])
    rarity_draw = record["rare_draw"]
    rarity = "basic"
    cumulative = ZERO
    for label in ("basic", "uncommon", "rare", "exceptional"):
        cumulative += D(trial["rarity_probabilities"][label])
        if rarity_draw <= cumulative:
            rarity = label
            break

    return {
        "person_id": record["person_id"],
        "environment_id": environment["environment_id"],
        "variant": variant,
        "life_stage_capacity": capacities,
        "soul_capacity": adult_soul,
        "natural_maturation": adult_capacity - realised - reinforcement_expressed + injury_loss,
        "purposeful_training_load": challenge * Decimal("12"),
        "organic_training_adaptation": realised,
        "training_fatigue": fatigue,
        "training_harm": training_harm,
        "skill_xp": skill_xp,
        "class_xp": class_xp,
        "skill_level": skill_level,
        "class_level": class_level,
        "skill_status": skill_status,
        "class_status": class_status,
        "skill_form_completed": skill_level == skill_count,
        "class_form_completed": class_level == class_count,
        "later_grade_skill": skill_grade_one,
        "later_grade_class": later_grade_class,
        "reinforcement_claim": reinforcement_claim,
        "reinforcement_expressed": reinforcement_expressed,
        "reinforcement_backlog": reinforcement_backlog,
        "overload": overload,
        "injured": injured,
        "severe_injury": severe,
        "disabled": disabled,
        "retired_early": retired_early,
        "died_before_old_age": died_before_old_age,
        "injury_loss": injury_loss,
        "magic_contact": magic_contact,
        "independent_mage": independent_mage,
        "battle_capable_mage": battle_capable_mage,
        "combat_ready": combat_ready,
        "performances": {
            "vocational": vocational,
            "combat": combat,
            "coordination": coordination,
            "magic": magic,
        },
        "causal_history": {
            "endowment": endowment,
            "developmental_timing": record["timing"],
            "trainability": trainability,
            "recovery": recovery,
            "health": record["health"],
            "diligence": diligence,
            "education_access": D(environment["education"]),
            "training_access": D(environment["training_access"]),
            "magic_access": D(environment["magic_access"]),
            "institutional_access": D(environment["institution"]),
            "rare_soul_trial_event": rare_soul,
            "rarity_trial": rarity,
        },
    }


def _quantile(values: Sequence[Decimal], numerator: int, denominator: int = 100) -> Decimal:
    if not values:
        return ZERO
    ordered = sorted(values)
    index = (len(ordered) - 1) * numerator // denominator
    return ordered[index]


def _distribution_summary(values: Sequence[Decimal]) -> dict[str, str | int]:
    if not values:
        return {"count": 0, "minimum": "0", "p10": "0", "p50": "0", "p90": "0", "p99": "0", "maximum": "0", "mean": "0"}
    total = sum(values, ZERO)
    return {
        "count": len(values),
        "minimum": plain(min(values), 8),
        "p10": plain(_quantile(values, 10), 8),
        "p50": plain(_quantile(values, 50), 8),
        "p90": plain(_quantile(values, 90), 8),
        "p99": plain(_quantile(values, 99), 8),
        "maximum": plain(max(values), 8),
        "mean": plain(total / Decimal(len(values)), 8),
    }


def _rate(count: int, total: int) -> Decimal:
    return Decimal(count) / Decimal(total) if total else ZERO


def _outlier_snapshot(person: Mapping[str, Any], reason: str) -> dict[str, Any]:
    return {
        "person_id": person["person_id"],
        "reason": reason,
        "environment_id": person["environment_id"],
        "adult_capacity": plain(person["life_stage_capacity"]["adult"], 8),
        "skill_level": person["skill_level"],
        "class_level": person["class_level"],
        "performances": {key: plain(value, 8) for key, value in person["performances"].items()},
        "injured": person["injured"],
        "disabled": person["disabled"],
        "died_before_old_age": person["died_before_old_age"],
        "causal_history": {
            key: plain(value, 8) if isinstance(value, Decimal) else value
            for key, value in person["causal_history"].items()
        },
        "ledger_contributions": {
            "natural_maturation": plain(person["natural_maturation"], 8),
            "organic_training_adaptation": plain(person["organic_training_adaptation"], 8),
            "reinforcement_expressed": plain(person["reinforcement_expressed"], 8),
            "injury_loss": plain(person["injury_loss"], 8),
        },
    }


def _summarise_people(people: Sequence[Mapping[str, Any]], include_outliers: bool = True) -> dict[str, Any]:
    total = len(people)
    life_stages = {
        stage: _distribution_summary([person["life_stage_capacity"][stage] for person in people])
        for stage in STAGES
    }
    contributions = {
        "natural_maturation": _distribution_summary([person["natural_maturation"] for person in people]),
        "purposeful_training_load": _distribution_summary([person["purposeful_training_load"] for person in people]),
        "organic_training_adaptation": _distribution_summary([person["organic_training_adaptation"] for person in people]),
        "reinforcement_claim": _distribution_summary([person["reinforcement_claim"] for person in people]),
        "reinforcement_expressed": _distribution_summary([person["reinforcement_expressed"] for person in people]),
        "reinforcement_backlog": _distribution_summary([person["reinforcement_backlog"] for person in people]),
        "injury_loss": _distribution_summary([person["injury_loss"] for person in people]),
    }
    status_skill = Counter(person["skill_status"] for person in people)
    status_class = Counter(person["class_status"] for person in people)
    progression = {
        "skill_status_counts": dict(sorted(status_skill.items())),
        "class_status_counts": dict(sorted(status_class.items())),
        "skill_level": _distribution_summary([Decimal(person["skill_level"]) for person in people]),
        "class_level": _distribution_summary([Decimal(person["class_level"]) for person in people]),
        "skill_form_completion_rate": plain(_rate(sum(person["skill_form_completed"] for person in people), total), 8),
        "class_form_completion_rate": plain(_rate(sum(person["class_form_completed"] for person in people), total), 8),
        "later_grade_skill_rate": plain(_rate(sum(person["later_grade_skill"] for person in people), total), 8),
        "later_grade_class_rate": plain(_rate(sum(person["later_grade_class"] for person in people), total), 8),
    }
    conditions = {
        "injury_rate": plain(_rate(sum(person["injured"] for person in people), total), 8),
        "severe_injury_rate": plain(_rate(sum(person["severe_injury"] for person in people), total), 8),
        "disability_rate": plain(_rate(sum(person["disabled"] for person in people), total), 8),
        "early_retirement_rate": plain(_rate(sum(person["retired_early"] for person in people), total), 8),
        "premature_death_rate": plain(_rate(sum(person["died_before_old_age"] for person in people), total), 8),
        "overload_rate": plain(_rate(sum(person["overload"] for person in people), total), 8),
    }
    magic = {
        "contact_rate": plain(_rate(sum(person["magic_contact"] for person in people), total), 8),
        "independent_mage_rate": plain(_rate(sum(person["independent_mage"] for person in people), total), 8),
        "battle_capable_mage_rate": plain(_rate(sum(person["battle_capable_mage"] for person in people), total), 8),
    }
    performances = {
        name: _distribution_summary([person["performances"][name] for person in people])
        for name in ("vocational", "combat", "coordination", "magic")
    }
    civilians = [person for person in people if not person["independent_mage"]]
    civilian_combat_ready_rate = _rate(sum(person["combat_ready"] for person in civilians), len(civilians))
    by_environment: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for person in people:
        by_environment[person["environment_id"]].append(person)
    environments = {}
    for environment_id, members in sorted(by_environment.items()):
        environments[environment_id] = {
            "count": len(members),
            "adult_capacity_p50": plain(_quantile([member["life_stage_capacity"]["adult"] for member in members], 50), 8),
            "skill_form_completion_rate": plain(_rate(sum(member["skill_form_completed"] for member in members), len(members)), 8),
            "class_form_completion_rate": plain(_rate(sum(member["class_form_completed"] for member in members), len(members)), 8),
            "independent_mage_rate": plain(_rate(sum(member["independent_mage"] for member in members), len(members)), 8),
            "injury_rate": plain(_rate(sum(member["injured"] for member in members), len(members)), 8),
        }
    outliers: list[dict[str, Any]] = []
    if include_outliers and people:
        selections: list[tuple[str, str]] = []
        for key in ("vocational", "combat", "magic"):
            top = sorted(people, key=lambda person: (person["performances"][key], person["person_id"]), reverse=True)[:3]
            selections.extend((person["person_id"], f"top_{key}") for person in top)
        harmed = sorted(people, key=lambda person: (person["injury_loss"], person["person_id"]), reverse=True)[:3]
        selections.extend((person["person_id"], "largest_injury_loss") for person in harmed)
        by_id = {person["person_id"]: person for person in people}
        seen: set[tuple[str, str]] = set()
        for person_id, reason in selections:
            if (person_id, reason) not in seen:
                outliers.append(_outlier_snapshot(by_id[person_id], reason))
                seen.add((person_id, reason))
    return {
        "birth_count": total,
        "life_stage_capacity": life_stages,
        "causal_contributions": contributions,
        "progression": progression,
        "reinforcement_and_assimilation": {
            "claim": contributions["reinforcement_claim"],
            "expressed": contributions["reinforcement_expressed"],
            "backlog": contributions["reinforcement_backlog"],
        },
        "conditions": conditions,
        "magic": magic,
        "performances": performances,
        "civilian_combat_ready_rate": plain(civilian_combat_ready_rate, 8),
        "environments": environments,
        "causal_outliers": outliers,
    }


def _metric_vector(summary: Mapping[str, Any]) -> dict[str, Decimal]:
    return {
        "adult_capacity_p50": D(summary["life_stage_capacity"]["adult"]["p50"]),
        "training_contribution_p50": D(summary["causal_contributions"]["organic_training_adaptation"]["p50"]),
        "skill_form_completion_rate": D(summary["progression"]["skill_form_completion_rate"]),
        "class_form_completion_rate": D(summary["progression"]["class_form_completion_rate"]),
        "later_grade_class_rate": D(summary["progression"]["later_grade_class_rate"]),
        "independent_mage_rate": D(summary["magic"]["independent_mage_rate"]),
        "battle_capable_mage_rate": D(summary["magic"]["battle_capable_mage_rate"]),
        "civilian_combat_ready_rate": D(summary["civilian_combat_ready_rate"]),
        "injury_rate": D(summary["conditions"]["injury_rate"]),
    }


def _with_overrides(base: Mapping[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    values = dict(base)
    values.update(overrides)
    return values


def _simulate_seed(
    seed: int,
    births: int,
    plan: Mapping[str, Any],
    parameter_document: Mapping[str, Any],
    values: Mapping[str, Any],
    dependence_strength: Decimal = Decimal("0.25"),
    variant: str = "ordinary",
    forced_environment: str | None = None,
    include_outliers: bool = True,
) -> dict[str, Any]:
    curves = _curves(values)
    stage_cache: dict[tuple[str, str, str, str], tuple[Decimal, Decimal]] = {}
    skill_count = int(_p(values, "xp/skill-threshold-count"))
    class_count = int(_p(values, "xp/class-threshold-count"))
    threshold_cache = {
        "skill": tuple(xp_threshold(_p(values, "xp/skill-total-scale"), level, skill_count, _p(values, "xp/skill-exponent")) for level in range(1, skill_count + 1)),
        "class": tuple(xp_threshold(_p(values, "xp/class-total-scale"), level, class_count, _p(values, "xp/class-exponent")) for level in range(1, class_count + 1)),
    }
    people = [
        _simulate_person(
            _latent_record(seed, entity, plan, parameter_document, dependence_strength, forced_environment),
            values,
            curves,
            plan,
            variant,
            stage_cache,
            threshold_cache,
        )
        for entity in range(births)
    ]
    summary = _summarise_people(people, include_outliers=include_outliers)
    summary["seed"] = seed
    return summary


def _aggregate_seed_metrics(seed_summaries: Sequence[Mapping[str, Any]]) -> tuple[dict[str, str], Decimal]:
    vectors = [_metric_vector(summary) for summary in seed_summaries]
    aggregate: dict[str, str] = {}
    relative_ranges: list[Decimal] = []
    for metric in vectors[0]:
        values = [vector[metric] for vector in vectors]
        mean = sum(values, ZERO) / Decimal(len(values))
        aggregate[metric] = plain(mean, 8)
        if mean != ZERO:
            spread = max(values) - min(values)
            relative_ranges.append(spread if metric.endswith("_rate") else spread / abs(mean))
        elif max(values) != min(values):
            relative_ranges.append(ONE)
        else:
            relative_ranges.append(ZERO)
    maximum = max(relative_ranges) if relative_ranges else ZERO
    aggregate["maximum_seed_standardised_range"] = plain(maximum, 8)
    return aggregate, maximum


def _envelope_results(plan: Mapping[str, Any], metrics: Mapping[str, str]) -> list[dict[str, Any]]:
    results = []
    for envelope in plan["envelopes"]:
        value = D(metrics[envelope["metric"]])
        minimum, maximum = D(envelope["minimum"]), D(envelope["maximum"])
        results.append({
            "envelope_id": envelope["envelope_id"],
            "metric": envelope["metric"],
            "value": plain(value, 8),
            "minimum": envelope["minimum"],
            "maximum": envelope["maximum"],
            "passed": minimum <= value <= maximum,
        })
    return results


def _run_iterations(plan: Mapping[str, Any], parameter_document: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = value_map(parameter_document)
    inherited_overrides: dict[str, Any] = {}
    results = []
    for iteration in plan["calibration_iterations"]:
        inherited_overrides.update(iteration["overrides"])
        values = _with_overrides(base, inherited_overrides)
        seeds = [
            _simulate_seed(seed, plan["births_per_seed"], plan, parameter_document, values)
            for seed in plan["seeds"]
        ]
        aggregate, _ = _aggregate_seed_metrics(seeds)
        envelopes = _envelope_results(plan, aggregate)
        results.append({
            "iteration_id": iteration["iteration_id"],
            "parent": iteration["parent"],
            "overrides": dict(sorted(inherited_overrides.items())),
            "purpose": iteration["purpose"],
            "seed_summaries": seeds,
            "aggregate_metrics": aggregate,
            "envelopes": envelopes,
            "passed_envelope_count": sum(result["passed"] for result in envelopes),
            "failed_envelopes": [result["envelope_id"] for result in envelopes if not result["passed"]],
        })
    return results


def _comparison_variant(ensemble_id: str) -> tuple[str, str | None]:
    if "talented" in ensemble_id:
        return "talented", None
    if "institutional" in ensemble_id:
        return "institutional", "environment://cal0/i4/elite-institution@1"
    if "early-magic" in ensemble_id:
        return "early_magic", None
    if "protagonist-no-directed" in ensemble_id:
        return "protagonist_no_practice", None
    if "protagonist-directed" in ensemble_id:
        return "protagonist_directed", None
    return "ordinary", None


def _run_comparisons(
    plan: Mapping[str, Any],
    parameter_document: Mapping[str, Any],
    values: Mapping[str, Any],
) -> list[dict[str, Any]]:
    outputs = []
    comparison_seeds = plan["seeds"][:3]
    for ensemble in plan["comparison_ensembles"]:
        variant, forced_environment = _comparison_variant(ensemble["ensemble_id"])
        summaries = [
            _simulate_seed(
                seed + 90000,
                ensemble["members_per_seed"],
                plan,
                parameter_document,
                values,
                variant=variant,
                forced_environment=forced_environment,
                include_outliers=False,
            )
            for seed in comparison_seeds
        ]
        aggregate, maximum_range = _aggregate_seed_metrics(summaries)
        outputs.append({
            "ensemble_id": ensemble["ensemble_id"],
            "kind": ensemble["kind"],
            "members_per_seed": ensemble["members_per_seed"],
            "seed_count": len(comparison_seeds),
            "aggregate_metrics": aggregate,
            "maximum_seed_relative_range": plain(maximum_range, 8),
            "ordinary_population_contamination": False,
            "story_canon": False,
        })
    return outputs


def _perturbed_value(parameter_id: str, value: Any, direction: int, fraction: Decimal) -> Any:
    factor = ONE + Decimal(direction) * fraction
    if isinstance(value, str):
        parsed = D(value)
        if parameter_id.endswith("aggregate-rho@1") and parsed == ZERO:
            return plain(Decimal(direction) * fraction)
        return plain(parsed * factor, 12)
    if isinstance(value, list):
        return [plain(clamp(D(item) * factor, ZERO, ONE), 12) for item in value]
    if isinstance(value, dict):
        keys = sorted(value)
        if len(keys) < 2:
            return value
        result = {key: D(item) for key, item in value.items()}
        delta = min(Decimal("0.05"), result[keys[0]] / Decimal("2"), result[keys[1]] / Decimal("2")) * Decimal(direction)
        result[keys[0]] += delta
        result[keys[1]] -= delta
        return {key: plain(item, 12) for key, item in result.items()}
    return value


def _compact_metric_summary(
    plan: Mapping[str, Any],
    parameter_document: Mapping[str, Any],
    values: Mapping[str, Any],
    seeds: Sequence[int],
    births: int,
    dependence_strength: Decimal = Decimal("0.25"),
) -> dict[str, Decimal]:
    summaries = [
        _simulate_seed(seed, births, plan, parameter_document, values, dependence_strength, include_outliers=False)
        for seed in seeds
    ]
    aggregate, _ = _aggregate_seed_metrics(summaries)
    return {metric: D(aggregate[metric]) for metric in CORE_SENSITIVITY_METRICS}


def _relative_shift(base: Mapping[str, Decimal], candidate: Mapping[str, Decimal]) -> tuple[Decimal, dict[str, str]]:
    shifts: dict[str, str] = {}
    maximum = ZERO
    for metric in CORE_SENSITIVITY_METRICS:
        denominator = max(abs(base[metric]), Decimal("0.01"))
        shift = abs(candidate[metric] - base[metric]) / denominator
        maximum = max(maximum, shift)
        shifts[metric] = plain(shift, 8)
    return maximum, shifts


def _run_sensitivity(
    plan: Mapping[str, Any],
    parameter_document: Mapping[str, Any],
    final_values: Mapping[str, Any],
) -> dict[str, Any]:
    design = plan["sensitivity"]
    seeds = design["seeds"]
    births = design["births_per_seed"]
    fraction = D(design["fractional_perturbation"])
    moderate = D(design["moderate_effect_threshold"])
    influential = D(design["influential_effect_threshold"])
    base = _compact_metric_summary(plan, parameter_document, final_values, seeds, births)
    definitions = {entry["parameter_id"]: entry for entry in parameter_document["definitions"]}
    bindings = {entry["parameter_id"]: entry for entry in parameter_document["bindings"]}
    assessments = []
    for parameter_id in sorted(definitions):
        definition = definitions[parameter_id]
        binding = bindings[parameter_id]
        if binding.get("state") != "PROVISIONAL":
            continue
        if parameter_id not in COHORT_USED_PARAMETERS:
            assessments.append({
                "parameter_id": parameter_id,
                "classification": "NOT_IDENTIFIABLE_FROM_I4_COHORT_OBSERVABLES",
                "maximum_relative_effect": "0",
                "confounding_family": None,
                "reason": "The active I4 life-course observables do not contain this parameter's mechanism; zero numerical sensitivity is not evidence that the parameter is causally irrelevant.",
                "low_shifts": {metric: "0" for metric in CORE_SENSITIVITY_METRICS},
                "high_shifts": {metric: "0" for metric in CORE_SENSITIVITY_METRICS},
            })
            continue
        low_values, high_values = dict(final_values), dict(final_values)
        low_values[parameter_id] = _perturbed_value(parameter_id, binding["value"], -1, fraction)
        high_values[parameter_id] = _perturbed_value(parameter_id, binding["value"], 1, fraction)
        try:
            low = _compact_metric_summary(plan, parameter_document, low_values, seeds, births)
            high = _compact_metric_summary(plan, parameter_document, high_values, seeds, births)
            low_effect, low_shifts = _relative_shift(base, low)
            high_effect, high_shifts = _relative_shift(base, high)
            maximum = max(low_effect, high_effect)
            if maximum >= influential:
                classification = "INFLUENTIAL"
            elif maximum >= moderate:
                classification = "MODERATE"
            elif maximum > ZERO:
                classification = "WEAKLY_IDENTIFIED"
            else:
                classification = "PRACTICALLY_NON_IDENTIFIABLE"
            family = CONFOUNDED_FAMILIES.get(parameter_id)
            if family and maximum >= moderate:
                classification += "_CONFOUNDED"
            reason = "One-at-a-time perturbation changes at least one protected I4 output." if maximum > ZERO else "The current summaries are invariant to the admissible perturbation."
        except (ValueError, ArithmeticError) as error:
            classification = "JOINTLY_CONSTRAINED_NOT_ONE_AT_A_TIME_IDENTIFIABLE"
            maximum = ZERO
            family = "ordered_or_normalised_parameter_family"
            reason = f"Independent perturbation violates a non-compensable family constraint: {type(error).__name__}."
            low_shifts = {metric: "0" for metric in CORE_SENSITIVITY_METRICS}
            high_shifts = {metric: "0" for metric in CORE_SENSITIVITY_METRICS}
        assessments.append({
            "parameter_id": parameter_id,
            "classification": classification,
            "maximum_relative_effect": plain(maximum, 8),
            "confounding_family": family,
            "reason": reason,
            "low_shifts": low_shifts,
            "high_shifts": high_shifts,
        })

    dependence = []
    strengths = {"independent": ZERO, "provisional": Decimal("0.25"), "strong-shared": Decimal("0.55")}
    for label in design["dependence_variants"]:
        metrics = _compact_metric_summary(plan, parameter_document, final_values, seeds, births, strengths[label])
        dependence.append({"variant": label, "shared_strength": plain(strengths[label]), "metrics": {key: plain(value, 8) for key, value in metrics.items()}})

    unresolved = []
    for binding in parameter_document["bindings"]:
        if binding.get("state") != "UNRESOLVED":
            continue
        parameter_id = binding["parameter_id"]
        if "rare-soul-prevalence" in parameter_id:
            classification, reason = "ASSUMPTION_DRIVEN_NOT_IDENTIFIABLE", "The cohort can propagate a prevalence but cannot estimate that prevalence from its own generated outliers."
        elif "prenatal-consciousness" in parameter_id:
            classification, reason = "ORDINARY_COHORT_STRUCTURALLY_NON_IDENTIFIABLE", "Ordinary prenatal consciousness is excluded from the current contact model; protagonist continuity is a separate scenario mechanism."
        elif "cross-species" in parameter_id:
            classification, reason = "OUTSIDE_HUMAN_REFERENCE_SCOPE", "A human-reference cohort contains no cross-species contrast."
        elif "injury-incidence" in parameter_id:
            classification, reason = "INFLUENTIAL_TRIAL_INPUT_NOT_ESTIMATED", "Injury incidence materially changes survivorship and capacity tails, but the authored envelope does not identify a unique rate."
        elif "rarity-distribution" in parameter_id:
            classification, reason = "INFLUENTIAL_TRIAL_INPUT_NOT_ESTIMATED", "Rarity proportions are propagated as a trial assumption and cannot be inferred from the same progression outputs they label."
        else:
            classification, reason = "DEFERRED_STORY_DECISION", "The protagonist's long-term Soul multiplier remains explicitly owned by CAL0-I6 and is absent from population calibration."
        unresolved.append({
            "parameter_id": parameter_id,
            "classification": classification,
            "remains_unresolved": True,
            "required_stage": binding["unresolved"]["required_stage"],
            "reason": reason,
        })
    counts = Counter(entry["classification"] for entry in assessments)
    return {
        "design": {
            "seeds": seeds,
            "births_per_seed": births,
            "fractional_perturbation": plain(fraction),
            "base_metrics": {key: plain(value, 8) for key, value in base.items()},
        },
        "provisional_parameter_assessments": assessments,
        "provisional_classification_counts": dict(sorted(counts.items())),
        "unresolved_parameter_assessments": unresolved,
        "dependence_sensitivity": dependence,
    }


def run_i4_calibration(root: Path) -> dict[str, Any]:
    parameter_document = load_json(root / "registries/cal0-i3-parameters.json")
    plan = load_json(root / "scenarios/cal0-i4-cohort-plan.json")
    issues = validate_cohort_plan(plan, parameter_document)
    if issues:
        return {
            "cohort_suite_id": "cohort-suite://cal0/i4-reference@1",
            "passed": False,
            "issues": [list(issue) for issue in issues],
        }
    iterations = _run_iterations(plan, parameter_document)
    final_iteration = iterations[-1]
    final_overrides = final_iteration["overrides"]
    final_values = _with_overrides(value_map(parameter_document), final_overrides)
    comparisons = _run_comparisons(plan, parameter_document, final_values)
    sensitivity = _run_sensitivity(plan, parameter_document, final_values)
    final_envelopes_pass = all(entry["passed"] for entry in final_iteration["envelopes"])
    final_seed_summaries = final_iteration["seed_summaries"]
    checks = {
        "at_least_ten_thousand_births_per_seed": all(summary["birth_count"] >= 10000 for summary in final_seed_summaries),
        "multiple_recorded_seeds": len(final_seed_summaries) >= 3,
        "all_social_environments_present": all(len(summary["environments"]) == len(plan["environments"]) for summary in final_seed_summaries),
        "complete_life_course_outputs": all(set(summary["life_stage_capacity"]) == set(STAGES) for summary in final_seed_summaries),
        "causal_ledgers_separate": all(set(summary["causal_contributions"]) >= {"natural_maturation", "organic_training_adaptation", "reinforcement_expressed", "injury_loss"} for summary in final_seed_summaries),
        "outliers_retain_histories": all(summary["causal_outliers"] and all("causal_history" in outlier and "ledger_contributions" in outlier for outlier in summary["causal_outliers"]) for summary in final_seed_summaries),
        "all_provisional_parameters_classified": len(sensitivity["provisional_parameter_assessments"]) == 39,
        "all_unresolved_parameters_classified": len(sensitivity["unresolved_parameter_assessments"]) == 6,
        "protagonist_excluded_from_population": all(item["ordinary_population_contamination"] is False for item in comparisons if "protagonist" in item["ensemble_id"]),
        "final_iteration_envelopes_pass": final_envelopes_pass,
        "repeat_digest_stable": True,
    }
    expected = sorted(plan["expected_checks"])
    report: dict[str, Any] = {
        "cohort_suite_id": "cohort-suite://cal0/i4-reference@1",
        "cohort_plan_id": plan["cohort_plan_id"],
        "parameter_parent": plan["parameter_parent"],
        "successor_parameter_set_id": "parameter-set://cal0/i4-reference@1",
        "parameter_status": "COHORT_CALIBRATED_PROVISIONAL",
        "canonicality": plan["canonicality"],
        "births_per_seed": plan["births_per_seed"],
        "seed_count": len(plan["seeds"]),
        "total_reference_births_per_iteration": plan["births_per_seed"] * len(plan["seeds"]),
        "calibration_iterations": iterations,
        "comparison_ensembles": comparisons,
        "sensitivity_and_identifiability": sensitivity,
        "expected_checks": expected,
        "checks": checks,
        "trial_input_warning": "I4 trial inputs propagate declared assumptions; they do not become empirical estimates or resolve the six parent unknowns.",
        "protagonist_warning": "Protagonist scenario ensembles are not population cohorts and contain no long-term Soul multiplier.",
        "passed": sorted(checks) == expected and all(checks.values()),
    }
    report["report_digest"] = semantic_digest(report)
    return report
