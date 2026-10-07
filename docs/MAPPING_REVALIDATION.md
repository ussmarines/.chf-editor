# Offline mapping revalidation

This review rechecked private archived CHF files, experiment records, game-saved copies and captures on 2026-10-07. It did not run Star Citizen or establish compatibility with a newer build. Historical game observations below concern LIVE 4.10.193.11644 / BioCorp 01.05.03.

## Validation summary

The review inspected 217 archived CHF files successfully and examined 36 experiment manifests. Thirty historical CHF hash references and 18 historical capture hash references were matched to archived artifacts. The three documented female UI pairs for Nose, Mouth and linked EyeLeft/EyeRight were authenticated against historical records and their logical diffs recomputed.

Both accepted private character exports remained byte-identical to their historical fingerprints. Each passed the 4,096-byte size, CRC32C, exact Zstandard frame length, complete v8 grammar, expected logical diff, preserved DNA sums, raw preservation of non-targeted payload bytes, and preservation of opaque container bytes. The existing eight tests passed separately with the female and male exports as local fixtures. None of these offline checks establishes current in-game loading, saving or appearance.

The existing seven material observations and five DNA observations were retained. Two material observations were added: an isolated root-dye red-channel effect and a negative secondary-copy experiment. All private preset bytes remained unchanged during the review.

## Evidence levels

Keep three claims separate: a source label or serialization group; a recorded UI gesture associated with a logical field or group; and an observed visible effect with game loading/saving evidence. A matching selector on another preset does not transfer a visual result. Individual DNA slots and head IDs remain anatomically unidentified.

| Field / group | Revalidated support | Remaining limit |
| --- | --- | --- |
| Freckles Opacity, float `58cb6193`, reference material 0 / submaterial 0 / parameter 15 | Recorded female one-control UI pair has authenticated source/output hashes and only this logical value changes, besides opaque container metadata. Female/male single-value variants and authenticated game-saved copies retain the value. | UI-to-float conversion and universal applicability remain unknown. The male experiment is not a male one-control UI pair. |
| Dye Amount, float `5ac1f64a`, female hair material 3 / submaterial 0 / parameter 2 | Archived UI pair changes the slider and this float, alongside small color changes. The isolated float variant and authenticated game-saved copy retain the value. | The visual effect was not clearly isolated; the UI pair is not a pure one-field diff. |
| Natural Color Variation, float `c8a79aa5`, female hair material 3 / submaterial 0 / parameter 4 | Archived UI states, isolated variants and panel-refresh observations support the existing bounded UI association. | Immediate post-import percentages were stale. No general percentage formula or isolated visual effect is established. A second material occurrence can retain a value without controlling this UI slider. |
| Natural Color / BaseMelanin, float `a300fab9` | Female hair and separate male hair, beard/moustache and eyebrow variants have authenticated source/output hashes, exact single-float diffs and authenticated game-saved copies retaining their values. Reviewed captures show light hair, beard or brows in the tested contexts. | The material/submaterial selector matters. The female default-hair normalization experiments do not establish the same visual effect under every dye state. |
| Root Dye Color / HairDyeColor2, color `09c9c7a2`, female hair material 3 / submaterial 0 / parameter 1 | The UI pair changes two copies together. An authenticated isolated red-byte variant and authenticated capture support the visible hair-color effect of the material 3 occurrence. | Only the red byte was isolated. The recorded re-save fingerprint for that experiment has 63 hex characters, so it cannot authenticate the re-save association. |
| Secondary HairDyeColor2, material 5 / submaterial 0 / parameter 0 | Authenticated one-byte variant and capture support the reported absence of a visible effect. An authenticated game-saved copy resets the tested byte. | This is negative evidence in one context, not proof that this occurrence is always unused. |
| Female Nose | Archived base/UI and balanced-weight experiments support the existing region-level observation. | No individual head ID or weight direction is established; captures and game-save associations must be evaluated independently. |
| Female Mouth | Archived base/UI and balanced-weight experiments support the existing region-level observation. | The isolated weight experiment did not show a clear visible difference. No individual contributor has an anatomical label. |
| Female EyeLeft + EyeRight | Archived UI states change both regions together. | The mirror-option state and individual marker semantics remain unknown; no clear visible shape effect was reported. |

## Additional structural coverage

The review matched 164 parameter occurrences across the two accepted private presets to labels in pinned StarBreaker and export groups in previously extracted game serialization records. Those are 75 occurrences in the female preset and 89 in the male preset, spanning 56 source labels: freckles, sun spots, hair pigment/dye, makeup and tattoo parameters. Repeated inclusion in export groups produced 541 group matches, not 541 independently confirmed controls.

Attachment strings match the stored little-endian CRC32 values; shader parameter names use the pinned StarBreaker CRC32C table or its explicitly manual aliases. These associations identify source naming and serialization context. They do not establish slider conversion, anatomy, valid ranges, texture substitution, or visible results. The original extracted-record build provenance remains historical.

The 56 labels comprise `FrecklesAmount`, `FrecklesOpacity`, `SunSpotsAmount`, `SunSpotsOpacity`; `BaseMelanin`, `BaseMelaninRedness`, `BaseMelaninVariation`, `DyeAmount`, `DyeFadeout`, `DyePigmentVariation`, `DyeShift`; `TattooAge`, `TattooHueRotation`, `TattooNumTilesU`, `TattooNumTilesV`, `TattooOffsetU`, `TattooOffsetV`; and 39 makeup names. For each of `Makeup1`, `Makeup2` and `Makeup3`, the observed suffixes are `MetalnessB/G/R`, `OpacityB/G/R`, `SmoothnessB/G/R`, `NumTilesU/V` and `OffsetU/V`. This is a list of source names, not a list of validated UI controls.

Archived DNA candidates also isolate EyebrowLeft/Right, CheekLeft/Right, Jaw and Crown groups. Their filenames alone cannot authenticate a one-control gesture. Several candidates contain accompanying color or hairstyle changes, and need a stronger provenance record before public UI mappings can be added.

## Provenance issues found

- Two early character-specific nose experiments lack an archived source matching the recorded SHA-256. Their output files are valid, but their complete source-to-output claim cannot be revalidated.
- A hairstyle manifest uses a display string for a deleted color record and a different diff ordering. Its hashes and normalized logical changes agree with the current reader; it is not a corrupt CHF. Its recorded screenshot could not be found with the expected hash.
- An archived file named as a jaw re-save has a different DNA state from the jaw candidate. A separately named verified copy preserves the candidate's DNA. The ambiguous filename must not be used as game-save proof.
- The accepted character exports remain structurally valid and byte-identical to their historical hashes. Their former installed paths were absent when checked. Archived integrity does not prove current installation, current game loading or a successful game save.

## Sources and reproducibility

Structural names: StarBreaker source revision `08302fbdd3a1cc704a0bc0977fb1841927a637bf`, including `starbreaker-chf/src/dna.rs` and `starbreaker-common/src/name_hash.rs`. All 210 entries in the local name catalog agree with the pinned source table and its manual mappings. GUID labels: StarChar source revision `2c4bace845a4004c78b50a7ed902a725545aa5e7`. Both local source checkout revisions were rechecked. The archived StarBreaker executable had no populated Windows file/product version; its binary version is unknown and is not inferred from a source checkout.

Previously extracted male/female `DNA V1.6` head-asset headers match the respective accepted presets' gender and variant hashes. That is header identity evidence; it does not identify individual blend contributors or their anatomical effects.

Private audit artifacts contain the per-file hashes, exact selectors, computed diffs, manifest associations and capture checks. They stay outside Git. Public entries remain bounded summaries with the limitations above; independent contributors need their own controlled pair in the relevant build. See [the experiment protocol](EXPERIMENTS.md) and [controlled game pair](CONTROLLED_GAME_PAIR.md).
