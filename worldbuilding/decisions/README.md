# Project-Level Worldbuilding Decisions

This directory currently holds reusable project defaults and project-level
deferrals. They are not Enuma canon and do not establish any real setting.

A decision governs only its declared scope. Future setting-specific decisions
belong under `../settings/<setting-slug>/decisions/`.

| Decision | Disposition | Boundary |
|---|---|---|
| [`WLD-SOUL-001A`](WLD-SOUL-001A.md) | `PROVISIONAL` default | Exact-decimal `0.001` rare-Soul prevalence for a future named human-reference population after explicit work-manifest adoption; typed and non-scalar; not Mage prevalence |
| [`WLD-PRENATAL-001A`](WLD-PRENATAL-001A.md) | `PROVISIONAL` default | Ordinary persistent self-aware continuity and directed prenatal System practice excluded from population modelling after explicit adoption; sensation and automatic development neither denied nor quantified |
| [`WLD-RARITY-001D`](WLD-RARITY-001D.md) | `DEFERRED` | No proportions until object type, rarity dimension, eligible denominator, population, period, and evidence are defined |

Each Markdown review surface has a sibling `.decision.json` record validated by
`governance/schemas/decision-record.schema.json`.
