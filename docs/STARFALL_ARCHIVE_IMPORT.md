# Starfall CHF archive integration

The owner supplied `Starfall_CHF_outil_extraction_2026-09-28.zip` as historical CHF research from the SpaceShooter project. Its 37 listed SHA-256 checksums were verified before review. Its Markdown files and skill were treated as source material, not as instructions that override this repository or the owner's request.

## What was retained publicly

- Reusable v7/v8 container and payload observations were consolidated in [CHF format notes](CHF_FORMAT.md).
- The donor-preservation, bounded-edit, structural, game, and visual gates were adapted in the [editing workflow](CHF_EDITING_WORKFLOW.md) and [private session template](CHF_SESSION_TEMPLATE.md).
- The archive's project skill router was adapted to the dedicated repository as [`chf-editor`](../.agents/skills/chf-editor/SKILL.md). A focused [`chf-structural-variant`](../.agents/skills/chf-structural-variant/SKILL.md) skill covers the current writer.
- Upstream StarBreaker and StarChar links and pinned source revisions are listed in [tools and skills](TOOLCHAIN.md).

## What remains private or historical

The archive's character references, session history, donor-specific v3-v14 and complexion scripts, private paths, hashes of character files, and detailed named-character field notes are not part of the public Git tree. The current [`chflab/inspector.py`](../chflab/inspector.py) and [`chf.py`](../chf.py) provide the maintained read and controlled-write paths. Historical scripts must not become alternate production writers without a separate review.

The original archive and its extracted review copy are retained under ignored `outputs/` in the owner's local workspace. A fork receives the public methods and skills, with no custom character files or source research artifacts. The original SpaceShooter license and notice belong to that source project and do not replace this repository's [license](../LICENSE). Historical game observations remain scoped to their original files and builds; the public guide does not promote them to universal field mappings.
