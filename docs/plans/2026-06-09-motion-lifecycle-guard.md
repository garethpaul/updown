# Motion Lifecycle Guard

## Status: Completed

## Context

The game starts CoreMotion device-motion updates in `begin()`, but the view did
not stop those updates when leaving the screen. Returning to the view also needs
to avoid starting duplicate motion callbacks.

## Objectives

- Preserve the motion-triggered play and stop flow.
- Restart motion updates when the game view appears.
- Skip duplicate motion update registration when updates are already active.
- Stop motion updates when the game view disappears.
- Add static checker coverage for the motion lifecycle contract.

## Work Completed

- Added `viewWillAppear` to resume motion setup through `begin()`.
- Made `begin()` return early when device-motion updates are already active.
- Added `viewWillDisappear` to stop device-motion updates and clear play/fetch
  state.
- Extended the static checker and updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_ios_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add manual device verification notes for motion thresholds.
- Add a local prompt fallback list for offline play.
