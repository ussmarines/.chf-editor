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

### Native skin UI/save pairs, 2026-10-07

Four named skin controls were changed separately on female and male generic
references with skin texture 11. Each consecutive game-save pair changes one
logical float at material 0, submaterial 0, hash `8e9e1272`:

| Control | Float index | Name hash | Female saved values | Male saved values |
| --- | ---: | --- | --- | --- |
| Freckles Amount | 29 | `e22777e8` | 0.507053 â†’ 0.992565 | 0.509233 â†’ 0.974386 |
| Freckles Opacity | 15 | `58cb6193` | 0.254373 â†’ 0.901458 | 0.250059 â†’ 0.883160 |
| Sun Spots Opacity | 26 | `6412c4cf` | 0 â†’ 0.901458 | 0 â†’ 0.883151 |
| Sun Spots Amount | 10 | `0fd24a55` | 0.250829 â†’ 0.901458 | 0.256332 â†’ 0.883160 |

The opacity and sun-spot captures support visible changes on these references.
Freckles Amount has an isolated UI mapping but an inconclusive visual effect.
The final female and male states reloaded with their four changed values; this
does not demonstrate separate reloads of each intermediate snapshot. Retention
through a no-gesture re-save remains unclaimed here. Saved snapshots pass structural inspection; these UI pairs do
not validate the separately prepared binary variants or arbitrary presets.
Freckles Opacity enriches its existing selector with additional scoped
observations; its owner's historical acceptance remains unchanged. Three other
selectors are added once, each carrying both sex-specific observations.

### Exact prepared variants loaded and saved, 2026-10-07

The separate accepted-export suite was subsequently tested: two unchanged
baseline inputs and six independent variants per sex were loaded, captured and
saved. All twelve targets retained their exact input float or balanced Nose
weights in structurally valid game saves. The saved copies were not reloaded.
This is target retention, not preservation of the entire input file by BioCorp.

Comparing textures by index shows one inserted texture at material 0/submaterial
0, index 9, GUID `2f485b5e2cdf8c2dae15216ee5677cab`, in every save. Existing texture
indices and GUIDs remain unchanged. Male saves additionally repeat four baseline
colour quantizations: material 0/submaterial 0/color 7 green 122→121; material
1/submaterials 0 and 1/color 0 green 122→121; material 2/submaterial 0/color 0 red
52→51. No other normalized logical differences remain. Ordinal texture-list
comparisons alone misleadingly suggest replaced female texture GUIDs.

BaseMelanin variants changed dark hair to near white on both tested references,
with submaterial hashes `1fc558bf` (female) and `cdd049df` (male), material 3,
submaterial 0, float 5, name hash `a300fab9`. These receive separate scoped
capture-supported entries; the older owner-accepted hairstyle observations are
preserved. Male FrecklesOpacity and SunSpotsOpacity visibly changed the tested
skin. Amount controls and Nose changes remain inconclusive. Female skin variants
remain inconclusive with other contributing controls at zero; this does not
overturn the visible generic-reference UI pairs. Retention establishes neither
anatomical meanings of head IDs nor universal substitution compatibility.

The [offline revalidation](MAPPING_REVALIDATION.md) records which archived claims were rechecked, additional bounded dye-color evidence, negative results and provenance gaps. Rechecking an archive does not constitute a new game test.
