---
title: "fix: Prevent immediate duplicate prompt values"
type: fix
date: 2026-06-13
---

# Prevent Immediate Duplicate Prompt Values

## Status: Completed

## Context

The offline prompt provider excludes only the previously selected array index.
If the prompt source contains duplicate strings at different indexes, the same
visible clue can still appear on consecutive play transitions even when a
different clue value is available.

## Requirements

- R1. Track the previously returned prompt value rather than only its index.
- R2. After the first selection, choose from prompt values that differ from the
  previous visible clue whenever at least one alternative exists.
- R3. Preserve duplicate entries as weighting among eligible values rather than
  globally deduplicating the prompt source.
- R4. Preserve empty sources, single-value or all-identical sources, injected
  index selection, and invalid-index failure behavior.
- R5. Add deterministic XCTest and portable contracts for duplicate-value
  repeat prevention and all-identical fallback.
- R6. Record local portable validation and require hosted Xcode/XCTest on the
  exact successor head.

## Scope Boundaries

This change does not alter the default prompt list, motion thresholds, UI text,
or random-number generator. It changes only the candidate pool passed to the
existing injected index provider.

## Implementation Units

### U1. Select by Visible Prompt Value

- **Files:** `UpDown/PromptProvider.swift`
- Build an eligible prompt array that excludes the previous returned value; if
  that would be empty, fall back to the original source.

### U2. Add Deterministic XCTest and Static Contracts

- **Files:** `UpDownTests/UpDownTests.swift`, `scripts/check_ios_contracts.py`
- Cover duplicate values with an available alternative, all-identical values,
  candidate counts, bounds checks, and previous-value updates.

### U3. Document and Verify

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`, this plan.
- Record portable checks, mutations, and the required hosted native evidence.

## Risks

- Candidate ordering must remain stable so injected deterministic selection and
  duplicate weighting stay understandable.
- Native Swift/XCTest execution is unavailable locally and must be confirmed by
  the hosted macOS job after push.

## Verification

- Focused offline prompt contracts: passed.
- `/tmp/engineering-bar/mutate-updown-prompt-value-repeat.sh`: rejected seven
  history, filter, fallback, deduplication, state-update, and XCTest mutations.
- `git diff --check`: passed.
- `make check`: passed all seven portable contract groups and truthfully
  reported that local `xcodebuild` is unavailable.
- `make -C /tmp/engineering-bar/updown-prompt-value-repeat-external/repo
  check`: passed the same portable gate from an external temporary path.
- Native Xcode/XCTest: unavailable locally; exact-head hosted verification is
  required after push.
