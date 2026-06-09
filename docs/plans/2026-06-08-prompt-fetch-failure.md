# Prompt Fetch Failure

## Status: Completed

## Context

The URL client reported invalid URLs and failed responses through its
`succeeded` callback flag, but `ViewController.play()` ignored that flag. A
failed or empty remote prompt response could still hide the spinner, show empty
game text, and mark the app as playing.

## Objectives

- Preserve the motion-triggered play/stop flow.
- Keep the remote prompt endpoint explicit.
- Show visible fallback text when prompt fetching fails.
- Keep `playing` false unless a non-empty prompt is loaded.
- Extend static checks to preserve the failure path.

## Work Completed

- Checked `succeeded` and `data.length` before displaying prompt text.
- Added a `Prompt unavailable` fallback.
- Kept `playing` false for failed or empty prompt responses.
- Extended `scripts/check_ios_contracts.py` and updated README, VISION, and
  CHANGES.

## Verification

- `python3 scripts/check_ios_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Replace the remote prompt endpoint with a configurable or local demo source.
- Add manual verification notes for motion thresholds.
