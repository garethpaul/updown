---
title: "fix: Filter blank offline prompts"
type: fix
date: 2026-06-13
---

# Filter Blank Offline Prompts

## Status: Planned

## Context

`PromptProvider` accepts any string in an injected or bundled source. Empty and
whitespace-only values can therefore become a playable clue, consume selection
history, and render as a blank game screen. The current default inventory is
valid, but future edits and deterministic tests should fail closed at the
provider boundary.

## Requirements

- R1. Remove empty and whitespace-only prompt values once during provider
  initialization.
- R2. Preserve the original display value for every nonblank prompt rather than
  trimming or rewriting user-visible clue text.
- R3. Preserve duplicate weighting and immediate-repeat prevention among the
  remaining candidates.
- R4. Avoid calling the injected index provider when every source value is
  blank.
- R5. Add XCTest and portable mutation-sensitive contracts for filtering,
  mixed-source selection, all-blank behavior, documentation, and completed-plan
  status.

## Implementation Units

### U1. Normalize the provider inventory

- **Files:** `UpDown/PromptProvider.swift`
- Filter source values with Foundation whitespace/newline trimming only for the
  blankness decision.
- Store each accepted value unchanged so visible formatting and duplicate
  weighting remain stable.

### U2. Cover the selection behavior

- **Files:** `UpDownTests/UpDownTests.swift`
- Prove an all-blank source returns `nil` without invoking the selector.
- Prove a mixed source exposes only nonblank candidates to deterministic
  selection and preserves their original value.
- Strengthen the default inventory assertion to reject whitespace-only values.

### U3. Preserve repository contracts and guidance

- **Files:** `scripts/check_ios_contracts.py`, `README.md`, `SECURITY.md`,
  `VISION.md`, `CHANGES.md`
- Register the completed plan and enforce the source, XCTest, and maintenance
  documentation contracts.

## Verification

- Run the focused prompt contracts, then local and external-working-directory
  `make check` under explicit timeouts.
- Reject hostile mutations for missing filtering, storing trimmed values,
  selector calls on all-blank sources, mixed-source candidate counts, default
  inventory drift, documentation removal, and stale plan status.
- Validate Python syntax, workflow YAML, Xcode project/XML/JSON resources,
  intended paths, generated artifacts, whitespace, conflict markers, and
  changed-line secret patterns.
- Report local XCTest as unavailable on this Linux host; rely on the exact-head
  hosted iOS job for native compilation and test execution.

## Scope Boundaries

- Do not change prompt ordering, duplicate weighting, repeat history, motion
  behavior, UI copy, dependencies, or project settings.
- Do not trim or otherwise normalize accepted display strings.
- Do not merge or close any pull request without explicit owner authorization.
