"""Strict canonical JSON helpers used by CAL0 manifests and identities."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class CanonicalisationError(ValueError):
    """Raised when a value cannot be represented without semantic ambiguity."""


def _check(value: Any, path: str = "$") -> None:
    if value is None or isinstance(value, (bool, int, str)):
        return
    if isinstance(value, float):
        raise CanonicalisationError(
            f"{path}: binary floating-point values are forbidden; use an exact decimal string"
        )
    if isinstance(value, list):
        for index, item in enumerate(value):
            _check(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalisationError(f"{path}: map keys must be strings")
            _check(item, f"{path}.{key}")
        return
    raise CanonicalisationError(f"{path}: unsupported value type {type(value).__name__}")


def canonical_bytes(value: Any) -> bytes:
    """Return deterministic UTF-8 JSON after rejecting lossy numeric values."""

    _check(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def semantic_digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()
