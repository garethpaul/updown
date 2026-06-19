---
title: "Deep-review motion ownership and prompt canonicalization"
date: 2026-06-19
---

# Deep-Review Motion Ownership and Prompt Canonicalization

## Status: Completed

## Context

The stacked maintenance changes rejected stale callbacks after view
disappearance and prevented exact prompt-value repeats. Two adjacent cases
remained: application deactivation did not end a still-visible view's motion
session, and visually equivalent prompt strings could repeat when their case,
width, whitespace, or Unicode composition differed.

## Changes

- Track view visibility and application activity in a testable lifecycle state.
- Invalidate callbacks, stop Core Motion, and reset the display whenever the app
  resigns active or the game view disappears.
- Start one fresh session only when the app is active and the view is visible.
- Compare prompt history with a stable canonical key while preserving source
  weighting and the original displayed clue.
- Add focused XCTest and portable contracts for both bug classes.

## Verification

- The new prompt regression test failed against the stacked head by selecting a
  canonically equivalent clue and passed after canonical-key selection.
- The new lifecycle tests initially failed to compile because no application
  ownership state existed and passed after the lifecycle boundary was added.
- `make check`, `xcodebuild analyze`, hosted checks, and physical-device motion
  behavior remain the final validation gates.
