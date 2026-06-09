# URL Client Host Guard

## Status: Completed

## Context

The prompt URL client already rejects non-HTTPS URLs before constructing a
request. A malformed HTTPS URL without a host could still pass the scheme check
and reach `NSMutableURLRequest`, leaving failure behavior to the networking
stack instead of the local validation path.

## Objectives

- Reject prompt request URLs that do not contain a host.
- Keep the existing HTTPS-only and HTTP status guards intact.
- Report malformed URL input through the existing failure callback.
- Extend static checks so host validation stays before request construction.

## Work Completed

- Added an optional host guard in `URL.get`.
- Completed missing or empty-host URL values with `succeeded: false`.
- Extended `scripts/check_ios_contracts.py` to require host validation before
  `NSMutableURLRequest`.
- Updated README, VISION, and CHANGES.

## Verification

- Negative check before implementation:
  `make check` failed with `URL client must guard request URL hosts`.
- `python3 scripts/check_ios_contracts.py`
- `make check`
- `git diff --check`

## Follow-Up Candidates

- Replace the remote prompt endpoint with a configurable or local demo source.
- Add route/client-level tests when the project is modernized.
