# Validated observations and remaining unknowns

Snapshot: 2026-10-07. Historical observations concern LIVE `4.10.193.11644`, BioCorp `01.05.03`. A status applies to its tested reference, selector and build. A structural match on a new file is a reason to test, not a validation of that file.

## Material observations

| Observation | UI-to-field mapping | Loading | Game saving | Visible effect |
| --- | --- | --- | --- | --- |
| Freckles Opacity | Female controlled UI pair isolates the float; male tested through a variant | Historically reported for female/male | Authenticated copies retain the tested value | Supported by historical female/male captures |
| Female hair Dye Amount | UI pair changes a group including the float and small color differences | Historically reported | Authenticated copy retains the tested float | Not isolated |
| Female hair Natural Color Variation | Bounded UI association after refreshing the Color panel | Historically reported | No authenticated roundtrip for the exact UI observation | Not isolated; immediate post-import slider readings were stale |
| Female hair BaseMelanin | UI pair changes a group; isolated float experiment supports its effect | Historically reported | Authenticated copy retains the value | Light hair in reviewed historical captures |
| Male hair BaseMelanin | Isolated float experiment; exact UI gesture not isolated | Historically reported | Authenticated copy retains the value | Light hair with dark beard in historical captures |
| Male beard/moustache BaseMelanin | Isolated float experiment; exact UI gesture not isolated | Historically reported | Authenticated copy retains the value | Light beard/moustache with dark hair in historical captures |
| Male eyebrow BaseMelanin | Isolated float experiment; exact UI gesture not isolated | Historically reported | Authenticated copy retains the value | Light brows in historical captures |
| Female root-dye color, material 3, red byte | UI pair changes two copies; one-byte experiment isolates this occurrence | Historically reported | Recorded re-save hash malformed; association unauthenticated | Burgundy hair in authenticated historical capture; only R was isolated |
| Secondary dye-color copy, material 5, red byte | Exact BioCorp control not established | Historically reported | Authenticated copy resets the byte | Negative observation: no visible change reported; not a usable validated color control |

The public catalog has **9 material observations**, including a negative result. It does not have nine universally validated controls. Numeric values remain raw CHF values; no general slider percentages or safe visual ranges have been established.

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

These counts are a reference snapshot, not a statement about every female or male preset. The GUI computes the matching observations for the file actually opened.

| Coverage | Reviewed female v8 export | Reviewed male v8 export |
| --- | ---: | ---: |
| Material float/color occurrences | 93 | 111 |
| Occurrences without a source name | 0 | 0 |
| Occurrences without a matching catalog observation | 91 | 109 |
| Occurrences without a matching historical positive visual observation | 92 | 109 |
| DNA regions without matching catalog UI evidence | 9 / 13 | 13 / 13 |

There are 200 material occurrences without matching observations across these files, with repeated names and hashes. This is not 200 unique controls. Even positive historical matches must be verified on the reviewed exports themselves.

## Current installed-file check and next tests

The two active character files were found under renamed filenames and authenticated byte-for-byte against the accepted archived exports. Their structure passes. The installed build manifest reports `4.10.193.11644`. This resolves the earlier absence of the original export filenames; it does not demonstrate a new game load or save.

No new game validation was performed in this session: Star Citizen was not running and native game observation/input was unavailable. Locally prepared experiments remain `not tested` for game loading, saving and visible effect until those outcomes are observed.

A private test bundle was prepared from the two authenticated active presets: six candidates per sex, each based on its unchanged baseline. It isolates FrecklesOpacity, FrecklesAmount, SunSpotsOpacity, SunSpotsAmount, BaseMelanin, or two balanced Nose weights. All 12 candidates pass the guarded writer, exact raw-payload and opaque-container preservation checks, single-frame Zstandard checking, and independent parsing with StarBreaker binary `0.3.2`. These are prepared experiments, not new game observations; no candidate was installed into the game directory.

Prioritize female/male paired tests for freckles and sun spots, hair pigment under controlled dye state, and balanced DNA weights. Preserve the baseline; import each candidate, refresh the measured panel, capture the same view and lighting, save a new copy without another gesture, compare the result, then reload that saved copy. Record loading, saving, value retention and visible effect separately. Do not infer a field's role merely because BioCorp retains its value.

## Guided editing

The GUI offers **Catalog observations**, **Observed visual changes**, and **All raw parameters**. Historical control labels and separate UI/load/save/visual statuses appear beside matching fields. Negative and inconclusive results are excluded from the positive visual filter. Guided color observations restrict the offered channels to those tested; raw mode permits other channels as unvalidated experiments.

DNA region and slot selections refresh their current weight. The balancing range is an integer encoding constraint, not a validated anatomical range. Region choices come from the open file, so a v7 preset is not offered the v8-only Neck region. Every export still uses the guarded writer and preserves source SHA checking, exact diffs and independent re-reading.

The full out-of-game creator and 3D preview remain deferred. See [remaining work](NEXT_STEPS.md), [mapping revalidation](MAPPING_REVALIDATION.md), and [experiment protocol](EXPERIMENTS.md).

## Upstream research checked

The upstream branches were checked again on 2026-10-07: StarBreaker `main` still points to `08302fbdd3a1cc704a0bc0977fb1841927a637bf`, and StarChar `master` to `2c4bace845a4004c78b50a7ed902a725545aa5e7`. The [StarBreaker DNA parser](https://github.com/diogotr7/StarBreaker/blob/08302fbdd3a1cc704a0bc0977fb1841927a637bf/crates/starbreaker-chf/src/dna.rs) supports the structural region/blend layout. The [StarChar blend interface](https://github.com/diogotr7/starchar/blob/2c4bace845a4004c78b50a7ed902a725545aa5e7/src/components/DnaQuadBlend.tsx) implements a four-contributor blend; it does not establish anatomical directions or validated game head-ID ranges. This research adds no new visual mapping.
