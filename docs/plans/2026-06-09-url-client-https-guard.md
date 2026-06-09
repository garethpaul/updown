# URL Client HTTPS Guard

## Status: Completed

## Context

The prompt endpoint is checked in as HTTPS, but the shared legacy URL client
still accepted any URL scheme a caller passed in. A future caller or endpoint
change could accidentally issue a non-HTTPS request before the HTTP response
guard had a chance to run.

## Objectives

- Preserve the current remote prompt flow.
- Reject non-HTTPS URL strings before constructing requests.
- Reuse the existing failure callback for unsupported schemes.
- Extend static checks so request construction remains behind the scheme guard.

## Work Completed

- Added an HTTPS scheme check immediately after URL parsing in `URL.get`.
- Returned `completed(succeeded: false, data: "")` for unsupported schemes.
- Extended `scripts/check_ios_contracts.py` to require the scheme guard before
  `NSMutableURLRequest` construction.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_ios_contracts.py`
- `make check`
- `git diff --check`

## Xcode Notes

`xcodebuild` was unavailable on this host, so simulator compilation was not run
here. The repository `make check` wrapper still runs the iOS build when
`xcodebuild` is available locally.

## Follow-Up Candidates

- Replace the remote prompt endpoint with a configurable or local demo source.
- Add simulator/device verification notes for motion thresholds.
