# Interstitial Ad Unit Guard

Status: Completed

## Context

The sample ships with the MoPub interstitial ad unit set to
`YOUR_AD_UNIT_ID`. The view controller still created an interstitial controller
with that placeholder and called `loadAd()` during startup. A historical sample
should keep the placeholder visible, but it should not make ad-network calls or
attempt presentation until a developer provides a real local ad unit ID.

## Plan

- Centralize the interstitial ad unit ID in one Swift constant.
- Skip interstitial delegate setup and `loadAd()` while the checked-in
  placeholder value is still present.
- Require the same configuration guard before presenting a loaded interstitial.
- Extend `scripts/check_ios_contracts.py` so future edits cannot reintroduce
  direct placeholder ad loading.

## Verification

- `python3 scripts/check_ios_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

On this non-macOS host, `make verify` runs the static checks and skips the Xcode
build because `xcodebuild` is unavailable.
