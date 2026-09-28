<!-- BEGIN brain.md -->
## Project Brain

This project keeps a **Project Brain**: a persistent memory layer for durable decisions, requirements, and constraints. Read `./BRAIN.md` for the full read/write contract.

Maintain the Brain as part of normal development:
- **At the start of a task:** load relevant context with the `brain` CLI (`list-pages`, `read-page`, `read-root`). Prefer a narrow read over scanning everything.
- **When a durable decision, requirement, constraint, or insight is settled:** capture it immediately with the `brain` CLI.
- **For implementation work that introduces no durable decision:** do not write to the Brain.
- **When overturning an earlier conclusion:** update the relevant page with the CLI.
- Store only information likely to remain useful for six months and difficult to reconstruct from code.
- All Brain reads and writes go through the `brain` CLI. Never edit Brain files by hand.

The `brain-setup`, `brain-page`, `brain-ingest`, and `brain-bootstrap` skills are installed globally. Prefer `brain init` to scaffold a new project.
<!-- END brain.md -->

## CHF project requirements

- Work on a `codex/` branch. Do not modify or merge into `main`, or access the game directory, without explicit user instructions. Publishing a preparation branch for the public-release task is authorized.
- Keep `.chf` files, videos, captures, `Data.p4k`, `Game2.dcb`, and extracted assets under `outputs/` or outside the repository. Never add them to Git.
- Preserve originals byte for byte. An export must pass size 4096, CRC32C, Zstandard limits, v7/v8 structure, opaque-region preservation, the expected logical diff, and an independent re-read.
- Report structural validity, in-game loading, in-game saving, and visual effect separately. None implies another.
- Provide a source and evidence level for every mapping. Names from StarBreaker/StarChar or `Game2.dcb` alone do not establish anatomical effects or substitution compatibility.
- Document StarBreaker revision `08302fbdd3a1cc704a0bc0977fb1841927a637bf` and StarChar revision `2c4bace845a4004c78b50a7ed902a725545aa5e7` as source revisions. Report the version of any binary separately.
- Phase 1 is understanding and controlled validation of parameters. Do not start a complete out-of-game character creator until the user explicitly approves that phase.
- Run targeted tests for both new female/male presets when those presets are part of the authorized local work. Historical scripts under `research/space-shooter/` are an archive, not the main writer.
- For library, API, or CLI questions, consult Context7 first. Graphify may help navigate local code; do not install a hook or watcher without an explicit need.
