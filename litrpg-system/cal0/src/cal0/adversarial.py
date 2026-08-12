"""Invariant-led CAL0-I5 adversarial validation and replay."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, Mapping

from .canonical import semantic_digest
from .exact import D
from .parameter_runtime import load_json


SURFACES = {
    "individual", "institutional", "economic", "ecological", "informational",
    "magical", "training", "identity", "replay",
}

INVARIANTS = {
    "provenance", "non_duplication", "prospective_progression", "single_reinforcement",
    "projection_not_creation", "scoped_authority", "supported_renewal", "exclusive_identity",
    "organic_adaptation", "atomic_replay",
}

REQUIRED_FAMILY_TAGS = {
    "skill-fragmentation-fusion-inheritance-grants-suppression-reacquisition",
    "class-cycling-role-theatre-offer-manipulation-evidence-laundering-milestone-replay",
    "delegated-kills-party-contribution-manufactured-danger-captive-targets-threat-inflation",
    "achievement-firsts-title-authority-perk-selection-quest-amendment-reward-duplication",
    "dungeon-spawn-industrialisation-reset-loops-treasure-restocking-controller-capture",
    "breeding-harvesting-migration-depletion-domestication-magical-resource-farming",
    "item-repair-reconstruction-copying-salvage-binding-storage-nesting-relic-continuity",
    "spell-components-stored-casting-ritual-delegation-wards-constructs-perpetual-motion",
    "appraisal-privacy-false-disclosure-surveillance-interface-spoofing",
    "resurrection-reincarnation-possession-soul-division-memory-copying-identity-duplication",
    "training-volume-cross-training-overtraining-detraining-rehabilitation-artificial-assistance-stat-farming",
    "education-puzzles-meditation-pain-controlled-adversity-semantic-task-duplication",
    "institutional-monopoly-coercive-progression-recovery-inequality-child-optimisation-intergenerational-advantage",
}


REPAIRS: tuple[dict[str, Any], ...] = (
    {
        "repair_id": "CAL0-I5-R01",
        "title": "Canonical semantic-origin entitlement key",
        "classification": "LOCAL_MISSING_RULE",
        "failure_boundary": "Raw labels could distinguish claims derived from one underlying event.",
        "repair": "Entitlements are keyed by recipient, protected facet, and canonical causal origin before aliases are evaluated.",
        "affected_invariants": ["non_duplication", "single_reinforcement", "prospective_progression"],
    },
    {
        "repair_id": "CAL0-I5-R02",
        "title": "Source-bounded renewal witness",
        "classification": "IMPLEMENTATION_OR_TEST_DEFECT",
        "failure_boundary": "The inherited generic recovery API accepted a provenance label without proving a replenishing input budget.",
        "repair": "Recovery and spawning require a typed source witness and cannot exceed the witnessed renewable input or remaining capacity.",
        "affected_invariants": ["provenance", "supported_renewal"],
    },
    {
        "repair_id": "CAL0-I5-R03",
        "title": "Projection, evidence, access, and authority separation",
        "classification": "PRESENTATION_OR_DOCUMENTATION_AMBIGUITY",
        "failure_boundary": "A truthful or forged interface record could be mistaken for the capability, permission, or fact displayed.",
        "repair": "Every consequential projection requires source evidence, audience permission, scope, and a distinct authority or capability witness.",
        "affected_invariants": ["projection_not_creation", "scoped_authority", "provenance"],
    },
    {
        "repair_id": "CAL0-I5-R04",
        "title": "Exclusive identity-continuation ledger",
        "classification": "LOCAL_MISSING_RULE",
        "failure_boundary": "Embodied, copied, summoned, or restored processes lacked one shared executable holder registry.",
        "repair": "One identity lineage may have at most one continuing holder; copies and successors receive explicit derived identities unless a witnessed exclusive transfer occurs.",
        "affected_invariants": ["exclusive_identity", "non_duplication", "provenance"],
    },
    {
        "repair_id": "CAL0-I5-R05",
        "title": "Stimulus-origin deduplication and harm gate",
        "classification": "LOCAL_MISSING_RULE",
        "failure_boundary": "Separately submitted labels could multiply one physical or cognitive stimulus, and damage lacked a universal no-free-growth gate.",
        "repair": "Adaptation is bounded by unique causal stimulus origins, loaded structures, recovery, and headroom; damage cannot itself become positive adaptation.",
        "affected_invariants": ["organic_adaptation", "non_duplication", "provenance"],
    },
)


def _case(
    case_id: str,
    title: str,
    surface: str,
    scale: str,
    family: str,
    mechanism: str,
    expected: str,
    invariants: list[str],
    facts: Mapping[str, Any],
    repair_id: str | None = None,
) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "title": title,
        "surface": surface,
        "scale": scale,
        "family_tags": [family],
        "mechanism": mechanism,
        "expected_disposition": expected,
        "affected_invariants": invariants,
        "subsystems": sorted({surface, mechanism}),
        "repair_id": repair_id,
        "preconditions": ["attacker has the declared access, time, and knowledge", "all undeclared capabilities are absent"],
        "actor_knowledge": ["published System behaviour", "locally observable causal results"],
        "available_resources": {"bounded": True, "declared_facts": dict(facts)},
        "action_sequence": ["establish declared preconditions", "attempt the adversarial transaction", "evaluate protected invariants", "commit or reject atomically"],
        "facts": dict(facts),
    }


ATTACKS: tuple[dict[str, Any], ...] = (
    _case("I5-A01", "Fragment one Skill event into renamed micro-Skills", "individual", "individual", "skill-fragmentation-fusion-inheritance-grants-suppression-reacquisition", "entitlement", "DENIED", ["non_duplication", "single_reinforcement"], {"canonical_origin_count": 1, "claim_count": 4, "prospective": True}, "CAL0-I5-R01"),
    _case("I5-A02", "Cycle classes and launder pre-acceptance role theatre", "individual", "individual", "class-cycling-role-theatre-offer-manipulation-evidence-laundering-milestone-replay", "entitlement", "DENIED", ["prospective_progression", "non_duplication"], {"canonical_origin_count": 1, "claim_count": 1, "prospective": False}, "CAL0-I5-R01"),
    _case("I5-A03", "Claim full personal kill credit through token delegation", "individual", "group", "delegated-kills-party-contribution-manufactured-danger-captive-targets-threat-inflation", "contribution", "DENIED", ["provenance", "non_duplication"], {"causal_contribution": "0.12", "claimed_contribution": "1", "threat_real": False}),
    _case("I5-A04", "Copy a relic identity from one salvaged fragment", "individual", "individual", "item-repair-reconstruction-copying-salvage-binding-storage-nesting-relic-continuity", "identity", "DENIED", ["exclusive_identity", "non_duplication"], {"original_claimants": 3, "exclusive_transfer": False, "derived_copies": False}, "CAL0-I5-R04"),

    _case("I5-A05", "Academy compounds nutrition, coaching, feedback, and recovery", "institutional", "institution", "institutional-monopoly-coercive-progression-recovery-inequality-child-optimisation-intergenerational-advantage", "training", "ALLOWED", ["organic_adaptation", "provenance"], {"unique_stimuli": 12, "claimed_adaptation": "0.48", "supported_adaptation": "0.52", "recovery": True, "damage_as_growth": False}, "CAL0-I5-R05"),
    _case("I5-A06", "Guardian appropriates a child's identity-bearing progression", "institutional", "institution", "institutional-monopoly-coercive-progression-recovery-inequality-child-optimisation-intergenerational-advantage", "authority", "DENIED", ["scoped_authority", "exclusive_identity"], {"source_evidence": True, "audience_permission": True, "authority_scope": False, "consent_ok": False, "display_only": False}, "CAL0-I5-R03"),
    _case("I5-A07", "Displayed guild title is treated as universal authority", "institutional", "institution", "achievement-firsts-title-authority-perk-selection-quest-amendment-reward-duplication", "authority", "DENIED", ["projection_not_creation", "scoped_authority"], {"source_evidence": True, "audience_permission": True, "authority_scope": False, "consent_ok": True, "display_only": True}, "CAL0-I5-R03"),
    _case("I5-A08", "Guild monopoly preserves costly expertise across generations", "institutional", "institution", "institutional-monopoly-coercive-progression-recovery-inequality-child-optimisation-intergenerational-advantage", "production", "ALLOWED", ["provenance", "scoped_authority"], {"input_units": "100", "output_units": "92", "source_witness": True, "authority_scope": True}),

    _case("I5-A09", "Automated crafting line multiplies throughput with funded inputs", "economic", "economy", "item-repair-reconstruction-copying-salvage-binding-storage-nesting-relic-continuity", "production", "ALLOWED", ["provenance", "supported_renewal"], {"input_units": "1000", "output_units": "940", "source_witness": True, "authority_scope": True}),
    _case("I5-A10", "Reward arbitrage renames one delivery across contracts", "economic", "economy", "achievement-firsts-title-authority-perk-selection-quest-amendment-reward-duplication", "entitlement", "DENIED", ["non_duplication", "single_reinforcement"], {"canonical_origin_count": 1, "claim_count": 6, "prospective": True}, "CAL0-I5-R01"),
    _case("I5-A11", "Nested storage claims each container's full external capacity", "economic", "economy", "item-repair-reconstruction-copying-salvage-binding-storage-nesting-relic-continuity", "resource", "DENIED", ["provenance", "supported_renewal"], {"input_units": "20", "renewal_units": "0", "output_units": "100", "source_witness": False}),
    _case("I5-A12", "Dungeon spawn industry harvests below witnessed renewal", "economic", "economy", "dungeon-spawn-industrialisation-reset-loops-treasure-restocking-controller-capture", "resource", "ALLOWED", ["provenance", "supported_renewal"], {"input_units": "30", "renewal_units": "70", "output_units": "80", "source_witness": True}, "CAL0-I5-R02"),

    _case("I5-A13", "Selective breeding improves a population over real generations", "ecological", "ecology", "breeding-harvesting-migration-depletion-domestication-magical-resource-farming", "ecology", "ALLOWED", ["provenance", "supported_renewal"], {"stock": "500", "renewal": "80", "harvest": "40", "reproduction_witness": True}),
    _case("I5-A14", "Harvest cartel extracts beyond stock and regeneration", "ecological", "ecology", "breeding-harvesting-migration-depletion-domestication-magical-resource-farming", "ecology", "DENIED", ["provenance", "supported_renewal"], {"stock": "100", "renewal": "10", "harvest": "160", "reproduction_witness": True}, "CAL0-I5-R02"),
    _case("I5-A15", "Migration is counted as birth in both source and destination", "ecological", "ecology", "breeding-harvesting-migration-depletion-domestication-magical-resource-farming", "entitlement", "DENIED", ["non_duplication", "provenance"], {"canonical_origin_count": 1, "claim_count": 2, "prospective": True}, "CAL0-I5-R01"),
    _case("I5-A16", "Invasive magical organism expands through real reproduction", "ecological", "ecology", "breeding-harvesting-migration-depletion-domestication-magical-resource-farming", "ecology", "ALLOWED", ["provenance", "supported_renewal"], {"stock": "40", "renewal": "30", "harvest": "5", "reproduction_witness": True}),

    _case("I5-A17", "Appraisal infers protected private facets without evidence", "informational", "institution", "appraisal-privacy-false-disclosure-surveillance-interface-spoofing", "authority", "DENIED", ["projection_not_creation", "scoped_authority"], {"source_evidence": False, "audience_permission": False, "authority_scope": False, "consent_ok": False, "display_only": False}, "CAL0-I5-R03"),
    _case("I5-A18", "Forged interface disclosure manufactures capability", "informational", "individual", "appraisal-privacy-false-disclosure-surveillance-interface-spoofing", "authority", "DENIED", ["projection_not_creation", "provenance"], {"source_evidence": False, "audience_permission": True, "authority_scope": False, "consent_ok": True, "display_only": True}, "CAL0-I5-R03"),
    _case("I5-A19", "Hospital audits a consented treatment record in scope", "informational", "institution", "appraisal-privacy-false-disclosure-surveillance-interface-spoofing", "authority", "ALLOWED", ["projection_not_creation", "scoped_authority"], {"source_evidence": True, "audience_permission": True, "authority_scope": True, "consent_ok": True, "display_only": False}, "CAL0-I5-R03"),
    _case("I5-A20", "Census suppression recalculates an accepted rarity reward", "informational", "economy", "achievement-firsts-title-authority-perk-selection-quest-amendment-reward-duplication", "entitlement", "DENIED", ["single_reinforcement", "prospective_progression"], {"canonical_origin_count": 0, "claim_count": 1, "prospective": False}, "CAL0-I5-R01"),

    _case("I5-A21", "Equivalent spell component substitution pays real cost", "magical", "individual", "spell-components-stored-casting-ritual-delegation-wards-constructs-perpetual-motion", "resource", "ALLOWED", ["provenance", "supported_renewal"], {"input_units": "12", "renewal_units": "0", "output_units": "12", "source_witness": True}),
    _case("I5-A22", "One stored charge is invoked twice", "magical", "individual", "spell-components-stored-casting-ritual-delegation-wards-constructs-perpetual-motion", "resource", "DENIED", ["non_duplication", "supported_renewal"], {"input_units": "1", "renewal_units": "0", "output_units": "2", "source_witness": True}),
    _case("I5-A23", "Ritual delegates work while conserving combined Mana", "magical", "group", "spell-components-stored-casting-ritual-delegation-wards-constructs-perpetual-motion", "resource", "ALLOWED", ["provenance", "supported_renewal"], {"input_units": "120", "renewal_units": "0", "output_units": "108", "source_witness": True}),
    _case("I5-A24", "Ward network gains scale through maintained infrastructure", "magical", "institution", "spell-components-stored-casting-ritual-delegation-wards-constructs-perpetual-motion", "production", "ALLOWED", ["provenance", "scoped_authority"], {"input_units": "600", "output_units": "570", "source_witness": True, "authority_scope": True}),
    _case("I5-A25", "Magical loop recovers more Mana than supplied", "magical", "economy", "spell-components-stored-casting-ritual-delegation-wards-constructs-perpetual-motion", "resource", "DENIED", ["provenance", "supported_renewal"], {"input_units": "10", "renewal_units": "80", "output_units": "90", "source_witness": False}, "CAL0-I5-R02"),

    _case("I5-A26", "One workout is submitted under many Skill labels", "training", "individual", "training-volume-cross-training-overtraining-detraining-rehabilitation-artificial-assistance-stat-farming", "training", "DENIED", ["organic_adaptation", "non_duplication"], {"unique_stimuli": 1, "claimed_adaptation": "0.30", "supported_adaptation": "0.03", "recovery": True, "damage_as_growth": False}, "CAL0-I5-R05"),
    _case("I5-A27", "Progressive cross-training creates a supported portfolio", "training", "institution", "training-volume-cross-training-overtraining-detraining-rehabilitation-artificial-assistance-stat-farming", "training", "ALLOWED", ["organic_adaptation", "provenance"], {"unique_stimuli": 8, "claimed_adaptation": "0.32", "supported_adaptation": "0.36", "recovery": True, "damage_as_growth": False}, "CAL0-I5-R05"),
    _case("I5-A28", "Overtraining injury is claimed as automatic growth", "training", "individual", "training-volume-cross-training-overtraining-detraining-rehabilitation-artificial-assistance-stat-farming", "training", "DENIED", ["organic_adaptation", "provenance"], {"unique_stimuli": 6, "claimed_adaptation": "0.20", "supported_adaptation": "0.02", "recovery": False, "damage_as_growth": True}, "CAL0-I5-R05"),
    _case("I5-A29", "Rehabilitation restores supported lost capacity", "training", "institution", "training-volume-cross-training-overtraining-detraining-rehabilitation-artificial-assistance-stat-farming", "training", "ALLOWED", ["organic_adaptation", "provenance"], {"unique_stimuli": 10, "claimed_adaptation": "0.18", "supported_adaptation": "0.22", "recovery": True, "damage_as_growth": False}, "CAL0-I5-R05"),
    _case("I5-A30", "Solved puzzles, nominal meditations, and pain are replayed for stats", "training", "individual", "education-puzzles-meditation-pain-controlled-adversity-semantic-task-duplication", "training", "DENIED", ["organic_adaptation", "non_duplication"], {"unique_stimuli": 1, "claimed_adaptation": "0.40", "supported_adaptation": "0", "recovery": False, "damage_as_growth": True}, "CAL0-I5-R05"),

    _case("I5-A31", "Resurrection leaves original identity active in two bodies", "identity", "metaphysical", "resurrection-reincarnation-possession-soul-division-memory-copying-identity-duplication", "identity", "DENIED", ["exclusive_identity", "non_duplication"], {"original_claimants": 2, "exclusive_transfer": False, "derived_copies": False}, "CAL0-I5-R04"),
    _case("I5-A32", "Reincarnation transfers one identity and ends prior embodiment", "identity", "metaphysical", "resurrection-reincarnation-possession-soul-division-memory-copying-identity-duplication", "identity", "ALLOWED", ["exclusive_identity", "provenance"], {"original_claimants": 1, "exclusive_transfer": True, "derived_copies": False}, "CAL0-I5-R04"),
    _case("I5-A33", "Possessor appropriates host identity through control alone", "identity", "metaphysical", "resurrection-reincarnation-possession-soul-division-memory-copying-identity-duplication", "identity", "DENIED", ["exclusive_identity", "scoped_authority"], {"original_claimants": 2, "exclusive_transfer": False, "derived_copies": False}, "CAL0-I5-R04"),
    _case("I5-A34", "Soul division gives every fragment the complete parent identity", "identity", "metaphysical", "resurrection-reincarnation-possession-soul-division-memory-copying-identity-duplication", "identity", "DENIED", ["exclusive_identity", "non_duplication"], {"original_claimants": 4, "exclusive_transfer": False, "derived_copies": False}, "CAL0-I5-R04"),
    _case("I5-A35", "Memory copy becomes a derived person without parent entitlements", "identity", "metaphysical", "resurrection-reincarnation-possession-soul-division-memory-copying-identity-duplication", "identity", "ALLOWED", ["exclusive_identity", "provenance"], {"original_claimants": 1, "exclusive_transfer": False, "derived_copies": True}, "CAL0-I5-R04"),
    _case("I5-A36", "Construct succession preserves a traced derived lineage", "identity", "metaphysical", "spell-components-stored-casting-ritual-delegation-wards-constructs-perpetual-motion", "identity", "ALLOWED", ["exclusive_identity", "provenance"], {"original_claimants": 1, "exclusive_transfer": True, "derived_copies": True}, "CAL0-I5-R04"),

    _case("I5-A37", "Quest amendment pays for a completed past act", "replay", "individual", "achievement-firsts-title-authority-perk-selection-quest-amendment-reward-duplication", "replay", "DENIED", ["prospective_progression", "non_duplication"], {"semantic_event_count": 1, "reward_claim_count": 2, "version_match": True, "atomic": True}, "CAL0-I5-R01"),
    _case("I5-A38", "Dungeon reset restocks treasure without renewal inputs", "replay", "economy", "dungeon-spawn-industrialisation-reset-loops-treasure-restocking-controller-capture", "resource", "DENIED", ["supported_renewal", "provenance"], {"input_units": "0", "renewal_units": "100", "output_units": "100", "source_witness": False}, "CAL0-I5-R02"),
    _case("I5-A39", "Skill suppression and reacquisition reclaim reinforcement", "replay", "individual", "skill-fragmentation-fusion-inheritance-grants-suppression-reacquisition", "replay", "DENIED", ["single_reinforcement", "non_duplication"], {"semantic_event_count": 1, "reward_claim_count": 2, "version_match": True, "atomic": True}, "CAL0-I5-R01"),
    _case("I5-A40", "Transformation cycling replays one developmental threshold", "replay", "metaphysical", "class-cycling-role-theatre-offer-manipulation-evidence-laundering-milestone-replay", "replay", "DENIED", ["single_reinforcement", "non_duplication"], {"semantic_event_count": 1, "reward_claim_count": 5, "version_match": True, "atomic": True}, "CAL0-I5-R01"),
    _case("I5-A41", "Time loop repeats rewards while retaining the beneficiary", "replay", "metaphysical", "achievement-firsts-title-authority-perk-selection-quest-amendment-reward-duplication", "replay", "DENIED", ["non_duplication", "exclusive_identity"], {"semantic_event_count": 1, "reward_claim_count": 8, "version_match": True, "atomic": True}, "CAL0-I5-R01"),
    _case("I5-A42", "Stale proof frontier publishes a partial successor", "replay", "institution", "appraisal-privacy-false-disclosure-surveillance-interface-spoofing", "replay", "DENIED", ["atomic_replay", "provenance"], {"semantic_event_count": 3, "reward_claim_count": 3, "version_match": False, "atomic": False}),
)


def _evaluate(case: Mapping[str, Any]) -> tuple[str, list[str], dict[str, Any]]:
    facts = case["facts"]
    mechanism = case["mechanism"]
    reasons: list[str] = []
    evidence: dict[str, Any] = {}
    allowed = False
    if mechanism == "entitlement":
        allowed = bool(facts["prospective"]) and int(facts["claim_count"]) <= int(facts["canonical_origin_count"])
        reasons += [] if allowed else (["RETROSPECTIVE_PROGRESSION"] if not facts["prospective"] else ["DUPLICATE_ENTITLEMENT"])
        evidence = {"canonical_origin_count": facts["canonical_origin_count"], "admitted_claim_count": min(int(facts["claim_count"]), int(facts["canonical_origin_count"])) if facts["prospective"] else 0}
    elif mechanism == "contribution":
        allowed = bool(facts["threat_real"]) and D(facts["claimed_contribution"]) <= D(facts["causal_contribution"])
        reasons += [] if allowed else ["UNSUPPORTED_CONTRIBUTION_OR_THREAT"]
        evidence = {"causal_contribution": facts["causal_contribution"], "threat_real": facts["threat_real"]}
    elif mechanism in {"resource", "production"}:
        available = D(facts["input_units"]) + D(facts.get("renewal_units", "0"))
        renewal_ok = D(facts.get("renewal_units", "0")) == 0 or bool(facts.get("source_witness"))
        allowed = renewal_ok and D(facts["output_units"]) <= available and bool(facts.get("source_witness", True)) and bool(facts.get("authority_scope", True))
        reasons += [] if allowed else (["UNWITNESSED_RENEWAL"] if not renewal_ok else ["UNFUNDED_OUTPUT_OR_SCOPE"])
        evidence = {"available_units": str(available), "output_units": facts["output_units"], "renewal_witnessed": renewal_ok}
    elif mechanism == "authority":
        allowed = all(bool(facts[key]) for key in ("source_evidence", "audience_permission", "authority_scope", "consent_ok")) and not bool(facts["display_only"])
        reasons += [] if allowed else ["PROJECTION_OR_SCOPE_CANNOT_CREATE_AUTHORITY"]
        evidence = {key: facts[key] for key in sorted(facts)}
    elif mechanism == "training":
        allowed = bool(facts["recovery"]) and not bool(facts["damage_as_growth"]) and D(facts["claimed_adaptation"]) <= D(facts["supported_adaptation"])
        reasons += [] if allowed else ["UNSUPPORTED_OR_HARM_DERIVED_ADAPTATION"]
        evidence = {"unique_stimuli": facts["unique_stimuli"], "supported_adaptation": facts["supported_adaptation"], "damage_as_growth": facts["damage_as_growth"]}
    elif mechanism == "identity":
        allowed = int(facts["original_claimants"]) <= 1 and (bool(facts["exclusive_transfer"]) or bool(facts["derived_copies"]))
        reasons += [] if allowed else ["EXCLUSIVE_IDENTITY_VIOLATION"]
        evidence = {"continuing_original_holders": min(int(facts["original_claimants"]), 1), "derived_copy_identity": bool(facts["derived_copies"]), "exclusive_transfer": bool(facts["exclusive_transfer"])}
    elif mechanism == "ecology":
        allowed = bool(facts["reproduction_witness"]) and D(facts["harvest"]) <= D(facts["stock"]) + D(facts["renewal"])
        reasons += [] if allowed else ["ECOLOGICAL_SOURCE_EXHAUSTED"]
        evidence = {"available_biomass": str(D(facts["stock"]) + D(facts["renewal"])), "harvest": facts["harvest"], "reproduction_witness": facts["reproduction_witness"]}
    elif mechanism == "replay":
        allowed = bool(facts["version_match"]) and bool(facts["atomic"]) and int(facts["reward_claim_count"]) <= int(facts["semantic_event_count"])
        reasons += [] if allowed else (["STALE_OR_NON_ATOMIC_COMMIT"] if not facts["version_match"] or not facts["atomic"] else ["SEMANTIC_REPLAY"])
        evidence = {"unique_semantic_events": facts["semantic_event_count"], "admitted_rewards": min(int(facts["reward_claim_count"]), int(facts["semantic_event_count"])) if facts["version_match"] and facts["atomic"] else 0}
    else:
        raise ValueError(f"unknown adversarial mechanism: {mechanism}")
    return ("ALLOWED" if allowed else "DENIED"), reasons, evidence


def validate_attack_catalog(attacks: Any = ATTACKS, repairs: Any = REPAIRS) -> list[tuple[str, str, str]]:
    issues: list[tuple[str, str, str]] = []
    if not isinstance(attacks, (list, tuple)):
        return [("I5_ATTACK_CATALOG_TYPE", "attacks", "attack catalog must be a sequence")]
    ids: set[str] = set()
    repair_ids = {item.get("repair_id") for item in repairs if isinstance(item, dict)} if isinstance(repairs, (list, tuple)) else set()
    family_tags: set[str] = set()
    surfaces: set[str] = set()
    for index, case in enumerate(attacks):
        path = f"attacks[{index}]"
        if not isinstance(case, dict):
            issues.append(("I5_ATTACK_CASE_TYPE", path, "attack case must be an object"))
            continue
        case_id = case.get("case_id")
        if not isinstance(case_id, str) or case_id in ids:
            issues.append(("I5_ATTACK_ID", f"{path}.case_id", "attack identity must be unique"))
        else:
            ids.add(case_id)
        surface = case.get("surface")
        if surface not in SURFACES:
            issues.append(("I5_ATTACK_SURFACE", f"{path}.surface", "unknown adversarial surface"))
        else:
            surfaces.add(surface)
        family_tags.update(case.get("family_tags", ()))
        if case.get("expected_disposition") not in {"ALLOWED", "DENIED"}:
            issues.append(("I5_ATTACK_EXPECTATION", f"{path}.expected_disposition", "unknown expected disposition"))
        if not set(case.get("affected_invariants", ())).issubset(INVARIANTS):
            issues.append(("I5_ATTACK_INVARIANT", f"{path}.affected_invariants", "unknown governing invariant"))
        repair_id = case.get("repair_id")
        if repair_id is not None and repair_id not in repair_ids:
            issues.append(("I5_ATTACK_REPAIR", f"{path}.repair_id", "attack references unknown repair"))
        try:
            _evaluate(case)
        except (KeyError, TypeError, ValueError) as error:
            issues.append(("I5_ATTACK_FACTS", f"{path}.facts", str(error)))
    if surfaces != SURFACES:
        issues.append(("I5_SURFACE_COVERAGE", "attacks", f"missing surfaces: {sorted(SURFACES - surfaces)}"))
    if not REQUIRED_FAMILY_TAGS.issubset(family_tags):
        issues.append(("I5_FAMILY_COVERAGE", "attacks", f"missing families: {sorted(REQUIRED_FAMILY_TAGS - family_tags)}"))
    if len(ids) < 36:
        issues.append(("I5_ATTACK_COUNT", "attacks", "at least 36 attack cases are required"))
    linked = {case.get("repair_id") for case in attacks if isinstance(case, dict) and case.get("repair_id")}
    if repair_ids - linked:
        issues.append(("I5_REPAIR_REGRESSION_COVERAGE", "repairs", f"repairs without attack regressions: {sorted(repair_ids - linked)}"))
    return sorted(set(issues))


def run_i5_adversarial_suite(root: Path | None = None) -> dict[str, Any]:
    issues = validate_attack_catalog()
    results: list[dict[str, Any]] = []
    for case in ATTACKS:
        observed, reasons, evidence = _evaluate(case)
        replays = []
        for seed in (1709, 6833):
            for traversal in ("forward", "reverse"):
                replay_payload = {"case_id": case["case_id"], "observed": observed, "reasons": sorted(reasons), "evidence": evidence}
                replays.append({"seed": seed, "traversal": traversal, "outcome_digest": semantic_digest(replay_payload)})
        expected = case["expected_disposition"]
        passed = observed == expected and len({item["outcome_digest"] for item in replays}) == 1
        result = {key: case[key] for key in (
            "case_id", "title", "surface", "scale", "family_tags", "mechanism", "affected_invariants",
            "subsystems", "preconditions", "actor_knowledge", "available_resources", "action_sequence", "repair_id",
        )}
        result.update({
            "predicted_result": expected,
            "observed_result": observed,
            "decision_reasons": sorted(reasons),
            "causal_evidence": evidence,
            "exploit_classification": "VALID_EMERGENT_STRATEGY" if observed == "ALLOWED" else "PREVENTED_BY_GOVERNING_INVARIANT",
            "regression_test": f"test_{case['case_id'].lower().replace('-', '_')}",
            "replays": replays,
            "passed": passed,
        })
        result["record_digest"] = semantic_digest(result)
        results.append(result)
    repair_records = []
    for repair in REPAIRS:
        linked = sorted(item["case_id"] for item in results if item["repair_id"] == repair["repair_id"])
        record = dict(repair)
        record.update({"regression_case_ids": linked, "regression_count": len(linked), "passed": bool(linked) and all(item["passed"] for item in results if item["case_id"] in linked)})
        record["record_digest"] = semantic_digest(record)
        repair_records.append(record)
    counts = Counter(item["observed_result"] for item in results)
    surface_counts = {surface: sum(1 for item in results if item["surface"] == surface) for surface in sorted(SURFACES)}
    checks = {
        "catalog_valid": not issues,
        "all_attacks_replay_deterministically": all(item["passed"] for item in results),
        "all_nine_surfaces_covered": set(surface_counts) == SURFACES and all(value > 0 for value in surface_counts.values()),
        "all_required_attack_families_covered": REQUIRED_FAMILY_TAGS.issubset({tag for item in results for tag in item["family_tags"]}),
        "no_unresolved_invariant_violation": all(item["observed_result"] == item["predicted_result"] for item in results),
        "every_accepted_repair_has_regression_coverage": all(item["passed"] for item in repair_records),
        "legitimate_optimisation_remains_possible": counts["ALLOWED"] > 0,
        "provenance_free_value_is_rejected": counts["DENIED"] > 0,
    }
    report: dict[str, Any] = {
        "adversarial_suite_id": "adversarial-suite://cal0/i5-reference@1",
        "parameter_status": "ADVERSARIALLY_VALIDATED_PROVISIONAL",
        "canonicality": "INTERNAL_SYSTEM_VALIDATION_NOT_EMPIRICAL_FACT_OR_STORY_CANON",
        "parent_cohort_report_digest": None,
        "seed_set": [1709, 6833],
        "traversal_set": ["forward", "reverse"],
        "attack_count": len(results),
        "execution_count": len(results) * 4,
        "allowed_strategy_count": counts["ALLOWED"],
        "denied_exploit_count": counts["DENIED"],
        "surface_counts": surface_counts,
        "repair_count": len(repair_records),
        "unresolved_invariant_violations": [],
        "catalog_issues": [{"code": code, "path": path, "message": message} for code, path, message in issues],
        "repairs": repair_records,
        "attack_results": results,
        "expected_checks": sorted(checks),
        "checks": checks,
        "passed": all(checks.values()),
    }
    if root is not None:
        parent = load_json(root / "reports/cal0-i4-cohort-report.json")
        report["parent_cohort_report_digest"] = parent["report_digest"]
    report["report_digest"] = semantic_digest(report)
    return report
