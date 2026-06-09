# Play State Bool

## Status: Completed

## Context

The motion callback used `playing` as an implicitly unwrapped optional Bool and
force-cast it before deciding whether to call `play()` or `stop()`. The state is
always initialized locally, so optional storage only made the legacy motion path
more fragile.

## Objectives

- Preserve the existing motion-triggered play/stop behavior.
- Keep `playing` as concrete local game state.
- Reject regressions that reintroduce implicitly unwrapped play state.
- Keep the static verification surface available through `make check`.

## Work Completed

- Replaced the implicitly unwrapped `playing` property with a concrete Bool.
- Removed the forced Bool cast from the motion callback.
- Extended `scripts/check_ios_contracts.py` to guard the play-state contract.
- Updated README, VISION, and CHANGES with the new guardrail.

## Verification

- `python3 scripts/check_ios_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add manual device notes for the motion thresholds.
- Replace the remote prompt endpoint with a configurable or local demo source.
