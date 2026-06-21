# Isolate Make Verification Authority

## Status: Completed

## Context

Protecting `ROOT` alone does not make repository verification authoritative.
GNU Make callers can still replace the recipe shell, load startup makefiles,
override the Makefile list, select non-executing or error-ignoring modes, or
embed Make syntax in an otherwise configurable executable value.

## Requirements

- Derive the repository root only from the reviewed Makefile path.
- Fix recipe execution to `/bin/sh` and reject injected startup makefiles.
- Reject replaced Makefile lists and dry-run, touch, question, or
  ignore-errors modes for every public target.
- Preserve a caller-selected literal Python executable, including paths with
  spaces and shell metacharacters, without evaluating Make syntax.
- Exercise every public target under command-line and environment root/shell
  attacks from a hostile external checkout path.
- Invoke hosted verification through `/usr/bin/make` on Linux and macOS.

## Scope Boundaries

- Do not change app behavior, Xcode settings, motion thresholds, prompt
  selection, deployment targets, or dependency state.
- Preserve truthful local skips when `xcodebuild` is unavailable.
- Preserve the existing macOS XCTest and simulator build paths.

## Verification

- `make check` passed from the repository and an external directory.
- The authority harness passed 35 public-target/root/shell cases, a literal
  hostile Python path, raw Make-syntax rejection, Makefile-list rejection,
  startup-file boundaries, caller `MAKEFLAGS` rejection, and ten unsafe mode
  rejections.
- The portable contract checker, Python compilation, workflow YAML parsing,
  project/plist/XML parsing, `git diff --check`, intended-path review, artifact
  audit, and changed-line secret audit passed.
- Native XCTest remained truthfully unavailable on Linux; hosted macOS
  `/usr/bin/make check` remains the exact-head native validation gate.
