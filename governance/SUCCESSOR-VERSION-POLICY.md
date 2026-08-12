# System Successor Version Policy

## Storage

Keep the imported v0.7.0 baseline at `litrpg-system/cal0/` unchanged. Store each
future candidate or accepted successor as an immutable sibling under:

```text
litrpg-system/successors/cal0-v<semantic-version>/
```

Each successor contains its own canonical specification, calibration annex,
source, schemas, registries, fixtures, reports, guides, tests, change register,
and content-pinning manifest. It must not depend on mutable artifacts inside a
different version.

## Lifecycle

1. Classify the request through `review-system-change`.
2. Create a candidate successor without editing any earlier baseline.
3. Record parent bundle, change class, affected invariants, migrations, and
   backward-compatibility boundary.
4. Rebuild and validate every affected artifact and regression surface.
5. Obtain explicit Author acceptance of both the successor and its activation.
6. Update `ACTIVE-SYSTEM-BASELINE.md` atomically with the accepting commit.
7. Regenerate routing indexes against the new active source and retain the old
   baseline for replay and historical story interpretation.

Candidate existence, passing partial tests, or a newer version number does not
make a successor authoritative. Stories remain pinned to the baseline recorded
in their contracts and progression provenance until an explicit migration is
accepted.

