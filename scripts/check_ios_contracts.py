#!/usr/bin/env python3
"""Static verification for the legacy UpDown iOS project."""

from pathlib import Path
import json
import plistlib
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs/plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-updown-baseline.md"


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


def check_project_manifest_references():
    project = read_text("UpDown.xcodeproj/project.pbxproj")
    plist_paths = sorted(set(re.findall(r"INFOPLIST_FILE = ([^;]+);", project)))
    require(plist_paths, "project must reference Info.plist files")
    for plist_path in plist_paths:
        path = ROOT / plist_path.strip('"')
        require(path.exists(), f"{plist_path} is referenced by Xcode but not checked in")
        load_plist(plist_path.strip('"'))

    require("UpDownTests.swift in Sources" in project, "test source must remain in the Xcode project")


def check_project_files_parse():
    app_info = load_plist("UpDown/Info.plist")
    test_info = load_plist("UpDownTests/Info.plist")
    require(app_info["UIMainStoryboardFile"] == "Main", "app must launch Main.storyboard")
    require(test_info["CFBundlePackageType"] == "BNDL", "test target must remain a bundle")

    for relative_path in [
        "UpDown/Base.lproj/Main.storyboard",
        "UpDown/Base.lproj/LaunchScreen.xib",
    ]:
        ET.parse(ROOT / relative_path)

    for path in (ROOT / "UpDown/Images.xcassets").rglob("Contents.json"):
        json.loads(path.read_text(encoding="utf-8"))


def check_url_client_guard():
    source = read_text("UpDown/URL.swift")
    require("NSURL(string: url)!" not in source, "URL client must not force-unwrap request URLs")
    require("data!" not in source, "URL client must not force-unwrap response data")
    require("strData!" not in source, "URL client must not force-unwrap decoded response text")
    require("try json" not in source, "URL client must not reference undefined JSON parsing state")
    require("completed(succeeded: false" in source, "URL client must report request/decode failures")


def check_remote_endpoint_is_https():
    view_controller = read_text("UpDown/ViewController.swift")
    require("https://garethpaul-app.appspot.com/api/updown" in view_controller, "remote prompt endpoint must stay HTTPS")


def check_prompt_fetch_failure_handling():
    view_controller = read_text("UpDown/ViewController.swift")
    require("if succeeded && data.length > 0" in view_controller, "prompt fetch must check success and non-empty data")
    require('"Prompt unavailable"' in view_controller, "prompt fetch failures must show visible fallback text")
    require("self.playing = false" in view_controller, "prompt fetch failures must keep playing state false")
    require(
        view_controller.index("if succeeded && data.length > 0") < view_controller.index('"Prompt unavailable"'),
        "prompt success branch must be checked before failure fallback",
    )


def check_motion_callback_guard():
    view_controller = read_text("UpDown/ViewController.swift")
    require("motion!" not in view_controller, "motion callback must not force-unwrap motion data")
    require("if let currentMotion = motion" in view_controller, "motion callback must guard optional motion data")


def check_play_state_is_not_implicitly_unwrapped():
    view_controller = read_text("UpDown/ViewController.swift")
    require("var playing = false as Bool!" not in view_controller, "play state must not be an implicitly unwrapped Bool")
    require("self.playing as Bool!" not in view_controller, "motion callback must not force-cast play state")
    require("var playing = false" in view_controller, "play state must remain initialized as a concrete Bool")


def check_prompt_fetch_inflight_guard():
    view_controller = read_text("UpDown/ViewController.swift")
    require("var fetchingPrompt = false" in view_controller, "prompt fetch state must start false")
    require("if self.fetchingPrompt" in view_controller, "play must skip duplicate prompt fetches")
    require("self.fetchingPrompt = true" in view_controller, "play must mark prompt fetches in flight")
    require("self.fetchingPrompt = false" in view_controller, "prompt completion must clear in-flight state")
    require(
        view_controller.index("if self.fetchingPrompt") < view_controller.index("url.get("),
        "duplicate prompt fetch guard must run before starting the network request",
    )
    require(
        view_controller.index("self.fetchingPrompt = true") < view_controller.index("url.get("),
        "prompt fetch must be marked in flight before starting the network request",
    )


def check_docs_plans():
    require(DOCS_PLANS.is_dir(), "docs/plans must exist")
    plans = sorted(DOCS_PLANS.glob("*.md"))
    require(plans, "docs/plans must contain completed maintenance plans")
    require(CANONICAL_PLAN in plans, f"{CANONICAL_PLAN.relative_to(ROOT)} must be present")

    for plan in plans:
        text = plan.read_text(encoding="utf-8")
        require("Status: Completed" in text, f"{plan.name} must be completed")
        require("make check" in text, f"{plan.name} must document make check verification")


def main():
    checks = [
        check_project_manifest_references,
        check_project_files_parse,
        check_url_client_guard,
        check_remote_endpoint_is_https,
        check_prompt_fetch_failure_handling,
        check_motion_callback_guard,
        check_play_state_is_not_implicitly_unwrapped,
        check_prompt_fetch_inflight_guard,
        check_docs_plans,
    ]
    try:
        for check in checks:
            check()
    except (AssertionError, ET.ParseError, json.JSONDecodeError, plistlib.InvalidFileException) as exc:
        return fail(str(exc))

    print(f"UpDown static contracts passed ({len(checks)} checks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
