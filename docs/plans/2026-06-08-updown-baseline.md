# UpDown Baseline

Status: Completed

## Scope

Preserve the legacy iOS motion-game prototype while keeping project files,
remote prompt fetching, URL handling, and CoreMotion callback behavior
statically verifiable.

## Completed Work

- Kept Xcode project, plist, storyboard, and asset checks behind `make check`.
- Preserved URL-client and HTTPS prompt endpoint guardrails.
- Preserved nil-safe CoreMotion callback checks.
- Added canonical `docs/plans` coverage to the iOS static contract checker.

## Verification

- `python3 scripts/check_ios_contracts.py`
- `make check`
- `git diff --check`
