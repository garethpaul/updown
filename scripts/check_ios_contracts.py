#!/usr/bin/env python3
"""Portable contracts for the modernized UpDown iOS project."""

from pathlib import Path
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
RETIRED_SDKS = ("Crashlytics.framework", "Fabric.framework", "MoPub.framework")


def fail(message):
    print(f"check_ios_contracts.py: {message}", file=sys.stderr)
    return 1


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load_plist(relative_path):
    with (ROOT / relative_path).open("rb") as plist_file:
        return plistlib.load(plist_file)


def check_project_files_parse():
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
    require("private var previousIndex: Int?" in provider, "prompt provider must track the previous prompt")
    require("prompts.count - 1" in provider, "prompt provider must select from alternatives after the first prompt")
    require("candidate >= previousIndex" in provider, "prompt provider must remap selections around the previous prompt")
    require("(0..<candidateCount).contains(candidate)" in provider, "injected indexes must be bounds checked")

    for test_name in (
        "testReturnsPromptAtInjectedIndex",
        "testEmptyPromptListReturnsNilWithoutSelectingIndex",
        "testInvalidInjectedIndexReturnsNil",
        "testConsecutiveSelectionsDoNotRepeatWhenAlternativesExist",
        "testSinglePromptCanBeSelectedRepeatedly",
        "testDefaultPromptSourceContainsPlayableValues",
    ):
        require(test_name in tests, f"XCTest coverage is missing {test_name}")


def check_motion_lifecycle_contracts():
    source = read_text("UpDown/ViewController.swift")
    tests = read_text("UpDownTests/UpDownTests.swift")
    require("[weak self]" in source, "motion callback must not retain the view controller")
    require("motionManager.isDeviceMotionAvailable" in source, "motion availability must be checked")
    require("!motionManager.isDeviceMotionActive" in source, "duplicate motion subscriptions must be prevented")
    require("motionManager.stopDeviceMotionUpdates()" in source, "motion updates must stop off screen")
    require("override func viewWillDisappear(_ animated: Bool)" in source, "modern lifecycle override must be used")
    require("promptProvider.nextPrompt()" in source, "motion play state must use the offline prompt provider")
    require("@IBOutlet private weak var gameText" in source, "storyboard outlet must avoid retaining its view")
    require("struct MotionHysteresisGate" in source, "motion thresholds must use a testable hysteresis gate")
    require("startRange: ClosedRange<Double> = 1.0...2.6" in source, "motion entry range must preserve the existing thresholds")
    require("continuationRange: ClosedRange<Double> = 0.9...2.7" in source, "motion continuation range must tolerate boundary noise")
    require("currentlyPlaying ? continuationRange : startRange" in source, "motion gate must choose thresholds from current play state")
    require("motionGate.shouldPlay(" in source, "motion callback must use the hysteresis gate")
    require("if (1...2.6).contains(magnitude)" not in source, "motion callback must not bypass hysteresis")
    for test_name in (
        "testStartsOnlyInsideStartRange",
        "testKeepsPlayingAcrossSmallBoundaryFluctuations",
        "testStopsOutsideContinuationRange",
    ):
        require(test_name in tests, f"XCTest coverage is missing {test_name}")


def check_hosted_verification():
    workflow = read_text(".github/workflows/check.yml")
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
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
        "run: make static",
        "run: make check",
    ):
        require(contract in workflow, f"hosted verification must include {contract!r}")
    require("@v" not in workflow, "hosted actions must use immutable commits")
    require("ubuntu-latest" not in workflow, "hosted static verification must use a fixed Ubuntu runner")
    require("group: check-${{ github.workflow }}-${{ github.ref }}" in workflow, "workflow concurrency must include workflow and ref")

    makefile = read_text("Makefile")
    require(
        "ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))" in makefile,
        "Makefile must resolve commands from the repository root",
    )
    require('"$(ROOT)/scripts/check_ios_contracts.py"' in makefile, "Makefile must use the rooted checker path")
    require('"$(ROOT)/scripts/test_ios.sh"' in makefile, "Makefile must use the rooted iOS test path")
    require('cd "$(ROOT)" && xcodebuild' in makefile, "Makefile must run builds from the repository root")

    test_script = read_text("scripts/test_ios.sh")
    require('ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"' in test_script, "iOS test script must resolve the repository root")
    require('cd "$ROOT"' in test_script, "iOS test script must run from the repository root")
    require("xcrun simctl list devices available -j" in test_script, "iOS tests must discover available simulators")
    require("xcrun simctl create UpDown-CI" in test_script, "iOS tests must create a simulator when only a runtime is installed")
    require("Designed for [iPad,iPhone]" in test_script, "iOS tests must retain an Apple Silicon fallback destination")


def check_docs_plans():
    require(DOCS_PLANS.is_dir(), "docs/plans must exist")
    plans = sorted(DOCS_PLANS.glob("*.md"))
    require(MODERNIZATION_PLAN in plans, f"{MODERNIZATION_PLAN.relative_to(ROOT)} must be present")
    require(HOSTED_VERIFICATION_PLAN in plans, f"{HOSTED_VERIFICATION_PLAN.relative_to(ROOT)} must be present")
    require(NO_REPEAT_PLAN in plans, f"{NO_REPEAT_PLAN.relative_to(ROOT)} must be present")
    require(MOTION_HYSTERESIS_PLAN in plans, f"{MOTION_HYSTERESIS_PLAN.relative_to(ROOT)} must be present")
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
        check_hosted_verification,
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
