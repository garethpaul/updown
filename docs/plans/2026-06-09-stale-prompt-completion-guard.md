# Stale Prompt Completion Guard

## Status: Completed

## Context

The prompt fetch path already prevents duplicate in-flight requests and clears
state when the game view disappears. A network completion could still arrive
after disappearance and update the label, spinner, or play state from a stale
request.

## Objectives

- Preserve successful remote prompt loading while the active request is current.
- Invalidate pending prompt completions when the view disappears.
- Avoid clearing a newer in-flight request from an older completion.
- Extend static checks so stale prompt completions remain guarded.

## Work Completed

- Added `promptRequestID` to track prompt request generations.
- Incremented the request generation when starting a prompt fetch.
- Captured each prompt fetch generation before dispatching completion work.
- Ignored completions whose captured generation no longer matches the active
  generation.
- Invalidated pending prompt completions when the game view disappears.
- Extended `scripts/check_ios_contracts.py` with stale completion guard
  coverage and completed-plan coverage.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_ios_contracts.py`
- `make check`
- `git diff --check`

## Xcode Notes

`xcodebuild` was unavailable on this host, so simulator compilation was not run
here. The repository `make check` wrapper still runs the iOS build when
`xcodebuild` is available locally.

## Follow-Up Candidates

- Cancel the underlying prompt request explicitly when the app moves off screen
  after migrating away from legacy `NSURLSession` usage.
- Add simulator/device verification notes for leaving the game screen during a
  slow prompt fetch.
