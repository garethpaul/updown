# Swift 5 Offline Modernization

Status: Completed

## Problem

The iOS 8-era app used obsolete Swift syntax, bundled 11 MB of retired MoPub,
Fabric, and Crashlytics binaries, and depended on a prompt endpoint that now
returns HTTP 404. Its XCTest target contained only generated placeholder tests,
and developer-specific framework paths prevented a reproducible build.

## Plan

1. Remove retired SDK binaries, imports, project references, upload phases, and
   absolute developer paths.
2. Migrate the app and test targets to Swift 5 with an iOS 13 floor and a shared
   Xcode scheme.
3. Replace the dead remote dependency with a bounded offline prompt provider.
4. Add deterministic XCTest for successful selection, empty sources, invalid
   indexes, and the default prompt inventory.
5. Preserve the motion-driven play/stop flow with modern lifecycle APIs and a
   non-retaining motion callback.

## Verification

- `make check`
- Shared `UpDown` XCTest scheme
- Portable project, source, resource, and workflow contracts
- `git diff --check`
