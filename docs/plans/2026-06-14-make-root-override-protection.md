# Protect the Make Repository Root from Overrides

## Status: Planned

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
