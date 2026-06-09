# Changes

## 2026-06-08

- Added canonical `docs/plans` coverage to the static iOS contract checker.
- Guarded CoreMotion callbacks so missing motion samples are skipped instead of
  force-unwrapped.
- Extended the static gate to cover nil-safe motion callback handling.
- Restored app and test `Info.plist` files referenced by the Xcode project.
- Added `make verify` and `make check` static gates for plist, storyboard, asset, project, and URL-client contracts.
- Hardened the prompt URL client so invalid URLs and failed responses report failure instead of force-unwrapping.
