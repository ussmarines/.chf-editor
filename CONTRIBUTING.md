# Contributing

## Local checks

The application uses Python 3 and the standard library. Its tests use `pytest`:

```powershell
python -m pytest -q
```

Run checks relevant to the files you changed. The GitHub Actions workflow also checks only files changed by a pull request or push for whitespace and common private-data patterns.

## Protect private data

Do not commit character presets (`.chf`), experiment manifests, game files or extracts, private images, screenshots, videos, credentials, or personal machine paths. Keep local research artifacts in the ignored `outputs/` directory. Use synthetic fixtures for tests.

## Pull requests

Use a `codex/` or descriptive feature branch and explain user-visible changes, evidence, limitations, and the checks run. Do not claim that structural validation establishes game loading, game saving, or a visual effect; report those evidence states separately.
