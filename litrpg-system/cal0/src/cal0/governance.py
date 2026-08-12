"""Deterministic provenance, transition, compatibility, and replay primitives."""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Callable, Iterable, Mapping, Sequence

from .canonical import semantic_digest
from .exact import D, ONE, ZERO, plain, sum_exact


def normalise_loadings(raw: Mapping[str, Decimal | str], signs: Mapping[str, int]) -> dict[str, Decimal]:
    if set(raw) != set(signs):
        raise ValueError("every loading requires one registered orientation sign")
    values = {key: D(value) for key, value in raw.items()}
    energy = sum_exact(value * value for value in values.values())
    if energy <= ZERO:
        raise ValueError("zero-energy loading block is invalid")
    root = energy.sqrt()
    result: dict[str, Decimal] = {}
    for key in sorted(values):
        sign = signs[key]
        if sign not in {-1, 1}:
            raise ValueError("registered orientation signs must be -1 or +1")
        result[key] = ZERO if values[key] == ZERO else Decimal(sign) * abs(values[key]) / root
    return result


def loading_energy(loadings: Iterable[Decimal]) -> Decimal:
    return sum_exact(value * value for value in loadings)


def matmul(left: Sequence[Sequence[Decimal]], right: Sequence[Sequence[Decimal]]) -> list[list[Decimal]]:
    if not left or not right or len(left[0]) != len(right):
        raise ValueError("matrix shapes do not compose")
    columns = list(zip(*right))
    return [[sum_exact(a * b for a, b in zip(row, column)) for column in columns] for row in left]


def transpose(matrix: Sequence[Sequence[Decimal]]) -> list[list[Decimal]]:
    return [list(column) for column in zip(*matrix)]


def covariance_from_loadings(loadings: Sequence[Sequence[Decimal]], residual: Sequence[Sequence[Decimal]]) -> list[list[Decimal]]:
    product = matmul(loadings, transpose(loadings))
    if len(product) != len(residual) or any(len(row) != len(product) for row in residual):
        raise ValueError("residual covariance shape mismatch")
    return [[product[i][j] + residual[i][j] for j in range(len(product))] for i in range(len(product))]


def is_psd(matrix: Sequence[Sequence[Decimal]], tolerance: Decimal = Decimal("0.000000000001")) -> bool:
    size = len(matrix)
    if size == 0 or any(len(row) != size for row in matrix):
        return False
    if any(abs(matrix[i][j] - matrix[j][i]) > tolerance for i in range(size) for j in range(size)):
        return False
    lower = [[ZERO for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(i + 1):
            subtotal = sum_exact(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                diagonal = matrix[i][i] - subtotal
                if diagonal < -tolerance:
                    return False
                lower[i][j] = max(ZERO, diagonal).sqrt()
            elif lower[j][j] == ZERO:
                if abs(matrix[i][j] - subtotal) > tolerance:
                    return False
                lower[i][j] = ZERO
            else:
                lower[i][j] = (matrix[i][j] - subtotal) / lower[j][j]
    return True


def normalise_covariance(covariance: Sequence[Sequence[Decimal]]) -> list[list[Decimal]]:
    diagonal = [covariance[index][index] for index in range(len(covariance))]
    if any(value <= ZERO for value in diagonal):
        raise ValueError("covariance diagonal must be positive")
    return [
        [covariance[i][j] / (diagonal[i] * diagonal[j]).sqrt() for j in range(len(covariance))]
        for i in range(len(covariance))
    ]


def stage_compose(
    state: Mapping[str, Decimal | str],
    stages: Sequence[tuple[str, Callable[[dict[str, Decimal]], dict[str, Decimal]]]],
) -> tuple[dict[str, Decimal], list[dict[str, Any]]]:
    current = {key: D(value) for key, value in state.items()}
    trace: list[dict[str, Any]] = []
    for stage_id, transform in stages:
        before = {key: plain(value) for key, value in sorted(current.items())}
        candidate = transform(dict(current))
        if any(not value.is_finite() for value in candidate.values()):
            raise ValueError("stage produced non-finite state")
        current = candidate
        trace.append({"stage": stage_id, "before": before, "after": {key: plain(value) for key, value in sorted(current.items())}})
    return current, trace


def dependency_closed_subsets(
    proposals: Iterable[str],
    dependencies: Mapping[str, Iterable[str]],
    conflicts: Iterable[tuple[str, str]],
    present: Iterable[str] = (),
) -> list[frozenset[str]]:
    nodes = sorted(set(proposals))
    present_set = set(present)
    conflict_set = {frozenset(pair) for pair in conflicts}
    valid: list[frozenset[str]] = []
    for count in range(len(nodes) + 1):
        for values in itertools.combinations(nodes, count):
            candidate = frozenset(values)
            if any(not set(dependencies.get(node, ())).issubset(candidate | present_set) for node in candidate):
                continue
            if any(pair.issubset(candidate) for pair in conflict_set):
                continue
            valid.append(candidate)
    maximal = [candidate for candidate in valid if not any(candidate < other for other in valid)]
    return sorted(maximal, key=lambda item: tuple(sorted(item)))


def atomic_commit(
    pre_state: Iterable[str],
    selected: Iterable[str],
    validation_passed: bool,
) -> tuple[frozenset[str], str]:
    frozen = frozenset(pre_state)
    candidate = frozen | frozenset(selected)
    if not validation_passed:
        return frozen, "ABORTED"
    return candidate, "COMMITTED"


def lexicographic_select(candidates: Mapping[str, Sequence[Any]]) -> str:
    if not candidates:
        raise ValueError("at least one candidate is required")
    width = {len(value) for value in candidates.values()}
    if len(width) != 1:
        raise ValueError("typed objective tuples must have equal width")
    best_value = max(candidates.values())
    finalists = sorted(key for key, value in candidates.items() if value == best_value)
    return finalists[0]


def pareto_frontier(candidates: Mapping[str, Sequence[Decimal]]) -> frozenset[str]:
    def dominates(left: Sequence[Decimal], right: Sequence[Decimal]) -> bool:
        return all(a >= b for a, b in zip(left, right)) and any(a > b for a, b in zip(left, right))

    return frozenset(
        candidate
        for candidate, values in candidates.items()
        if not any(other != candidate and dominates(other_values, values) for other, other_values in candidates.items())
    )


def elimination_cascade(
    frontier: Iterable[str],
    predicates: Sequence[Callable[[frozenset[str]], frozenset[str] | None]],
) -> tuple[frozenset[str], tuple[str, ...]]:
    current = frozenset(frontier)
    trace: list[str] = []
    for predicate in predicates:
        proposed = predicate(current)
        if proposed is None:
            trace.append("inapplicable")
        elif not proposed or not proposed.issubset(current):
            trace.append("invalid")
        elif proposed == current:
            trace.append("no_distinction")
        else:
            current = proposed
            trace.append("narrowed")
        if len(current) == 1:
            break
    return current, tuple(trace)


def version_node_identity(parents: Iterable[str], scope: str, delta: Mapping[str, Any]) -> str:
    return semantic_digest({"parents": sorted(set(parents)), "scope": scope, "delta": delta})


def ancestors(node: str, parents: Mapping[str, Iterable[str]]) -> frozenset[str]:
    result: set[str] = set()
    stack = list(parents.get(node, ()))
    while stack:
        current = stack.pop()
        if current in result:
            continue
        result.add(current)
        stack.extend(parents.get(current, ()))
    return frozenset(result)


def maximal_common_ancestors(nodes: Iterable[str], parents: Mapping[str, Iterable[str]]) -> frozenset[str]:
    selected = tuple(nodes)
    if not selected:
        return frozenset()
    common = set(ancestors(selected[0], parents) | {selected[0]})
    for node in selected[1:]:
        common &= set(ancestors(node, parents) | {node})
    return frozenset(
        candidate
        for candidate in common
        if not any(candidate != other and candidate in ancestors(other, parents) for other in common)
    )


STRENGTH = {"unsupported": 0, "low": 1, "moderate": 2, "high": 3}


def weakest_strength(values: Iterable[str]) -> str:
    materialised = list(values)
    if not materialised:
        return "unsupported"
    return min(materialised, key=lambda value: STRENGTH[value])


def proof_identity(premises: Iterable[Mapping[str, Any]], rule: str, scope: str, dimension: str) -> str:
    canonical = sorted((dict(premise) for premise in premises), key=semantic_digest)
    return semantic_digest({"premises": canonical, "rule": rule, "scope": scope, "dimension": dimension})


def affected_closure(changed: Iterable[str], dependants: Mapping[str, Iterable[str]]) -> frozenset[str]:
    result = set(changed)
    stack = list(changed)
    while stack:
        current = stack.pop()
        for dependant in dependants.get(current, ()):
            if dependant not in result:
                result.add(dependant)
                stack.append(dependant)
    return frozenset(result)


def attenuation_path(edges: Iterable[Decimal | str], variances: Iterable[Decimal | str]) -> tuple[Decimal, Decimal]:
    attenuation = ONE
    for edge in edges:
        attenuation *= D(edge)
    transfer_variance = sum_exact(D(value) for value in variances)
    return attenuation, transfer_variance


def deduplicate_events(paths: Iterable[Iterable[str]]) -> frozenset[str]:
    return frozenset(itertools.chain.from_iterable(paths))


def conservative_variance(weights: Sequence[Decimal], sigmas: Sequence[Decimal], correlations: Sequence[Sequence[Decimal]], structural: Decimal = ZERO) -> Decimal:
    if not (len(weights) == len(sigmas) == len(correlations)):
        raise ValueError("variance inputs have incompatible shapes")
    total = structural * structural
    for i in range(len(weights)):
        for j in range(len(weights)):
            total += weights[i] * sigmas[i] * correlations[i][j] * sigmas[j] * weights[j]
    return total


def relation(left: frozenset[str], right: frozenset[str]) -> str:
    if left == right:
        return "equal"
    if left.isdisjoint(right):
        return "disjoint"
    if left <= right:
        return "subset"
    if right <= left:
        return "superset"
    return "overlap"


@dataclass(frozen=True)
class Guard:
    facet: str
    scope: frozenset[str] | None
    mode: str
    derivation: tuple[str, ...] = ()


def guards_conflict(left: Guard, right: Guard, aliases: Mapping[str, str]) -> tuple[bool, str]:
    left_root = aliases.get(left.facet, left.facet)
    right_root = aliases.get(right.facet, right.facet)
    if left_root != right_root:
        return False, "different_facet"
    if left.scope is None or right.scope is None:
        scope_relation = "unknown"
    else:
        scope_relation = relation(left.scope, right.scope)
    if scope_relation == "disjoint":
        return False, "proved_disjoint_scope"
    if left.mode == right.mode == "read":
        return False, "read_read"
    return True, f"{left_root}:{scope_relation}:{left.mode}/{right.mode}"


def compile_guard_closure(
    guards: Iterable[Guard],
    aliases: Mapping[str, str],
    obligations: Mapping[str, Iterable[tuple[str, frozenset[str] | None, str]]],
) -> tuple[Guard, ...]:
    expanded: list[Guard] = []
    for guard in guards:
        root = aliases.get(guard.facet, guard.facet)
        expanded.append(Guard(root, guard.scope, guard.mode, guard.derivation + (guard.facet,)))
        for facet, scope, mode in obligations.get(guard.facet, ()):
            expanded.append(Guard(aliases.get(facet, facet), scope, mode, guard.derivation + (guard.facet, facet)))
    return tuple(sorted(set(expanded), key=lambda item: (item.facet, sorted(item.scope) if item.scope else [], item.mode, item.derivation)))


def compose_certificates(certificates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if not certificates:
        raise ValueError("certificate composition requires premises")
    scopes = [frozenset(item["scope"]) for item in certificates]
    scope = frozenset.intersection(*scopes)
    restrictions = sorted(set(itertools.chain.from_iterable(item.get("restrictions", ()) for item in certificates)))
    queries = sorted(set(itertools.chain.from_iterable(item.get("queries", ()) for item in certificates)))
    recovery: set[str] = set()
    for item in certificates:
        recovery.update(item.get("recovery", ()))
        recovery.update(item.get("sources", ()))
    strength = weakest_strength(item.get("strength", "unsupported") for item in certificates)
    record = {
        "premises": sorted(item["id"] for item in certificates),
        "scope": sorted(scope),
        "strength": strength,
        "restrictions": restrictions,
        "queries": queries,
        "recovery": sorted(recovery),
    }
    record["id"] = semantic_digest(record)
    return record


def decision_episode(parent: str | None, frontier: Iterable[str], selected: str, cutoff: str, mandate: str, scope: Iterable[str]) -> dict[str, Any]:
    candidates = sorted(set(frontier))
    if selected not in candidates:
        raise ValueError("selected repair is not on the frontier")
    record = {
        "parent": parent,
        "frontier": candidates,
        "selected": selected,
        "cutoff": cutoff,
        "mandate": mandate,
        "scope": sorted(set(scope)),
    }
    record["id"] = semantic_digest(record)
    return record


def admit_appeal(request: Mapping[str, Any], source_scope: frozenset[str]) -> tuple[bool, str]:
    if not request.get("authorised"):
        return False, "standing"
    if not request.get("provenance"):
        return False, "provenance"
    if not request.get("material"):
        return False, "materiality"
    scope = frozenset(request.get("scope", ()))
    if not scope or scope.isdisjoint(source_scope):
        return False, "scope"
    if request.get("ground") not in {"evidence_correction", "process_defect", "jurisdiction"}:
        return False, "ground"
    return True, "admitted"


def checkpoint_admission(reference_cost: Decimal | str, candidate_cost: Decimal | str, benefit_floor: Decimal | str, non_loss: bool) -> tuple[bool, Decimal]:
    baseline, candidate = D(reference_cost), D(candidate_cost)
    if baseline <= ZERO or candidate < ZERO:
        raise ValueError("checkpoint costs are invalid")
    benefit = (baseline - candidate) / baseline
    return non_loss and benefit >= D(benefit_floor), benefit
