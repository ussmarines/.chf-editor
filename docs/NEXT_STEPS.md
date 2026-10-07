# Remaining work

The local tool already inspects and compares CHF v7/v8 files and exports narrow DNA or material experiments. The next work is ordered by evidence needed, rather than by UI size.

[Save monitoring](SAVE_MONITOR.md) now automates stable-save snapshots, field diffs
and user-labelled candidate associations, with optional local foreground-game
captures. An owner-driven retest confirmed the visible-game-area fallback for
that session; general graphics-mode compatibility remains unverified. Pixel
variation does not identify a slider or validate anatomy.

The [2026-10-07 offline revalidation](MAPPING_REVALIDATION.md) authenticated historical pairs and captures, added two bounded dye-color observations, and documented provenance gaps. The remaining priorities below concern new game evidence and wider scope; repeating an archive inspection cannot supply those results.

The [validation status](VALIDATION_STATUS.md) distinguishes UI mapping, loading, saving and visual results. The catalog now has 14 unique material selectors and five DNA observations. Eight skin UI/save pairs were collected across female/male generic references. All twelve prepared variants loaded and saved with their target values retained; those saved copies have not been reloaded. Both hair BaseMelanin variants visibly changed the tested reference; several skin and Nose effects remain inconclusive. Guided material filters and separate status labels, Zstandard detection and the native roundtrip check are implemented. Phase two is deferred.

Owner acceptance of the six positive screenshot-backed material effects is
**closed as VALIDATED** on 2026-10-07. Do not request the same visual approval
again unless the tested rendering/context changes or a new defect is reported.
The priorities below concern new candidates, missing evidence and wider scope.
The optional [REA investigation skill](REA_REVIEW.md) supplies an evidence method;
it is not a CHF parser, an anatomy oracle or a replacement for BioCorp tests.

1. **Complete saved-copy reloads and unresolved visual tests.** Reload the twelve saved variants separately and verify retained values with refreshed panels. Isolate skin Amount effects with a nonzero companion opacity, and obtain comparable views for balanced Nose weights. Preserve separate structural, loading, saving and visual verdicts. New candidates/builds require their own tests; existing results do not transfer automatically.
2. **Collect controlled saves for more UI controls.** Save a baseline and a second file after exactly one gesture. Inspect the logical diff. If several fields change, document the group and isolate individual roles through another controlled experiment. Repeat on female and male presets where the claim is meant to cover both.
3. **Grow the evidence catalog only within proven scope.** Record source revisions, game build, structural selector, observed effect, and unresolved ambiguity. Keep private CHF files and captures out of Git.
4. **Improve guided editing from confirmed mappings.** Add user-facing controls only when their limits, context, load behavior, and save behavior have been shown. Revisit easier Zstandard setup and modularizing the writer when a real user flow requires it.
5. **Seek approval for phase two.** A complete out-of-game character creator and 3D preview need a separate design and validation phase. Current source labels and file structure are insufficient to promise faithful appearance.

The [controlled pair protocol](CONTROLLED_GAME_PAIR.md) and [experiment record](CHF_SESSION_TEMPLATE.md) specify the next in-game handoff. The [architecture](ARCHITECTURE.md) shows where later work belongs.
