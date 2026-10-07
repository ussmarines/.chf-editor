# Tools, sources, and agent skills

This page lists the public tools and source projects referenced by CHF Editor. A fork contains the Python application, its tests, documentation, and GitHub configuration. The external projects below are linked to their original Git repositories; no third-party binaries, game data, private presets, or private research files are bundled.

## Run the application

| Tool | Role | Official source | Needed by a fork? |
| --- | --- | --- | --- |
| Python 3 | Runs `gui.py`, `chf.py`, and the standard-library test suite. Tkinter is part of compatible Python installations. | [python/cpython](https://github.com/python/cpython) | Yes. Check that `python -m tkinter` opens a window before using the GUI. |
| Zstandard (`libzstd.dll`) | Reads and writes the compressed CHF payload through the native library. | [facebook/zstd](https://github.com/facebook/zstd) | Yes for CHF operations. Supply a compatible Windows DLL yourself and select it in the GUI or pass `--zstd-dll` to the CLI. |
| Git | Clones the repository and manages contributions. | [git/git](https://github.com/git/git) | Needed to clone or contribute; not needed to run an already downloaded copy. |

Core CHF operations have no pip dependency manifest: they use Python's standard library plus a locally supplied native Zstandard library. Optional window captures have the pinned `requirements-monitor.txt` manifest described below. The tests use `unittest`; private file based tests need local `CHF_TEST_SOURCE` and `CHF_ZSTD_DLL` values. See the [README](../README.md) for usage.

## Research references

These projects informed the field and format research. They are **not runtime dependencies** and are not bundled with this repository.

| Project | Official repository | Source revision documented here |
| --- | --- | --- |
| StarBreaker | [diogotr7/StarBreaker](https://github.com/diogotr7/StarBreaker) | [`08302fbdd3a1cc704a0bc0977fb1841927a637bf`](https://github.com/diogotr7/StarBreaker/commit/08302fbdd3a1cc704a0bc0977fb1841927a637bf) |
| StarChar | [diogotr7/starchar](https://github.com/diogotr7/starchar) | [`2c4bace845a4004c78b50a7ed902a725545aa5e7`](https://github.com/diogotr7/starchar/commit/2c4bace845a4004c78b50a7ed902a725545aa5e7) |

Use the upstream repositories' own licenses if you download or reuse their code. A source revision is separate from the version of any binary you run. Their labels and names do not, by themselves, prove a visual or anatomical effect in Star Citizen.

## Optional agent workflow

None of the agent tools below are required to run CHF Editor. They are not included in the public package, so a fork owner can choose and install them independently.

| Tool or skill | Why it appears in this project | Official repository |
| --- | --- | --- |
| OpenAI Codex | Agent instructions for contributors live in `AGENTS.md`. | [openai/codex](https://github.com/openai/codex) |
| Project Brain skills: `brain-setup`, `brain-page`, `brain-ingest`, `brain-bootstrap` | `BRAIN.md`, `AGENTS.md`, and `CLAUDE.md` describe this optional persistent decision workflow. The `brain-page` skill supplies the `brain` CLI. | [mindmuxai/brain.md](https://github.com/mindmuxai/brain.md/tree/main/skills) |
| Context7 MCP | Agent instruction to consult current library and API documentation. | [upstash/context7](https://github.com/upstash/context7) |
| Graphify | Optional local code navigation; no hook or watcher is installed by this repository. | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) |

The fork **does** include three project-local skills: [`chf-editor`](../.agents/skills/chf-editor/SKILL.md) for navigation, [`chf-structural-variant`](../.agents/skills/chf-structural-variant/SKILL.md) for bounded edits, and the optional [`reverse-engineer-anything`](../.agents/skills/reverse-engineer-anything/SKILL.md) investigation instructions. The first two are documented in [the archive integration note](STARFALL_ARCHIVE_IMPORT.md); REA's pinned source, MIT notice and restricted use are in [its review](REA_REVIEW.md). REA's CLI, MCP server and analysis engines are not installed or bundled. Install an agent that understands project-local `SKILL.md` files if you want to invoke them; the Python application does not depend on an agent.

Get a compatible native Zstandard library from the [official Zstandard source and releases](https://github.com/facebook/zstd/releases). Supply its DLL path explicitly; this repository does not download or bundle third-party binaries. No Python framework or pip package is needed for core CHF operations.

Core inspection, editing and save monitoring use the standard library. Optional
local game-window screenshots require Pillow, pinned in
[`requirements-monitor.txt`](../requirements-monitor.txt). See
[monitor setup and capture limitations](SAVE_MONITOR.md).

An owner-driven 2026-10-07 monitor retest authenticated captured BioCorp images
and a before/after save pair using the visible-game-area fallback. This is a
scoped capture success, not general graphics-mode compatibility or automatic UI
recognition. Native character-editor input used for the separate validation
suite belongs to the agent session; CHF Editor does not bundle an input driver.

Alternatively, set `CHF_ZSTD_DLL` once in your shell and omit `--zstd-dll`. The GUI's **Detect / check** button checks required exports and a real compression/decompression roundtrip, and displays the loaded library version. Detection searches the environment and standard Python executable/DLL/library locations; it does not recursively scan the computer or install a library. An invalid explicit or environment path is rejected rather than silently replaced. The version function and compression API are documented in the [official Zstandard manual](https://facebook.github.io/zstd/zstd_manual.html); Tkinter selection handling follows the [Python ttk documentation](https://docs.python.org/3/library/tkinter.ttk.html).

The public repository intentionally omits the local `brain/` pages because they contain private experiment provenance. To use Project Brain in a fork, obtain the skills from the upstream repository, then run `node <brain-page-skill>/bin/brain.mjs init` from your fork's root and create your own pages. The application works without this agent workflow.

## Native-library tests

The native roundtrip test needs `CHF_ZSTD_DLL` in the test process environment;
otherwise its `SKIPPED` result means the library was not configured, not that
Zstandard is broken. An existing compatible library is sufficient. In PowerShell:

```powershell
$env:CHF_ZSTD_DLL = 'C:\path\to\libzstd.dll'
python -m unittest discover -s tests -p test_zstd_runtime.py -v
```

The command must finish with three tests passing and no skipped native check.
For full private-fixture tests, also provide `CHF_TEST_SOURCE` for the selected
local female or male reference, then run `python -m unittest discover -s tests -v`.
Keep machine-specific launchers/configuration under ignored `outputs/`, scope
environment changes to that invocation and restore previous values afterwards.
Do not modify global environment settings or unrelated projects to configure CHF.

## GitHub features in a fork

The fork inherits [`.github/dependabot.yml`](../.github/dependabot.yml) for monthly GitHub Actions version update checks and the [changed-file workflow](../.github/workflows/changed-files.yml). That workflow runs on pull requests and `main` pushes, checking changed paths only to conserve Actions minutes. GitHub account settings, branch protection, security features, and repository-level Actions permissions may need to be enabled separately by the fork owner. Use the [GitHub documentation](https://github.com/github/docs) for those settings.

The [funding file](../.github/FUNDING.yml) points to the original project's PayPal page. Fork owners should review that link for their own repository. The copyright and attribution notice in [`LICENSE`](../LICENSE) must be retained when the code is redistributed under its terms.
