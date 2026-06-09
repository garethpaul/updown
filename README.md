# updown

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/updown` is an Apple platform application or Swift sample. UpDown iOS App - Guess the word from clues your friends give you

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: C/C++ headers (29), Swift (5), JavaScript (1).

## Repository Contents

- `Crashlytics.framework` - source or example code
- `Fabric.framework` - source or example code
- `MoPub.framework` - source or example code
- `SECURITY.md` - security reporting and disclosure guidance
- `UpDown` - source or example code
- `UpDown.xcodeproj` - Xcode project file
- `UpDownTests` - source or example code
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: Crashlytics.framework, Fabric.framework, MoPub.framework, UpDown, UpDownTests
- Dependency and build manifests: none detected
- Entry points or build surfaces: UpDown.xcodeproj
- Test-looking files: UpDownTests/UpDownTests.swift

## Getting Started

### Prerequisites

- Git
- macOS with Xcode for building Apple platform projects

### Setup

```bash
git clone https://github.com/garethpaul/updown.git
cd updown
```

The setup commands above are derived from repository files. Legacy mobile, Python, or JavaScript samples may require older SDKs or package versions than a modern workstation uses by default.

## Running or Using the Project

- Open `UpDown.xcodeproj` in Xcode, choose the app or sample scheme, and run it on the matching simulator/device.
- Run `make check` for static project, URL-client, motion callback, motion
  lifecycle, and play state checks.
  The build step runs Xcode only on hosts where `xcodebuild` is installed.

## Testing and Verification

- `make check` runs plist, storyboard, asset, project, Fabric build-secret,
  URL-client, HTTPS scheme, HTTP status, prompt failure, prompt in-flight,
  motion callback, motion lifecycle, stale prompt completion, and play-state
  contract checks.
- Completed maintenance plans live under `docs/plans` and are checked by
  `make check`.
- Xcode's test action or `xcodebuild test` with the appropriate scheme and destination on macOS

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- Set `FABRIC_API_KEY` and `FABRIC_BUILD_SECRET` locally when Fabric dSYM
  upload is needed during Xcode builds. The build phase skips that upload when
  the variables are absent.

## Security and Privacy Notes

- Review changes touching authentication or token handling; examples from the scan include Crashlytics.framework/Versions/A/Headers/Crashlytics.h, UpDown/URL.swift.
- Review changes touching external API calls or credential-adjacent configuration; examples from the scan include Crashlytics.framework/Versions/A/Headers/Crashlytics.h, Fabric.framework/Versions/A/Headers/Fabric.h.
- Review changes touching network requests, sockets, or service endpoints; examples from the scan include MoPub.framework/Versions/A/Headers/MPAdConversionTracker.h, UpDown/ViewController.swift.
- Review changes touching mobile permissions or privacy-sensitive device data; examples from the scan include MoPub.framework/Versions/A/Headers/MPAdView.h, MoPub.framework/Versions/A/Headers/MPBannerCustomEventDelegate.h, MoPub.framework/Versions/A/Headers/MPCollectionViewAdPlacer.h, MoPub.framework/Versions/A/Headers/MPInterstitialAdController.h, and 5 more.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include MoPub.framework/Versions/A/Headers/MPAdConversionTracker.h, MoPub.framework/Versions/A/Headers/MPNativeAd.h, MoPub.framework/Versions/A/Headers/MPNativeCustomEvent.h, MoPub.framework/Versions/A/Resources/MoPub.bundle/mraid.js, and 1 more.
- Review changes touching database, model, or persistence code; examples from the scan include MoPub.framework/Versions/A/Headers/MPClientAdPositioning.h, MoPub.framework/Versions/A/Headers/MPServerAdPositioning.h.

## Maintenance Notes

- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-updown-baseline.md` for the current static
  verification baseline.
- See `docs/plans/2026-06-08-prompt-fetch-failure.md` for visible remote
  prompt failure handling.
- See `docs/plans/2026-06-08-play-state-bool.md` for non-optional game-state
  handling in the motion callback.
- See `docs/plans/2026-06-09-prompt-fetch-inflight-guard.md` for duplicate
  remote prompt fetch prevention.
- See `docs/plans/2026-06-09-motion-lifecycle-guard.md` for stopping and
  idempotently restarting CoreMotion updates with the view lifecycle.
- See `docs/plans/2026-06-09-fabric-build-secret-env.md` for keeping Fabric
  build upload credentials out of the Xcode project.
- See `docs/plans/2026-06-09-url-client-status-guard.md` for rejecting
  non-2xx remote prompt responses before decoding body text.
- See `docs/plans/2026-06-09-url-client-https-guard.md` for rejecting
  non-HTTPS prompt request URLs before constructing requests.
- See `docs/plans/2026-06-09-stale-prompt-completion-guard.md` for ignoring
  stale remote prompt completions after the game view disappears.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
