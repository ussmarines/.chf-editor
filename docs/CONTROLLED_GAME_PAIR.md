# First controlled pair in Star Citizen

Goal: connect **one visible control** to its CHF diff on a recorded LIVE build without inferring an effect from a hash name. Keep both `default_*.chf` source files unchanged.

## In-game steps

1. Copy `default_women.chf` to a private backup folder **outside the game directory** and record its SHA-256. Keep the original unchanged.
2. Load the character in BioCorp. Without changing any control, save a new copy named `lab_woman_00_baseline.chf`.
3. Choose **one** clearly named slider, preferably `Freckles Amount` if available. Record its tab and before/after values. Change only this slider by a noticeable amount; do not change the hairstyle, color, DNA, or any other option. Save a second copy named `lab_woman_01_one_control.chf`.
4. Capture both states at a matching angle, zoom, and lighting. Record whether both files reload and whether saving succeeds.
5. Provide the local paths to the two `.chf` files, the captures, and the control name and values. The files can stay in a private local folder; they do not belong in Git.

## What the laboratory checks

`chf.py diff` checks the CRC, Zstandard payload, v8 structure, and all logical differences. If the game save also changes other fields (normalization, timestamps, equipment), the pair remains **ambiguous** and should be repeated. A visible effect and a simple diff can support a mapping as “confirmed for this build.” Repeat the protocol for the male profile and other control families before generalizing.

Detailed game captures and experiment files are private and intentionally omitted from this public repository. Public evidence summaries and their limits are in [the experiment notes](EXPERIMENTS.md#published-evidence-catalog).
