# No Immediate Prompt Repeat

Status: Completed

## Context

The offline prompt provider selected independently on every play transition,
so the same clue could appear twice in a row even when alternatives were
available.

## Changes

- Retained the previous prompt index in the provider.
- Selected from all other indexes after the first prompt and remapped the
  injected candidate around the previous index.
- Preserved safe behavior for empty, single-item, and invalid-index sources.
- Added deterministic XCTest and portable contracts for repeat prevention.
- Made repository commands root-independent and fixed the Linux CI runner.

## Verification

- `make check`
- `python3 -m py_compile scripts/check_ios_contracts.py`
- Mutation checks for prompt history, bounds, tests, CI, and Makefile contracts
- `git diff --check`

CoreMotion thresholds still require physical-device verification.
