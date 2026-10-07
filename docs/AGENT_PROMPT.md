# Prompt for a local agent

Work in this repository to help the user inspect or make a controlled edit to a local Star Citizen character preset. Read `AGENTS.md` and `docs/AGENT_WORKFLOW.md` first. Ask the user to select the female or male source preset if that choice is not already clear. Do not upload `.chf` files, images, or captures, and do not modify original files.

1. Ask only for information that is still needed: the selected local preset, the desired change, and any reference image or in-game observation. Keep all private files on the user's machine.
2. Use the GUI or the supported `inspect` and `diff` CLI commands to examine the chosen preset. Do not assume an `agent-context`, `agent-choices`, or recipe-composition command exists.
3. Propose one controlled experiment with its reasons and uncertainties. Use the GUI or `variant` / `variant-param` to create a new output under `outputs/`. Never replace an existing file. Inspect the resulting manifest and logical diff.
4. Report structural validity, in-game loading, saving by BioCorp, target retention, saved-copy reload, and visible effect separately. Consult `docs/VALIDATION_STATUS.md` before repeating accepted experiments. If native character-editor testing is authorized and available, execute bounded tests in that scope; otherwise give the user exact steps and wait for observed results before making visual claims. Refresh measured panels after loading. Do not start gameplay, restart the game or change system settings without relevant authorization.
5. Preserve source files unchanged and keep any personal presets, manifests, images, and captures outside Git.

This tool does not render a 3D character or calculate exact CHF values from an image. A visual reference can guide a hypothesis, but it does not directly determine file parameters.

Optional local save monitoring and captures are documented in
`docs/SAVE_MONITOR.md`. They do not automate input or establish a visual mapping.
