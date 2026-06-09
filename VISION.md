## UpDown Vision

UpDown is a legacy iOS motion game prototype that uses device motion to switch
between play and stop states, fetches prompt text from a remote endpoint, and
shows MoPub interstitial ads.

The repository is useful as a small CoreMotion, ad-network, and remote-content
sample from its original SDK era.

The goal is to preserve the prototype while making motion, ad, and remote
content behavior explicit.

The current focus is:

Priority:

- Preserve the motion-triggered play/stop flow
- Keep ad-unit IDs as developer-provided configuration
- Skip ad loading while the checked-in MoPub placeholder ad unit is still in use
- Keep Fabric build upload credentials in local environment variables
- Make remote prompt fetching visible
- Treat Fabric/Crashlytics, MoPub, and Swift versions as legacy
- Keep remote prompt fetch failures non-crashing and visible
- Keep play state false when remote prompts fail to load
- Require HTTPS before issuing prompt requests
- Require prompt request URLs to include a host before request construction
- Reject non-2xx remote prompt responses before treating body text as content
- Avoid duplicate remote prompt fetches while a fetch is already in flight
- Ignore stale remote prompt completions after the game view disappears
- Treat missing CoreMotion samples as non-crashing no-ops
- Stop CoreMotion updates when the game view is off screen
- Keep motion play state as concrete local state, not an implicitly unwrapped
  optional

Next priorities:

- Add README setup notes and app purpose
- Replace the remote prompt endpoint with a configurable or local demo source
- Add manual verification notes for motion thresholds
- Modernize SDKs only in a dedicated compatibility pass

Contribution rules:

- One PR = one focused motion, prompt, ad, SDK, or documentation change.
- Do not commit ad credentials or analytics secrets.
- Keep remote content endpoints explicit.
- Include device notes for motion behavior changes.

## Security And Responsible Use

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

The app can use motion data, ads, and remote content. It should not collect
motion or usage data silently, and remote responses should not be trusted as
safe UI content without validation.

## What We Will Not Merge (For Now)

- Checked-in ad credentials
- Loading ads from placeholder ad-unit IDs
- Hidden analytics
- Silent remote endpoint changes
- Broad SDK rewrites without preserving the prototype behavior

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
