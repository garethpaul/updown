# Make Authority Isolation

## Status: Completed

## Context

The repository protected its derived root, but GNU Make still accepted caller-
controlled shell, startup-file, execution-mode, and Python expression state.

## Implementation

- Hardened the checked-in Makefile after its parse boundary without changing
  Swift, project assets, prompt selection, or CoreMotion behavior.
- Public aliases use double-colon rules, embed reviewed root plus literal
  Python/Xcode command values before later non-override target variables can
  alter them, and pin `/bin/sh -c` against later non-override shell assignments.
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
- Regressions reject all seven later single-colon recipe replacements, protect
  ordinary later root/Python/Xcode/shell variables, reject PATH-shadowed Xcode,
  and retain explicit executable controls for the caller-program boundary.

## Scope Boundary

This is a local checked-in-Makefile boundary, not a sandbox for caller-supplied
Make programs. GNU Make startup files are parsed before repository checks, so
their parse-time code remains outside the local trust boundary. Later makefiles
using GNU Make `override` directives likewise remain outside the local trust
boundary. Python executable selection, including PATH resolution of the default
`python3`, is caller-controlled rather than authenticated by this repository.

Within that boundary, later non-override assignments cannot redirect the
reviewed root, Python command, Xcode command, or recipe shell; later single-colon
recipes fail closed; and PATH cannot replace Xcode or simulator helper tools.
This change does not alter application behavior or claim physical-device motion
validation.
