# Game Text VoiceOver Transitions

Status: Completed

## Problem

The game updated its full-screen clue label without announcing dynamic text to
VoiceOver. Its unavailable state also remained logically non-playing, so a
sustained in-range motion sample could repeatedly request and render the same
failure state.

## Decision

- Expose whether the display state is truly idle rather than inferring prompt
  eligibility from the playing flag alone.
- Request a prompt only from idle and reset any non-idle state after motion
  leaves the active range.
- Make the clue label an explicit accessibility element and give it a hint
  describing the tilt interaction.
- Announce prompt and unavailable states, while keeping idle/reset transitions
  silent so backgrounding or navigation does not speak stale UI.

## Verification

- XCTest covers unavailable-to-idle reset, the label hint, and announcement
  selection for idle, prompt, and unavailable states.
- The portable contract requires explicit idle gating and the VoiceOver post.
- `make check` remains the canonical gate; physical VoiceOver and CoreMotion
  behavior still requires the documented device checklist.
