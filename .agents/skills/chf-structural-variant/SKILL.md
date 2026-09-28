---
name: chf-structural-variant
description: Prepare or inspect one bounded CHF v7/v8 experiment with source preservation, structural validation, an exact diff, and separate game and visual verdicts.
---

# Controlled CHF structural variant

Use this workflow when an authorized task calls for inspecting or editing a local `.chf`. It does not establish a character's appearance or a universal mapping from field names.

1. Read [`docs/CHF_FORMAT.md`](../../../docs/CHF_FORMAT.md), [`docs/CHF_EDITING_WORKFLOW.md`](../../../docs/CHF_EDITING_WORKFLOW.md), and the relevant current code. Confirm the source file and target game build. Record the source SHA-256 and keep its bytes intact.
2. Run `chf.py inspect` with a compatible Zstandard DLL. Reject unsupported versions, invalid CRC32C, inconsistent lengths, unconsumed payload, or unexplained structure. Keep the inspector output private when it contains file paths or values from a private preset.
3. State one exact change and why its field location is known. For DNA, use `variant` to balance two weights in one region. For an existing material value, use `variant-param` with the exact source SHA-256, indices, and name hash. Preserve head IDs, GUIDs, flags, unrelated values, and opaque bytes.
4. Let the maintained writer create a **new** output and manifest. It must refuse compressed-stream overlap with nonzero container bytes, recalculate CRC32C, re-parse the candidate, compare the logical diff to the requested change, and independently re-read the result. Do not weaken a failed guard or overwrite the source to force an export.
5. Record the output SHA-256 and structural verdict. Game loading, game saving, and visual effect stay `NOT TESTED` until each has been observed in the target build. If game testing is authorized, use a controlled before/after pair and comparable captures; distinguish preset display from a successful game save.
6. Save the populated [session record](../../../docs/CHF_SESSION_TEMPLATE.md) under ignored `outputs/`. Never commit private presets, manifests, screenshots, game extracts, or character-specific donor recipes.

If a source is missing or a new game version no longer matches the supported grammar, stop the edit at that boundary and investigate the current source and format. The user must explicitly validate phase 1 before development of a full out-of-game character creator.
