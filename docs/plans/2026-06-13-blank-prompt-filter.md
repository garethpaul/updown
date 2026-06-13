---
title: "fix: Filter blank offline prompts"
type: fix
date: 2026-06-13
---

# Filter Blank Offline Prompts

## Status: Completed

## Context

`PromptProvider` accepts any string in an injected or bundled source. Empty and
whitespace-only values can therefore become a playable clue, consume selection
history, and render as a blank game screen. The current default inventory is
valid, but future edits and deterministic tests should fail closed at the
provider boundary.

## Requirements

- R1. Remove empty and whitespace-only prompt values once during provider
  initialization.
- R2. Preserve the original display value for every nonblank prompt rather than
  trimming or rewriting user-visible clue text.
- R3. Preserve duplicate weighting and immediate-repeat prevention among the
  remaining candidates.
- R4. Avoid calling the injected index provider when every source value is
  blank.
- R5. Add XCTest and portable mutation-sensitive contracts for filtering,
  mixed-source selection, all-blank behavior, documentation, and completed-plan
  status.

## Implementation Units

### U1. Normalize the provider inventory

- **Files:** `UpDown/PromptProvider.swift`
- Filter source values with Foundation whitespace/newline trimming only for the
  blankness decision.
- Store each accepted value unchanged so visible formatting and duplicate
  weighting remain stable.

### U2. Cover the selection behavior

- **Files:** `UpDownTests/UpDownTests.swift`
- Prove an all-blank source returns `nil` without invoking the selector.
- Prove a mixed source exposes only nonblank candidates to deterministic
  selection and preserves their original value.
- Strengthen the default inventory assertion to reject whitespace-only values.

### U3. Preserve repository contracts and guidance

- **Files:** `scripts/check_ios_contracts.py`, `README.md`, `SECURITY.md`,
  `VISION.md`, `CHANGES.md`
- Register the completed plan and enforce the source, XCTest, and maintenance
  documentation contracts.

## Verification

- The focused offline prompt contract passed after implementation.
- The pre-completion portable gate passed all seven non-plan contract groups.
- Fifteen hostile mutations covering filter removal, empty-only filtering,
  display-value rewriting, missing or weakened XCTest assertions,
  documentation drift, and stale plan status were rejected.
- Python checker syntax validation passed.
- Final local and external-working-directory `make check` runs are executed
  after this completed-plan record is written so the canonical plan contract
  validates the shipped state.
- Local XCTest truthfully skipped because `xcodebuild` is unavailable on this
  Linux host; exact-head hosted iOS validation is required before completion.

## Work Completed

- Filtered empty and whitespace-only values once during provider
  initialization using Foundation whitespace/newline classification.
- Preserved each accepted clue string unchanged, including intentional leading
  or trailing spaces, and retained duplicate weighting and repeat history.
- Added deterministic all-blank, mixed-source, display-preservation, and
  strengthened default-inventory XCTest contracts.

## Scope Boundaries

- Do not change prompt ordering, duplicate weighting, repeat history, motion
  behavior, UI copy, dependencies, or project settings.
- Do not trim or otherwise normalize accepted display strings.
- Do not merge or close any pull request without explicit owner authorization.
