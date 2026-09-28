# Contributing

Contributions are welcome: bug reports, documentation corrections, focused code changes, and reproducible findings about the CHF format.

## Before you contribute

- Read the [README](README.md), [security policy](SECURITY.md), and [license](LICENSE). The project permits noncommercial use under the PolyForm Noncommercial License 1.0.0; preserve the required notice in redistributed copies and forks.
- Open an issue for a substantial change so its scope and evidence can be discussed before implementation.
- Submit only work you have the right to contribute. By opening a pull request, you agree that your contribution may be distributed under this project's PolyForm Noncommercial License 1.0.0.
- Do not submit `.chf` presets, game files or extracts, experiment manifests, screenshots, videos, credentials, email addresses, or personal machine paths. Use synthetic examples and place private local work under `outputs/`.

## Submit a pull request

1. Create a focused branch and describe the change and why it is needed.
2. Run checks relevant to the files you changed. For Python changes, use `python -m unittest discover -s tests -v`; tests that require private CHF inputs use `CHF_TEST_SOURCE` and `CHF_ZSTD_DLL` and may be skipped when those files are unavailable.
3. Review the entire diff for private data and generated files before pushing.
4. Open a pull request and state what you checked, what remains unverified, and any user-visible effect.

The GitHub Actions workflow checks changed paths for whitespace and common private-data patterns. It is intentionally limited to changed files to conserve CI minutes.

## Evidence in reports

Keep these claims separate: structural validity, in-game loading, saving by the game, and visible effect. When proposing a field mapping, provide the source and the level of proof. A label or hash alone does not establish an anatomical effect.

For vulnerabilities or accidental disclosure, use the private reporting route described in [SECURITY.md](SECURITY.md).
