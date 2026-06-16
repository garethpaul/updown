---
title: "fix: Ignore stale Core Motion callbacks"
date: 2026-06-16
---

# Ignore Stale Core Motion Callbacks

## Status: Completed

## Context

`viewWillDisappear` stops device-motion updates and clears `playing`, but an
already queued callback on the main queue can still execute afterward. Without
an update-session identity check, that stale callback can select a prompt,
change the off-screen label, and restore active play state before the view is
shown again.

## Requirements

- R1. Assign a distinct generation to every started motion-update session.
- R2. Ignore callbacks whose captured generation is no longer current.
- R3. Invalidate the current generation before stopping updates when the view
  disappears.
- R4. Preserve weak controller capture, main-queue delivery, duplicate-start
  prevention, unavailable-sample reset, and existing hysteresis thresholds.
- R5. Add deterministic XCTest for current, invalidated, and replacement
  session generations without requiring motion hardware.
- R6. Add portable contracts for production integration, test registration,
  maintained guidance, and completed-plan evidence.
- R7. Hostile mutations must reject removed callback validation, late or
  missing invalidation, weakened generation semantics, removed tests, guidance
  drift, and stale plan status.

## Scope Boundaries

- Do not change motion thresholds, prompt selection, UI copy, update frequency,
  or Core Motion APIs.
- Do not retain attitude data or claim physical-device validation.
- Do not replace the existing lifecycle or unavailable-sample behavior.

## Implementation Units

### U1. Model motion update sessions

- **Files:** `UpDown/ViewController.swift`
- Add a small value type that begins, invalidates, and validates monotonically
  identified motion sessions.

### U2. Reject stale callbacks

- **Files:** `UpDown/ViewController.swift`
- Capture the generation when updates start, require it in the callback, and
  invalidate it before stopping updates on disappearance.

### U3. Add deterministic coverage

- **Files:** `UpDownTests/UpDownTests.swift`, `scripts/check_ios_contracts.py`
- Cover current acceptance, invalidation rejection, replacement rejection,
  production wiring, and checker registration.

### U4. Preserve maintained guidance

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Record that queued callbacks cannot mutate game state after the motion
  session ends.

## Verification

- The focused stale-callback contract passed production integration,
  generation semantics, invalidation ordering, XCTest, checker-registration,
  and maintained-guidance assertions.
- All seven portable implementation groups passed before the plan completion
  gate was enabled.
- Seven isolated hostile mutations were rejected across callback validation,
  invalidation ordering, equality semantics, generation advancement, XCTest,
  checker registration, and README guidance. The completed-plan mutation was
  rejected by the final full gate.
- Repository and external-directory `make check` passed all eight portable
  groups. Native XCTest and build steps were truthfully skipped because
  `xcodebuild` is unavailable on this Linux host; hosted macOS CI remains the
  authoritative compiler and XCTest gate.
- Physical motion behavior remains covered by the pending device checklist and
  is not claimed by static or simulator evidence.
