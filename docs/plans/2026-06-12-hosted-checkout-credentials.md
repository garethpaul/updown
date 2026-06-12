# Hosted Checkout Credentials

Status: Completed

## Problem

The static and iOS hosted jobs use read-only repository permissions, but both
checkout steps retain the workflow token in local Git configuration. Neither
job performs a later Git operation, so the credential is unnecessary.

## Plan

1. Disable credential persistence on both pinned checkout steps.
2. Parse checkout step blocks in the portable checker and require the setting
   inside each block exactly once.
3. Reject missing, enabled, duplicated, or relocated credential settings.
4. Preserve the existing Python matrix, simulator-backed XCTest, immutable
   action pins, and runtime bounds.

## Verification

- `make check` passed all 6 portable contract groups; Xcode execution was
  skipped because this Linux host does not provide `xcodebuild`.
- `make -f /home/gjones/code/private/repos/garethpaul/updown/Makefile check`
  passed from an external working directory with the same 6 contract groups.
- Isolated missing, relocated, and enabled credential-setting mutations were
  each rejected by the checkout-step contract.
- An isolated missing `__pycache__/` ignore mutation was rejected by the cache
  hygiene contract.
- `python3 -m py_compile scripts/check_ios_contracts.py`, Ruby YAML parsing of
  `.github/workflows/check.yml`, and `git diff --check` passed.
