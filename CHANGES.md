# Changes

## 2026-06-09

- Added an in-flight prompt fetch guard so repeated motion updates do not start
  duplicate remote prompt requests before the active request completes.
- Added static checker coverage for prompt fetch in-flight state.

## 2026-06-08

- Replaced the implicitly unwrapped `playing` state with a concrete Bool and
  added a static guard against forced play-state casts.
- Made remote prompt fetch failures show fallback text and keep play state
  false instead of entering play mode with empty content.
- Added canonical `docs/plans` coverage to the static iOS contract checker.
- Guarded CoreMotion callbacks so missing motion samples are skipped instead of
  force-unwrapped.
- Extended the static gate to cover nil-safe motion callback handling.
- Restored app and test `Info.plist` files referenced by the Xcode project.
- Added `make verify` and `make check` static gates for plist, storyboard, asset, project, and URL-client contracts.
- Hardened the prompt URL client so invalid URLs and failed responses report failure instead of force-unwrapping.
