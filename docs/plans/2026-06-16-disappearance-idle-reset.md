---
title: "fix: Reset the game UI when the view disappears"
date: 2026-06-16
---

# Reset The Game UI When The View Disappears

## Status: Completed

## Context

`viewWillDisappear` invalidates Core Motion, stops updates, and clears
`playing`, but it leaves the currently visible prompt in `gameText`. Returning
to the same controller can therefore show a stale prompt while the game is
logically idle and waiting for a new motion transition.

## Requirements

- R1. Reset the prompt label to the existing idle copy whenever the view
  disappears.
- R2. Reuse the existing `stop()` transition so visible and logical idle state
  cannot drift.
- R3. Preserve callback invalidation before stopping Core Motion updates.
- R4. Preserve the stale-callback generation guard, hysteresis thresholds,
  prompt selection, and motion-start behavior.
- R5. Add deterministic XCTest for active and already-idle disappearance
  resets without requiring motion hardware.
- R6. Add mutation-sensitive portable contracts for ordering, tests, guidance,
  checker registration, and completed-plan evidence.

## Scope Boundaries

- Do not change prompt copy, motion thresholds, update frequency, or Core
  Motion APIs.
- Do not claim physical-device execution from Linux static validation.

## Implementation Units

### U1. Centralize disappearance reset

- **Files:** `UpDown/ViewController.swift`
- Route disappearance through `stop()` after invalidating and stopping motion
  updates.

### U2. Add deterministic coverage

- **Files:** `UpDownTests/UpDownTests.swift`, `scripts/check_ios_contracts.py`
- Model the lifecycle reset independently of motion hardware and enforce
  production ordering and checker registration.

### U3. Preserve maintained guidance

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Record that leaving the game clears any visible prompt and returns to idle.

## Verification

- Run the focused disappearance-reset contract and full repository/external
  `make check` gates.
- Reject isolated mutations for direct state clearing, stale prompt retention,
  invalidation ordering, missing tests, guidance drift, checker unregistration,
  and stale plan status.
- Audit the exact diff, generated artifacts, file modes, conflicts, and
  credential-like additions before committing.

## Runtime Boundary

Local `xcodebuild` and physical-device motion are unavailable on this Linux
host. Hosted macOS CI remains the authoritative compiler and XCTest gate.

## Work Completed

- Added a testable display-state value that keeps prompt text and play state
  synchronized across prompt, unavailable, and idle transitions.
- Routed view disappearance through the shared `stop()` transition after
  callback invalidation and Core Motion shutdown.
- Added active and already-idle XCTest cases plus a registered portable
  contract for source ordering, state semantics, tests, guidance, and plan
  evidence.
- Updated maintained lifecycle, security, vision, checklist, and change notes.

## Verification Completed

- `python3 -m py_compile scripts/check_ios_contracts.py`
- Focused `check_disappearance_idle_reset_contracts` execution.
- All eight implementation and repository contract groups excluding the
  deliberate in-progress plan-status gate before this completion record.
- Repository-root and external-directory `make check` passed all nine portable
  groups; native XCTest was truthfully skipped because `xcodebuild` is absent.
- Eight isolated mutations were rejected for shared-stop removal, reset
  reordering, omitted rendering, missing idle-text reset, removed XCTest,
  README drift, checker unregistration, and stale plan status.
