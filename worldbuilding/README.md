# Worldbuilding

This directory holds reusable project-level worldbuilding governance and, when
created, isolated settings. One live setting container exists: the
provisionally authorized Project Hearthway development container, with no
fully accepted fictional canon. A superseded parallel bootstrap (Continuity
One) is archived under `archive/settings/continuity-one/`; see
[`INDEX.md`](INDEX.md) for the supersession trail.

- [`INDEX.md`](INDEX.md) routes readers to accepted setting facts and open decisions.
- `decisions/` currently records project-level defaults and deferrals; these are not detailed world canon.
- `settings/<setting-slug>/` isolates each setting's manifest, constitution, canon, proposals, decisions, and indexes.
- [`settings/shared-universe-001/`](settings/shared-universe-001/) has narrow
  `ACCEPTED` / `PROVISIONAL` authority for the Project Hearthway identity, its
  main-series relationship, four bounded Lineage II records, one bounded basin
  exchange-and-regional-horizon record, one bounded lake spring breeding-pulse
  record, one bounded mass-breeder foundational body-plan record, one bounded
  mass-breeder osmoregulation-and-passive-buoyancy record, one bounded
  family-care migrant foundational body-plan and mobile-refuge record, one
  bounded family-care migrant outlet-passage choreography record, one bounded
  initial-region physical scaffold, one bounded initial-outlet mixed-reach
  sequence, three bounded basin-flora records, one bounded initial ridge-spur
  settlement working-landscape record, and one bounded lake-road practical
  travel-scale record, plus one bounded upper-shore staging-and-seasonal-spur
  endpoint record and one bounded imperial-collapse-arc-and-neighbor-frame
  history record; all
  other detailed fictional material remains proposed.
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

Within a setting, add folders only when sufficient accepted or provisional
material exists:

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
