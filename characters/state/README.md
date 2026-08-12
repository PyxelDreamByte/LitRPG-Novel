# Character State

State snapshots are derived from accepted profiles and chapter deltas. They may include location, condition, resources, inventory, equipment, relationships, knowledge, commitments, System progression, and active constraints.

Each snapshot records the latest included chapter/event and its build provenance. If it conflicts with an accepted event or profile, rebuild it; do not patch the snapshot as if it were primary canon.

A snapshot uses `workflow_status: DERIVED`. Its `canon_status` describes the
status of the source state it projects and never gives the snapshot authority
over an accepted profile, manuscript, or delta.
