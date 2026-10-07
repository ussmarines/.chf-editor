# Agent-assisted workflow

An agent that can read local files and run commands can assist with this project. The CHF editor itself requires no AI provider or API key. The application does not upload files.

## Supported workflow

1. Keep `.chf` presets, images, captures, and experiment manifests under the locally ignored `outputs/` directory or outside the repository. Preserve source files byte for byte.
2. Ask the user to choose a female or male preset when it is not already clear. These presets are expected to be supplied locally; the public repository does not include them.
3. Select the Zstandard library in the GUI, or pass it with `--zstd-dll` to the CLI. The supported CLI commands are `inspect`, `diff`, `variant`, and `variant-param`.
4. Inspect the selected file first. Propose a limited experiment with reasons and uncertainty. `variant` adjusts two DNA weights in one region while preserving the region total. `variant-param` changes one existing material float or color channel and requires the source SHA-256 and exact field coordinates.
5. Export to a new local path under `outputs/`. The writer refuses to overwrite a file, creates an experiment manifest, re-reads the export, checks structural integrity, and reports the logical diff.
6. Treat an output as structurally checked only. Any in-game load, game save, or visible result must be observed and reported separately. Compare captures only when angle, zoom, lighting, and hairstyle are controlled.

The current CLI does not provide `agent-context`, `agent-choices`, `compose`, or a JSON recipe runner. Do not document or claim these capabilities unless they are implemented and released.

## Privacy and evidence

Do not send character files, reference images, captures, or experiment manifests to a remote agent or commit them to Git. The public evidence catalog contains bounded summaries, not the private source files or their SHA-256 fingerprints. Its mappings are specific to their recorded structural context and do not establish the same effect on another preset. See [the experiment protocol](EXPERIMENTS.md#published-evidence-catalog).

An image can guide a hypothesis but cannot directly determine CHF values. No faithful standalone 3D preview is provided.

## Authorized local game validation

Read [current validation status](VALIDATION_STATUS.md) before repeating accepted
experiments. Native character-editor tests may be performed when the user has
authorized them and the session exposes suitable controls. Keep that scope
explicit: permission to test the editor does not authorize gameplay, game
restarts, unrelated applications or system changes. Parallel agents should
analyze files or documentation while one agent controls the UI.

Refresh the measured panel after loading; Hair > Color can retain stale values.
Record variant loading, observed saving, exact target retention and saved-copy
reload separately. Compare texture entries by their index when BioCorp inserts
a texture, and separate baseline colour quantization from the target change.
The [save monitor](SAVE_MONITOR.md) can archive local evidence, but its control
labels are user-supplied candidate associations rather than recognition.

## Optional binary investigation

The project-local REA skill is an optional evidence-driven investigation guide,
not a runtime dependency. Its [review and limits](REA_REVIEW.md) explain when it
helps. Use normal project tools for source analysis, CHF parsing and screenshot
acceptance. Binary/runtime access, installation of external engines and MCP
configuration are separate operations requiring an explicit relevant scope.
Character evidence and accepted results belong here, not in SpaceShooter.
