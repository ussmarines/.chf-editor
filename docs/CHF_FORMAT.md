# CHF v7/v8 format notes

These notes describe the **observed local `.chf` format** supported by this repository. They consolidate the supplied Starfall CHF research archive with the current [`chflab/inspector.py`](../chflab/inspector.py) implementation. The source reference is [StarBreaker's `starbreaker-chf` at `08302fbdd3a1cc704a0bc0977fb1841927a637bf`](https://github.com/diogotr7/StarBreaker/tree/08302fbdd3a1cc704a0bc0977fb1841927a637bf/crates/starbreaker-chf/src). A future game version may differ.

## Fixed container

The supported files are exactly **4,096 bytes**. Multi-byte numbers below are little-endian.

| Offset | Size | Meaning |
| --- | ---: | --- |
| `0x00` | 2 | Magic `0x4242`. |
| `0x02` | 2 | Opaque header value; preserve it. |
| `0x04` | 4 | CRC32C of bytes `[16, 4096)`, including bytes after the compressed stream. |
| `0x08` | 4 | Compressed Zstandard stream length. |
| `0x0C` | 4 | Declared decompressed payload length. |
| `0x10` | Variable | Zstandard stream, followed by container bytes that may include opaque data. |

The stream must fit inside the container without overwriting opaque bytes. Never truncate it to make it fit. Some game-saved files have nonzero bytes near the end of the container; zeroing or replacing them is not a proven safe normalization. The current writer preserves the input container where it can, refuses overlap with nonzero bytes, retains the last eight bytes, then recalculates CRC32C. The reader checks the declared decompressed size and consumes the complete supported payload.

## Decompressed payload

For the v7/v8 structures supported here, the reader consumes this sequence:

1. `female_version: u32`, expected to be `2`, then internal version `7` or `8` as `u32`.
2. Body type and voice GUIDs, 16 bytes each.
3. DNA byte length as `u64`, followed by DNA data.
4. Declared ItemPort node total as `u64`, followed by the recursive ItemPort tree.
5. Group marker `u32 = 5`, followed by material definitions.
6. For observed v8 files, a terminal `u32 = 0` after the final material.

The current parser checks that the declared ItemPort total matches the parsed nodes and that no unexplained payload bytes remain. The v8 terminal zero and complete-consumption rule describe the supported samples; they are not a promise about every future version. `intParams` and `Decals` described in some game serialization contexts are not established as sections of this local binary layout.

## DNA matrix

The supported v7 profile has 12 face regions and the supported v8 profile has 13, with four blends per region. The research archive observed DNA blocks of 216 bytes for v7 and 232 bytes for v8; this is a sample observation. V8 adds `Neck` at index 12.

| Index | Region | Index | Region |
| ---: | --- | ---: | --- |
| 0 | EyebrowLeft | 7 | CheekLeft |
| 1 | EyebrowRight | 8 | CheekRight |
| 2 | EyeLeft | 9 | Mouth |
| 3 | EyeRight | 10 | Jaw |
| 4 | Nose | 11 | Crown |
| 5 | EarLeft | 12 | Neck (v8) |
| 6 | EarRight | | |

The DNA header contains a name hash, `gender_hash`, `variant_hash`, a zero field, region count, blends per region, an unknown `u16`, and `max_head_id`. Each blend is `(value: u16, head_id: u16)`. The binary order is **interleaved by blend slot, then region**: `region_index = i % region_count`, `slot = i // region_count`. Using a v7 stride of 12 on v8 silently shifts later values. Treat `head_id`, `variant_hash`, `gender_hash`, the unknown header value, and `max_head_id` as opaque unless separately proven.

[StarChar's DNA editor at `2c4bace845a4004c78b50a7ed902a725545aa5e7`](https://github.com/diogotr7/starchar/blob/2c4bace845a4004c78b50a7ed902a725545aa5e7/src/components/DnaQuadBlend.tsx) displays four contributors in a quadrilateral. Its UI calculates bilinear weights `(1-x)(1-y)`, `x(1-y)`, `xy`, `(1-x)y` scaled to 65,535. That describes StarChar's controls, not an anatomical map for the head IDs or a universal game constraint.

## ItemPorts and materials

Each ItemPort node contains a port name hash, item GUID, child count, tail count, and its recursive children. The tail count is serializer bookkeeping. Preserve the entire tree, ordering, and unknown values when changing an unrelated field. A GUID alone does not identify a safe item substitution.

A material has an attachment hash, base material GUID, flags, a structural empty GUID, a submaterial count, and group marker `5`. Submaterials contain a name hash, textures, float parameters, and color parameters. A texture has a zero marker, index byte, and GUID. A float parameter has a name hash, `f32`, and structural zero; a local color has a name hash, four RGBA bytes, and structural zero. Group markers separate submaterials according to the supported serializer layout. Preserve flags, GUIDs, texture lists, order, and non-targeted parameters. A raw parameter hash or type does not prove its visible effect.

## Evidence boundary

The parser can establish structure, values, and differences. Mapping an editor control to a field requires two game saves from the same build with one control changed. Compatibility and appearance require the relevant game load, save, and comparable captures. Keep those findings separate in the [editing workflow](CHF_EDITING_WORKFLOW.md) and [experiment protocol](EXPERIMENTS.md).
