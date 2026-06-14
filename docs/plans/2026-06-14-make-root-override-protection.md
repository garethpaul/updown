# Protect the Make Repository Root from Overrides

## Status: Completed

## Context

GNU Make command-line assignments can replace the ordinary Makefile-derived
`ROOT`, redirecting static contracts, simulator tests, and builds away from the
reviewed checkout.

## Requirements

- Protect the Makefile-derived root with `override`.
- Preserve the configurable Python command and existing iOS test/build targets.
- Require exact protected root and Python lines in the portable checker.
- Pass local, external-directory, and hostile-root full gates.
- Reject root, checker, Python override, and plan-status regressions.
- Preserve hosted macOS/Xcode and CodeQL workflow coverage unchanged.

## Verification Plan

- focused hosted-verification contract and Python compilation
- bounded local, external-directory, and hostile-root `make check`
- eight focused mutations
- workflow YAML, project XML/JSON/plist, SVG XML, artifact, whitespace, and
  changed-line secret audits

## Scope Boundaries

- Do not alter Swift behavior, project settings, dependencies, workflows, or
  branch-protection requirements.
- Do not merge or close stacked pull requests without owner authorization.

## Work Completed

- Protected the Makefile-derived root while preserving the Python override.
- Added exact-line checker contracts and registered this completed plan.

## Verification

- Python compilation and the focused hosted-verification contract passed.
- Local, external-directory, and hostile-root `make check` runs passed under
  300-second timeouts with all seven portable groups; local XCTest correctly
  remained unavailable on Linux.
- Eight hostile root, checker, Python override, and plan-status mutations were
  rejected.
- Python syntax, workflow YAML, project XML/JSON/plist, SVG XML, intended-path,
  artifact, `git diff --check`, and changed-line secret audits passed.
