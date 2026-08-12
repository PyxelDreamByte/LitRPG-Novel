# Standalone Novels

Each novel is an independent work root containing:

```text
<novel-slug>/
├── work-manifest.md
├── <novel-slug>.work-manifest.json
├── work-contract.md
├── standalone-novel-contract.md
├── characters/
├── world-overlay/
├── workbench/{context-packs,runs}/
└── units/main/
    ├── outline/chapter-cards/
    ├── manuscript/chapters/
    ├── state/{deltas,snapshots}/
    ├── continuity/
    └── editorial/
```

Use unit token `main` and unit path `units/main`. Use the matching templates in `../templates/`. A standalone novel may share an explicitly named setting, use only a work-local overlay, or declare an independent setting.
