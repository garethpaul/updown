# State-Specific VoiceOver Hints

Status: Completed

## Problem

The full-screen label retained the same “tilt up” accessibility hint in every
display state. VoiceOver therefore instructed a player to tilt upward while a
prompt was already active, after prompt selection failed, and even when device
motion was unavailable.

## Decision

- Keep the label as one accessibility element.
- Give idle state a tilt-up instruction.
- Give an active prompt a lower-to-reset instruction.
- Give unavailable prompt inventory a lower-to-reset-before-retry instruction.
- Remove the interaction hint when device motion is unavailable because no
  tilt action can resolve that state.
- Update the label hint whenever display state is rendered without changing
  the existing one-shot announcements.

## Test-First Plan

1. Add XCTest expectations for idle, playing, prompt-unavailable, and
   motion-unavailable hints.
2. Extend the portable contract to reject the static tilt-up hint.
3. Run the checker and record the missing state-specific API failure.
4. Implement the smallest display-state hint mapping and render update.
5. Synchronize README, security, vision, agent, and change guidance.
6. Run `make check`, external-directory verification, hosted XCTest/build, and
   exact-head review before merge.

## Verification

The portable checker failed before the state-specific hint API existed. The
new source contract and XCTest coverage distinguish all four display states.
All 11 static checks and 35 Make authority cases pass through root and external
`make check`; Python compilation and `git diff --check` pass. Local native
tests/build skip because `xcodebuild` is unavailable. Hosted XCTest/build,
three Python static matrices, and Swift/Python/Actions CodeQL pass on the
implementation head. Codex review failed before analysis with HTTP 401; the
exact head received a clean immutable manual review. Spoken guidance and
CoreMotion input still require physical-device verification.
