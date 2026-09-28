# Local CHF Laboratory

A local Python GUI and command-line tool for inspecting Star Citizen `.chf` v7/v8 presets, comparing files, and creating controlled variants. Balanced DNA edits preserve the region's total weight. Material edits are limited to parameters already present in the source file.

This tool does not render 3D characters. Structural validation does not prove that Star Citizen loads a file, that BioCorp saves it, or that a change has a visible effect.

## Privacy

This public repository contains no character presets, game files, screenshots, or videos. Default and custom character files, experiment manifests, and extracted game data are private and are not included. Local outputs belong under `outputs/`, which is excluded from Git. The public evidence catalog omits private file fingerprints and links to the published limitations in [the experiment notes](docs/EXPERIMENTS.md#published-evidence-catalog).

Before publishing changes, review the full diff for secrets, personal data, machine-specific paths, and private character data. GitHub secret scanning and push protection are enabled; the changed-file workflow also checks only files in each push or pull request. These safeguards cannot guarantee that every form of sensitive data is detected.

## Requirements

- Windows and Python 3. Tkinter is required for the GUI.
- A compatible native Zstandard library (`libzstd.dll`) is required for CHF operations.
- The test suite uses Python's standard `unittest` library.

## Quick start

```powershell
git clone https://github.com/ussmarines/.chf-editor.git
cd .chf-editor
python -m unittest discover -s tests -v
python gui.py
```

In the GUI, browse for the Zstandard DLL and open local female and male presets. The application provides six tabs: Overview, DNA, ItemPorts, Materials, Diff, and Evidence. The Evidence tab shows available mappings and their limits. No game folder or machine-specific path is assumed.

## Command-line examples

Every CHF command accepts `--zstd-dll` with the path to your library:

```powershell
$dll = 'C:\path\to\libzstd.dll'
python chf.py --zstd-dll $dll inspect 'C:\presets\character.chf'
python chf.py --zstd-dll $dll diff 'C:\presets\before.chf' 'C:\presets\after.chf'
python chf.py --zstd-dll $dll variant 'C:\presets\default_women.chf' 'C:\outputs\nose-test.chf' --part Nose --slot 0 --balance-slot 1 --value 12000 --game-version 'LIVE build' --control 'manual Nose weight experiment'
```

`variant` changes two balanced DNA weights in one region. `variant-param` changes one existing material value and requires the current source SHA-256 plus the field indices and hash. The CLI supports `inspect`, `diff`, `variant`, and `variant-param`; it does not provide an agent automation or recipe-composition command. Commands refuse to overwrite existing outputs and create an experiment manifest.

The reader checks the fixed file size, CRC32C, decompression limits, v7/v8 structure, and payload consumption. Exports are re-read and their logical diff is checked. Always keep original files unchanged.

The tests that exercise CHF read/write operations require local paths in `CHF_TEST_SOURCE` and `CHF_ZSTD_DLL`. Private presets and the Zstandard library are not included. Tests that do not need those files still run normally.

## Evidence and in-game checks

Report these separately: structural validity, in-game loading, saving by the game, and observed visual effect. Field names and observations from one preset do not establish the same effect on another. BioCorp checks require in-game validation and comparable captures.

- [Controlled in-game pair protocol](docs/CONTROLLED_GAME_PAIR.md)
- [Experiment workflow and evidence limits](docs/EXPERIMENTS.md)
- [Agent workflow](docs/AGENT_WORKFLOW.md)
- [Security policy](SECURITY.md)
- [Contribution guide](CONTRIBUTING.md)

## License

The source code is licensed under the [PolyForm Noncommercial License 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0). Commercial use is prohibited; copies and modified derivatives may only be used and distributed for permitted noncommercial purposes under its terms. Forks and redistributed copies must preserve the copyright and attribution notice in [`LICENSE`](LICENSE). Public repositories can be forked through GitHub's service; the license governs permitted use and redistribution of the code.

## Support

[Support this project via PayPal](https://paypal.me/ussmarinesdot)
