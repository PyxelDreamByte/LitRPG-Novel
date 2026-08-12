"""Typed CAL0-I3 provisional-parameter validation and bounded rehearsal sampling."""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path
from typing import Any, Iterable, Mapping

from .exact import D, ONE, PRECISION, ZERO, plain


IssueTuple = tuple[str, str, str]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(
            handle,
            parse_float=lambda value: (_ for _ in ()).throw(
                ValueError(f"binary/JSON floating-point token forbidden: {value}")
            ),
        )


def _issue(code: str, path: str, message: str) -> IssueTuple:
    return code, path, message


def _decimal(value: Any) -> Decimal | None:
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        return None
    try:
        return D(value)
    except (InvalidOperation, TypeError, ValueError):
        return None


def _bound_ok(value: Decimal, domain: Mapping[str, Any]) -> bool:
    minimum = _decimal(domain.get("minimum")) if "minimum" in domain else None
    maximum = _decimal(domain.get("maximum")) if "maximum" in domain else None
    if minimum is not None:
        if domain.get("minimum_inclusive", True) and value < minimum:
            return False
        if not domain.get("minimum_inclusive", True) and value <= minimum:
            return False
    if maximum is not None:
        if domain.get("maximum_inclusive", True) and value > maximum:
            return False
        if not domain.get("maximum_inclusive", True) and value >= maximum:
            return False
    return True


def _validate_value(definition: Mapping[str, Any], value: Any, path: str) -> list[IssueTuple]:
    issues: list[IssueTuple] = []
    value_type = definition.get("value_type")
    domain = definition.get("domain", {})
    if value_type == "bounded_integer":
        if not isinstance(value, int) or isinstance(value, bool):
            return [_issue("I3_VALUE_TYPE", path, "bounded integer value required")]
        if not _bound_ok(D(value), domain):
            issues.append(_issue("I3_VALUE_OUT_OF_DOMAIN", path, "integer value lies outside its domain"))
        return issues
    if value_type == "exact_decimal":
        parsed = _decimal(value)
        if parsed is None:
            return [_issue("I3_VALUE_TYPE", path, "exact-decimal string required")]
        if not _bound_ok(parsed, domain):
            issues.append(_issue("I3_VALUE_OUT_OF_DOMAIN", path, "decimal value lies outside its domain"))
        return issues
    if value_type == "exact_decimal_sequence":
        if not isinstance(value, list):
            return [_issue("I3_VALUE_TYPE", path, "exact-decimal sequence required")]
        expected_length = domain.get("length")
        if isinstance(expected_length, int) and len(value) != expected_length:
            issues.append(_issue("I3_VALUE_SHAPE", path, "sequence length does not match its definition"))
        parsed = [_decimal(item) for item in value]
        if any(item is None for item in parsed):
            issues.append(_issue("I3_VALUE_TYPE", path, "sequence contains a non-decimal value"))
            return issues
        numbers = [item for item in parsed if item is not None]
        if any(not _bound_ok(item, domain) for item in numbers):
            issues.append(_issue("I3_VALUE_OUT_OF_DOMAIN", path, "sequence contains a value outside its domain"))
        if domain.get("strictly_increasing") and any(right <= left for left, right in zip(numbers, numbers[1:])):
            issues.append(_issue("I3_SEQUENCE_ORDER", path, "sequence must be strictly increasing"))
        if domain.get("nondecreasing") and any(right < left for left, right in zip(numbers, numbers[1:])):
            issues.append(_issue("I3_SEQUENCE_ORDER", path, "sequence must be nondecreasing"))
        return issues
    if value_type == "exact_decimal_map":
        if not isinstance(value, dict):
            return [_issue("I3_VALUE_TYPE", path, "exact-decimal map required")]
        expected = set(domain.get("keys", []))
        if expected and set(value) != expected:
            issues.append(_issue("I3_VALUE_SHAPE", path, "map keys do not match its definition"))
        parsed = {key: _decimal(item) for key, item in value.items()}
        if any(item is None for item in parsed.values()):
            issues.append(_issue("I3_VALUE_TYPE", path, "map contains a non-decimal value"))
            return issues
        numbers = [item for item in parsed.values() if item is not None]
        if any(not _bound_ok(item, domain) for item in numbers):
            issues.append(_issue("I3_VALUE_OUT_OF_DOMAIN", path, "map contains a value outside its domain"))
        required_sum = _decimal(domain.get("sum")) if "sum" in domain else None
        if required_sum is not None and sum(numbers, ZERO) != required_sum:
            issues.append(_issue("I3_VALUE_NORMALISATION", path, "map values do not sum to the required total"))
        return issues
    if value_type == "distribution":
        issues.append(_issue("I3_VALUE_STATE", path, "distribution-valued definition must remain unresolved at I3"))
        return issues
    issues.append(_issue("I3_VALUE_TYPE", path, f"unknown value type: {value_type}"))
    return issues


def _is_psd(matrix: list[list[Decimal]]) -> bool:
    """Deterministic Decimal Cholesky admission for symmetric PSD matrices."""

    count = len(matrix)
    lower = [[ZERO for _ in range(count)] for _ in range(count)]
    with localcontext() as ctx:
        ctx.prec = PRECISION
        for row in range(count):
            for column in range(row + 1):
                subtotal = sum((lower[row][k] * lower[column][k] for k in range(column)), ZERO)
                if row == column:
                    pivot = matrix[row][row] - subtotal
                    if pivot < ZERO:
                        return False
                    lower[row][column] = pivot.sqrt() if pivot > ZERO else ZERO
                else:
                    numerator = matrix[row][column] - subtotal
                    if lower[column][column] == ZERO:
                        if numerator != ZERO:
                            return False
                        lower[row][column] = ZERO
                    else:
                        lower[row][column] = numerator / lower[column][column]
    return True


def validate_parameter_registry(document: Any) -> list[IssueTuple]:
    if not isinstance(document, dict):
        return [_issue("I3_REGISTRY_TYPE", "i3_parameters", "parameter registry must be an object")]
    issues: list[IssueTuple] = []
    definitions = document.get("definitions", [])
    bindings = document.get("bindings", [])
    distributions = document.get("distributions", [])
    blocks = document.get("dependence_blocks", [])
    if document.get("calibration_status") != "PROVISIONAL_UNCALIBRATED":
        issues.append(_issue("I3_PARAMETER_STATUS", "i3_parameters.calibration_status", "I3 parameters must remain provisional and uncalibrated"))

    definition_by_id: dict[str, Mapping[str, Any]] = {}
    for index, definition in enumerate(definitions if isinstance(definitions, list) else []):
        path = f"i3_parameters.definitions[{index}]"
        parameter_id = definition.get("parameter_id") if isinstance(definition, dict) else None
        if not isinstance(parameter_id, str) or not parameter_id.startswith("parameter://cal0/"):
            issues.append(_issue("I3_PARAMETER_ID", f"{path}.parameter_id", "invalid parameter identity"))
            continue
        if parameter_id in definition_by_id:
            issues.append(_issue("I3_PARAMETER_DUPLICATE", f"{path}.parameter_id", "duplicate parameter identity"))
        definition_by_id[parameter_id] = definition
        for field in ("meaning", "owner", "classification", "value_type", "units", "domain", "boundary_behaviour", "precision", "provenance", "version"):
            if field not in definition:
                issues.append(_issue("I3_PARAMETER_FIELD", f"{path}.{field}", "required parameter-definition field missing"))

    binding_by_parameter: dict[str, Mapping[str, Any]] = {}
    binding_ids: set[str] = set()
    distribution_ids = {entry.get("distribution_id") for entry in distributions if isinstance(entry, dict)}
    for index, binding in enumerate(bindings if isinstance(bindings, list) else []):
        path = f"i3_parameters.bindings[{index}]"
        if not isinstance(binding, dict):
            issues.append(_issue("I3_BINDING_TYPE", path, "binding must be an object"))
            continue
        binding_id = binding.get("binding_id")
        parameter_id = binding.get("parameter_id")
        state = binding.get("state")
        if not isinstance(binding_id, str) or binding_id in binding_ids:
            issues.append(_issue("I3_BINDING_ID", f"{path}.binding_id", "binding identity must be unique"))
        else:
            binding_ids.add(binding_id)
        if parameter_id not in definition_by_id:
            issues.append(_issue("I3_BINDING_UNKNOWN_PARAMETER", f"{path}.parameter_id", "binding references an unknown parameter"))
            continue
        if parameter_id in binding_by_parameter:
            issues.append(_issue("I3_BINDING_DUPLICATE", f"{path}.parameter_id", "parameter has more than one binding"))
        binding_by_parameter[parameter_id] = binding
        if state in {"LOCKED", "PROVISIONAL", "SCENARIO"}:
            if "value" not in binding:
                issues.append(_issue("I3_BINDING_VALUE_MISSING", f"{path}.value", "concrete binding requires a value"))
            else:
                issues.extend(_validate_value(definition_by_id[parameter_id], binding["value"], f"{path}.value"))
            if state == "PROVISIONAL" and not isinstance(binding.get("uncertainty"), dict):
                issues.append(_issue("I3_UNCERTAINTY_MISSING", f"{path}.uncertainty", "provisional value requires uncertainty metadata"))
            if state == "SCENARIO" and not str(binding.get("canonicality", "")).startswith("REFERENCE_ONLY"):
                issues.append(_issue("I3_SCENARIO_CANONICALITY", f"{path}.canonicality", "scenario value must be explicitly reference-only"))
        elif state == "DISTRIBUTED":
            if binding.get("distribution_id") not in distribution_ids:
                issues.append(_issue("I3_DISTRIBUTION_UNKNOWN", f"{path}.distribution_id", "distributed binding references an unknown distribution"))
            if "value" in binding:
                issues.append(_issue("I3_VALUE_STATE_CONFLICT", f"{path}.value", "distributed binding cannot conceal a fixed value"))
        elif state == "UNRESOLVED":
            unresolved = binding.get("unresolved")
            if not isinstance(unresolved, dict) or unresolved.get("state") != "UNRESOLVED":
                issues.append(_issue("I3_UNRESOLVED_INVALID", f"{path}.unresolved", "valid unresolved marker required"))
            elif "value" in unresolved or "value" in binding:
                issues.append(_issue("I3_VALUE_STATE_CONFLICT", path, "unresolved binding cannot contain a value"))
            elif unresolved.get("required_stage") not in {"CAL0-I4", "CAL0-I5", "CAL0-I6", "CAL0-I7"}:
                issues.append(_issue("I3_UNRESOLVED_STAGE", f"{path}.unresolved.required_stage", "I3 exit requires a later explicit resolution stage"))
        else:
            issues.append(_issue("I3_BINDING_STATE", f"{path}.state", "unknown binding state"))

    missing = sorted(set(definition_by_id) - set(binding_by_parameter))
    extra = sorted(set(binding_by_parameter) - set(definition_by_id))
    if missing or extra:
        issues.append(_issue("I3_BINDING_CLOSURE", "i3_parameters.bindings", f"missing={missing}; extra={extra}"))

    distribution_by_id: dict[str, Mapping[str, Any]] = {}
    for index, distribution in enumerate(distributions if isinstance(distributions, list) else []):
        path = f"i3_parameters.distributions[{index}]"
        if not isinstance(distribution, dict):
            issues.append(_issue("I3_DISTRIBUTION_TYPE", path, "distribution must be an object"))
            continue
        distribution_id = distribution.get("distribution_id")
        if not isinstance(distribution_id, str) or distribution_id in distribution_by_id:
            issues.append(_issue("I3_DISTRIBUTION_ID", f"{path}.distribution_id", "distribution identity must be unique"))
            continue
        distribution_by_id[distribution_id] = distribution
        if distribution.get("family") != "bounded_triangular" or distribution.get("truncation") != "hard":
            issues.append(_issue("I3_DISTRIBUTION_BOUNDS", path, "I3 rehearsal distributions must use hard-bounded triangular families"))
        parameters = distribution.get("parameters", {})
        support = distribution.get("support", {})
        low, mode, high = (_decimal(parameters.get(key)) for key in ("minimum", "mode", "maximum"))
        support_low, support_high = (_decimal(support.get(key)) for key in ("minimum", "maximum"))
        if None in {low, mode, high, support_low, support_high} or not (low <= mode <= high):
            issues.append(_issue("I3_DISTRIBUTION_BOUNDS", path, "distribution requires finite minimum <= mode <= maximum"))
        elif low != support_low or high != support_high or support.get("closed") is not True:
            issues.append(_issue("I3_DISTRIBUTION_SUPPORT", path, "support must exactly match closed triangular bounds"))
        target = distribution.get("target_parameter_id")
        if target not in definition_by_id:
            issues.append(_issue("I3_DISTRIBUTION_TARGET", f"{path}.target_parameter_id", "unknown distribution target"))
        if not isinstance(distribution.get("seed_namespace"), str) or not distribution.get("seed_namespace"):
            issues.append(_issue("I3_DISTRIBUTION_SEED", f"{path}.seed_namespace", "reproducible seed namespace required"))
        if not isinstance(distribution.get("uncertainty"), dict):
            issues.append(_issue("I3_UNCERTAINTY_MISSING", f"{path}.uncertainty", "distribution uncertainty required"))

    block_ids: set[str] = set()
    for index, block in enumerate(blocks if isinstance(blocks, list) else []):
        path = f"i3_parameters.dependence_blocks[{index}]"
        if not isinstance(block, dict):
            issues.append(_issue("I3_DEPENDENCE_TYPE", path, "dependence block must be an object"))
            continue
        block_id = block.get("dependence_id")
        if not isinstance(block_id, str) or block_id in block_ids:
            issues.append(_issue("I3_DEPENDENCE_ID", f"{path}.dependence_id", "dependence identity must be unique"))
        else:
            block_ids.add(block_id)
        members = block.get("members", [])
        matrix_raw = block.get("correlation_matrix", [])
        if not isinstance(members, list) or not isinstance(matrix_raw, list) or len(matrix_raw) != len(members):
            issues.append(_issue("I3_DEPENDENCE_SHAPE", path, "matrix shape must match member count"))
            continue
        matrix: list[list[Decimal]] = []
        malformed = False
        for row in matrix_raw:
            if not isinstance(row, list) or len(row) != len(members):
                malformed = True
                break
            parsed_row = [_decimal(value) for value in row]
            if any(value is None for value in parsed_row):
                malformed = True
                break
            matrix.append([value for value in parsed_row if value is not None])
        if malformed:
            issues.append(_issue("I3_DEPENDENCE_SHAPE", path, "matrix must be a complete exact-decimal square"))
            continue
        if any(matrix[i][i] != ONE for i in range(len(matrix))) or any(matrix[i][j] != matrix[j][i] for i in range(len(matrix)) for j in range(len(matrix))):
            issues.append(_issue("I3_DEPENDENCE_SYMMETRY", path, "correlation matrix must be symmetric with unit diagonal"))
        elif not _is_psd(matrix):
            issues.append(_issue("I3_DEPENDENCE_NOT_PSD", path, "correlation matrix is not positive semidefinite"))

    for index, distribution in enumerate(distributions if isinstance(distributions, list) else []):
        if isinstance(distribution, dict) and distribution.get("dependence") not in block_ids:
            issues.append(_issue("I3_DEPENDENCE_UNKNOWN", f"i3_parameters.distributions[{index}].dependence", "distribution references an unknown dependence block"))

    def concrete(parameter_id: str) -> Decimal | None:
        binding = binding_by_parameter.get(parameter_id, {})
        return _decimal(binding.get("value"))

    order = [
        concrete("parameter://cal0/adaptation/maintenance@1"),
        concrete("parameter://cal0/adaptation/peak@1"),
        concrete("parameter://cal0/adaptation/excessive@1"),
        concrete("parameter://cal0/adaptation/stop@1"),
    ]
    if any(value is None for value in order) or not all(left < right for left, right in zip(order, order[1:])):
        issues.append(_issue("I3_HORMETIC_ORDER", "i3_parameters.bindings", "maintenance < peak < excessive < stop is required"))

    parameter_sets = document.get("parameter_sets", [])
    if len(parameter_sets) != 1 or parameter_sets[0].get("parameter_set_id") != "parameter-set://cal0/i3-reference@1":
        issues.append(_issue("I3_PARAMETER_SET", "i3_parameters.parameter_sets", "exactly one active I3 reference parameter set is required"))
    else:
        parameter_set = parameter_sets[0]
        if parameter_set.get("bindings") != "ALL_REGISTRY_BINDINGS":
            issues.append(_issue("I3_PARAMETER_SET_CLOSURE", "i3_parameters.parameter_sets[0].bindings", "I3 reference set must close over all registry bindings"))
        unresolved_count = sum(1 for binding in bindings if isinstance(binding, dict) and binding.get("state") == "UNRESOLVED")
        if parameter_set.get("unresolved_count") != unresolved_count:
            issues.append(_issue("I3_UNRESOLVED_COUNT", "i3_parameters.parameter_sets[0].unresolved_count", "declared unresolved count does not match bindings"))
    return sorted(set(issues))


def binding_map(document: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {binding["parameter_id"]: binding for binding in document["bindings"]}


def value_map(document: Mapping[str, Any]) -> dict[str, Any]:
    return {
        parameter_id: binding["value"]
        for parameter_id, binding in binding_map(document).items()
        if binding.get("state") in {"LOCKED", "PROVISIONAL", "SCENARIO"}
    }


def deterministic_u01(seed: str, namespace: str) -> Decimal:
    digest = hashlib.sha256(f"{namespace}\x1f{seed}".encode("utf-8")).digest()
    numerator = int.from_bytes(digest, "big")
    denominator = (1 << (8 * len(digest))) - 1
    with localcontext() as ctx:
        ctx.prec = PRECISION
        return Decimal(numerator) / Decimal(denominator)


def bounded_triangular_sample(distribution: Mapping[str, Any], seed: str) -> Decimal:
    parameters = distribution["parameters"]
    low, mode, high = (D(parameters[key]) for key in ("minimum", "mode", "maximum"))
    if not low <= mode <= high or low == high:
        raise ValueError("invalid bounded triangular distribution")
    u = deterministic_u01(seed, distribution["seed_namespace"])
    split = (mode - low) / (high - low)
    with localcontext() as ctx:
        ctx.prec = PRECISION
        if u <= split:
            return low + (u * (high - low) * (mode - low)).sqrt()
        return high - ((ONE - u) * (high - low) * (high - mode)).sqrt()


def rehearsal_samples(document: Mapping[str, Any], seeds: Iterable[str]) -> dict[str, dict[str, str]]:
    distributions = sorted(document["distributions"], key=lambda item: item["distribution_id"])
    return {
        str(seed): {
            distribution["target_parameter_id"]: plain(bounded_triangular_sample(distribution, str(seed)), 12)
            for distribution in distributions
        }
        for seed in seeds
    }
