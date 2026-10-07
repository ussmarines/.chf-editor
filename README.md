# CHF Editor — Star Citizen Character Preset Inspector & Controlled Editor

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows-0078D4?logo=windows11&logoColor=white)](#requirements)
[![Star Citizen CHF](https://img.shields.io/badge/Star%20Citizen-CHF%20v7%2Fv8-111827)](#what-you-can-do)
[![Changed files](https://github.com/ussmarines/.chf-editor/actions/workflows/changed-files.yml/badge.svg)](https://github.com/ussmarines/.chf-editor/actions/workflows/changed-files.yml)
[![License](https://img.shields.io/badge/license-PolyForm%20Noncommercial%201.0.0-2563EB)](LICENSE)

**Inspect, diff, validate, and make narrowly scoped changes to Star Citizen `.chf` character presets (v7/v8) with a local Python GUI and CLI.**

CHF Editor is a public-source **Star Citizen character preset tool** for examining `.chf` files, comparing character DNA presets, exploring DNA regions and weights, inspecting ItemPorts and materials, and creating controlled variants. It is designed for reproducible technical investigation rather than blind preset rewriting.

The application runs locally on Windows, preserves the original input, refuses to overwrite an existing output, and does **not** include character presets, extracted game files, or game assets.

> [!NOTE]
> CHF Editor is an unofficial community project and is not affiliated with or endorsed by Cloud Imperium Games.

> [!IMPORTANT]
> A structurally valid file is not proof that Star Citizen will load it, save it, or show the intended visual change. Test those outcomes separately in the game.

## At a glance

| | |
| --- | --- |
| **Game / format** | Star Citizen character presets, CHF v7/v8 |
| **Interfaces** | Tkinter GUI and Python CLI |
| **Core workflows** | Inspect, compare/diff, controlled DNA variants, controlled material variants, validation |
| **Platform** | Windows |
| **Compression** | Zstandard through a compatible native `libzstd.dll` |
| **Data model** | Local-first; bring your own legally obtained `.chf` files |
| **License** | PolyForm Noncommercial License 1.0.0 |

## What you can do

| Task | Available now |
| --- | --- |
| Explore a Star Citizen character preset | View its structure, DNA regions, ItemPorts, materials, and available evidence in the GUI. |
| Compare two CHF files | Inspect logical differences with the `diff` command or GUI. |
| Test a DNA change | Change one weight and balance it with another weight in the same region. |
| Test a material change | Change one existing float or color component with an exact source SHA-256 guard. |
| Validate an export | Check size, CRC32C, Zstandard bounds, v7/v8 structure, and the expected logical diff; re-read the result independently. |

The tool does not render characters, compose complete character recipes, automatically infer visual meaning from unverified fields, or act as a general-purpose save editor.

## Get started

### Requirements

- Windows
- Python 3
- Tkinter for the GUI
- A compatible native Zstandard DLL (`libzstd.dll`) for CHF operations
- Your own legally obtained Star Citizen `.chf` character preset files

Clone and launch the GUI:

```powershell
git clone https://github.com/ussmarines/.chf-editor.git
cd .chf-editor
python gui.py
```

In the GUI, select your Zstandard DLL and browse for local presets. The tabs cover **Overview**, **DNA**, **ItemPorts**, **Materials**, **Diff**, and **Evidence**. No game installation path is built into the application.

### Command-line examples

Set the DLL path once in your PowerShell session:

```powershell
$dll = 'C:\path\to\libzstd.dll'
python chf.py --zstd-dll $dll inspect 'C:\presets\character.chf'
python chf.py --zstd-dll $dll diff 'C:\presets\before.chf' 'C:\presets\after.chf'
```

Create a single controlled DNA experiment:

```powershell
python chf.py --zstd-dll $dll variant 'C:\presets\source.chf' 'C:\presets\nose-test.chf' --part Nose --slot 0 --balance-slot 1 --value 12000 --game-version 'LIVE build' --control 'manual Nose weight experiment'
```

The CLI also provides `variant-param` for one existing material value. Run `python chf.py variant-param --help` for its required source hash, field indices, and value options. Every export includes an experiment manifest; keep it with your local test files.

## Evidence and safety

Report four results independently: **file structure**, **loading in the game**, **saving by the game**, and **visible effect**. A field name or a result from one preset does not establish the same behavior for another preset.

Keep presets, manifests, screenshots, videos, and extracted game files private. Store local experiments under `outputs/`, which Git excludes. Review your changes before opening a pull request; automated checks look for common sensitive patterns in changed files but cannot detect everything.

## Documentation

| Guide | Purpose |
| --- | --- |
| [Controlled game comparison](docs/CONTROLLED_GAME_PAIR.md) | Make comparable before/after saves and captures. |
| [CHF format](docs/CHF_FORMAT.md) | Understand the supported v7/v8 container and payload. |
| [Editing workflow](docs/CHF_EDITING_WORKFLOW.md) | Preserve a source, make one change, and validate each result. |
| [Architecture](docs/ARCHITECTURE.md) | See the reader, evidence catalog, writer, and GUI boundaries. |
| [Remaining work](docs/NEXT_STEPS.md) | Follow the phase-one validation and mapping priorities. |
| [Experiments and evidence](docs/EXPERIMENTS.md) | Understand the published evidence and its limits. |
| [Mapping revalidation](docs/MAPPING_REVALIDATION.md) | Review rechecked historical observations, source-label coverage, and provenance gaps. |
| [Agent workflow](docs/AGENT_WORKFLOW.md) | Run bounded experiments with clear provenance. |
| [Tools and skills](docs/TOOLCHAIN.md) | Find official sources and set up a fork. |
| [Archive integration](docs/STARFALL_ARCHIVE_IMPORT.md) | See what was retained from the supplied Starfall research. |
| [Security policy](SECURITY.md) | Report vulnerabilities privately. |

## Contribute

Contributions are welcome: bug reports, documentation corrections, focused code changes, and reproducible findings about the CHF format.

Open an issue for a proposal or submit a pull request with a focused change, relevant checks, and a clear description of evidence and limitations. Read the [contribution guide](CONTRIBUTING.md) before submitting. Please do not include private character files or personal data.

## License and support

The code is available under the [PolyForm Noncommercial License 1.0.0](LICENSE). Contributions and forks must respect its noncommercial terms and preserve the required copyright and attribution notice.

You may support the project through [PayPal](https://paypal.me/ussmarinesdot).
