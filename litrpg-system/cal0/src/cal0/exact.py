"""Exact-decimal helpers for CAL0 reference engines.

Canonical CAL0 records never contain binary floating-point values.  Runtime
transcendentals use a fixed Decimal context and are serialised back to plain
decimal strings before entering a replay record.
"""

from __future__ import annotations

from decimal import Decimal, localcontext
from typing import Iterable


PRECISION = 50
ZERO = Decimal("0")
ONE = Decimal("1")
TWO = Decimal("2")


def D(value: Decimal | int | str) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, float):
        raise TypeError("binary floating-point input is forbidden")
    return Decimal(str(value))


def clamp(value: Decimal, lower: Decimal, upper: Decimal) -> Decimal:
    if lower > upper:
        raise ValueError("lower bound exceeds upper bound")
    return min(upper, max(lower, value))


def positive(value: Decimal) -> Decimal:
    return max(ZERO, value)


def power(base: Decimal, exponent: Decimal) -> Decimal:
    if base < ZERO:
        raise ValueError("fractional exact-decimal power requires non-negative base")
    if base == ZERO:
        if exponent > ZERO:
            return ZERO
        raise ValueError("zero base requires a positive exponent")
    if exponent == exponent.to_integral_value():
        return base ** int(exponent)
    with localcontext() as ctx:
        ctx.prec = PRECISION
        return (exponent * base.ln()).exp()


def tanh(value: Decimal) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = PRECISION
        e2x = (TWO * value).exp()
        return (e2x - ONE) / (e2x + ONE)


def sum_exact(values: Iterable[Decimal]) -> Decimal:
    return sum(values, ZERO)


def plain(value: Decimal, places: int | None = None) -> str:
    if not value.is_finite():
        raise ValueError("non-finite decimals are forbidden")
    if places is not None:
        quantum = Decimal(1).scaleb(-places)
        value = value.quantize(quantum)
    rendered = format(value, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    if rendered in {"", "-0"}:
        return "0"
    return rendered


def close(left: Decimal, right: Decimal, tolerance: Decimal = Decimal("0.000000001")) -> bool:
    return abs(left - right) <= tolerance
