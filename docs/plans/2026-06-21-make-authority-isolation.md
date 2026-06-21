# Make Authority Isolation

## Status: Completed

## Context

The repository protected its derived root, but GNU Make still accepted caller-
controlled shell, startup-file, execution-mode, and Python expression state.

## Implementation

- Hardened Make startup and every public target without changing Swift,
  project assets, prompt selection, or CoreMotion behavior.
- Added an adversarial authority harness and pinned CI to `/usr/bin/make`.

## Verification

- Repository and external-directory `make check` exercise the static contracts,
  Make authority harness, and documented host skips.
- Authority tests cover target/root/shell cases, a literal hostile Python path,
  command and environment Make-syntax rejection, command and environment
  `MAKEFILE_LIST` rejection, startup boundaries, caller `MAKEFLAGS`, and ten
  non-executing or error-ignoring modes.
- Synthetic authority cases deliberately hide platform tools such as
  `xcodebuild`, keeping their results deterministic on Linux and macOS while
  the ordinary `make check` path still runs available platform validation.

## Scope Boundary

This change does not alter application behavior or claim physical-device motion
validation.
