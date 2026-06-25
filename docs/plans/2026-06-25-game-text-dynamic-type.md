---
title: "Support Dynamic Type for game text"
date: 2026-06-25
---

# Game Text Dynamic Type

## Status: Completed

## Context

The single full-screen label used a fixed 72-point Helvetica Bold font, one
line, and tail truncation. That preserved the prototype look but ignored the
user's content-size preference and could hide longer clues instead of wrapping.

Apple documents `UIFontMetrics` as the supported way to scale a custom font for
Dynamic Type and allows a maximum point size when the interface cannot safely
accommodate unbounded scaling. A label with `numberOfLines = 0` and word
wrapping can use the available full-screen height rather than truncating text.

## Changes

- Add a reusable `GameTextStyle` with a 72-point bold baseline.
- Scale through large-title font metrics with a 120-point maximum.
- Enable automatic content-size-category updates.
- Allow unlimited lines and word-boundary wrapping.
- Apply the style before the initial display state renders.
- Add XCTest and portable contracts for the accessibility configuration.

## Verification

- The new portable contract failed before `GameTextStyle` existed.
- `make check` passes all 10 portable checks and 35 Make authority cases; local
  XCTest and build skip because `xcodebuild` is unavailable.
- A hostile mutation removing `numberOfLines = 0` fails the portable contract.
- `git diff --check` passes.
- Hosted macOS must compile and run the UIKit test against Xcode 16.
- Manual device review remains appropriate for the largest accessibility sizes
  and does not replace the pending Core Motion checklist.
