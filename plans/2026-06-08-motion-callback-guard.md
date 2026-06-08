# Motion Callback Guard

## Problem

The CoreMotion update callback force-unwrapped `motion`, so an update delivered
with no motion sample could crash the prototype before it could ignore the bad
sample.

## TDD Evidence

1. Extended `scripts/check_ios_contracts.py` with a nil-safe motion callback
   contract.
2. Ran `make lint` before changing `ViewController.swift` and confirmed the new
   check failed on `motion!`.
3. Guarded the optional motion sample with `if let currentMotion = motion` and
   reran the full verification gate.

## Verification

- `make lint`
- `make test`
- `make build`
- `make verify`
- `make check`
- `git diff --check`
