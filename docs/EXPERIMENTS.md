# Experiment protocol

1. Start with a game save whose provenance and SHA-256 are recorded. Keep the original outside `outputs/`.
2. Record the exact Star Citizen build. Change one control in the editor and save a second time; compare the files with `diff`. If several logical fields change, associate the gesture with the **group** of changed fields only; individual field roles remain ambiguous.
3. For a binary experiment, use `variant` (two balanced DNA weights in the same region, preserving the sum) or `variant-param` (a material float or RGBA channel). The latter requires the source SHA-256, indices, and exact `name_hash`. The manifest records SHA values and the diff. Do not infer anatomy from `head_id` or map a UI control from a hash name alone. Understanding a UI gesture still requires a BioCorp-saved pair.
4. Load the base and variant separately in the same game build. **After each import, open the corresponding character and click the sub-tab being measured again (Hair > Color can show values from the previous character). Verify that the panel refreshed before reading a percentage or slider position.** Capture front, profile, and matching lighting. Record detection, loading, stability, and whether saving succeeds.
5. Update `screenshots`, `game_version`, `game_load`, and `visual_verdict` in the local manifest. Allowed verdicts: `effect confirmed`, `no visible effect`, `ambiguous`, or `not tested`. Record concrete observations and keep any game-saved file separately.

A successful inspection is only `STRUCTURAL_PASS`. Structural validity, in-game loading, in-game saving, and observed appearance are separate claims.

## Published evidence catalog

The public GUI and JSON catalogs provide bounded summaries of reported UI pairs and one-field experiments for DNA regions and material parameters. The source files, experiment manifests, screenshots, character presets, and their SHA-256 fingerprints are private and intentionally omitted from this repository. The catalog's selectors identify the observed structural context; they do not identify a private character file. Entries are scoped observations, not universal field meanings. An identical hash or DNA signature does not prove an effect on a different preset. Where a catalog entry lacks a publicly reproducible source artifact, report that provenance limitation and validate any intended change in the relevant game build.

BioCorp may change additional values while saving. Preserve such fields as opaque data unless their meaning is independently established.
