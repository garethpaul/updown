# CodeQL Manual Swift Build

Status: Completed

## Problem

GitHub CodeQL default setup completes actions and Python analysis quickly, but
its Swift autobuild remained opaque and in progress after the canonical macOS
job had already built the shared scheme and passed XCTest. The project contains
both app and test targets, so automatic target selection adds avoidable
ambiguity to a security gate.

## Plan

1. Replace default setup with an immutable-pinned advanced CodeQL workflow.
2. Analyze actions and Python without a build on fixed Ubuntu 24.04.
3. Analyze Swift through an explicit unsigned, single-architecture `UpDown`
   app-target build while the canonical Check workflow retains XCTest.
4. Bound the instrumented Swift job at 25 minutes to leave analysis headroom.
5. Enforce triggers, permissions, pins, build mode, target, architecture, and
   timeout through the portable repository checker.

## Verification

- `make check` passed all 7 portable contract groups; Xcode execution was
  skipped because this Linux host does not provide `xcodebuild`.
- External-working-directory `make check` passed the same 7 groups.
- Ruby parsed both workflow files.
- Isolated autobuild, mutable-action, target, permission, and timeout mutations
  were rejected by the portable checker.
- At exact head `81bb80c8bd1130ed3d5f965ed5521ce040ee35bc`, functional
  run `27425076431` passed and CodeQL run `27425076248` passed actions,
  Python, and Swift analysis. The Swift job completed in 14m43s, including a
  successful 13m04s instrumented app-target build, within the 25-minute bound.
- `python3 -m py_compile scripts/check_ios_contracts.py` and
  `git diff --check` passed.
