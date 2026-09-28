# CHF Editor

**Inspect, compare, and make controlled changes to Star Citizen character presets.**

CHF Editor is a local Python application for `.chf` v7/v8 files. It offers a graphical interface and a command-line tool for examining a preset, comparing two saves, and creating a narrowly scoped experiment. It does not include character presets or game assets.

> [!IMPORTANT]
> A structurally valid file is not proof that Star Citizen will load it, save it, or show the intended visual change. Test those outcomes separately in the game.

## What you can do

| Task | Available now |
| --- | --- |
| Explore a preset | View its structure, DNA regions, ItemPorts, materials, and available evidence in the GUI. |
| Compare two saves | Inspect their logical differences with the `diff` command or GUI. |
| Test a DNA change | Change one weight and balance it with another weight in the same region. |
| Test a material change | Change one existing float or color component with an exact source SHA-256 guard. |
| Validate an export | Check size, CRC32C, Zstandard bounds, v7/v8 structure, and the expected logical diff; re-read the result independently. |

The tool preserves the original input and refuses to overwrite an existing output. It does not render characters, compose complete recipes, or infer the visual meaning of an unverified field.

## Get started

**Requirements:** Windows, Python 3, Tkinter for the GUI, and a compatible native Zstandard DLL (`libzstd.dll`) for CHF operations. Bring your own legally obtained `.chf` files; none are distributed here.

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

| Guide | Purpose |
| --- | --- |
| [Controlled game comparison](docs/CONTROLLED_GAME_PAIR.md) | Make comparable before/after saves and captures. |
| [CHF format](docs/CHF_FORMAT.md) | Understand the supported v7/v8 container and payload. |
| [Editing workflow](docs/CHF_EDITING_WORKFLOW.md) | Preserve a source, make one change, and validate each result. |
| [Experiments and evidence](docs/EXPERIMENTS.md) | Understand the published evidence and its limits. |
| [Agent workflow](docs/AGENT_WORKFLOW.md) | Run bounded experiments with clear provenance. |
| [Tools and skills](docs/TOOLCHAIN.md) | Find official sources and set up a fork. |
| [Archive integration](docs/STARFALL_ARCHIVE_IMPORT.md) | See what was retained from the supplied Starfall research. |
| [Security policy](SECURITY.md) | Report vulnerabilities privately. |

## Contribute

Contributions are welcome. Open an issue for a proposal or submit a pull request with a focused change, relevant checks, and a clear description of evidence and limitations. Read the [contribution guide](CONTRIBUTING.md) before submitting. Please do not include private character files or personal data.

## License and support

The code is available under the [PolyForm Noncommercial License 1.0.0](LICENSE). Contributions and forks must respect its noncommercial terms and preserve the required copyright and attribution notice. You may support the project through [PayPal](https://paypal.me/ussmarinesdot).
