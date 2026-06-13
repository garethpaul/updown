# Changes

## 2026-06-13

- Reset active play to the existing idle prompt when Core Motion reports an
  error or omits an attitude sample, while leaving idle state unchanged.
- Added deterministic XCTest and portable contracts for unavailable motion
  samples without changing valid-sample hysteresis thresholds.
- Prevented duplicate prompt strings at different indexes from appearing as
  consecutive visible clues while preserving eligible duplicate weighting and
  all-identical source behavior.

## 2026-06-12

- Disabled checkout credential persistence in both hosted jobs and bound the
  fail-closed contract to each pinned checkout step.
- Ignored Python bytecode caches produced by local contract compilation.
- Replaced opaque default Swift CodeQL autobuild with a pinned advanced
  workflow that explicitly builds the unsigned `UpDown` app target.

## 2026-06-10

- Added a testable motion hysteresis gate so small sensor fluctuations at the
  play thresholds do not stop, restart, and consume another prompt.
- Prevented consecutive duplicate prompts while preserving empty, single-item,
  and invalid-selector behavior with deterministic XCTest coverage.
- Made local Make and test-script execution root-independent and fixed the
  static CI job to Ubuntu 24.04.
- Migrated the project to Swift 5, Xcode 16, and an iOS 13 deployment target
  with explicit app/test bundle identifiers and a shared test scheme.
- Replaced the dead remote prompt endpoint with a bundled offline prompt
  provider and added four deterministic XCTest cases.
- Removed the retired MoPub, Fabric, and Crashlytics binaries, build phase,
  imports, ad behavior, analytics startup, and developer-specific search paths.
- Modernized CoreMotion lifecycle code with a weak callback capture and removed
  obsolete spinner state from the storyboard.
- Completed the iPad and App Store icon catalog with opaque generated assets.
- Added least-privilege Python contract CI plus a real macOS Xcode test job.
- Made hosted Xcode tests discover or create an iPhone simulator and fall back
  to the Apple Silicon iOS-app destination when runner images expose no device.

## 2026-06-10

- Added least-privilege GitHub Actions static verification on Python 3.10,
  3.12, and 3.14 with immutable action pins and a bounded runtime.
- Extended the local iOS contract checker to enforce workflow triggers,
  permissions, action provenance, matrix, timeout, and command.
- Documented that hosted CI covers portable contracts while Xcode and device
  validation still require macOS.

## 2026-06-09

- Skipped MoPub interstitial loading and presentation while the checked-in
  placeholder ad unit ID is still configured.
- Added static checker coverage for interstitial ad-unit configuration guards.
- Rejected prompt request URLs without a host before constructing URL requests.
- Added static checker coverage for URL client host validation.
- Rejected non-HTTPS prompt request URLs in the URL client before constructing
  requests.
- Added static checker coverage for HTTPS-only prompt URL handling.
- Added a prompt request-generation guard so stale remote prompt completions do
  not update game UI or play state after the view disappears.
- Added static checker coverage for stale prompt completion invalidation.
- Moved Fabric dSYM upload credentials out of the Xcode project build phase and
  into local environment variables.
- Added static checker coverage that rejects checked-in Fabric build secrets.
- Rejected non-2xx remote prompt responses in the URL client before decoding
  response text.
- Added static checker coverage for HTTP status handling in the URL client.
- Stopped CoreMotion device-motion updates when the game view disappears and
  made motion startup idempotent when the view appears.
- Added static checker coverage for the motion lifecycle guard.
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
