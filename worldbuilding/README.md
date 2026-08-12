# Worldbuilding

This directory holds reusable project-level worldbuilding governance and, when
created, isolated settings. No real setting has been instantiated yet.

- [`INDEX.md`](INDEX.md) routes readers to accepted setting facts and open decisions.
- `decisions/` currently records project-level defaults and deferrals; these are not detailed world canon.
- `settings/<setting-slug>/` will isolate each real setting's manifest, constitution, canon, proposals, decisions, and indexes.
- Root `canon/`, `proposals/`, and `indexes/` are legacy/reserved and must not receive new setting-specific facts.
- `templates/` contains proposal and decision templates.

Worldbuilding created during chapter drafting remains proposed until it appears
in the chapter delta, passes consistency review, and is explicitly accepted by
the Author into the correct setting tree.

## Multi-setting rule

Every real setting uses `worldbuilding/settings/<setting-slug>/`. Its
discoverable `<setting-slug>.setting-manifest.json` declares the stable
`setting://` ID, authority status, root, and index. The setting constitution and
each linked work manifest declare their scopes, shared-setting relationship,
adopted project defaults, and work-specific Author decisions.

The project defaults `WLD-SOUL-001A` and `WLD-PRENATAL-001A` bind a future work
only when that work manifest explicitly adopts them. An independent work may
override either only through its own Author decision. No setting inherits
fictional facts or modelling assumptions merely because they exist elsewhere in
this repository.

## Recommended canon taxonomy

Within a future setting, add folders only when sufficient accepted material exists:

- cosmology and metaphysics;
- geography, geology, climate, and locations;
- chronology and history;
- peoples, cultures, languages, and religions;
- institutions, politics, law, and conflict;
- economy, technology, craft, and infrastructure;
- ecology, species, and life cycles;
- magic as experienced, taught, regulated, and interpreted;
- customs, calendars, measures, names, and material culture.

These are navigation categories, not separate universes of fact. Cross-link shared causes and consequences.
