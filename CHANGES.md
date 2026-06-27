# Changes

## 2026-06-26 18:32 PDT

- **Priority:** P2 accurate VoiceOver action guidance.
- **Summary:** Replaced the label's permanent tilt-up hint with state-specific
  VoiceOver hints for idle, active prompt, prompt-unavailable, and
  motion-unavailable states.
- **Work:** Added a pure hint mapping, updated it with every rendered display
  state, preserved one-shot announcements, and removed the impossible action
  hint when CoreMotion is unavailable.
- **Tests:** Added XCTest coverage for all four display states and tightened the
  portable checker to reject a static tilt hint or incorrect state ordering.
- **Validation:** The checker first failed because the state-specific API did
  not exist. All 11 static checks and 35 Make authority cases pass through root
  and external-directory `make check`; Python compilation and
  `git diff --check` pass. Local XCTest/build skip because `xcodebuild` is
  unavailable. Hosted run 28274571178 passes XCTest/build and Python
  3.10/3.12/3.14 static contracts; CodeQL run 28274571175 passes Swift,
  Python, and Actions analysis on implementation head `bd4a90b`.
- **Review:** Required `codex review --base origin/master` failed before
  analysis with OpenAI HTTP 401. Immutable exact-head review confirmed state
  ordering, prompt-text collision behavior, nil motion-unavailable guidance,
  render-time assignment, test coverage, and a clean diff with no actionable
  finding.
- **Blockers:** Spoken VoiceOver phrasing and physical tilt behavior still
  require device verification.

## 2026-06-26 04:07 PDT

- **Priority:** P2 accessible one-screen prompt transitions.
- **Summary:** Announced prompt and unavailable transitions to VoiceOver while
  preventing sustained tilt from continuously retrying unavailable inventory.
- **Work:** Added explicit idle-state semantics, one-shot accessibility
  announcements, a tilt instruction hint, three XCTest regressions, portable
  contracts, project guidance, and a completed plan.
- **Threads:** No open issue or pull request covered this focused accessibility
  and state-transition gap.
- **Validation:** The test-first portable contract failed before idle and
  VoiceOver ownership existed. Focused static, native, root/external, and hosted
  checks are required before merge.
- **Blockers:** VoiceOver speech and physical CoreMotion thresholds still
  require a device run; simulator XCTest cannot reproduce actual tilt input.
- **Next action:** Review the exact branch head and merge only after hosted
  checks pass.

## 2026-06-26 04:05 PDT

- **Priority:** P2 truthful unavailable-motion state.
- **Summary:** Replaced the impossible tilt instruction with an explicit
  `Motion unavailable` non-playing state when CoreMotion reports that device
  motion is not available.
- **Work:** Added a pure display-state transition, split hardware availability
  from the existing active-session guard, rendered the unavailable state before
  returning, and preserved lifecycle resets and callback-error handling.
- **Threads:** No delegated threads were used.
- **Files:** Updated the view controller, XCTest and portable contracts, public
  behavior documentation, project priorities, agent guidance, and a completed
  implementation plan.
- **Validation:** The new portable contract first failed because the source had
  no unavailable-device branch. All 10 static checks and 35 Make authority
  cases pass through root and external-directory `make check`, and
  `git diff --check` passes. Local XCTest/build skip because `xcodebuild` is
  unavailable; hosted Xcode and CodeQL remain merge gates.
- **Findings:** A device without CoreMotion support silently retained `Tilt the
  phone up for a word`, directing the user toward an action that could never
  start a prompt.
- **Blockers:** Local native XCTest/build require Xcode; simulator or physical
  hardware verification remains necessary for the actual CoreMotion boundary.
- **Next action:** Confirm the exact PR head on hosted Xcode and exercise the
  unavailable path on a simulator or device configuration that reports no
  device-motion support.

## 2026-06-25 09:42 PDT

- **Priority:** P2 readable one-screen game text.
- **Summary:** Added capped Dynamic Type scaling and multiline word wrapping to
  the full-screen idle and clue label.
- **Work:** Preserved the existing 72-point bold baseline, scaled it with
  `UIFontMetrics` up to 120 points, enabled automatic content-size updates, and
  removed single-line tail truncation.
- **Threads:** No delegated threads were used.
- **Files:** Updated the game text style, XCTest and portable contracts,
  accessibility guidance, and a completed plan.
- **Validation:** The portable contract failed before the style helper existed;
  a hostile mutation removing multiline support is rejected, the 10 static
  checks and all 35 Make authority cases pass through `make check`, and
  `git diff --check` passes. Local XCTest/build skip because `xcodebuild` is
  unavailable; hosted Xcode and CodeQL remain merge gates.
- **Findings:** The storyboard label was fixed at 72 points, one line, and tail
  truncation despite occupying the entire screen.
- **Blockers:** Physical-device motion behavior and extreme accessibility sizes
  still require manual device verification.

## 2026-06-21

- Isolated repository verification from caller-controlled Make startup files,
  shell state, execution modes, root overrides, and executable expressions.
- Added adversarial Make authority coverage and pinned hosted verification to
  `/usr/bin/make` without changing Swift or CoreMotion behavior.
- Rejected later single-colon recipe replacement, embedded reviewed root and
  literal Python/Xcode values before later non-override target assignments,
  pinned the public recipe shell, and removed PATH control of Xcode helpers.
- Kept GNU Make startup parse code outside the enforceable boundary while
  requiring absolute interpreters and isolating Python from `PYTHONPATH`,
  user-site packages, and `sitecustomize.py`.

## 2026-06-19

- Canonicalized prompt comparison without rewriting display values, preventing
  immediate repeats caused by case, width, whitespace, or equivalent Unicode.
- Invalidated Core Motion sessions when the app resigns active and restarted a
  single fresh session only for an active, visible game view.

## 2026-06-16

- Rejected queued Core Motion callbacks from ended view sessions before they
  can restore an off-screen prompt or active play state.
- Cleared visible prompt state when the game view disappears so the controller
  returns with synchronized idle UI and play state.

## 2026-06-14

- Added a pending physical-device checklist for exact motion entry,
  continuation, reset, unavailable-sample, and view-lifecycle behavior without
  claiming simulator or static checks as device evidence.

## 2026-06-13

- Filtered blank and whitespace-only offline prompts at provider initialization
  while preserving accepted clue text and duplicate weighting.
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
