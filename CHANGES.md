# Changes

## 2026-06-08

- Restored app and test `Info.plist` files referenced by the Xcode project.
- Added `make verify` and `make check` static gates for plist, storyboard, asset, project, and URL-client contracts.
- Hardened the prompt URL client so invalid URLs and failed responses report failure instead of force-unwrapping.
