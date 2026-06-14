# Motion Device Verification Checklist

## Status: Completed

## Context

The motion gate has deterministic XCTest coverage, but a simulator cannot
reproduce physical attitude changes or validate whether the thresholds feel
stable in a user's hand.

## Priority

Document a repeatable physical-device checklist tied to the exact motion
hysteresis and lifecycle behavior in source, while keeping device execution
truthfully unclaimed.

## Requirements

- Record the `1.0...2.6` idle-to-playing entry range and `0.9...2.7` playing
  continuation range.
- Verify that entering the play range selects one prompt and small boundary
  fluctuations do not consume another prompt.
- Verify that lowering outside the continuation range resets the idle text.
- Verify that motion errors or missing samples reset active play.
- Verify that leaving the view stops updates and clears active play, and that
  returning restarts updates without duplicate subscriptions.
- State that the checklist requires a physical iOS 13+ device and remains
  unexecuted until device evidence is recorded.
- Add fail-closed documentation, source, suite, roadmap, changelog, and plan
  contracts plus hostile mutations.

## Verification

- Focused static checklist and source contracts passed.
- The repository and external-directory `make check` passed.
- Eight hostile device-checklist mutations were rejected across threshold,
  transition, lifecycle, status, documentation, suite, roadmap, and plan-status
  contracts.
- Final artifact, credential, exact-diff, and hosted verification audits remain
  the shipping gate.

## Scope Boundary

This change does not alter motion thresholds or lifecycle behavior, claim a
physical-device run, retain motion history, or replace the existing XCTest and
hosted simulator coverage.
