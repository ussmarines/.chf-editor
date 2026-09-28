# Controlled CHF editing workflow

This workflow adapts the reusable parts of the supplied Starfall research archive to CHF Editor. It applies to generic local v7/v8 experiments. Historical scripts tied to individual character donors are not the maintained writer; use [`chf.py`](../chf.py) for new controlled variants.

## 1. Choose and preserve the source

Use a real preset saved by the target game build when possible. Record its SHA-256, game build, provenance, and the behavior you intend to measure. Keep the original byte-for-byte intact and work from a copy. If the necessary source is missing, obtain an authorized source instead of reconstructing one from an image or a character description.

Before editing, run `inspect` and record the 4,096-byte container, magic, CRC32C, Zstandard sizes, internal version, DNA dimensions, ItemPort total, materials, and opaque container tail. If a new game save differs from the supported grammar, investigate the format before editing it.

## 2. Isolate one question

To map a game UI control, create a **before/after pair in the same game build** with only that control changed. Record the displayed values and comparable captures, then run `diff`. If several logical fields change, attribute the gesture only to the group until a second controlled pair isolates the field. A v7-to-v8 conversion is not a one-control experiment.

For an offline variant, change the smallest understood value:

- `variant` changes two DNA weights in one region so their sum remains constant, without changing head IDs.
- `variant-param` changes one existing material float or RGBA component, guarded by the exact source SHA-256, location, and name hash.

Do not invent a `head_id`, GUID, hairstyle, tattoo, scar, or material mapping from its label. Keep non-targeted ItemPorts, materials, hashes, flags, and opaque bytes unchanged.

## 3. Validate before game use

The maintained writer recompresses the payload, checks that it fits without overwriting nonzero container data, writes sizes and CRC32C, re-parses the candidate, verifies the expected logical diff, and independently re-reads the output. An output must pass all of those checks before it is offered for game testing. Record the source and output hashes in the local experiment manifest.

A new compression result may have different compressed bytes or size despite an expected logical payload diff. Compare structure and protected container regions, not SHA-256 alone. Never repair an oversized stream by truncating it.

## 4. Test in the target game build

Record these separately: preset detection, loading, editor stability, game saving, and visible effect. For visual comparison, use similar lighting and front, three-quarter, and profile views. Reopen the relevant editor panel after loading each preset before trusting its displayed value. Keep game-saved outputs and captures private under `outputs/` or outside the repository.

Promote a file as a reusable game-tested base only after it loads, remains editable, and saves successfully in the documented build. If a variant crashes or corrupts the appearance, return to the last known working base and inspect only the bounded diff. Structural success does not imply a visual or game verdict.

## 5. Preserve a reproducible record

Use the [session record template](CHF_SESSION_TEMPLATE.md) alongside the generated `.experiment.json`. Record source and output hashes, exact tool and game versions, intentional values, preserved fields, structural result, game result, screenshots, and unresolved questions. Never commit the populated manifest, preset, or captures.

See [format notes](CHF_FORMAT.md), [controlled game pair protocol](CONTROLLED_GAME_PAIR.md), and [published evidence limits](EXPERIMENTS.md) for details.
