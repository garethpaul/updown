# UpDown

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Device Preview

<!-- DEVICE-PREVIEW-IMAGE -->
![Device preview](docs/device-preview.svg)

## Overview

UpDown is a small iOS word-guessing game. Hold the phone upright to display a
prompt, give clues to friends, then lower the phone to reset for the next word.
CoreMotion drives the play/stop transition.

The game works fully offline. Its original prompt service now returns HTTP 404,
so prompts are bundled in the app instead of fetched over the network. The
retired MoPub, Fabric, and Crashlytics binary SDKs have also been removed; the
app contains no advertising or analytics integration.

## Supported Toolchain

- Xcode 16
- Swift 5
- iOS 13 or later
- iPhone and iPad simulator/device targets

## Setup

```bash
git clone https://github.com/garethpaul/updown.git
cd updown
open UpDown.xcodeproj
```

Select the shared `UpDown` scheme and run on a simulator or device. A physical
device provides the meaningful CoreMotion experience; simulator tests validate
the build and offline prompt behavior but cannot reproduce real tilting.

## Verification

- `make static` validates the Xcode graph, plists, Interface Builder XML,
  assets, Swift 5/iOS 13 settings, offline prompt contracts, motion lifecycle,
  motion threshold hysteresis, shared scheme, CI, and completed maintenance
  plans.
- `make test` runs the `UpDown` XCTest scheme when `xcodebuild` is available.
- `make build` builds the simulator app without code signing.
- `make check` runs portable contracts everywhere and real XCTest on macOS.

GitHub Actions runs static contracts on Python 3.10, 3.12, and 3.14 on Ubuntu
24.04 and runs the full Xcode test scheme on macOS 15. Workflow permissions are
read-only, superseded runs are cancelled, and action revisions are pinned to
immutable commits. Neither checkout step persists the workflow credential.

## Tested Behavior

XCTest verifies deterministic prompt selection, immediate-repeat prevention,
single-item and empty-source behavior, out-of-range selector handling, the
bundled prompt inventory, and motion threshold hysteresis.
Static contracts additionally require motion callbacks to avoid retaining the
view controller, prevent duplicate subscriptions, tolerate small threshold
fluctuations while playing, and stop when the view leaves the screen.

## Privacy and Security

- Prompt selection is local and does not contact a server.
- The app does not contain ad, analytics, or crash-reporting SDKs.
- Motion data is processed in memory only while the game view is visible.
- No credentials, API keys, or developer-specific build paths are required.

## Limitations

- Motion thresholds still require physical-device verification.
- The bundled prompt list is intentionally small and English-only.
- The UI preserves the original single-screen prototype rather than adding
  scoring, categories, accessibility customization, or multiplayer state.

## Repository Guide

- `UpDown` contains the app, offline prompt provider, storyboard, and assets.
- `UpDownTests` contains XCTest coverage for prompt selection.
- `UpDown.xcodeproj` contains the shared build/test scheme.
- `scripts/check_ios_contracts.py` provides portable repository contracts.
- `docs/plans`, `CHANGES.md`, `SECURITY.md`, and `VISION.md` record maintenance
  decisions and project scope.
- `docs/plans/2026-06-10-no-immediate-prompt-repeat.md` records the completed
  prompt repeat-prevention change.
- `docs/plans/2026-06-10-motion-threshold-hysteresis.md` records the completed
  motion boundary stabilization change.
- `docs/plans/2026-06-12-hosted-checkout-credentials.md` records the
  credential-free static and iOS checkout contract.

## Contributing

Preserve the motion-driven game flow, avoid adding hidden data collection, and
run `make check` before opening a pull request. Document physical-device
verification when changing motion thresholds or lifecycle behavior.
