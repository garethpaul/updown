# Motion Threshold Hysteresis

Status: Completed

## Context

The controller used one exact motion range for both entering and leaving play.
Small sensor fluctuations around either boundary could therefore stop and
restart the game, consuming a new prompt without a meaningful device movement.

## Changes

- Preserve the existing `1.0...2.6` range for entering play.
- Use a slightly wider `0.9...2.7` range while already playing.
- Isolate the state decision in a deterministic `MotionHysteresisGate`.
- Add XCTest and portable contracts for entry, boundary tolerance, and exit.

## Verification

- `make check`
- Remove the continuation-range selection and confirm the static contract fails
  before restoring it.
- Physical-device threshold feel still requires manual verification.
