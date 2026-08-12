"""CAL0-I6 story-facing projections, reference sheets, and scenario validation."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping

from .canonical import semantic_digest
from .engines import attribute_index
from .exact import D, plain
from .parameter_runtime import load_json


VIEW_KINDS = (
    "private_backend",
    "author_facing",
    "character_accessible",
    "appraisal_derived",
    "institutional_record",
    "reader_facing",
)

PROTAGONIST_MILESTONES = (
    "earliest_coherent_prenatal_contact",
    "first_accepted_skill",
    "late_gestation",
    "birth",
    "ordinary_awakening_age",
    "first_mage_acceptance",
    "first_mage_form_completion",
    "advanced_not_overwhelming",
)

COMPARISON_ROLES = (
    "ordinary_civilian",
    "trained_professional",
    "institutional_mage",
    "soldier",
    "creature",
    "exceptional_non_protagonist",
)

REQUIRED_SCENARIO_FAMILIES = (
    "natural_growth_without_xp",
    "prenatal_skill_progression",
    "resistance_training",
    "running_and_assault_course",
    "mathematics_and_puzzles",
    "meditation",
    "civilian_vocation",
    "institutional_inequality",
    "party_contribution_dispute",
    "dungeon_spawn_economy",
    "magical_research_and_invention",
    "craft_repair_appraisal_salvage",
    "injury_rehabilitation_resurrection",
    "powerful_individual_vs_institution",
    "nonmagical_knowledge_to_magic",
)

AUTHORING_TYPES = (
    "character", "skill", "class", "spell", "item", "dungeon", "institution",
    "progression_event", "notification", "scene",
)


def _attributes(physical: str, mental: str, soul: str) -> dict[str, dict[str, str]]:
    p, m, s = D(physical), D(mental), D(soul)
    capacities = {
        "Might": p * D("0.95"),
        "Finesse": p * D("0.85"),
        "Alacrity": p * D("0.90"),
        "Vitality": p * D("1.05"),
        "Perception": (p + m) * D("0.475"),
        "Cognition": m,
        "Focus": m * D("0.95"),
        "Will": m * D("0.80") + s * D("0.20"),
        "Depth": s * D("0.95"),
        "Coherence": s,
        "Resonance": s * D("1.05"),
    }
    return {
        name: {"reference_capacity": plain(value, 8), "absolute_index": plain(attribute_index(value), 4)}
        for name, value in capacities.items()
    }


def _skill(name: str, level: int, xp: str, state: str = "active", source: str = "earned") -> dict[str, Any]:
    return {"name": name, "level": level, "xp": xp, "state": state, "source": source, "reinforcement_claims_conserved": True}


def _class(name: str, level: int, xp: str, form: str = "first", state: str = "active") -> dict[str, Any]:
    return {"name": name, "level": level, "xp": xp, "form": form, "state": state, "prospective_since_acceptance": True, "parent_xp_transferred": False}


def _sheet(
    sheet_id: str,
    label: str,
    role: str,
    milestone: str,
    age: str,
    life_stage: str,
    physical: str,
    mental: str,
    soul: str,
    traits: Iterable[str],
    skills: Iterable[Mapping[str, Any]] = (),
    classes: Iterable[Mapping[str, Any]] = (),
    mana: str = "0",
    magic: Iterable[str] = (),
    institution: str | None = None,
    condition: str = "healthy",
    reader_summary: str = "",
    secret: str = "No undeclared secret.",
) -> dict[str, Any]:
    attrs = _attributes(physical, mental, soul)
    sheet = {
        "sheet_id": sheet_id,
        "canonicality": "I6_AUTHORING_REFERENCE_NOT_FIXED_STORY_CANON",
        "identity": {
            "label": label,
            "role": role,
            "milestone": milestone,
            "age": age,
            "life_stage": life_stage,
            "species": "human" if role != "creature" else "glimmerhart",
            "exclusive_identity_holder": True,
            "identity_lineage": f"identity-lineage://cal0/i6/{sheet_id.split('/')[-1]}",
        },
        "traits": list(traits),
        "attributes": attrs,
        "resources": {
            "health": {"state": condition, "projection": "typed integrity and viability; not a universal hit-point pool"},
            "stamina": {"state": "available", "projection": "task-conditioned operating headroom"},
            "mana": {"working_reserve": mana, "projection": "source-to-effect network; reserve is not generation"},
        },
        "progression": {"skills": [dict(item) for item in skills], "classes": [dict(item) for item in classes]},
        "magic": {"methods": list(magic), "independent": bool(magic) and mana != "0", "constraints": ["knowledge", "compatible Mana", "control", "recovery", "preparation", "countermeasures"]},
        "equipment": [],
        "social": {"institution": institution, "offices": [], "authority_scopes": []},
        "conditions": [] if condition == "healthy" else [{"cause": condition, "state": "active", "recovery_required": True}],
        "epistemic_access": {
            "self_exact_core": role != "creature" and life_stage not in {"early_prenatal", "mid_prenatal"},
            "self_exact_owned_progression": role != "creature",
            "appraisal_disclosure": ["identity.label", "identity.life_stage", "visible_conditions"],
            "institutional_disclosure": ["identity.label", "licensed_roles", "verified_progression"],
        },
        "causal_ledgers": {
            "natural_maturation": {"present": True, "separate_from_xp": True},
            "purposeful_training": {"present": bool(skills), "separate_from_adaptation": True},
            "organic_adaptation": {"present": bool(skills), "damage_grants_growth": False},
            "skill_xp": {"present": bool(skills), "prospective": True},
            "class_xp": {"present": bool(classes), "prospective": True},
            "reinforcement": {"claims_conserved": True},
            "assimilation": {"safe_governor": True, "backlog_preserved": True},
        },
        "backend_uncertainty": ["scenario timing", "local opportunity", "plot-specific opposition"],
        "unresolved_inputs": ["rare-Soul prevalence", "ordinary prenatal consciousness", "cross-species scale", "injury incidence", "rarity distribution"],
        "secrets": [secret],
        "author_notes": {
            "reader_summary": reader_summary,
            "power_is_not_totalled": True,
            "causal_vulnerabilities_remain": ["surprise", "incomplete information", "commitment", "recovery", "environment", "institutions", "dependants"],
        },
    }
    sheet["sheet_digest"] = semantic_digest(sheet)
    return sheet


REFERENCE_SHEETS: tuple[dict[str, Any], ...] = (
    _sheet("sheet://cal0/i6/protagonist-contact@1", "Protagonist", "protagonist", "earliest_coherent_prenatal_contact", "gestational-week-20", "early_prenatal", "0.05", "0.075", "0.10", ["Reincarnate Continuity", "Unusual Soul Strength (non-scalar)"], reader_summary="A flicker of coherent awareness survives between long silences."),
    _sheet("sheet://cal0/i6/protagonist-first-skill@1", "Protagonist", "protagonist", "first_accepted_skill", "gestational-week-24", "mid_prenatal", "0.10", "0.14", "0.18", ["Reincarnate Continuity", "Embodied Integration", "Unusual Soul Strength (non-scalar)"], [_skill("Embodied Integration", 1, "0.216")], reader_summary="Intent, sensation, and movement become one fragile repeatable practice."),
    _sheet("sheet://cal0/i6/protagonist-late-gestation@1", "Protagonist", "protagonist", "late_gestation", "gestational-week-37", "late_prenatal", "0.45", "0.52", "0.58", ["Reincarnate Continuity", "Embodied Integration", "Soul Consolidation (candidate evidence)"], [_skill("Embodied Integration", 2, "1.84"), _skill("Directed Attention", 1, "0.72")], reader_summary="He can practise in brief windows, but growth and recovery still belong to the body around him."),
    _sheet("sheet://cal0/i6/protagonist-birth@1", "Protagonist", "protagonist", "birth", "newborn", "newborn", "0.6409375", "0.66984375", "0.685625", ["Reincarnate Continuity", "Embodied Integration", "Unusual Soul Strength (non-scalar)"], [_skill("Embodied Integration", 2, "2.46"), _skill("Directed Attention", 1, "1.10")], reader_summary="Exceptional continuity does not make a newborn physically independent."),
    _sheet("sheet://cal0/i6/protagonist-awakening@1", "Protagonist", "protagonist", "ordinary_awakening_age", "10-years", "child", "0.82", "0.90", "0.95", ["Reincarnate Continuity", "Embodied Integration", "Soul Consolidation"], [_skill("Embodied Integration", 16, "19.20"), _skill("Directed Attention", 12, "13.40"), _skill("Soul Consolidation", 8, "8.90")], mana="0.08", reader_summary="Years of private practice make him strange and disciplined, not adult."),
    _sheet("sheet://cal0/i6/protagonist-mage-acceptance@1", "Protagonist", "protagonist", "first_mage_acceptance", "12.4-years", "adolescent", "0.95", "1.12", "1.25", ["Reincarnate Continuity", "Embodied Integration", "Soul Consolidation"], [_skill("Embodied Integration", 22, "27.60"), _skill("Mana Perception", 14, "16.90"), _skill("Arcane Method", 9, "10.20")], [_class("Mage", 1, "0")], mana="0.22", magic=["mana perception", "contained spark", "simple shaping"], reader_summary="The Mage offer recognises what he has begun to do; it does not retroactively pay for childhood."),
    _sheet("sheet://cal0/i6/protagonist-mage-completion@1", "Protagonist", "protagonist", "first_mage_form_completion", "30-years", "adult", "1.35", "2.80", "3.20", ["Reincarnate Continuity", "Embodied Integration", "Soul Consolidation", "Arcane Synthesis"], [_skill("Embodied Integration", 74, "82.10"), _skill("Mana Perception", 100, "106"), _skill("Arcane Method", 100, "106"), _skill("Magical Research", 88, "94.40")], [_class("Mage", 100, "205", "first", "complete")], mana="2.40", magic=["structured spell design", "wards", "ritual participation", "diagnostic magic"], institution="independent researcher with negotiated archive access", reader_summary="His first Mage form is complete, but breadth, preparation, politics, and recovery still decide what he can accomplish."),
    _sheet("sheet://cal0/i6/protagonist-advanced@1", "Protagonist", "protagonist", "advanced_not_overwhelming", "55-years", "mature_adult", "1.85", "5.50", "6.80", ["Reincarnate Continuity", "Embodied Integration", "Soul Consolidation", "Arcane Synthesis"], [_skill("Embodied Integration", 100, "106", "complete"), _skill("Mana Perception", 100, "106", "complete"), _skill("Arcane Method", 100, "106", "complete"), _skill("Magical Research", 100, "106", "complete"), _skill("Soul Consolidation", 76, "84.20")], [_class("Mage", 100, "205", "first", "complete"), _class("Synthetic Archmage", 47, "96.10", "successor")], mana="7.60", magic=["novel spell systems", "regional wards with infrastructure", "ritual leadership", "arcane medicine", "prepared counter-magic"], institution="independent school and research network", reader_summary="He is formidable through synthesis and preparation, yet cannot ignore logistics, surprise, hostile environments, simultaneous demands, or people he must protect."),

    _sheet("sheet://cal0/i6/ordinary-civilian@1", "Mara the Baker", "ordinary_civilian", "comparison", "35-years", "adult", "1.00", "1.05", "0.95", ["Experienced Artisan"], [_skill("Baking", 47, "50.8"), _skill("Household Accounting", 21, "23.1")], [_class("Baker", 28, "35.0")], institution="town bakers' fellowship", reader_summary="A capable civilian with economically valuable mastery and no generic combat package."),
    _sheet("sheet://cal0/i6/trained-professional@1", "Edrin the Field Surgeon", "trained_professional", "comparison", "32-years", "adult", "1.40", "1.55", "1.10", ["Institutionally Trained"], [_skill("Surgery", 63, "70.1"), _skill("Diagnosis", 58, "64.2"), _skill("Endurance", 31, "36.4")], [_class("Field Surgeon", 49, "61.7")], institution="royal medical college", reader_summary="Training, tools, and institutional support create real expertise without transferring it to every member."),
    _sheet("sheet://cal0/i6/institutional-mage@1", "Sister Aelwen", "institutional_mage", "comparison", "42-years", "adult", "1.20", "2.40", "2.60", ["Licensed Ritual Custodian"], [_skill("Mana Perception", 71, "78.3"), _skill("Ward Maintenance", 76, "83.7"), _skill("Ritual Coordination", 68, "74.2")], [_class("Temple Mage", 64, "92.5")], mana="2.10", magic=["ward maintenance", "ritual casting", "sanctuary diagnostics"], institution="island temple network", reader_summary="Her office supplies keys, archives, peers, and infrastructure; it is not the source of her personal Skills."),
    _sheet("sheet://cal0/i6/soldier@1", "Cadoc", "soldier", "comparison", "29-years", "adult", "1.65", "1.20", "0.95", ["Campaign Veteran"], [_skill("Spear", 61, "67.5"), _skill("Shield", 57, "62.1"), _skill("Marching", 52, "56.0")], [_class("Household Soldier", 52, "66.8")], institution="regional warband", reader_summary="A trained fighter whose readiness still depends on formation, equipment, condition, orders, and terrain."),
    _sheet("sheet://cal0/i6/glimmerhart@1", "Old Antler", "creature", "comparison", "9-years", "adult", "1.80", "0.55", "1.20", ["Mana-Sensitive Herbivore", "Seasonal Migrant"], [_skill("Forest Navigation", 39, "42.0"), _skill("Threat Sensing", 33, "35.1")], mana="0.18", magic=["ambient Mana sensing"], reader_summary="A mythological animal with a real life cycle, learned capabilities, and no universal monster level or corpse loot table."),
    _sheet("sheet://cal0/i6/exceptional-non-protagonist@1", "Master Iorwerth", "exceptional_non_protagonist", "comparison", "70-years", "older_adult", "2.00", "4.80", "4.50", ["Exceptional Natural Endowment", "Long Institutional Career"], [_skill("Arcane Method", 100, "106", "complete"), _skill("Battle Magic", 94, "101.3"), _skill("Magical Research", 88, "93.0")], [_class("War Mage", 100, "205", "first", "complete"), _class("Arcane Strategist", 22, "38.4", "successor")], mana="5.30", magic=["battle magic", "counter-magic", "fortification rituals", "strategic scrying"], institution="royal arcane command", reader_summary="An exceptional rival whose advantages arise from talent, survival, responsibility, archives, staff, and decades of work."),
)


def project_sheet(sheet: Mapping[str, Any], view_kind: str) -> dict[str, Any]:
    if view_kind not in VIEW_KINDS:
        raise ValueError(f"unknown sheet view: {view_kind}")
    if view_kind == "private_backend":
        result = dict(sheet)
    elif view_kind == "author_facing":
        result = {key: sheet[key] for key in ("sheet_id", "canonicality", "identity", "traits", "attributes", "resources", "progression", "magic", "equipment", "social", "conditions", "causal_ledgers", "backend_uncertainty", "unresolved_inputs", "author_notes")}
    elif view_kind == "character_accessible":
        result = {key: sheet[key] for key in ("sheet_id", "identity", "traits", "attributes", "resources", "progression", "magic", "equipment", "conditions")}
        result["access_basis"] = "self-access and owned progression only"
    elif view_kind == "appraisal_derived":
        result = {
            "sheet_id": sheet["sheet_id"],
            "identity": {key: sheet["identity"][key] for key in ("label", "life_stage", "species")},
            "visible_conditions": sheet["conditions"],
            "disclosed_traits": sheet["traits"][:1],
            "confidence": "moderate",
            "scope": sheet["epistemic_access"]["appraisal_disclosure"],
            "omissions_are_not_negative_facts": True,
        }
    elif view_kind == "institutional_record":
        result = {
            "sheet_id": sheet["sheet_id"],
            "identity": {key: sheet["identity"][key] for key in ("label", "role", "age", "species")},
            "institution": sheet["social"]["institution"],
            "verified_progression": {"skills": sheet["progression"]["skills"], "classes": sheet["progression"]["classes"]},
            "record_scope": sheet["epistemic_access"]["institutional_disclosure"],
            "record_is_not_omniscient": True,
        }
    else:
        result = {
            "sheet_id": sheet["sheet_id"],
            "name": sheet["identity"]["label"],
            "life_stage": sheet["identity"]["life_stage"],
            "summary": sheet["author_notes"]["reader_summary"],
            "visible_progression": [f"{item['name']} {item['level']}" for item in sheet["progression"]["skills"][:3]],
            "visible_conditions": [item["cause"] for item in sheet["conditions"]],
            "exact_backend_withheld": True,
        }
    result["view_kind"] = view_kind
    result["source_sheet_digest"] = sheet["sheet_digest"]
    result["view_digest"] = semantic_digest(result)
    return result


def _scenario(
    scenario_id: str,
    family: str,
    title: str,
    inputs: Mapping[str, Any],
    knowledge: Iterable[str],
    sequence: Iterable[str],
    changes: Mapping[str, Any],
    interface: Iterable[str],
    reader: str,
    checks: Iterable[str],
) -> dict[str, Any]:
    item = {
        "scenario_id": scenario_id,
        "family": family,
        "title": title,
        "canonicality": "I6_WORKED_REFERENCE_NOT_FIXED_PLOT",
        "parameter_set": "parameter-set://cal0/i4-reference@1",
        "inputs": dict(inputs),
        "actor_knowledge": list(knowledge),
        "causal_sequence": list(sequence),
        "state_changes": dict(changes),
        "interface_outputs": list(interface),
        "reader_facing_projection": reader,
        "expected_checks": list(checks),
    }
    item["scenario_digest"] = semantic_digest(item)
    return item


SCENARIOS: tuple[dict[str, Any], ...] = (
    _scenario("scenario://cal0/i6/natural-growth@1", "natural_growth_without_xp", "Fetal and childhood attributes rise through maturation", {"start_capacity": "0.01928119", "birth_capacity": "0.65381944", "child_capacity": "0.82", "formal_xp": "0"}, ["author knows developmental programme", "character has no ordinary fetal interface"], ["structures mature", "foundation becomes realised", "rated capacities rise", "no progression reward is issued"], {"natural_maturation": "positive", "skill_xp": "0", "class_xp": "0", "reinforcement": "0"}, ["Physical development increased", "No Skill notification"], "The child grows stronger because a body is forming and maturing, not because infancy awards levels.", ["maturation_positive", "xp_zero", "ledgers_separate"]),
    _scenario("scenario://cal0/i6/prenatal-skill@1", "prenatal_skill_progression", "Prenatal Skill acceptance, reinforcement, and partial assimilation", {"directed_load": "0.18", "conscious_fraction": "0.12", "skill_xp": "0.216", "reinforcement_claim": "0.0015", "assimilated": "0.000375", "backlog": "0.001125"}, ["protagonist can access self-only interface", "he does not know the backend formula"], ["repeat intent-sensation calibration", "System recognises coherent domain", "accept Embodied Integration", "earn prospective XP", "create absolute claim", "safe governor assimilates part"], {"natural_maturation": "unchanged route", "skill_xp": "0.216", "reinforcement": "0.0015", "assimilation": "0.000375", "backlog": "0.001125"}, ["Embodied Integration accepted", "Reinforcement partially assimilated", "Recovery demand elevated"], "A tiny success matters because it is coherent and repeatable; most of the fetus's growth still comes from gestation.", ["claim_conserved", "partial_assimilation", "no_retroactive_xp"]),
    _scenario("scenario://cal0/i6/resistance@1", "resistance_training", "Press-ups create adaptation and Skill evidence", {"sessions": 24, "challenge": "0.65", "supported_adaptation": "0.018", "skill_xp": "0.52"}, ["trainee knows technique and recovery plan"], ["load chest, arms, trunk", "recover", "remodel loaded structures", "record movement-quality evidence"], {"purposeful_training": "15.60 load-units", "organic_adaptation": "0.018", "skill_xp": "0.52", "class_xp": "0"}, ["Condition: fatigued", "Calisthenics evidence increased"], "Repeated press-ups improve the structures actually loaded; renaming each set would not multiply the gain.", ["adaptation_supported", "skill_and_attribute_separate", "no_label_duplication"]),
    _scenario("scenario://cal0/i6/assault-course@1", "running_and_assault_course", "Running and an assault course create a different portfolio", {"sessions": 16, "endurance_load": "0.58", "coordination_load": "0.72", "adaptation": "0.021"}, ["coach sees gait and obstacle errors"], ["sustain running", "climb and vault", "receive feedback", "recover"], {"Might": "0.003", "Alacrity": "0.006", "Vitality": "0.008", "Finesse": "0.004", "organic_adaptation": "0.021"}, ["Movement portfolio improved", "Fatigue elevated"], "The runner gains endurance, timing, balance, and obstacle method rather than the same portfolio as a lifter.", ["portfolio_distinct", "recovery_required", "headroom_respected"]),
    _scenario("scenario://cal0/i6/mathematics@1", "mathematics_and_puzzles", "Mathematics separates knowledge, Skill, Cognition, and Focus", {"novel_problems": 40, "repeated_solved_problems": 60, "study_hours": "32"}, ["student knows the taught methods", "teacher supplies corrective feedback"], ["learn representation", "solve novel problems", "receive correction", "consolidate knowledge"], {"knowledge_units": "12", "Mathematics_skill_xp": "0.90", "Cognition_adaptation": "0.006", "Focus_adaptation": "0.008", "repeated_problem_extra_gain": "0"}, ["Mathematics evidence increased", "Focus strained"], "Knowing a theorem, practising mathematical method, and developing reliable mental capacity are related but not interchangeable.", ["knowledge_separate", "skill_xp_separate", "repetition_deduplicated"]),
    _scenario("scenario://cal0/i6/meditation@1", "meditation", "Meditation separates attention, regulation, and Soul contact", {"sessions": 30, "minutes": 20, "verified_soul_contact_events": 3}, ["practitioner can distinguish breath, attention, emotion, and anomalous contact imperfectly"], ["stabilise attention", "observe emotion", "recover", "test suspected Soul contact"], {"Focus_adaptation": "0.007", "Will_adaptation": "0.003", "attention_skill_xp": "0.64", "soul_contact_evidence": "3", "unsupported_spiritual_power": "0"}, ["Attention steadier", "Possible Soul contact: low confidence"], "Calm attention becomes more reliable; three unusual contacts justify investigation, not a universal spiritual-power bonus.", ["attention_and_soul_separate", "unsupported_claim_zero", "evidence_confidence_present"]),
    _scenario("scenario://cal0/i6/civilian@1", "civilian_vocation", "Civilian vocational mastery without generic combat", {"years": 14, "baking_level": 47, "class_level": 28}, ["baker knows recipes, ovens, suppliers, and local demand"], ["work repeatedly with variation", "correct failures", "teach apprentices", "manage production"], {"Baking_skill": 47, "Baker_class": 28, "combat_readiness": "0.06"}, ["Baking 47", "Baker 28"], "Mara can run a bakery under pressure and teach others; she has not become a fighter merely by gaining levels.", ["vocation_capable", "combat_not_generic", "institutional_support_causal"]),
    _scenario("scenario://cal0/i6/institutional-inequality@1", "institutional_inequality", "Elite academy and under-resourced trainee diverge causally", {"same_endowment": True, "years": 6, "elite_support": "0.90", "low_support": "0.35"}, ["author knows nutrition, coaching, safety, peers, and archives differ"], ["assign equal initial aptitude", "vary support", "train", "record interruptions and recovery"], {"elite_skill_level": 54, "low_resource_skill_level": 31, "elite_injury_days": 12, "low_resource_injury_days": 49}, ["Progress differs; cause: support and interruption"], "The academy does not create talent from nothing; it converts resources and institutional capability into more reliable development.", ["same_endowment_retained", "support_causes_difference", "no_free_institutional_skill"]),
    _scenario("scenario://cal0/i6/party-dispute@1", "party_contribution_dispute", "Party contribution and reward dispute", {"event_id": "event:ogre-bridge", "contributions": {"fighter": "0.42", "healer": "0.25", "scout": "0.18", "porter": "0.15"}, "reward_units": "100"}, ["party observes only part of each contribution", "ledger has evidence with uncertainty"], ["fight and evacuate", "record causal contribution", "compare claims", "allocate scoped reward"], {"fighter_reward": "42", "healer_reward": "25", "scout_reward": "18", "porter_reward": "15", "personal_kill_claims": 1}, ["Contribution ledger contested", "Allocation recorded with evidence scope"], "The killing blow matters, but so do warning, treatment, supply, and evacuation; one event is not four personal solo victories.", ["contribution_sums_one", "reward_conserved", "event_not_duplicated"]),
    _scenario("scenario://cal0/i6/dungeon-economy@1", "dungeon_spawn_economy", "Dungeon spawning and treasure economy remain source-bounded", {"mana_input": "1000", "biomass_input": "500", "spawn_cost": "800", "treasure_input": "150", "maintenance": "500", "harvest": "700"}, ["controller knows measured flows, not hidden maximums"], ["collect inputs", "spawn organisms", "form treasure", "harvest", "allow recovery"], {"total_input": "1500", "total_committed": "1450", "residual": "50", "unwitnessed_restock": "0"}, ["Dungeon reserve low", "Spawn rate reduced"], "Industrial use is possible, but heavy harvest lowers later output unless real inputs and recovery restore the mechanism.", ["matter_conserved", "mana_conserved", "renewal_witnessed"]),
    _scenario("scenario://cal0/i6/magical-research@1", "magical_research_and_invention", "Research, spell construction, teaching, and derivative invention", {"experiments": 18, "successful_replications": 5, "teacher_scaffolding": True}, ["researcher knows anatomy and current spell grammar", "student receives method but not mastery"], ["form hypothesis", "build spell graph", "test", "replicate", "document", "teach", "student reconstructs derivative"], {"knowledge_claims": 7, "research_skill_xp": "2.40", "spell_identity": "derived-method", "student_skill_xp": "0.48", "teacher_xp_from_student_work": "0"}, ["New method validated: narrow scope", "Derivative method recorded"], "Teaching transmits representation and correction; the student still has to build a working method and the teacher does not own the student's progress.", ["knowledge_and_skill_separate", "replication_required", "derivative_provenance_preserved"]),
    _scenario("scenario://cal0/i6/craft-salvage@1", "craft_repair_appraisal_salvage", "Crafting, repair, appraisal, salvage, and ownership", {"item": "river-sword", "replaced_components": ["grip", "guard"], "salvaged_fragment": "old-guard"}, ["smith sees material and wear", "enchantment remains partly unidentified"], ["appraise facets", "repair grip", "replace guard", "test", "record salvage and owner consent"], {"item_identity": "preserved", "quality": "improved", "unknown_enchantment": "still unknown", "salvage_identity": "derived component", "ownership": "unchanged"}, ["Condition improved", "Enchantment: unresolved facet"], "Repair can restore function without revealing every secret, changing ownership, or cloning the sword's history onto a discarded guard.", ["identity_preserved_once", "unknown_not_erased", "ownership_separate"]),
    _scenario("scenario://cal0/i6/injury-return@1", "injury_rehabilitation_resurrection", "Injury, healing, rehabilitation, death, and return", {"injury": "severed_tendon", "death_minutes": 4, "return_mechanism": "exclusive-soul-reconstitution"}, ["healer knows anatomy and ritual limits", "identity evidence is incomplete until return"], ["stabilise", "repair", "rehabilitate", "death occurs in counterfactual branch", "verify exclusive identity", "reconstitute if feasible"], {"healing": "repair incomplete without rehabilitation", "skill_xp_preserved": True, "reinforcement_reclaimed": False, "continuing_identity_holders": 1}, ["Condition: recovering", "Return confirmed; no duplicate continuity"], "Magic can restore a life only through a supported path; it does not erase rehabilitation, create a spare original, or repay completed levels.", ["healing_staged", "identity_exclusive", "rewards_not_replayed"]),
    _scenario("scenario://cal0/i6/institution-vs-power@1", "powerful_individual_vs_institution", "Prepared institution opposes a powerful individual", {"individual_mana": "6.20", "ward_nodes": 24, "responders": 80, "preparation_days": 12}, ["institution has partial intelligence", "individual does not know every ward"], ["prepare layered wards", "disperse reserves", "deny information", "force repeated commitments", "rotate responders"], {"individual_first_breach": "successful", "second_layer": "holds", "individual_mana_remaining": "1.10", "institutional_losses": 7}, ["Ward layer one breached", "Countermeasure network adapting"], "The mage is terrifying and wins local exchanges, but preparation, information, distributed capacity, and recovery prevent one number from deciding the conflict.", ["individual_power_real", "institutional_capability_real", "no_total_power_score"]),
    _scenario("scenario://cal0/i6/knowledge-to-magic@1", "nonmagical_knowledge_to_magic", "Anatomy and mathematics become inputs to a new magical method", {"anatomy_knowledge": "advanced", "mathematical_model": "validated", "arcane_experiments": 27}, ["protagonist remembers concepts but must map them to local bodies, Mana, and spell grammar"], ["observe local anatomy", "test Earth-derived hypothesis", "build magical representation", "run failed experiments", "validate narrow repair method"], {"earth_knowledge_xp_transfer": "0", "local_research_skill_xp": "3.10", "arcane_method_skill_xp": "2.20", "new_spell": "Tendon Alignment Lattice", "failed_experiments": 19}, ["New spell validated: tendon alignment only", "Source knowledge recorded; mastery earned locally"], "Old knowledge shortens the path to a useful question; the magical answer is still invented, tested, and learned in this world.", ["no_retroactive_mage_xp", "local_validation_required", "new_method_provenance_complete"]),
)


AUTHORING_CHECKLISTS: tuple[dict[str, Any], ...] = tuple(
    {
        "artifact_type": artifact_type,
        "required_questions": [
            "What is causally true?",
            "What source records or observes it?",
            "Who can access and interpret it?",
            "What costs, dependencies, recovery, and failure remain?",
            "What provenance key prevents semantic duplication?",
            "What should the viewpoint and reader actually see?",
        ],
        "locked_checks": ["no universal total power", "no label-created capability", "no retrospective progression", "no duplicated identity or entitlement", "no unwitnessed resource or renewal", "no damage-derived free growth"],
        "type_specific_checks": {
            "character": ["species and life stage", "absolute attributes", "condition", "Skills/classes separately", "access and relationships"],
            "skill": ["coherent domain", "evidence", "acceptance", "XP", "attestation", "techniques", "reinforcement"],
            "class": ["role pattern", "prospective acceptance", "responsibility", "Class XP", "successor ancestry"],
            "spell": ["method graph", "Mana source", "control", "casting stages", "interruption", "residuals"],
            "item": ["components", "identity continuity", "quality", "condition", "ownership", "appraisal uncertainty"],
            "dungeon": ["site/controller", "inputs", "spawn mechanism", "recovery", "ecology", "claims"],
            "institution": ["people", "assets", "procedures", "authority scopes", "distributed capability", "turnover"],
            "progression_event": ["canonical event origin", "live requirements", "contribution", "entitlement", "assimilation"],
            "notification": ["source", "access", "confidence", "significance", "reader relevance"],
            "scene": ["truth", "record", "access", "interpretation", "presentation", "reader need"],
        }[artifact_type],
    }
    for artifact_type in AUTHORING_TYPES
)


NOTIFICATION_TEMPLATES: tuple[dict[str, Any], ...] = (
    {"notification_type": "skill_progress", "template": "{skill} increased. Improved: {facet}. Reinforcement: {assimilation_state}. Recovery demand: {recovery_state}.", "must_not_imply": ["full backend access", "instant assimilation"]},
    {"notification_type": "offer", "template": "New {lineage_type} offer: {name}. Basis: {evidence_summary}. Acceptance creates prospective progression.", "must_not_imply": ["retroactive XP", "random reroll"]},
    {"notification_type": "condition", "template": "Condition: {label}. Known cause: {cause_or_unknown}. Current risk: {risk_scope}. Recommended response: {response}.", "must_not_imply": ["perfect diagnosis", "fixed timer"]},
    {"notification_type": "appraisal", "template": "Appraisal result ({confidence}): {disclosed_facets}. Unresolved: {unknown_facets}.", "must_not_imply": ["omniscience", "authority", "ownership"]},
)


DECISION_RESOLUTION = {
    "registry_id": "decision-resolution://cal0/i6/authoring@1",
    "parent_unresolved_record_preserved": True,
    "resolutions": [
        {
            "parameter_id": "parameter://cal0/protagonist/long-term-soul-multiplier@1",
            "parent_state": "UNRESOLVED",
            "active_resolution": "NOT_APPLICABLE_NONSCALAR_PROFILE",
            "classification": "STORY_DECISION_RESOLVED_WITHOUT_NUMERICAL_COEFFICIENT",
            "rule": "No universal Soul multiplier exists. Reincarnate Continuity preserves identity; Embodied Integration and Soul Consolidation earn facet-specific development in Depth, Coherence, Resonance, boundary integrity, coupling, recovery, and safe assimilation.",
            "reference_sheet_values_are": "I6_AUTHORING_REFERENCE_NOT_FIXED_STORY_CANON",
            "architecture_reopened": False,
            "coefficient_changed": False,
        }
    ],
    "remaining_active_residuals": [
        {"name": "rare-Soul prevalence", "classification": "SETTING_CONTENT"},
        {"name": "ordinary prenatal consciousness", "classification": "SETTING_CONTENT"},
        {"name": "cross-species scale", "classification": "FUTURE_OPTIONAL_EXTENSION"},
        {"name": "injury incidence", "classification": "CALIBRATION_INPUT_NOT_EMPIRICAL_ESTIMATE"},
        {"name": "rarity distribution", "classification": "SETTING_AND_CALIBRATION_INPUT"},
    ],
}


CHANGE_CLASSIFICATIONS = (
    "PRESENTATION_CLARIFICATION",
    "PARAMETER_CHANGE",
    "IMPLEMENTATION_CORRECTION",
    "LOCAL_RULE_REPAIR",
    "SUBSYSTEM_REVISION",
    "ARCHITECTURE_REOPENING",
)


def _build_change_register(parent_i5: Mapping[str, Any]) -> dict[str, Any]:
    classification_map = {
        "CAL0-I5-R01": "LOCAL_RULE_REPAIR",
        "CAL0-I5-R02": "IMPLEMENTATION_CORRECTION",
        "CAL0-I5-R03": "PRESENTATION_CLARIFICATION",
        "CAL0-I5-R04": "LOCAL_RULE_REPAIR",
        "CAL0-I5-R05": "LOCAL_RULE_REPAIR",
    }
    entries = [
        {
            "entry_id": repair["repair_id"],
            "source_stage": "CAL0-I5",
            "title": repair["title"],
            "classification": classification_map[repair["repair_id"]],
            "status": "CLOSED_REGRESSION_PINNED",
            "finding": repair["failure_boundary"],
            "resolution": repair["repair"],
            "evidence": repair["regression_case_ids"],
            "source_record_digest": repair["record_digest"],
            "architecture_reopened": False,
        }
        for repair in parent_i5["repairs"]
    ]
    entries.append({
        "entry_id": "CAL0-I6-C01",
        "source_stage": "CAL0-I6",
        "title": "Replace the proposed protagonist Soul multiplier with a non-scalar profile",
        "classification": "PRESENTATION_CLARIFICATION",
        "status": "CLOSED_AUTHORING_PINNED",
        "finding": "A single multiplier would collapse distinct Soul facets and falsely imply one universal power coefficient.",
        "resolution": DECISION_RESOLUTION["resolutions"][0]["rule"],
        "evidence": [
            "registries/cal0-i6-decision-resolution.json",
            "characters/cal0-i6-reference-sheets.json",
            "guide/litrpg-system-story-guide.md",
        ],
        "source_record_digest": semantic_digest(DECISION_RESOLUTION["resolutions"][0]),
        "architecture_reopened": False,
    })
    register: dict[str, Any] = {
        "register_id": "change-register://cal0/i6-governance@1",
        "classification_order": list(CHANGE_CLASSIFICATIONS),
        "classification_rules": {
            "PRESENTATION_CLARIFICATION": "Meaning is preserved while its interface, explanation, or story-facing projection is made unambiguous.",
            "PARAMETER_CHANGE": "A numerical or categorical calibration value changes without changing its model family.",
            "IMPLEMENTATION_CORRECTION": "Executable behavior is brought back into agreement with an already-governing rule.",
            "LOCAL_RULE_REPAIR": "A bounded rule is added or narrowed to protect existing architecture and invariants.",
            "SUBSYSTEM_REVISION": "One subsystem contract changes and requires explicit downstream migration.",
            "ARCHITECTURE_REOPENING": "A protected cross-system invariant or model-family decision is reconsidered.",
        },
        "entry_count": len(entries),
        "open_entry_count": 0,
        "entries": entries,
        "open_entries": [],
        "new_changes_require": [
            "one controlled classification",
            "affected protected facets",
            "evidence and regression identity",
            "migration impact",
            "explicit architecture-reopening decision",
        ],
    }
    register["register_digest"] = semantic_digest(register)
    return register


def _validate_sheets(sheets: Iterable[Mapping[str, Any]]) -> list[str]:
    materialised = list(sheets)
    issues: list[str] = []
    ids = [item.get("sheet_id") for item in materialised]
    if len(ids) != len(set(ids)):
        issues.append("duplicate_sheet_id")
    milestones = {item["identity"]["milestone"] for item in materialised if item["identity"]["role"] == "protagonist"}
    if milestones != set(PROTAGONIST_MILESTONES):
        issues.append("protagonist_milestone_coverage")
    roles = {item["identity"]["role"] for item in materialised}
    if not set(COMPARISON_ROLES).issubset(roles):
        issues.append("comparison_role_coverage")
    for item in materialised:
        payload = dict(item)
        digest = payload.pop("sheet_digest", None)
        if digest != semantic_digest(payload):
            issues.append(f"sheet_digest:{item.get('sheet_id')}")
        if set(item.get("attributes", {})) != {"Might", "Finesse", "Alacrity", "Vitality", "Perception", "Cognition", "Focus", "Will", "Depth", "Coherence", "Resonance"}:
            issues.append(f"attribute_coverage:{item.get('sheet_id')}")
    return sorted(set(issues))


def _validate_scenarios(scenarios: Iterable[Mapping[str, Any]]) -> list[str]:
    materialised = list(scenarios)
    issues: list[str] = []
    families = [item.get("family") for item in materialised]
    if set(families) != set(REQUIRED_SCENARIO_FAMILIES) or len(families) != len(REQUIRED_SCENARIO_FAMILIES):
        issues.append("scenario_family_coverage")
    required = {"inputs", "actor_knowledge", "causal_sequence", "state_changes", "interface_outputs", "reader_facing_projection", "expected_checks"}
    for item in materialised:
        if not required.issubset(item):
            issues.append(f"scenario_shape:{item.get('scenario_id')}")
        payload = dict(item)
        digest = payload.pop("scenario_digest", None)
        if digest != semantic_digest(payload):
            issues.append(f"scenario_digest:{item.get('scenario_id')}")
    return sorted(set(issues))


def build_i6_artifacts(root: Path) -> dict[str, Any]:
    sheet_issues = _validate_sheets(REFERENCE_SHEETS)
    scenario_issues = _validate_scenarios(SCENARIOS)
    views = [project_sheet(sheet, kind) for sheet in REFERENCE_SHEETS for kind in VIEW_KINDS]
    forbidden = {"secrets", "backend_uncertainty", "unresolved_inputs", "causal_ledgers"}
    projection_leaks = [
        f"{view['sheet_id']}:{view['view_kind']}"
        for view in views
        if view["view_kind"] not in {"private_backend", "author_facing"} and forbidden.intersection(view)
    ]
    protagonist = [item for item in REFERENCE_SHEETS if item["identity"]["role"] == "protagonist"]
    chronological = [D(item["attributes"]["Vitality"]["reference_capacity"]) for item in protagonist[:4]]
    parent_i5 = load_json(root / "reports/cal0-i5-adversarial-report.json")
    change_register = _build_change_register(parent_i5)
    checks = {
        "fourteen_reference_sheets_present": len(REFERENCE_SHEETS) == 14,
        "protagonist_milestones_complete": not sheet_issues and len(protagonist) == 8,
        "comparison_roles_complete": set(COMPARISON_ROLES).issubset({item["identity"]["role"] for item in REFERENCE_SHEETS}),
        "six_views_per_sheet": len(views) == len(REFERENCE_SHEETS) * len(VIEW_KINDS),
        "projections_do_not_leak_private_backend": not projection_leaks,
        "prenatal_growth_is_monotone": chronological == sorted(chronological),
        "all_minimum_scenarios_present": not scenario_issues,
        "scenario_records_are_story_complete": all(item["expected_checks"] for item in SCENARIOS),
        "ten_authoring_templates_present": {item["artifact_type"] for item in AUTHORING_CHECKLISTS} == set(AUTHORING_TYPES),
        "notification_templates_preserve_epistemic_limits": all(item["must_not_imply"] for item in NOTIFICATION_TEMPLATES),
        "soul_multiplier_resolved_without_scalar": DECISION_RESOLUTION["resolutions"][0]["active_resolution"] == "NOT_APPLICABLE_NONSCALAR_PROFILE",
        "i5_repairs_represented_in_locked_checks": all(any(needle in " ".join(item["locked_checks"]) for item in AUTHORING_CHECKLISTS) for needle in ("duplicat", "resource", "identity", "growth")),
        "change_register_is_closed_and_classified": change_register["open_entry_count"] == 0 and all(item["classification"] in CHANGE_CLASSIFICATIONS for item in change_register["entries"]),
    }
    report: dict[str, Any] = {
        "authoring_suite_id": "authoring-suite://cal0/i6-reference@1",
        "parameter_status": "AUTHORING_VALIDATED_PROVISIONAL",
        "canonicality": "AUTHORING_REFERENCE_NOT_EMPIRICAL_FACT_OR_FIXED_PLOT",
        "parent_i5_report_digest": parent_i5["report_digest"],
        "sheet_count": len(REFERENCE_SHEETS),
        "protagonist_milestone_count": len(protagonist),
        "comparison_sheet_count": len(REFERENCE_SHEETS) - len(protagonist),
        "view_kind_count": len(VIEW_KINDS),
        "projection_count": len(views),
        "scenario_count": len(SCENARIOS),
        "authoring_template_count": len(AUTHORING_CHECKLISTS),
        "notification_template_count": len(NOTIFICATION_TEMPLATES),
        "change_entry_count": change_register["entry_count"],
        "active_residual_count": len(DECISION_RESOLUTION["remaining_active_residuals"]),
        "sheet_issues": sheet_issues,
        "scenario_issues": scenario_issues,
        "projection_leaks": projection_leaks,
        "expected_checks": sorted(checks),
        "checks": checks,
        "passed": all(checks.values()),
    }
    report["report_digest"] = semantic_digest(report)
    return {
        "reference_sheets": {"registry_id": "sheet-registry://cal0/i6-reference@1", "sheets": list(REFERENCE_SHEETS)},
        "projections": {"projection_registry_id": "projection-registry://cal0/i6-reference@1", "view_kinds": list(VIEW_KINDS), "views": views},
        "scenarios": {"scenario_suite_id": "scenario-suite://cal0/i6-story@1", "scenarios": list(SCENARIOS)},
        "authoring_checklists": {"checklist_registry_id": "checklist-registry://cal0/i6-authoring@1", "templates": list(AUTHORING_CHECKLISTS)},
        "notification_templates": {"notification_registry_id": "notification-registry://cal0/i6-authoring@1", "templates": list(NOTIFICATION_TEMPLATES)},
        "decision_resolution": DECISION_RESOLUTION,
        "change_register": change_register,
        "report": report,
    }
