# REA skill review and project scope

Reviewed and installed instructions on 2026-10-07 from
[`morluto/rea`](https://github.com/morluto/rea), pinned to
[`dda8e6a72890f87bdf8bbd3250b68b6648aae553`](https://github.com/morluto/rea/commit/dda8e6a72890f87bdf8bbd3250b68b6648aae553).
Upstream skill metadata: version `27`; repository package declares `4.1.0`.
No REA package or engine binary was installed, so neither is an installed-runtime
version. The six Markdown instruction files are copied unchanged under
`.agents/skills/reverse-engineer-anything/`, with the upstream MIT notice.

## Review verdict

**CAUTION: useful optional instructions, not approval for the full runtime.**
SkillSpector was not available on PATH; no automated SkillSpector scan ran.
Manual review covered the complete six-file skill, referenced workflows,
upstream package manifest and license. The installed scope contains no script,
dependency manifest, executable, hook, MCP registration or hidden persistence.
This is not a security certification of REA's server, providers or supply chain.

The official skill quick validator was blocked by missing `PyYAML`; no dependency
was installed to bypass that limit. A newline-normalized comparison confirmed all
six installed instruction files and the MIT notice match the pinned source.

The instructions include network-enabled `npx ...@latest` setup/diagnostic
examples, optional application/process capture, artifact extraction and provider
database annotations. These have effects beyond reading instructions. Upstream
wording that an operation needs no separate permission flag does not authorize it
in this project. Root `AGENTS.md`, privacy, host permissions and the user's exact
request take precedence. No upstream script, installer, `doctor`, `setup`, MCP
server or provider was executed during this review.

## Fit for CHF work

- Useful for a future authorized investigation where existing source and the CHF
  parser cannot explain a shipped binary's behavior, with a specific local target
  and a suitable already available analysis provider.
- Useful now as an evidence method: distinguish observation, inference and unknown;
  reuse compatible results; scope comparisons; preserve contradictory/negative
  evidence; report missing authorities instead of inventing a conclusion.
- Not needed to analyze this complete Python source repository, record screenshot
  acceptance, parse `.chf` files, infer individual head anatomy, or render a faithful
  character. REA itself says to skip ordinary source-repository architecture work.
- Not authorization to inspect or attach to Star Citizen, access the game directory,
  install Ghidra/Java/Hopper/IDA, alter global agent configuration or export private
  characters, captures, game assets or populated experiment manifests.

## Applied in the current task

The evidence method separates six capture-supported positive material effects
accepted by the owner from ambiguous effects, captured negative results, missing
game-save authentication and experiments not yet tested. The
[validation status](VALIDATION_STATUS.md#owner-visual-acceptance-2026-10-07)
and catalog record that distinction. Existing accepted private exports remain
unchanged. Local tests check positive filtering/counts, negative exclusion,
reference scope and the GUI's explicit owner-validation label.

This uses the skill's investigation method, not an REA tool invocation. No REA
Evidence IDs, decompilation results, runtime captures, new anatomical mappings or
game-session PASS are claimed. Native discovery is available on the next turn of
an agent session rooted in this repository, not a SpaceShooter session; the
instruction files have already been read for this task.
