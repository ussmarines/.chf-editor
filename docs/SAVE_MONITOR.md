# Monitoring saves and optional local game captures

Open **Monitor saves** in CHF Editor. Choose a CHF just saved from the intended
character, enter the exact control being tested and the game build, then start.
Change one control in BioCorp and save. The monitor compares each stable save
with the previous accepted snapshot, displays the diff and names known material
fields, and archives the pair and JSON report under ignored `outputs/monitor/`.
It never writes to the watched file or promotes the public evidence catalog.

Default mode watches the chosen file, suitable for saving over the same test
filename. Enable new-file detection for **Save as** in its folder. Monitoring is
nonrecursive, limited to 256 CHF files, and pauses if multiple files change or a
different body/voice/version appears. Use a test filename and retain your original.
One-second polling plus one second of stable contents gives approximately two
seconds of detection delay on an otherwise idle system. Faster intervening saves
can be missed; wait for the reported diff before making the next gesture.
Incomplete, locked and invalid-CRC files are retried without replacing the baseline.

The control name and build are user-reported and frozen at session start. For a
different control, stop, select the latest saved CHF and restart. No screen
recognition establishes the gesture name. A single parameter or DNA region yields
a **candidate association**; changes across groups remain **ambiguous**. Returning
the slider to its starting position provides an additional inverse pair. Neither
case alone proves anatomy, a safe range, successful reload or a visible effect.

## Optional screen capture

Install the optional pinned dependency in the Python environment that launches
the GUI:

```powershell
python -m pip install -r requirements-monitor.txt
python gui.py
```

To open monitoring setup with capture preselected, run
`python gui.py --monitor --capture`. Capturing begins only after **Démarrer**.
The optional `--preset`, `--zstd-dll` and `--game-build` arguments prefill setup.

Enable the capture checkbox before starting and keep **Star Citizen in the
foreground**. The application samples that game's window approximately once per
second, displays a whole-window pixel-change metric, and stores before/after PNGs
only alongside detected save events. A bounded in-memory buffer also keeps the
last ten successful captures. Each detected save archives the buffered frames
since the previous save in `NNNN-sequence/`, as JPEG quality 90 with a timestamped
`index.json`. This can show the gesture leading up to the file diff; it is not a
continuous video stream to an agent or automatic marker recognition. Long gaps
or gestures between samples may be absent. Captures are local and resized to fit
1920 x 1080. The first successful capture or the previous saved capture provides
the before image; it is not synchronized with slider movements. Wait for an active
capture before the first gesture. No image is sent to an external service.

The capture verifies the foreground executable is `StarCitizen.exe` using the
[Windows foreground-window API](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getforegroundwindow)
and process identity, then uses
[Pillow's HWND capture](https://github.com/python-pillow/Pillow/blob/12.1.0/docs/releasenotes/11.2.1.rst).
If direct window capture is blank or fails, the application instead captures the
visible game client area, with physical-pixel coordinates and multi-monitor
support. Foreground identity and window position are checked around that capture;
focus/position changes discard the result. It does not switch to another
foreground application. Keep the game unobscured: overlays within the game area
may appear in this fallback. The UI and save records identify `window` versus
`visible_game_area`. Capture errors and recoveries are recorded locally in
`capture-log.jsonl`, and the save's screen record includes its exact error.
Captured pixels include menus, animation, view changes and lighting: the metric
is not a face-shape measurement, OCR, slider identification or visual validation.

Native game capture was **not executed in the development agent session**, where
native computer APIs were disabled. Synthetic pixel tests and file-monitoring
tests do not establish that Star Citizen's rendered window can be captured. Verify
that the first recorded PNG shows BioCorp before relying on the capture record.

File monitoring works without Pillow. All populated sessions, CHF snapshots,
images and machine-specific launchers remain private under `outputs/`. No runtime
attachment, input automation, game modification or complete character creator is
included.
