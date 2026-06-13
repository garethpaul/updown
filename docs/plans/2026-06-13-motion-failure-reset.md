---
title: "fix: Reset play state when motion delivery fails"
date: 2026-06-13
---

# Reset Play State When Motion Delivery Fails

## Status: Completed

## Context

The device-motion callback ignores its error argument and returns when an
attitude sample is missing. If delivery fails while a prompt is active, the UI
can remain in the playing state even though motion can no longer drive the stop
transition.

## Requirements

- R1. Treat a Core Motion error or missing attitude as an unavailable sample.
- R2. Reset an active game to the existing idle prompt when a sample is
  unavailable.
- R3. Leave an already idle game unchanged on unavailable samples.
- R4. Preserve the existing hysteresis thresholds and valid-sample play/stop
  transitions.
- R5. Keep the callback weakly captured and main-queue delivered.
- R6. Add deterministic XCTest and portable contracts for active and idle
  failure handling without requiring physical motion hardware.

## Scope Boundaries

- Do not change motion thresholds, prompt selection, UI copy, update frequency,
  or Core Motion APIs.
- Do not claim physical-device motion validation from simulator CI.

## Verification

- `python3 -B -c '...check_motion_lifecycle_contracts()'` passed callback,
  active-reset, idle-stability, weak-capture, and XCTest-presence contracts.
- Full local, external-directory, and space-containing-path `make check` runs
  passed all seven portable groups; native XCTest runs in hosted macOS CI.
- Nine hostile mutations covering ignored errors, missing-sample handling,
  active reset, idle stability, weak capture, removed XCTest cases, and stale
  plan status were rejected.
- Swift source review, workflow contracts, `git diff --check`, generated-
  artifact, and focused secret reviews are included in final validation.
