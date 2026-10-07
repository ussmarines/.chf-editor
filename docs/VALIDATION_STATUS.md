# Validated observations and remaining unknowns

Snapshot: 2026-10-07. Historical observations concern LIVE `4.10.193.11644`, BioCorp `01.05.03`. A status applies to its tested reference, selector and build. A structural match on a new file is a reason to test, not a validation of that file.

## Material observations

### Owner visual acceptance, 2026-10-07

The owner accepts the effects already validated through screenshots. The six
capture-backed positive catalog observations below are **VALIDATED by owner**:
freckles opacity, female hair pigment, male hair pigment, male beard/moustache
pigment, male eyebrow pigment, and the female root-dye red channel. Their catalog
status is `owner_validated_capture`, also displayed by the GUI. This closes visual
acceptance for those historical references, not for an arbitrary matching preset.

The captured negative secondary-dye observation is accepted as a negative result,
not promoted to a usable color control. Ambiguous effects, DNA observations
without comparable captures, and newly prepared candidates keep their current
status. Loading, saving, UI mapping and channel restrictions remain independent;
in particular, accepting the root-dye capture does not authenticate its malformed
re-save fingerprint. The already accepted private character exports stay accepted
and unchanged. No new game session or screenshot is claimed by this decision.

| Observation | UI-to-field mapping | Loading | Game saving | Visible effect |
| --- | --- | --- | --- | --- |
| Freckles Opacity | Female controlled UI pair isolates the float; male tested through a variant | Historically reported for female/male | Authenticated copies retain the tested value | VALIDATED by owner from historical female/male captures |
| Female hair Dye Amount | UI pair changes a group including the float and small color differences | Historically reported | Authenticated copy retains the tested float | Not isolated |
| Female hair Natural Color Variation | Bounded UI association after refreshing the Color panel | Historically reported | No authenticated roundtrip for the exact UI observation | Not isolated; immediate post-import slider readings were stale |
| Female hair BaseMelanin | UI pair changes a group; isolated float experiment supports its effect | Historically reported | Authenticated copy retains the value | VALIDATED by owner: light hair in historical captures |
| Male hair BaseMelanin | Isolated float experiment; exact UI gesture not isolated | Historically reported | Authenticated copy retains the value | VALIDATED by owner: light hair with dark beard in historical captures |
| Male beard/moustache BaseMelanin | Isolated float experiment; exact UI gesture not isolated | Historically reported | Authenticated copy retains the value | VALIDATED by owner: light beard/moustache with dark hair in historical captures |
| Male eyebrow BaseMelanin | Isolated float experiment; exact UI gesture not isolated | Historically reported | Authenticated copy retains the value | VALIDATED by owner: light brows in historical captures |
| Female root-dye color, material 3, red byte | UI pair changes two copies; one-byte experiment isolates this occurrence | Historically reported | Recorded re-save hash malformed; association unauthenticated | VALIDATED by owner: burgundy hair in historical capture; only R was isolated |
| Secondary dye-color copy, material 5, red byte | Exact BioCorp control not established | Historically reported | Authenticated copy resets the byte | Accepted negative observation: no visible change reported; not a usable validated color control |

The public catalog has **14 material contexts with unique selectors**, including a negative result and additional scoped observations. The table above retains the nine historical contexts; later native tests are summarized below. These are not fourteen universally validated controls. Numeric values remain raw CHF values; no general slider percentages or safe visual ranges have been established.

## DNA observations

| Observation | UI mapping / experiment | Loading and saving | Visible effect |
| --- | --- | --- | --- |
| Female nose-tip marker | Authenticated one-gesture pair changes the Nose group | Historical game saves and reload reported | User-reported shape change; no comparable capture pair |
| Female balanced Nose weights | Two weights changed; head IDs unchanged | Historical load; authenticated game-saved weights retained | User-reported clear change; anatomical direction not established |
| Female lower-lip marker | Authenticated one-gesture pair changes the Mouth group | Historical game saves and reload reported | User-reported shape change; no comparable capture pair |
| Female balanced Mouth weights | Two weights changed; head IDs unchanged | Historical load; authenticated game-saved weights retained | Negative/inconclusive: no clear difference reported |
| Female inner-eye marker | Authenticated pair changes EyeLeft and EyeRight together | Historical game saves and reload reported | No clear difference; mirror-option state unknown |

These are **5 observations** covering four female region names. Individual `head_id` identities, anatomical meaning of each blend contributor, and the direction of an individual weight change remain **unvalidated for all regions**.

Additional archived eyebrow, cheek, jaw and crown candidates establish structural differences but lack sufficiently authenticated gesture provenance for new public UI mappings. Female EarLeft/EarRight and Neck have no matching UI evidence. There is no male UI-region mapping in the current DNA catalog.

## Coverage of the reviewed private exports

These counts were recomputed against the unchanged reviewed baselines and the expanded catalog on 2026-10-07. They are not a statement about every female or male preset. The GUI computes the matching observations for the file actually opened.

| Coverage | Reviewed female v8 export | Reviewed male v8 export |
| --- | ---: | ---: |
| Material float/color occurrences | 93 | 111 |
| Occurrences without a source name | 0 | 0 |
| Occurrences without a matching catalog observation | 87 | 105 |
| Occurrences without a matching positive visual observation | 89 | 106 |
| DNA regions without matching catalog UI evidence | 9 / 13 | 13 / 13 |

There are 192 material occurrences without matching observations across these files, with repeated names and hashes. This is not 192 unique controls. Matching selectors identify evidence contexts; they do not establish every matching field's visual effect on this file.

## Current installed-file check and next tests

The two active character files were found under renamed filenames and authenticated byte-for-byte against the accepted archived exports. Their structure passes. The installed build manifest reports `4.10.193.11644`. This resolves the earlier absence of the original export filenames; it does not demonstrate a new game load or save.

At the earlier preparation snapshot, no new game validation had been performed:
Star Citizen was not running and native game observation/input was unavailable.
The later native UI/save observations below are separate from the prepared
binary experiments, subsequently tested as recorded below.

A private test bundle was prepared from the two authenticated active presets: six candidates per sex, each based on its unchanged baseline. It isolates FrecklesOpacity, FrecklesAmount, SunSpotsOpacity, SunSpotsAmount, BaseMelanin, or two balanced Nose weights. All 12 candidates pass the guarded writer, exact raw-payload and opaque-container preservation checks, single-frame Zstandard checking, and independent parsing with StarBreaker binary `0.3.2`. At preparation time these were offline experiments and no candidate had been installed. The subsequent exact-file native validation is recorded below.

Prioritize female/male paired tests for freckles and sun spots, hair pigment under controlled dye state, and balanced DNA weights. Preserve the baseline; import each candidate, refresh the measured panel, capture the same view and lighting, save a new copy without another gesture, compare the result, then reload that saved copy. Record loading, saving, value retention and visible effect separately. Do not infer a field's role merely because BioCorp retains its value.

## Native skin UI/save validation, 2026-10-07

Eight controlled pairs, four per sex, connect Freckles Amount, Freckles Opacity,
Sun Spots Opacity and Sun Spots Amount to exact float occurrences on generic
female and male references, skin texture 11. Every pair changes one logical
float, and the archived game-save snapshots pass structural inspection.
The [pair summary](EXPERIMENTS.md#native-skin-uisave-pairs-2026-10-07) records
selectors and values. These observations concern LIVE `4.10.193.11644`, BioCorp
`01.05.03`; originals and private evidence remain outside tracked files.

UI mapping and observed game saving are supported for all eight pairs. Captures
support visible opacity and sun-spot changes on the tested references;
Freckles Amount remains visually inconclusive. The final female and male group
states were reloaded with their four changed values. Individual intermediate
reloads and retention through a no-gesture re-save are not claimed by this snapshot. The historical six owner
acceptances remain intact; new capture-supported observations do not acquire
owner acceptance. The separate twelve Alia/Corvin binary candidates were subsequently tested as
recorded below; no head-ID anatomical meaning is established.

## Exact prepared-suite game validation, 2026-10-07

The two accepted-export baselines and all twelve prepared variants were loaded,
captured and saved. All saved files pass structural inspection. Input and saved
SHA-256 fingerprints were independently checked; every target float or complete
balanced Nose region retained its exact input values. No subsequent reload of
the saved variant copies is claimed. Target retention and observed saving are
separate from whole-file equality: BioCorp inserts texture index 9 in every
save, and repeats four baseline colour quantizations on the male reference.
Texture matching by index confirms existing GUIDs remain unchanged; see the
[exact-suite summary](EXPERIMENTS.md#exact-prepared-variants-loaded-and-saved-2026-10-07).

Both BaseMelanin variants visibly changed hair from dark to near white. Male
FrecklesOpacity and SunSpotsOpacity also had visible effects. Amount controls,
balanced Nose changes, and the female skin variants remain inconclusive; the
female reference's other contributing skin controls at zero limit interpretation.
These results do not generalize visual mappings or establish individual head-ID
anatomy. New hair selectors use capture-supported evidence, preserving the six
historical owner acceptances. Five installed originals and all fourteen suite
inputs were checked byte-for-byte unchanged; the initial female working copy
was restored in the character editor after testing.

## Local native-library validation, 2026-10-07

An existing Zstandard `1.5.7` library passed the runtime version/API check and
actual compression/decompression roundtrip. With `CHF_ZSTD_DLL` configured for
the invocation, all three native-library tests passed without a skip. The full
local suite then passed 16 tests with the female private baseline and 16 with
the male baseline, with no skips in either run. This is offline library/export
evidence, not a new game load, save, screenshot or anatomical mapping.

The machine-specific launcher remains under ignored `outputs/local-runtime/`;
it restores the caller's environment and working directory after execution.
No DLL download, binary vendoring or global environment modification was needed.
See [native-library setup and tests](TOOLCHAIN.md#native-library-tests).

The final publication check used the existing optional monitor environment and
unchanged female and male baselines. All 31 tests passed on each reference, with
no skips, including the synthetic capture/sequence tests and native Zstandard
roundtrip. These tests do not operate the game or supply missing visual/reload
evidence. The Brain migration preserved 23 historical entries, accepted the new
evidence entry through the standard CLI, and passed link checking.

## Guided editing

The GUI offers **Catalog observations**, **Observed visual changes**, and **All raw parameters**. Historical control labels and separate UI/load/save/visual statuses appear beside matching fields. Negative and inconclusive results are excluded from the positive visual filter. Guided color observations restrict the offered channels to those tested; raw mode permits other channels as unvalidated experiments.

DNA region and slot selections refresh their current weight. The balancing range is an integer encoding constraint, not a validated anatomical range. Region choices come from the open file, so a v7 preset is not offered the v8-only Neck region. Every export still uses the guarded writer and preserves source SHA checking, exact diffs and independent re-reading.

The full out-of-game creator and 3D preview remain deferred. See [remaining work](NEXT_STEPS.md), [mapping revalidation](MAPPING_REVALIDATION.md), and [experiment protocol](EXPERIMENTS.md).

## Upstream research checked

The upstream branches were checked again on 2026-10-07: StarBreaker `main` still points to `08302fbdd3a1cc704a0bc0977fb1841927a637bf`, and StarChar `master` to `2c4bace845a4004c78b50a7ed902a725545aa5e7`. The [StarBreaker DNA parser](https://github.com/diogotr7/StarBreaker/blob/08302fbdd3a1cc704a0bc0977fb1841927a637bf/crates/starbreaker-chf/src/dna.rs) supports the structural region/blend layout. The [StarChar blend interface](https://github.com/diogotr7/starchar/blob/2c4bace845a4004c78b50a7ed902a725545aa5e7/src/components/DnaQuadBlend.tsx) implements a four-contributor blend; it does not establish anatomical directions or validated game head-ID ranges. This research adds no new visual mapping.
