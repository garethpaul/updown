# AGENTS.md

## Repository purpose

`garethpaul/updown` is an Apple platform application or Swift sample. UpDown iOS App - Guess the word from clues your friends give you

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `UpDown.xcodeproj` - Xcode project
- `plans` - repository source or sample assets
- `UpDown` - repository source or sample assets
- `UpDownTests` - repository source or sample assets

## Development commands

- Install dependencies: no repository-specific install command is documented.
- Full baseline: `make check`
- Combined verification: `make verify`
- Lint/static checks: `make lint`
- Tests: `make test`
- Build: `make build`
- Local Apple development: `open UpDown.xcodeproj`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- The application and tests use Swift 5 and support iOS 13 or later.
- Keep the shared `UpDown` scheme, explicit bundle identifiers, and simulator-safe no-signing build intact.
- VoiceOver announcements must follow explicit non-idle prompt transitions;
  sustained tilt must not repeatedly announce unavailable prompt inventory.
- State-specific VoiceOver hints must never instruct a tilt action when motion
  is unavailable or a prompt is already active.

## Testing guidance

- Test-related files detected: `UpDownTests/UpDownTests.swift`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- Prompt selection is intentionally offline; do not add a network dependency without an explicit product requirement and deterministic fallback.
- Do not reintroduce retired advertising, analytics, or crash-reporting binary frameworks.
- CoreMotion behavior must still be verified on a physical device when thresholds or lifecycle behavior change.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-updown-baseline.md` for the current static verification baseline.
- See `docs/plans/2026-06-26-motion-unavailable-state.md` for the explicit
  unavailable-device state contract.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
