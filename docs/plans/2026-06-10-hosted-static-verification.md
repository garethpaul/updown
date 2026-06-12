# Hosted Verification

Status: Completed

## Problem

The repository had portable contracts but no hosted workflow. A static-only
workflow would still leave the modernized Swift source, shared scheme, XCTest,
storyboard compilation, and simulator link step unverified.

## Plan

1. Add least-privilege portable verification on Python 3.10, 3.12, and 3.14,
   with manual dispatch for maintenance checks.
2. Pin third-party actions to verified immutable commits and bound runtime.
3. Add a macOS 15 job that runs the shared Xcode test scheme through the same
   `make check` command developers use.
4. Enforce triggers, permissions, cancellation, matrix, pins, runner, timeout,
   and commands through the portable checker.

## Verification

- `make check`
- `python3 -m py_compile scripts/check_ios_contracts.py`
- `git diff --check`
