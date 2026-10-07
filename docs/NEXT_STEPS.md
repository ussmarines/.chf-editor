# Remaining work

The local tool already inspects and compares CHF v7/v8 files and exports narrow DNA or material experiments. The next work is ordered by evidence needed, rather than by UI size.

[Save monitoring](SAVE_MONITOR.md) now automates stable-save snapshots, field diffs
and user-labelled candidate associations, with optional local foreground-game
captures. Actual game-window capture remains to be verified on the target machine;
pixel variation does not identify a slider or validate anatomy.

The [2026-10-07 offline revalidation](MAPPING_REVALIDATION.md) authenticated historical pairs and captures, added two bounded dye-color observations, and documented provenance gaps. The remaining priorities below concern new game evidence and wider scope; repeating an archive inspection cannot supply those results.

The [validation status](VALIDATION_STATUS.md) now distinguishes UI mapping, loading, saving and visual results for every catalog observation. Guided material filters and separate status labels are implemented, as are Zstandard environment/Python-location detection and a native roundtrip check. The accepted installed presets have been identified under renamed filenames. New game observations and a broader set of proven controls remain pending; phase two is deferred.

Owner acceptance of the six positive screenshot-backed material effects is
**closed as VALIDATED** on 2026-10-07. Do not request the same visual approval
again unless the tested rendering/context changes or a new defect is reported.
The priorities below concern new candidates, missing evidence and wider scope.
The optional [REA investigation skill](REA_REVIEW.md) supplies an evidence method;
it is not a CHF parser, an anatomy oracle or a replacement for BioCorp tests.

1. **Validate each new candidate in the target game build.** Record four separate outcomes: structural validity, BioCorp loading, BioCorp saving, and visible effect. Include the build, source and output hashes, and comparable captures in private records. Existing results from another candidate or build do not transfer automatically.
2. **Collect controlled saves for more UI controls.** Save a baseline and a second file after exactly one gesture. Inspect the logical diff. If several fields change, document the group and isolate individual roles through another controlled experiment. Repeat on female and male presets where the claim is meant to cover both.
3. **Grow the evidence catalog only within proven scope.** Record source revisions, game build, structural selector, observed effect, and unresolved ambiguity. Keep private CHF files and captures out of Git.
4. **Improve guided editing from confirmed mappings.** Add user-facing controls only when their limits, context, load behavior, and save behavior have been shown. Revisit easier Zstandard setup and modularizing the writer when a real user flow requires it.
5. **Seek approval for phase two.** A complete out-of-game character creator and 3D preview need a separate design and validation phase. Current source labels and file structure are insufficient to promise faithful appearance.

The [controlled pair protocol](CONTROLLED_GAME_PAIR.md) and [experiment record](CHF_SESSION_TEMPLATE.md) specify the next in-game handoff. The [architecture](ARCHITECTURE.md) shows where later work belongs.
