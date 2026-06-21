#!/usr/bin/env python3
"""Portable contracts for the modernized UpDown iOS project."""

from pathlib import Path
import ast
import json
import plistlib
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs/plans"
MODERNIZATION_PLAN = DOCS_PLANS / "2026-06-10-swift5-offline-modernization.md"
HOSTED_VERIFICATION_PLAN = DOCS_PLANS / "2026-06-10-hosted-static-verification.md"
NO_REPEAT_PLAN = DOCS_PLANS / "2026-06-10-no-immediate-prompt-repeat.md"
MOTION_HYSTERESIS_PLAN = DOCS_PLANS / "2026-06-10-motion-threshold-hysteresis.md"
CHECKOUT_CREDENTIALS_PLAN = DOCS_PLANS / "2026-06-12-hosted-checkout-credentials.md"
CODEQL_PLAN = DOCS_PLANS / "2026-06-12-codeql-manual-swift-build.md"
PROMPT_VALUE_REPEAT_PLAN = DOCS_PLANS / "2026-06-13-no-immediate-prompt-value-repeat.md"
MOTION_FAILURE_RESET_PLAN = DOCS_PLANS / "2026-06-13-motion-failure-reset.md"
BLANK_PROMPT_FILTER_PLAN = DOCS_PLANS / "2026-06-13-blank-prompt-filter.md"
MAKE_ROOT_PROTECTION_PLAN = DOCS_PLANS / "2026-06-14-make-root-override-protection.md"
MAKE_AUTHORITY_ISOLATION_PLAN = DOCS_PLANS / "2026-06-21-make-authority-isolation.md"
MOTION_DEVICE_CHECKLIST_PLAN = DOCS_PLANS / "2026-06-14-motion-device-verification-checklist.md"
STALE_MOTION_CALLBACK_PLAN = DOCS_PLANS / "2026-06-16-stale-motion-callback-guard.md"
DISAPPEARANCE_IDLE_RESET_PLAN = DOCS_PLANS / "2026-06-16-disappearance-idle-reset.md"
RETIRED_SDKS = ("Crashlytics.framework", "Fabric.framework", "MoPub.framework")


def fail(message):
    print(f"check_ios_contracts.py: {message}", file=sys.stderr)
    return 1


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def registered_main_checks():
    checker_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    for node in checker_tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            for statement in node.body:
                if (
                    isinstance(statement, ast.Assign)
                    and any(isinstance(target, ast.Name) and target.id == "checks" for target in statement.targets)
                    and isinstance(statement.value, (ast.List, ast.Tuple))
                ):
                    return {
                        element.id for element in statement.value.elts if isinstance(element, ast.Name)
                    }
    return set()


def workflow_step_blocks(workflow, action):
    lines = workflow.splitlines()
    blocks = []
    prefix = "- name: Check out repository"

    for index, line in enumerate(lines):
        if line.strip() != prefix:
            continue
        indentation = len(line) - len(line.lstrip())
        block = [line]
        for following_line in lines[index + 1 :]:
            following_indentation = len(following_line) - len(following_line.lstrip())
            if following_line.strip() and following_indentation <= indentation:
                break
            block.append(following_line)
        text = "\n".join(block)
        if action in text:
            blocks.append(text)

    return blocks


def load_plist(relative_path):
    with (ROOT / relative_path).open("rb") as plist_file:
        return plistlib.load(plist_file)


def check_project_files_parse():
    gitignore = read_text(".gitignore")
    require("__pycache__/" in gitignore, "Python bytecode cache directories must be ignored")
    require("*.py[cod]" in gitignore, "Python bytecode files must be ignored")

    project = read_text("UpDown.xcodeproj/project.pbxproj")
    plist_paths = sorted(set(re.findall(r"INFOPLIST_FILE = ([^;]+);", project)))
    require(plist_paths, "project must reference Info.plist files")
    for plist_path in plist_paths:
        normalized = plist_path.strip('"')
        require((ROOT / normalized).exists(), f"{normalized} is referenced but missing")
        load_plist(normalized)

    for relative_path in (
        "UpDown/Base.lproj/Main.storyboard",
        "UpDown/Base.lproj/LaunchScreen.xib",
        "UpDown.xcodeproj/xcshareddata/xcschemes/UpDown.xcscheme",
    ):
        ET.parse(ROOT / relative_path)

    for path in (ROOT / "UpDown/Images.xcassets").rglob("Contents.json"):
        json.loads(path.read_text(encoding="utf-8"))

    icon_catalog = read_text("UpDown/Images.xcassets/AppIcon.appiconset/Contents.json")
    for icon in ("Icon-iPad-76@2x.png", "Icon-iPad-83.5@2x.png", "Icon-AppStore-1024.png"):
        require(icon in icon_catalog and (ROOT / "UpDown/Images.xcassets/AppIcon.appiconset" / icon).exists(), f"required app icon is missing: {icon}")


def check_modern_project_contracts():
    project = read_text("UpDown.xcodeproj/project.pbxproj")
    scheme = read_text("UpDown.xcodeproj/xcshareddata/xcschemes/UpDown.xcscheme")

    require("PromptProvider.swift in Sources" in project, "prompt provider must compile in the app target")
    require("UpDownTests.swift in Sources" in project, "XCTest source must compile in the test target")
    require(project.count("SWIFT_VERSION = 5.0;") >= 6, "all project and target configurations must use Swift 5")
    require(project.count("IPHONEOS_DEPLOYMENT_TARGET = 13.0;") >= 6, "all configurations must target iOS 13+")
    require("PRODUCT_BUNDLE_IDENTIFIER = com.garethpaul.UpDown;" in project, "app bundle identifier must be explicit")
    require("PRODUCT_BUNDLE_IDENTIFIER = com.garethpaul.UpDownTests;" in project, "test bundle identifier must be explicit")
    require("ENABLE_TESTABILITY = YES;" in project, "Debug app builds must support @testable XCTest imports")
    require("/Users/" not in project, "Xcode project must not contain developer-specific absolute paths")
    require("UpDownTests.xctest" in scheme and 'skipped = "NO"' in scheme, "shared scheme must run UpDownTests")

    for sdk in RETIRED_SDKS:
        require(not (ROOT / sdk).exists(), f"retired bundled SDK must be removed: {sdk}")
        require(sdk not in project, f"Xcode project must not reference retired SDK: {sdk}")


def check_offline_prompt_contracts():
    provider = read_text("UpDown/PromptProvider.swift")
    tests = read_text("UpDownTests/UpDownTests.swift")
    all_swift = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "UpDown").glob("*.swift"))

    require(not (ROOT / "UpDown/URL.swift").exists(), "dead remote prompt client must remain removed")
    for forbidden in ("URLSession", "appspot.com", "import MoPub", "import Fabric", "import Crashlytics"):
        require(forbidden not in all_swift, f"app source must remain independent of {forbidden}")

    prompts_match = re.search(r"static let defaultPrompts = \[(?P<body>.*?)\n    \]", provider, re.DOTALL)
    require(prompts_match is not None, "default offline prompt source must be present")
    require(len(re.findall(r'^\s*".+",?$', prompts_match.group("body"), re.MULTILINE)) >= 20, "offline source must contain at least 20 prompts")
    require("guard !prompts.isEmpty" in provider, "empty prompt sources must fail safely")
    require("final class PromptProvider" in provider, "prompt provider must retain selection history")
    require("private var previousPromptKey: String?" in provider, "prompt provider must track the previous canonical value")
    require("prompts.filter { $0.comparisonKey != previousKey }" in provider, "prompt provider must exclude the previous canonical value")
    require("alternatives.isEmpty ? prompts : alternatives" in provider, "all-identical prompt sources must remain playable")
    require("indexProvider(candidates.count)" in provider, "injected selection must use the eligible candidate count")
    require("candidates.indices.contains(candidate)" in provider, "injected candidate indexes must be bounds checked")
    require("previousPromptKey = prompt.comparisonKey" in provider, "prompt provider must remember the returned canonical value")
    require("Set(" not in provider, "eligible duplicate prompts must retain source weighting")
    require("import Foundation" in provider, "blank prompt filtering must import Foundation string utilities")
    require(
        "self.prompts = prompts.compactMap" in provider
        and "guard !comparisonKey.isEmpty" in provider,
        "prompt provider must filter empty and whitespace-only source values once during initialization",
    )
    require(
        "self.prompts = prompts.map" not in provider,
        "prompt provider must preserve accepted display strings instead of rewriting them",
    )
    for contract in (
        "private static func comparisonKey(for prompt: String) -> String",
        ".components(separatedBy: .whitespacesAndNewlines)",
        '.joined(separator: " ")',
        ".precomposedStringWithCanonicalMapping",
        "options: [.caseInsensitive, .widthInsensitive]",
        'Locale(identifier: "en_US_POSIX")',
    ):
        require(contract in provider, f"prompt canonicalization must include {contract}")

    for test_name in (
        "testReturnsPromptAtInjectedIndex",
        "testEmptyPromptListReturnsNilWithoutSelectingIndex",
        "testWhitespaceOnlyPromptListReturnsNilWithoutSelectingIndex",
        "testMixedPromptListFiltersBlankValuesWithoutRewritingClues",
        "testInvalidInjectedIndexReturnsNil",
        "testConsecutiveSelectionsDoNotRepeatWhenAlternativesExist",
        "testSinglePromptCanBeSelectedRepeatedly",
        "testDuplicatePromptValuesDoNotRepeatWhenAnotherValueExists",
        "testEligibleDuplicateValuesRetainTheirSelectionWeight",
        "testAllIdenticalPromptValuesRemainPlayable",
        "testVisuallyEquivalentPromptValuesDoNotRepeatWhenAlternativeExists",
        "testDefaultPromptSourceContainsPlayableValues",
    ):
        require(test_name in tests, f"XCTest coverage is missing {test_name}")
    require(
        'XCTAssertEqual(provider.nextPrompt(), "  padded clue  ")' in tests,
        "XCTest must prove accepted prompt display strings are not trimmed",
    )
    whitespace_test = re.search(
        r"func testWhitespaceOnlyPromptListReturnsNilWithoutSelectingIndex\(\) \{(?P<body>.*?)\n    \}",
        tests,
        re.DOTALL,
    )
    require(
        whitespace_test is not None
        and "XCTFail" in whitespace_test.group("body")
        and "XCTAssertNil(provider.nextPrompt())" in whitespace_test.group("body"),
        "XCTest must prove all-blank sources return nil without selecting an index",
    )
    mixed_test = re.search(
        r"func testMixedPromptListFiltersBlankValuesWithoutRewritingClues\(\) \{(?P<body>.*?)\n    \}",
        tests,
        re.DOTALL,
    )
    require(
        mixed_test is not None and "XCTAssertEqual(count, 2)" in mixed_test.group("body"),
        "XCTest must prove mixed sources expose only nonblank candidates",
    )
    require(
        "PromptProvider.defaultPrompts.allSatisfy" in tests
        and "trimmingCharacters(in: .whitespacesAndNewlines).isEmpty" in tests,
        "XCTest must reject whitespace-only values in the default prompt inventory",
    )

    documentation = {
        "README.md": "blank and whitespace-only prompt values",
        "SECURITY.md": "Blank offline prompt values",
        "VISION.md": "Reject blank offline prompt values",
        "CHANGES.md": "Filtered blank and whitespace-only offline prompts",
    }
    for relative_path, phrase in documentation.items():
        require(phrase in read_text(relative_path), f"{relative_path} must document blank prompt filtering")


def check_motion_lifecycle_contracts():
    source = read_text("UpDown/ViewController.swift")
    tests = read_text("UpDownTests/UpDownTests.swift")
    require("[weak self]" in source, "motion callback must not retain the view controller")
    require(
        "startDeviceMotionUpdates(to: .main) { [weak self] motion, error in" in source,
        "motion callback must capture the delivery error for fail-safe handling",
    )
    require("motionManager.isDeviceMotionAvailable" in source, "motion availability must be checked")
    require("!motionManager.isDeviceMotionActive" in source, "duplicate motion subscriptions must be prevented")
    require("motionManager.stopDeviceMotionUpdates()" in source, "motion updates must stop off screen")
    require("override func viewWillDisappear(_ animated: Bool)" in source, "modern lifecycle override must be used")
    for contract in (
        "struct MotionLifecycleState",
        "var shouldRunMotionUpdates: Bool",
        "isViewVisible && isApplicationActive",
        "UIApplication.willResignActiveNotification",
        "UIApplication.didBecomeActiveNotification",
        "private func synchronizeMotionUpdates()",
        "private func endMotionUpdates()",
    ):
        require(contract in source, f"application motion lifecycle must include {contract}")
    require("promptProvider.nextPrompt()" in source, "motion play state must use the offline prompt provider")
    require("@IBOutlet private weak var gameText" in source, "storyboard outlet must avoid retaining its view")
    require("struct MotionHysteresisGate" in source, "motion thresholds must use a testable hysteresis gate")
    require("startRange: ClosedRange<Double> = 1.0...2.6" in source, "motion entry range must preserve the existing thresholds")
    require("continuationRange: ClosedRange<Double> = 0.9...2.7" in source, "motion continuation range must tolerate boundary noise")
    require("currentlyPlaying ? continuationRange : startRange" in source, "motion gate must choose thresholds from current play state")
    require("motionGate.shouldPlay(" in source, "motion callback must use the hysteresis gate")
    require(
        "func shouldResetForUnavailableSample(currentlyPlaying: Bool) -> Bool" in source,
        "motion failures must use a testable active-state reset decision",
    )
    require(
        "guard error == nil, let attitude = motion?.attitude else" in source,
        "motion callback must treat errors and missing attitudes as unavailable samples",
    )
    require(
        "motionGate.shouldResetForUnavailableSample(currentlyPlaying: displayState.playing)" in source,
        "motion callback must consult the unavailable-sample reset decision",
    )
    require(
        "func shouldResetForUnavailableSample(currentlyPlaying: Bool) -> Bool {\n        currentlyPlaying\n    }" in source,
        "unavailable samples must reset only an active game",
    )
    unavailable_guard = source[
        source.index("guard error == nil, let attitude = motion?.attitude else") :
        source.index("let magnitude = sqrt(")
    ]
    unavailable_contracts = (
        "guard error == nil, let attitude = motion?.attitude else",
        "if motionGate.shouldResetForUnavailableSample(currentlyPlaying: displayState.playing)",
        "stop()",
        "return",
    )
    unavailable_positions = [unavailable_guard.index(contract) for contract in unavailable_contracts]
    require(
        unavailable_positions == sorted(unavailable_positions),
        "motion errors and missing samples must reset active play before returning",
    )
    require("if (1...2.6).contains(magnitude)" not in source, "motion callback must not bypass hysteresis")

    readme = read_text("README.md")
    for phrase in (
        "Physical-Device Motion Checklist",
        "outside magnitude `1.0...2.6`",
        "within `0.9...2.7`",
        "exactly one prompt appears",
        "returns the game to idle",
        "one motion subscription resumes",
        "pending physical-device execution",
        "docs/plans/2026-06-14-motion-device-verification-checklist.md",
    ):
        require(phrase in readme, f"README must document device verification contract: {phrase}")
    require(
        "Keep physical-device threshold and lifecycle verification notes" in read_text("VISION.md"),
        "VISION must preserve the physical-device verification boundary",
    )
    require(
        "pending physical-device checklist" in read_text("CHANGES.md"),
        "CHANGES must record the pending physical-device checklist",
    )
    for test_name in (
        "testStartsOnlyInsideStartRange",
        "testKeepsPlayingAcrossSmallBoundaryFluctuations",
        "testStopsOutsideContinuationRange",
        "testUnavailableSampleResetsActivePlayState",
        "testUnavailableSampleLeavesIdleStateUnchanged",
        "testVisibleActiveViewRunsMotionUpdates",
        "testBackgroundingVisibleViewSuspendsMotionUpdates",
        "testForegroundingVisibleViewRestartsMotionUpdates",
        "testForegroundingHiddenViewDoesNotStartMotionUpdates",
        "testViewAppearingWhileApplicationIsInactiveDoesNotStartMotionUpdates",
    ):
        require(test_name in tests, f"XCTest coverage is missing {test_name}")


def check_stale_motion_callback_contracts():
    source = read_text("UpDown/ViewController.swift")
    tests = read_text("UpDownTests/UpDownTests.swift")

    for contract in (
        "struct MotionUpdateSession",
        "private(set) var generation = 0",
        "mutating func begin() -> Int",
        "mutating func invalidate()",
        "func accepts(_ capturedGeneration: Int) -> Bool",
        "private var motionUpdateSession = MotionUpdateSession()",
        "let motionGeneration = motionUpdateSession.begin()",
        "guard motionUpdateSession.accepts(motionGeneration) else",
    ):
        require(contract in source, f"stale motion callback guard must include {contract}")

    session = source[
        source.index("struct MotionUpdateSession") :
        source.index("final class ViewController")
    ]
    require(session.count("generation += 1") == 2, "begin and invalidate must each advance the motion generation")
    require("return generation" in session, "begin must return the advanced motion generation")
    require(
        "capturedGeneration == generation" in session,
        "motion callbacks must match the current generation exactly",
    )

    end_updates = source[
        source.index("private func endMotionUpdates()") :
        source.index("private func beginMotionUpdates()")
    ]
    invalidate_position = end_updates.index("motionUpdateSession.invalidate()")
    stop_position = end_updates.index("motionManager.stopDeviceMotionUpdates()")
    require(
        invalidate_position < stop_position,
        "motion callbacks must be invalidated before updates stop",
    )

    callback = source[
        source.index("startDeviceMotionUpdates(to: .main)") :
        source.index("let magnitude = sqrt(")
    ]
    require(
        callback.index("guard let self else") < callback.index("guard motionUpdateSession.accepts(motionGeneration) else"),
        "motion callback must validate its captured session after weak self recovery",
    )
    require(
        callback.index("guard motionUpdateSession.accepts(motionGeneration) else")
        < callback.index("guard error == nil, let attitude = motion?.attitude else"),
        "stale callbacks must return before processing samples or errors",
    )

    for test_name in (
        "testCurrentGenerationIsAccepted",
        "testInvalidatedGenerationIsRejected",
        "testReplacementSessionRejectsPreviousGeneration",
    ):
        require(test_name in tests, f"XCTest coverage is missing {test_name}")
    require(
        "XCTAssertTrue(session.accepts(generation))" in tests,
        "XCTest must accept the current motion generation",
    )
    require(
        "session.invalidate()" in tests and "XCTAssertFalse(session.accepts(generation))" in tests,
        "XCTest must reject an invalidated motion generation",
    )
    require(
        "XCTAssertFalse(session.accepts(previousGeneration))" in tests
        and "XCTAssertTrue(session.accepts(currentGeneration))" in tests,
        "XCTest must reject a replaced generation and accept its replacement",
    )
    require(
        "check_stale_motion_callback_contracts" in registered_main_checks(),
        "stale motion callback contracts must remain registered",
    )

    documentation = {
        "README.md": "Queued callbacks from an ended motion session are ignored",
        "SECURITY.md": "Queued callbacks from ended Core Motion sessions are rejected",
        "VISION.md": "Ignore queued callbacks from ended CoreMotion sessions",
        "CHANGES.md": "Rejected queued Core Motion callbacks from ended view sessions",
    }
    for relative_path, phrase in documentation.items():
        require(phrase in read_text(relative_path), f"{relative_path} must document stale motion callback rejection")


def check_disappearance_idle_reset_contracts():
    source = read_text("UpDown/ViewController.swift")
    tests = read_text("UpDownTests/UpDownTests.swift")

    for contract in (
        "struct GameDisplayState",
        'static let idleText = "Tilt the phone up for a word"',
        'static let unavailableText = "No prompts available"',
        "private(set) var text = GameDisplayState.idleText",
        "private(set) var playing = false",
        "mutating func show(prompt: String)",
        "mutating func showUnavailable()",
        "mutating func stop()",
        "private var displayState = GameDisplayState()",
        "gameText.text = displayState.text",
    ):
        require(contract in source, f"game display state must include {contract}")

    display_state = source[
        source.index("struct GameDisplayState") :
        source.index("final class ViewController")
    ]
    state_transitions = (
        "text = prompt\n        playing = true",
        "text = Self.unavailableText\n        playing = false",
        "text = Self.idleText\n        playing = false",
    )
    for transition in state_transitions:
        require(transition in display_state, f"game display transition must preserve {transition!r}")

    disappearance = source[
        source.index("override func viewWillDisappear(_ animated: Bool)") :
        source.index("@objc private func applicationWillResignActive()")
    ]
    for contract in (
        "motionLifecycleState.viewWillDisappear()",
        "synchronizeMotionUpdates()",
    ):
        require(contract in disappearance, f"view disappearance must include {contract}")

    end_updates = source[
        source.index("private func endMotionUpdates()") :
        source.index("private func beginMotionUpdates()")
    ]
    ordered_contracts = (
        "motionUpdateSession.invalidate()",
        "motionManager.stopDeviceMotionUpdates()",
        "stop()",
    )
    positions = [end_updates.index(contract) for contract in ordered_contracts]
    require(
        positions == sorted(positions),
        "view disappearance must invalidate callbacks, stop motion, then reset the display",
    )
    require(
        "playing = false" not in end_updates,
        "view disappearance must use the shared stop transition instead of clearing state directly",
    )

    stop_method = source[
        source.index("private func stop()") :
        source.index("private func renderDisplayState()")
    ]
    require(
        stop_method.index("displayState.stop()") < stop_method.index("renderDisplayState()"),
        "the stop transition must reset state before rendering idle UI",
    )

    for test_name in (
        "testStoppingActiveGameReturnsVisibleAndLogicalStateToIdle",
        "testStoppingIdleGameKeepsVisibleAndLogicalStateIdle",
    ):
        require(test_name in tests, f"XCTest coverage is missing {test_name}")
    require(
        tests.count("XCTAssertFalse(state.playing)") >= 2
        and tests.count("XCTAssertEqual(state.text, GameDisplayState.idleText)") >= 2,
        "XCTest must prove active and idle stops synchronize visible and logical state",
    )
    require(
        "check_disappearance_idle_reset_contracts" in registered_main_checks(),
        "disappearance idle-reset contracts must remain registered",
    )

    documentation = {
        "README.md": "Leaving the game view clears any visible prompt and returns the display to idle",
        "SECURITY.md": "Leaving the game view clears visible prompt state",
        "VISION.md": "Reset visible and logical game state together when the view disappears",
        "CHANGES.md": "Cleared visible prompt state when the game view disappears",
    }
    for relative_path, phrase in documentation.items():
        require(phrase in read_text(relative_path), f"{relative_path} must document disappearance idle reset")


def check_hosted_verification():
    workflow = read_text(".github/workflows/check.yml")
    checkout_action = "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10"
    for contract in (
        "pull_request:",
        "workflow_dispatch:",
        "branches:\n      - master",
        "permissions:\n  contents: read",
        "cancel-in-progress: true",
        "runs-on: ubuntu-24.04",
        "runs-on: macos-15",
        "timeout-minutes: 15",
        'python-version: ["3.10", "3.12", "3.14"]',
        checkout_action,
        "persist-credentials: false",
        "run: /usr/bin/make static",
        "run: /usr/bin/make check",
    ):
        require(contract in workflow, f"hosted verification must include {contract!r}")
    require("@v" not in workflow, "hosted actions must use immutable commits")
    checkout_blocks = workflow_step_blocks(workflow, checkout_action)
    require(len(checkout_blocks) == 2, "both hosted jobs must define one pinned checkout step")
    require(
        all("\n        with:\n          persist-credentials: false" in block for block in checkout_blocks),
        "each checkout step must disable credential persistence in its own with block",
    )
    require(workflow.count("persist-credentials:") == 2, "credential persistence must be configured exactly twice")
    require("persist-credentials: true" not in workflow, "hosted checkout credentials must not persist")
    require("ubuntu-latest" not in workflow, "hosted static verification must use a fixed Ubuntu runner")
    require("group: check-${{ github.workflow }}-${{ github.ref }}" in workflow, "workflow concurrency must include workflow and ref")

    makefile = read_text("Makefile")
    makefile_lines = set(makefile.splitlines())
    for contract in (
        ".DEFAULT_GOAL := check",
        ".SECONDEXPANSION:",
        "PYTHON ?= python3",
        "override PYTHON := $(value PYTHON)",
        "override SHELL := /bin/sh",
        "override .SHELLFLAGS := -c",
        "override MAKEFILES :=",
        "ifneq ($(origin MAKEFILE_LIST),file)",
        "export ROOT",
        "root-test:",
        '\t/bin/sh "$$ROOT/scripts/test-makefile-root.sh"',
    ):
        require(contract in makefile_lines, f"Makefile authority contract is missing {contract!r}")
    require("MAKEFLAGS must not be overridden" in makefile, "Makefile must reject caller MAKEFLAGS assignments")
    require("MAKEFILES must be empty" in makefile, "Makefile must reject startup include files")
    require("MAKEFILE_LIST must not be overridden" in makefile, "Makefile must reject Makefile-list replacement")
    require("PYTHON must be a literal executable path" in makefile, "Makefile must reject Python Make syntax")
    require('"$$PYTHON" "$$ROOT/scripts/check_ios_contracts.py"' in makefile, "Makefile must use the rooted checker path")
    require('"$$ROOT/scripts/test_ios.sh"' in makefile, "Makefile must use the rooted iOS test path")
    require('cd "$$ROOT" && xcodebuild' in makefile, "Makefile must run builds from the repository root")
    require("verify: root-test static test" in makefile_lines, "full verification must run the authority harness")

    authority_test = read_text("scripts/test-makefile-root.sh")
    for contract in (
        "35 target/authority cases",
        "literal hostile Python path",
        "MAKEFILE_LIST must not be overridden",
        "MAKEFILES must be empty",
        "MAKEFLAGS must not be overridden",
        "--ignore-errors",
    ):
        require(contract in authority_test, f"Make authority harness must include {contract!r}")

    test_script = read_text("scripts/test_ios.sh")
    require('ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"' in test_script, "iOS test script must resolve the repository root")
    require('cd "$ROOT"' in test_script, "iOS test script must run from the repository root")
    require("xcrun simctl list devices available -j" in test_script, "iOS tests must discover available simulators")
    require("xcrun simctl create UpDown-CI" in test_script, "iOS tests must create a simulator when only a runtime is installed")
    require("Designed for [iPad,iPhone]" in test_script, "iOS tests must retain an Apple Silicon fallback destination")


def check_codeql_verification():
    workflow = read_text(".github/workflows/codeql.yml")
    for contract in (
        "push:\n    branches:\n      - master",
        "pull_request:",
        "schedule:",
        "workflow_dispatch:",
        "permissions:\n  contents: read\n  security-events: write",
        "group: codeql-${{ github.workflow }}-${{ github.ref }}",
        "runs-on: ubuntu-24.04",
        "runs-on: macos-15",
        "timeout-minutes: 10",
        "timeout-minutes: 25",
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
        "github/codeql-action/init@8aad20d150bbac5944a9f9d289da16a4b0d87c1e",
        "github/codeql-action/analyze@8aad20d150bbac5944a9f9d289da16a4b0d87c1e",
        "persist-credentials: false",
        "languages: swift",
        "build-mode: manual",
        "-project UpDown.xcodeproj",
        "-sdk iphonesimulator",
        "ARCHS=arm64",
        "ONLY_ACTIVE_ARCH=YES",
        "CODE_SIGNING_ALLOWED=NO",
    ):
        require(contract in workflow, f"CodeQL verification must include {contract!r}")
    require("\n          -target UpDown\n" in workflow, "Swift CodeQL must build the exact UpDown app target")
    require("autobuild" not in workflow, "Swift CodeQL must use the explicit app-target build")
    require("@v" not in workflow, "CodeQL actions must use immutable commits")
    require(workflow.count("persist-credentials:") == 2, "both CodeQL checkout steps must configure credentials")
    require("persist-credentials: true" not in workflow, "CodeQL checkout credentials must not persist")
    require(workflow.count("timeout-minutes: 25") == 1, "Swift CodeQL must retain one 25-minute bound")


def check_docs_plans():
    require(DOCS_PLANS.is_dir(), "docs/plans must exist")
    plans = sorted(DOCS_PLANS.glob("*.md"))
    require(MODERNIZATION_PLAN in plans, f"{MODERNIZATION_PLAN.relative_to(ROOT)} must be present")
    require(HOSTED_VERIFICATION_PLAN in plans, f"{HOSTED_VERIFICATION_PLAN.relative_to(ROOT)} must be present")
    require(NO_REPEAT_PLAN in plans, f"{NO_REPEAT_PLAN.relative_to(ROOT)} must be present")
    require(MOTION_HYSTERESIS_PLAN in plans, f"{MOTION_HYSTERESIS_PLAN.relative_to(ROOT)} must be present")
    require(CHECKOUT_CREDENTIALS_PLAN in plans, f"{CHECKOUT_CREDENTIALS_PLAN.relative_to(ROOT)} must be present")
    require(CODEQL_PLAN in plans, f"{CODEQL_PLAN.relative_to(ROOT)} must be present")
    require(PROMPT_VALUE_REPEAT_PLAN in plans, f"{PROMPT_VALUE_REPEAT_PLAN.relative_to(ROOT)} must be present")
    require(MOTION_FAILURE_RESET_PLAN in plans, f"{MOTION_FAILURE_RESET_PLAN.relative_to(ROOT)} must be present")
    require(BLANK_PROMPT_FILTER_PLAN in plans, f"{BLANK_PROMPT_FILTER_PLAN.relative_to(ROOT)} must be present")
    require(MAKE_ROOT_PROTECTION_PLAN in plans, f"{MAKE_ROOT_PROTECTION_PLAN.relative_to(ROOT)} must be present")
    require(
        MAKE_AUTHORITY_ISOLATION_PLAN in plans,
        f"{MAKE_AUTHORITY_ISOLATION_PLAN.relative_to(ROOT)} must be present",
    )
    require(MOTION_DEVICE_CHECKLIST_PLAN in plans, f"{MOTION_DEVICE_CHECKLIST_PLAN.relative_to(ROOT)} must be present")
    require(STALE_MOTION_CALLBACK_PLAN in plans, f"{STALE_MOTION_CALLBACK_PLAN.relative_to(ROOT)} must be present")
    require(
        DISAPPEARANCE_IDLE_RESET_PLAN in plans,
        f"{DISAPPEARANCE_IDLE_RESET_PLAN.relative_to(ROOT)} must be present",
    )
    require(
        "check_stale_motion_callback_contracts" in registered_main_checks(),
        "stale motion callback contracts must remain registered",
    )
    require(
        "check_disappearance_idle_reset_contracts" in registered_main_checks(),
        "disappearance idle-reset contracts must remain registered",
    )
    for plan in plans:
        text = plan.read_text(encoding="utf-8")
        require("Status: Completed" in text, f"{plan.name} must be completed")
        require("make check" in text, f"{plan.name} must document make check verification")


def main():
    checks = (
        check_project_files_parse,
        check_modern_project_contracts,
        check_offline_prompt_contracts,
        check_motion_lifecycle_contracts,
        check_stale_motion_callback_contracts,
        check_disappearance_idle_reset_contracts,
        check_hosted_verification,
        check_codeql_verification,
        check_docs_plans,
    )
    try:
        for check in checks:
            check()
    except (AssertionError, ET.ParseError, json.JSONDecodeError, plistlib.InvalidFileException) as exc:
        return fail(str(exc))

    print(f"UpDown static contracts passed ({len(checks)} checks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
