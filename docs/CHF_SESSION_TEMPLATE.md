# Private CHF session record template

Copy this template into an ignored `outputs/` file for each meaningful experiment. It is a human evidence record; the CLI also writes a machine-readable `.experiment.json` next to an output. Never commit a populated record that identifies a private preset or local path.

```text
Date:
Goal and single control under test:
Game branch and exact build:

Source file (private):
Source provenance and status (game-saved / donor / tested base):
Source SHA-256:
Source size and internal version:
Original preserved at:

Tool name, version or commit:
Zstandard library version:
Source CRC32C / compressed size / decompressed size:
DNA region count and blends per region:
ItemPort declared and parsed node counts:
Material, submaterial, texture, float and color counts:
Opaque header and container tail recorded:

Intentional change, before -> after:
Evidence for field mapping (source and proof level):
Fields and opaque regions explicitly preserved:
Expected logical diff:

Output file (private):
Output SHA-256:
4096 bytes / CRC32C / Zstandard / full parse: PASS | FAIL | NOT TESTED
Independent re-read and expected diff: PASS | FAIL | NOT TESTED
Unexpected changes:

Game preset detected: PASS | FAIL | NOT TESTED
Game load: PASS | FAIL | NOT TESTED
Editor stable: PASS | FAIL | NOT TESTED
Game save: PASS | FAIL | NOT TESTED
Game-saved output SHA-256, if obtained:
Target values retained on independent saved-file re-read: PASS | FAIL | NOT TESTED
Other save normalization compared with baseline (textures by index):
Saved-copy reload: PASS | FAIL | NOT TESTED
Values after reload and refreshed panel:
Comparable front / three-quarter / profile captures (private):
Observed visual effect: CONFIRMED | NONE SEEN | AMBIGUOUS | NOT TESTED

Decision: keep as experiment | game-tested base | reject
Last known working base for rollback:
Unresolved questions and next controlled test:
```

Use `UNKNOWN` for an unknown field or cause. A generated file is never marked game-tested from structural checks alone.
