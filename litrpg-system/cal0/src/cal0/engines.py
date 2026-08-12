"""Reference implementations for CAL0 maturation, adaptation, XP, and reinforcement.

The functions implement selected model topology with caller-supplied synthetic
parameters.  They deliberately contain no population or protagonist defaults.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from decimal import Decimal, localcontext
from typing import Iterable, Mapping, Sequence

from .canonical import semantic_digest
from .exact import D, ONE, PRECISION, TWO, ZERO, clamp, plain, positive, power, sum_exact, tanh


def _sign(value: Decimal) -> int:
    return 1 if value > ZERO else -1 if value < ZERO else 0


def _endpoint_slope(h0: Decimal, h1: Decimal, d0: Decimal, d1: Decimal) -> Decimal:
    slope = ((TWO * h0 + h1) * d0 - h0 * d1) / (h0 + h1)
    if _sign(slope) != _sign(d0):
        return ZERO
    if _sign(d0) != _sign(d1) and abs(slope) > abs(Decimal("3") * d0):
        return Decimal("3") * d0
    return slope


@dataclass(frozen=True)
class Pchip:
    """Shape-preserving piecewise cubic Hermite interpolation."""

    x: tuple[Decimal, ...]
    y: tuple[Decimal, ...]
    slopes: tuple[Decimal, ...]

    @classmethod
    def compile(cls, x: Sequence[Decimal | str], y: Sequence[Decimal | str]) -> "Pchip":
        xs = tuple(D(value) for value in x)
        ys = tuple(D(value) for value in y)
        if len(xs) != len(ys) or len(xs) < 2:
            raise ValueError("PCHIP requires equally sized x/y sequences with at least two anchors")
        if any(right <= left for left, right in zip(xs, xs[1:])):
            raise ValueError("PCHIP anchors must have strictly increasing coordinates")
        h = tuple(xs[index + 1] - xs[index] for index in range(len(xs) - 1))
        delta = tuple((ys[index + 1] - ys[index]) / h[index] for index in range(len(h)))
        if len(xs) == 2:
            slopes = (delta[0], delta[0])
        else:
            values: list[Decimal] = [_endpoint_slope(h[0], h[1], delta[0], delta[1])]
            for index in range(1, len(xs) - 1):
                left = delta[index - 1]
                right = delta[index]
                if left == ZERO or right == ZERO or _sign(left) != _sign(right):
                    values.append(ZERO)
                else:
                    w1 = TWO * h[index] + h[index - 1]
                    w2 = h[index] + TWO * h[index - 1]
                    values.append((w1 + w2) / (w1 / left + w2 / right))
            values.append(_endpoint_slope(h[-1], h[-2], delta[-1], delta[-2]))
            slopes = tuple(values)
        return cls(xs, ys, slopes)

    def evaluate(self, coordinate: Decimal | str, boundary: str = "error") -> Decimal:
        value = D(coordinate)
        if value < self.x[0]:
            if boundary == "clamp":
                return self.y[0]
            raise ValueError("coordinate precedes first PCHIP anchor")
        if value > self.x[-1]:
            if boundary == "clamp":
                return self.y[-1]
            raise ValueError("coordinate exceeds last PCHIP anchor")
        if value == self.x[-1]:
            return self.y[-1]
        index = next(i for i in range(len(self.x) - 1) if self.x[i] <= value <= self.x[i + 1])
        h = self.x[index + 1] - self.x[index]
        t = (value - self.x[index]) / h
        t2 = t * t
        t3 = t2 * t
        h00 = TWO * t3 - Decimal("3") * t2 + ONE
        h10 = t3 - TWO * t2 + t
        h01 = -TWO * t3 + Decimal("3") * t2
        h11 = t3 - t2
        return (
            h00 * self.y[index]
            + h10 * h * self.slopes[index]
            + h01 * self.y[index + 1]
            + h11 * h * self.slopes[index + 1]
        )


def project_coordinate(
    baseline: Decimal | str,
    offset: Decimal | str,
    minimum_offset: Decimal | str,
    maximum_offset: Decimal | str,
    domain: tuple[Decimal | str, Decimal | str] = ("0", "1"),
) -> Decimal:
    bounded_offset = clamp(D(offset), D(minimum_offset), D(maximum_offset))
    return clamp(D(baseline) + bounded_offset, D(domain[0]), D(domain[1]))


def timing_seed_offset(seed: Decimal | str, bound: Decimal | str) -> Decimal:
    return D(bound) * tanh(D(seed))


def realise_foundation_step(
    realised: Decimal | str,
    programme: Decimal | str,
    endowment: Decimal | str,
    support: Decimal | str,
    disruption: Decimal | str,
    rise_rate: Decimal | str,
    loss_rate: Decimal | str,
    dt: Decimal | str,
) -> tuple[Decimal, Decimal]:
    target = D(programme) * D(endowment) * D(support) - D(disruption)
    current = D(realised)
    derivative = D(rise_rate) * positive(target - current) - D(loss_rate) * positive(current - target)
    return target, current + D(dt) * derivative


def generalised_mean(
    values: Mapping[str, Decimal | str],
    weights: Mapping[str, Decimal | str],
    rho: Decimal | str,
) -> Decimal:
    if set(values) != set(weights) or not values:
        raise ValueError("values and weights must name the same non-empty component set")
    parsed_weights = {key: D(value) for key, value in weights.items()}
    if any(weight < ZERO for weight in parsed_weights.values()) or sum_exact(parsed_weights.values()) != ONE:
        raise ValueError("weights must be non-negative and sum exactly to one")
    parsed_values = {key: D(value) for key, value in values.items()}
    if any(value <= ZERO for value in parsed_values.values()):
        raise ValueError("reference generalised mean requires positive component values")
    exponent = D(rho)
    with localcontext() as ctx:
        ctx.prec = PRECISION
        if exponent == ZERO:
            return sum_exact(parsed_weights[key] * parsed_values[key].ln() for key in parsed_values).exp()
        powered = sum_exact(parsed_weights[key] * power(parsed_values[key], exponent) for key in parsed_values)
        return power(powered, ONE / exponent)


def maturation_capacity(
    values: Mapping[str, Decimal | str],
    weights: Mapping[str, Decimal | str],
    rho: Decimal | str,
    species_scale: Decimal | str = "1",
    structural_gate: Decimal | str = "1",
) -> Decimal:
    return D(species_scale) * clamp(D(structural_gate), ZERO, ONE) * generalised_mean(values, weights, rho)


def attribute_index(reference_capacity: Decimal | str) -> Decimal:
    ratio = D(reference_capacity)
    if ratio < ZERO:
        raise ValueError("reference capacity cannot be negative")
    with localcontext() as ctx:
        ctx.prec = PRECISION
        return Decimal("10") * (ONE + ratio).ln() / TWO.ln()


def reference_capacity(attribute_index_value: Decimal | str) -> Decimal:
    return power(TWO, D(attribute_index_value) / Decimal("10")) - ONE


@dataclass(frozen=True)
class DoseVector:
    absolute_demand: Decimal
    relative_challenge: Decimal
    exposure: Decimal
    technique: Decimal
    novelty: Decimal
    feedback: Decimal
    loaded_structures: Mapping[str, Decimal]

    @classmethod
    def synthetic(
        cls,
        absolute_demand: Decimal | str,
        relative_challenge: Decimal | str,
        exposure: Decimal | str,
        technique: Decimal | str,
        novelty: Decimal | str,
        feedback: Decimal | str,
        loaded_structures: Mapping[str, Decimal | str],
    ) -> "DoseVector":
        bounded = [D(technique), D(novelty), D(feedback)]
        if any(value < ZERO or value > ONE for value in bounded):
            raise ValueError("technique, novelty, and feedback must be inside [0,1]")
        loads = {key: D(value) for key, value in loaded_structures.items()}
        if any(value < ZERO for value in loads.values()):
            raise ValueError("loaded-structure weights cannot be negative")
        return cls(D(absolute_demand), D(relative_challenge), D(exposure), *bounded, loads)


def opportunity_kernel(dose: DoseVector) -> tuple[Decimal, dict[str, Decimal]]:
    total = (
        dose.exposure
        * dose.absolute_demand
        / (ONE + dose.absolute_demand)
        * min(dose.relative_challenge, Decimal("1.25"))
        * dose.technique
        * dose.novelty
        * dose.feedback
    )
    return total, {name: total * weight for name, weight in dose.loaded_structures.items()}


def smoothstep(value: Decimal) -> Decimal:
    bounded = clamp(value, ZERO, ONE)
    return Decimal("3") * bounded * bounded - TWO * bounded * bounded * bounded


def hormetic_outputs(
    challenge: Decimal | str,
    maintenance: Decimal | str,
    peak: Decimal | str,
    excessive: Decimal | str,
    stop: Decimal | str,
    harm_scale: Decimal | str,
    harm_exponent: Decimal | str,
) -> tuple[Decimal, Decimal, Decimal]:
    chi = D(challenge)
    low, top, risk, end = D(maintenance), D(peak), D(excessive), D(stop)
    if not (ZERO <= low < top < risk < end):
        raise ValueError("hormetic boundaries are not strictly ordered")
    if chi <= low or chi >= end:
        opportunity = ZERO
    elif chi <= top:
        opportunity = smoothstep((chi - low) / (top - low))
    else:
        opportunity = ONE - smoothstep((chi - top) / (end - top))
    fatigue = max(ZERO, chi)
    harm = D(harm_scale) * power(positive(chi - risk), D(harm_exponent))
    return opportunity, fatigue, harm


def asymmetric_beta_window(
    challenge: Decimal | str,
    maintenance: Decimal | str,
    stop: Decimal | str,
    mode: Decimal | str,
    concentration: Decimal | str,
) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    chi, lower, upper = D(challenge), D(maintenance), D(stop)
    m, kappa = D(mode), D(concentration)
    if not (lower < upper and ZERO < m < ONE and kappa > TWO):
        raise ValueError("invalid asymmetric-beta window")
    alpha = ONE + m * (kappa - TWO)
    beta = ONE + (ONE - m) * (kappa - TWO)
    peak = lower + m * (upper - lower)
    if chi <= lower or chi >= upper:
        return ZERO, alpha, beta, peak
    x = (chi - lower) / (upper - lower)
    with localcontext() as ctx:
        ctx.prec = PRECISION
        log_value = (alpha - ONE) * x.ln() + (beta - ONE) * (ONE - x).ln()
        log_peak = (alpha - ONE) * m.ln() + (beta - ONE) * (ONE - m).ln()
        return (log_value - log_peak).exp(), alpha, beta, peak


def headroom(realised: Decimal | str, envelope: Decimal | str, beta: Decimal | str = "1") -> Decimal:
    capacity = D(envelope)
    if capacity <= ZERO:
        raise ValueError("adaptation envelope must be positive")
    return power(positive(ONE - D(realised) / capacity), D(beta))


def detrained(realised: Decimal | str, loss_fraction: Decimal | str) -> Decimal:
    loss = clamp(D(loss_fraction), ZERO, ONE)
    return D(realised) * (ONE - loss)


def transition_commit(
    eligible: bool,
    attempted: bool,
    outcome: str,
    recovery_complete: bool,
    validations: Iterable[bool],
    pre_envelope: Decimal | str,
    post_envelope: Decimal | str,
    realised: Decimal | str,
) -> dict[str, str | bool]:
    committed = eligible and attempted and outcome == "successful" and recovery_complete and all(validations)
    return {
        "committed": committed,
        "envelope": plain(D(post_envelope) if committed else D(pre_envelope)),
        "realised": plain(D(realised)),
    }


def deterministic_attempt_seed(world_seed: str, entity_id: str, transition_id: str, attempt_id: str) -> str:
    payload = "\x1f".join((world_seed, entity_id, transition_id, attempt_id)).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def deterministic_transition_outcome(
    latent_state: Mapping[str, Decimal | str],
    seed: str,
    resolver_version: str,
) -> str:
    dimensions = {key: D(value) for key, value in latent_state.items()}
    if any(value < ZERO or value > ONE for value in dimensions.values()):
        raise ValueError("transition dimensions must be bounded in [0,1]")
    identity = semantic_digest({"latent": {key: plain(value) for key, value in dimensions.items()}, "seed": seed, "resolver": resolver_version})
    minimum = min(dimensions.values()) if dimensions else ZERO
    if minimum < Decimal("0.30"):
        return "failed"
    if dimensions.get("stability", ONE) < Decimal("0.50"):
        return "maladaptive"
    if minimum < Decimal("0.70"):
        return "partial"
    # Identity is retained in the calculation contract even though this
    # synthetic decision surface has no stochastic branch.
    if not identity.startswith("sha256:"):
        raise AssertionError("unreachable invalid identity")
    return "successful"


def constraint_first_transition(
    required: Iterable[str],
    present: Iterable[str],
    dimensions: Mapping[str, Decimal | str],
    minima: Mapping[str, Decimal | str],
    recovered: bool,
) -> dict[str, object]:
    missing = sorted(set(required) - set(present))
    if missing:
        return {"status": "rejected", "cause": "missing_structure", "missing": missing, "committed": False}
    parsed = {key: D(value) for key, value in dimensions.items()}
    failed = sorted(key for key, value in minima.items() if parsed.get(key, ZERO) < D(value))
    if failed:
        return {"status": "rejected", "cause": "non_compensable_minimum", "failed": failed, "committed": False}
    return {"status": "successful" if recovered else "provisional", "cause": None, "committed": recovered}


def xp_scale(base: Decimal | str, grade_multiplier: Decimal | str, grade: int) -> Decimal:
    if grade < 0:
        raise ValueError("grade cannot be negative")
    return D(base) * power(D(grade_multiplier), Decimal(grade))


def xp_threshold(total_scale: Decimal | str, threshold: int, count: int, exponent: Decimal | str) -> Decimal:
    if not (0 <= threshold <= count and count > 0):
        raise ValueError("threshold must lie inside the form")
    return D(total_scale) * power(Decimal(threshold) / Decimal(count), D(exponent))


def blocked_xp_credit(
    current: Decimal | str,
    next_threshold: Decimal | str,
    following_cost: Decimal | str,
    overhang_fraction: Decimal | str,
    taper_exponent: Decimal | str,
    raw_xp: Decimal | str,
    relevance: Decimal | str,
) -> tuple[Decimal, Decimal]:
    value, next_value, cost = D(current), D(next_threshold), D(following_cost)
    omega, exponent = D(overhang_fraction), D(taper_exponent)
    cap = next_value + omega * cost
    if omega == ZERO or value >= cap:
        return ZERO, cap
    z = clamp((value - next_value) / (omega * cost), ZERO, ONE)
    credit = min(D(raw_xp) * clamp(D(relevance), ZERO, ONE) * power(ONE - z, exponent), cap - value)
    return max(ZERO, credit), cap


@dataclass(frozen=True)
class ReinforcementClaim:
    claim_id: str
    source_lineage: str
    source_level: int
    total_budget: Decimal
    distribution: Mapping[str, Decimal]
    provenance: tuple[str, ...]

    @classmethod
    def create(
        cls,
        source_lineage: str,
        source_level: int,
        total_budget: Decimal | str,
        distribution: Mapping[str, Decimal | str],
        provenance: Iterable[str],
    ) -> "ReinforcementClaim":
        weights = {key: D(value) for key, value in distribution.items()}
        if sum_exact(weights.values()) != ONE or any(value < ZERO for value in weights.values()):
            raise ValueError("reinforcement distribution must be non-negative and sum to one")
        budget = D(total_budget)
        if budget < ZERO:
            raise ValueError("reinforcement budget cannot be negative")
        record = {
            "source_lineage": source_lineage,
            "source_level": source_level,
            "total_budget": plain(budget),
            "distribution": {key: plain(value) for key, value in sorted(weights.items())},
            "provenance": sorted(set(provenance)),
        }
        return cls(semantic_digest(record), source_lineage, source_level, budget, weights, tuple(record["provenance"]))

    def allocate(self) -> dict[str, Decimal]:
        return {attribute: self.total_budget * weight for attribute, weight in self.distribution.items()}


def assimilate_claim(
    claim: ReinforcementClaim,
    current: Mapping[str, Decimal | str],
    throughput_fraction: Decimal | str,
) -> dict[str, dict[str, Decimal]]:
    fraction = clamp(D(throughput_fraction), ZERO, ONE)
    allocation = claim.allocate()
    result: dict[str, dict[str, Decimal]] = {}
    for attribute in sorted(allocation):
        full = allocation[attribute]
        assimilated = full * fraction
        backlog = full - assimilated
        start = D(current[attribute])
        result[attribute] = {
            "start": start,
            "claim": full,
            "assimilated": assimilated,
            "backlog": backlog,
            "new_reference": start + assimilated,
            "new_index": attribute_index(start + assimilated),
        }
    return result


def claim_conservation(rows: Mapping[str, Mapping[str, Decimal]], total_budget: Decimal) -> bool:
    claims = sum_exact(row["claim"] for row in rows.values())
    assimilated = sum_exact(row["assimilated"] for row in rows.values())
    backlog = sum_exact(row["backlog"] for row in rows.values())
    return claims == total_budget and assimilated + backlog == total_budget


@dataclass(frozen=True)
class ResourceLedger:
    """Typed exact-decimal resource pool with explicit reservations and provenance."""

    resource_id: str
    capacity: Decimal
    available: Decimal
    reservations: Mapping[str, Decimal]
    consumed_total: Decimal
    events: tuple[Mapping[str, str], ...]

    @classmethod
    def create(cls, resource_id: str, capacity: Decimal | str, available: Decimal | str | None = None) -> "ResourceLedger":
        cap = D(capacity)
        current = cap if available is None else D(available)
        if cap < ZERO or current < ZERO or current > cap:
            raise ValueError("resource capacity and availability are inconsistent")
        return cls(resource_id, cap, current, {}, ZERO, ())

    def _successor(self, operation: str, available: Decimal, reservations: Mapping[str, Decimal], consumed: Decimal, provenance: str, amount: Decimal) -> "ResourceLedger":
        if available < ZERO or sum_exact(reservations.values()) + available > self.capacity:
            raise ValueError("resource conservation invariant failed")
        event = {
            "operation": operation,
            "amount": plain(amount),
            "provenance": provenance,
            "predecessor": self.identity,
        }
        return ResourceLedger(self.resource_id, self.capacity, available, dict(reservations), consumed, self.events + (event,))

    @property
    def identity(self) -> str:
        return semantic_digest({
            "resource_id": self.resource_id,
            "capacity": plain(self.capacity),
            "available": plain(self.available),
            "reservations": {key: plain(value) for key, value in sorted(self.reservations.items())},
            "consumed_total": plain(self.consumed_total),
            "events": list(self.events),
        })

    def reserve(self, reservation_id: str, amount: Decimal | str, provenance: str) -> "ResourceLedger":
        value = D(amount)
        if value < ZERO or value > self.available or reservation_id in self.reservations:
            raise ValueError("resource reservation is invalid")
        reservations = dict(self.reservations)
        reservations[reservation_id] = value
        return self._successor("reserve", self.available - value, reservations, self.consumed_total, provenance, value)

    def consume(self, reservation_id: str, amount: Decimal | str, provenance: str) -> "ResourceLedger":
        value = D(amount)
        reserved = self.reservations.get(reservation_id)
        if reserved is None or value < ZERO or value > reserved:
            raise ValueError("resource consumption exceeds its reservation")
        reservations = dict(self.reservations)
        remainder = reserved - value
        if remainder == ZERO:
            del reservations[reservation_id]
        else:
            reservations[reservation_id] = remainder
        return self._successor("consume", self.available, reservations, self.consumed_total + value, provenance, value)

    def release(self, reservation_id: str, provenance: str) -> "ResourceLedger":
        if reservation_id not in self.reservations:
            raise ValueError("unknown resource reservation")
        reservations = dict(self.reservations)
        value = reservations.pop(reservation_id)
        return self._successor("release", self.available + value, reservations, self.consumed_total, provenance, value)

    def recover(
        self,
        amount: Decimal | str,
        provenance: str,
        source_available: Decimal | str,
        source_witness: str,
    ) -> "ResourceLedger":
        value = D(amount)
        source = D(source_available)
        if value < ZERO or source < ZERO:
            raise ValueError("resource recovery and source availability cannot be negative")
        if not source_witness:
            raise ValueError("resource recovery requires a source witness")
        reservation_total = sum_exact(self.reservations.values())
        recovered = min(value, source, self.capacity - reservation_total - self.available)
        return self._successor("recover", self.available + recovered, self.reservations, self.consumed_total, f"{provenance}|{source_witness}", recovered)
