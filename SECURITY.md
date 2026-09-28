# Security policy

## Reporting a vulnerability

Please report security issues privately through GitHub's **Report a vulnerability** feature for this repository. Do not open a public issue containing credentials, private character files, game assets, screenshots, or other personal data.

This project is a local CHF research and editing tool. It does not provide a hosted service. Security reports should include the affected commit, a concise impact description, and a minimal reproduction with all private data removed.

## Private data

Do not commit `.chf` presets, experiment manifests, game assets or extracts, videos, screenshots, credentials, or machine-specific paths. The public repository's changed-file workflow checks modified paths for these common artifact and personal-data patterns; it is a safeguard, not a guarantee that every secret can be detected.
