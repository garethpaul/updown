# URL Client Status Guard

## Status: Completed

## Context

The URL client already handled invalid URLs, network errors, nil response data,
and decode failures. It still treated any decodable response body as success,
including HTTP error pages from the remote prompt endpoint.

## Objectives

- Preserve the legacy prompt-fetching flow.
- Treat only HTTP 2xx responses as successful prompt fetches.
- Return the existing failure callback for non-HTTP or non-2xx responses.
- Validate status before decoding response text.
- Extend static checks to preserve the behavior.

## Work Completed

- Added `NSHTTPURLResponse` inspection to `URL.get`.
- Rejected status codes below 200 or greater than or equal to 300.
- Kept failure handling on the existing `completed(succeeded: false, data: "")`
  path.
- Extended `scripts/check_ios_contracts.py`.
- Updated README, VISION, and CHANGES.

## Verification

- Negative check: `python3 scripts/check_ios_contracts.py` failed before the
  HTTP status guard was added.
- `python3 scripts/check_ios_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Replace the remote prompt endpoint with a configurable or local demo source.
- Add manual verification notes for motion thresholds.
