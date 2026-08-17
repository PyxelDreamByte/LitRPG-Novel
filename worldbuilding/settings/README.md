# Setting Isolation

The `setting://shared-universe-001` container is the first setting development
frontier. Its identity and reciprocal relationship with
`work://series/project-hearthway-main` are `ACCEPTED` / `PROVISIONAL`, and it
contains eighteen bounded provisional setting records. No fictional setting record
is fully accepted. Each additional setting follows the same isolated structure:

```text
worldbuilding/settings/<setting-slug>/
├── <setting-slug>.setting-manifest.json
├── setting-constitution.md
├── canon/
├── proposals/
├── decisions/
└── indexes/
```

Start from `worldbuilding/templates/setting-manifest.template.json`, copy it as
`<setting-slug>.setting-manifest.json`, and use
`worldbuilding/templates/setting-constitution.md` for the Author-facing scope.
The exact `*.setting-manifest.json` suffix is required for discovery. A setting
container must represent a real Author-selected development frontier, not merely
reserve a name. Display titles may remain temporary while the stable setting ID
preserves continuity.

The machine manifest follows the single contract at
`litrpg-system/story-integration/schemas/setting-manifest.schema.json` and must
declare:

- stable `setting://` ID, title, and root without a trailing slash;
- workflow and canon status; and
- the setting-local index path and all adopting work IDs.

The setting constitution records the setting boundary and Author-facing
decision surfaces. Each adopting work must resolve back to this manifest with
the same `shared_setting_id`; each shared-world work must also appear in
`adopting_work_ids`. Each work manifest independently declares its shared world
references and default guardrails. A project default binds only when the work
manifest explicitly adopts its decision URI, adopted scope, and effective
decision ID (for example, `WLD-SOUL-001A`); an empty adoption list means none
are adopted. `ACCEPTED` or `PROVISIONAL` setting authority additionally
requires `accepted_on` and an indexed `approval_decision_uri`.
