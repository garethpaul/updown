# Prompt Fetch In-Flight Guard

## Status: Completed

## Context

The motion callback starts a prompt fetch when the device enters the play range.
Because `playing` is only set after a successful prompt response, repeated
motion updates could call `play()` again while the first network request was
still in flight. That can create unnecessary duplicate prompt requests and race
the text shown to the player.

## Objectives

- Preserve the existing motion-driven play flow.
- Track prompt fetches that are already in flight.
- Skip duplicate `play()` requests until the active prompt fetch completes.
- Clear in-flight state on both successful and failed prompt responses.
- Keep static checks covering the duplicate-fetch guard.

## Work Completed

- Added a concrete `fetchingPrompt` state flag.
- Guarded `play()` so it returns before starting a duplicate prompt request.
- Marked prompt fetches in flight before starting the network request.
- Cleared the in-flight flag when prompt completion returns to the main queue.
- Extended the static checker and updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_ios_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Stop motion updates when the view disappears or the app enters the
  background.
- Add a local prompt fallback list for offline play.
