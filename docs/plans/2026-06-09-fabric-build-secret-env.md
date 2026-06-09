# Fabric Build Secret Environment

## Status: Completed

## Context

The Xcode project contained a Fabric run-script build phase with literal
credential arguments. Build upload credentials should stay in a developer or CI
environment instead of being committed to the project file.

## Objectives

- Preserve the existing Fabric dSYM upload hook for configured local builds.
- Remove checked-in Fabric API key and build-secret arguments.
- Skip the Fabric upload clearly when local credentials are absent.
- Add static checker coverage that rejects literal Fabric run-script secrets.

## Work Completed

- Replaced literal Fabric run-script arguments with `FABRIC_API_KEY` and
  `FABRIC_BUILD_SECRET` environment-variable checks.
- Added a skip message when those variables are not set.
- Extended `scripts/check_ios_contracts.py` to reject committed Fabric
  run-script secrets.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_ios_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add CI documentation for setting Fabric upload credentials only in protected
  build environments.
- Modernize Fabric/Crashlytics only in a dedicated SDK compatibility pass.
