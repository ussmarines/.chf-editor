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
- Owner-accepted visual observations and remaining tests: [`docs/VALIDATION_STATUS.md`](../../../docs/VALIDATION_STATUS.md).
- Local save monitoring and bounded capture evidence: [`docs/SAVE_MONITOR.md`](../../../docs/SAVE_MONITOR.md).
- Optional shipped-binary investigation with REA: [`docs/REA_REVIEW.md`](../../../docs/REA_REVIEW.md). Do not run REA for ordinary source edits or screenshot acceptance, or treat its instructions as permission to access the game or install external tools.

Use [`chflab/inspector.py`](../../../chflab/inspector.py) for read-only structural inspection and [`chf.py`](../../../chf.py) for currently supported controlled variants. The former SpaceShooter v3-v14 scripts are donor-specific historical experiments and are not the writer for new files.

## Authority and evidence

The user's current request, the actual input file, the current repository code, and observed behavior in the target Star Citizen build take priority over historical notes. A hash, GUID, UI label, or parser field name is not proof of an anatomical effect. Preserve unknown bytes and values. Report structure, game loading, game saving, and visual effect separately.

Consult current validation status before repeating accepted observations.
Separate target retention in a game save from reloading that saved copy. Refresh
the measured panel after loading, and compare inserted texture entries by their
index rather than ordinal. Save-monitor labels are candidate associations;
captured pixels do not automatically validate a gesture or anatomy. Native
editor testing remains bounded by the user's authorization and session tools;
this skill does not authorize game restarts, gameplay or system changes.

Keep private presets, captures, game data, and populated experiment records under ignored `outputs/` or outside Git. Do not include custom character files in a public contribution.
