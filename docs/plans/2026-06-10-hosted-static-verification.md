# Hosted Static Verification

Status: Completed

## Problem

The repository had 13 grouped static checks for the legacy Xcode project,
Swift safety guards, resources, framework placeholders, and documentation, but
no hosted workflow ran them. This Linux environment cannot honestly claim an
iOS build because `xcodebuild` is unavailable.

## Plan

1. Add least-privilege GitHub Actions verification on Python 3.10 and 3.12.
2. Pin third-party actions to verified immutable commits and bound runtime.
3. Enforce the workflow trigger, permissions, matrix, pins, timeout, and
   `make check` command through the local static checker.
4. Document that hosted CI validates portable contracts while Xcode build and
   device behavior remain a separate macOS verification boundary.

## Verification

- `make check`
- `python3 -m py_compile scripts/check_ios_contracts.py`
- Negative workflow-permission mutation rejected by `make lint`
- `git diff --check`
