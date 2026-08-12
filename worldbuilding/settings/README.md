# Setting Isolation

No setting exists here yet. When the Author begins one, create:

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
The exact `*.setting-manifest.json` suffix is required for discovery. Do not
create a setting directory merely to reserve a name.

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

## Setting-first bootstrap

A real shared setting may begin before any story work exists. Before its
manifest exists, a bounded `SETTING_INIT` run may decide only the setting's
identity, slug, title, authority envelope, constitutional scope, and proposed
shell location/status. After explicit Author approval it creates the empty
`DRAFT`/`PROPOSED` shell and setting-local initiation decision, then stops.

During subsequent bounded setting-authority work, before or after works adopt the setting:

- the discoverable setting manifest and paired `setting-constitution.md` are
  the authoring boundary;
- `adopting_work_ids` remains reciprocal with every adopting work manifest;
- proposals, decisions, canon, and indexes stay beneath the declared
  `setting_root`;
- setting-local structured decisions declare the matching `setting_id`;
- no work manifest, story contract, protagonist, character, outline, or chapter
  is created to satisfy the workflow; and
- project defaults are never inherited silently. Work-level adoption requires a
  work manifest. Before a work exists, the Author may instead approve a
  setting-local rule with explicit provenance and scope.

After the setting becomes accepted or provisional authority, a separately
approved work may adopt it through reciprocal manifest references.
