# Characters

This directory provides character conventions and templates. Ordinary character records live beneath their owning work root, separating durable definition from story-changing state without contaminating other works.

- `profiles/` — accepted identity, history, values, capabilities, and voice constraints.
- `relationships/` — typed relationship edges and their provenance.
- `arcs/` — intended development, pressures, turning points, and protected destinations.
- `knowledge/` — what a character knows, believes, suspects, misunderstands, or cannot access.
- `state/` — generated or event-derived current snapshots.
- `templates/` — authoring templates.

CAL0 reference characters are fixtures and do not belong here unless the Author separately creates a story character inspired by one, with a new identity and explicit decisions.

Use `character://<work-type>/<work-slug>/<character-slug>` and
`snapshot://<work-type>/<work-slug>/<character-slug>/<unit>/<chapter>` as primary IDs.
Retain `CHR-###` values only as `display_code` labels.

Every record also names `work://<work-type>/<work-slug>`. Similar names in different works never imply shared identity. Cross-work characters require an explicit approved contract.

## State rule

Profiles describe durable canon. Accepted chapter deltas describe change. Current snapshots are derived from those sources and must be reproducible. An outline may describe intended future development but never current truth.
