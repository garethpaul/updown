## UpDown Vision

UpDown is a small iOS motion game that uses device motion to switch between
play and stop states and selects prompts from a bundled offline source.

The repository is useful as a focused CoreMotion and deterministic prompt-state
sample that builds with a supported Swift toolchain.

The goal is to preserve the prototype while keeping motion lifecycle, prompt
selection, privacy, and build behavior explicit and testable.

The current focus is:

Priority:

- Preserve the motion-triggered play/stop flow
- Keep prompt selection offline and deterministic under test
- Avoid immediately repeating a prompt when alternatives are available
- Treat duplicate prompt strings as the same visible clue for repeat prevention
- Reject blank offline prompt values without rewriting accepted clue text
- Keep advertising, analytics, and crash-reporting SDKs out of the app
- Keep the Swift 5 / iOS 13+ project reproducible with a shared test scheme
- Reset active play safely when CoreMotion reports an error or missing sample
- Tolerate small sensor fluctuations at motion play-state boundaries
- Stop CoreMotion updates when the game view is off screen
- Keep motion play state as concrete local state, not an implicitly unwrapped
  optional

Next priorities:

- Add physical-device verification notes for motion thresholds
- Expand prompt categories without adding network or tracking dependencies
- Improve accessibility while preserving the one-screen game flow

Contribution rules:

- One PR = one focused motion, prompt, build, or documentation change.
- Do not add hidden analytics, advertising identifiers, or remote prompt calls.
- Include device notes for motion behavior changes.

## Security And Responsible Use

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

The app processes motion data only while its game view is visible. It should
not retain motion history or add silent usage collection.

## What We Will Not Merge (For Now)

- Hidden analytics
- Remote prompt dependencies without an explicit offline fallback
- Broad rewrites that discard the motion-driven prototype behavior

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
