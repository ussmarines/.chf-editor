---
name: chf-editor
description: Navigate the CHF Editor project's format, evidence, safety, and editing guidance for Star Citizen .chf v7/v8 work.
---

# CHF Editor project guide

This project skill adapts the `spaceshooter-star-citizen-chf` router supplied in the Starfall research archive. It points to the maintained public files in this repository. Historical character briefs and donor-specific scripts are not part of this skill.

## Start from the current project

Read the repository's `AGENTS.md` and the current source before acting. Load only the document relevant to the question:

- Binary layout and opaque fields: [`docs/CHF_FORMAT.md`](../../../docs/CHF_FORMAT.md).
- Safe editing and game validation: [`docs/CHF_EDITING_WORKFLOW.md`](../../../docs/CHF_EDITING_WORKFLOW.md).
- Private experiment record: [`docs/CHF_SESSION_TEMPLATE.md`](../../../docs/CHF_SESSION_TEMPLATE.md).
- Controlled UI-save pair: [`docs/CONTROLLED_GAME_PAIR.md`](../../../docs/CONTROLLED_GAME_PAIR.md).
- Published evidence and limitations: [`docs/EXPERIMENTS.md`](../../../docs/EXPERIMENTS.md).
- Runtime dependencies and upstream revisions: [`docs/TOOLCHAIN.md`](../../../docs/TOOLCHAIN.md).

Use [`chflab/inspector.py`](../../../chflab/inspector.py) for read-only structural inspection and [`chf.py`](../../../chf.py) for currently supported controlled variants. The former SpaceShooter v3-v14 scripts are donor-specific historical experiments and are not the writer for new files.

## Authority and evidence

The user's current request, the actual input file, the current repository code, and observed behavior in the target Star Citizen build take priority over historical notes. A hash, GUID, UI label, or parser field name is not proof of an anatomical effect. Preserve unknown bytes and values. Report structure, game loading, game saving, and visual effect separately.

Keep private presets, captures, game data, and populated experiment records under ignored `outputs/` or outside Git. Do not include custom character files in a public contribution.
