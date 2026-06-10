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
STALE_PROMPT_PLAN = DOCS_PLANS / "2026-06-09-stale-prompt-completion-guard.md"
HTTPS_URL_PLAN = DOCS_PLANS / "2026-06-09-url-client-https-guard.md"
URL_HOST_PLAN = DOCS_PLANS / "2026-06-09-url-client-host-guard.md"
INTERSTITIAL_AD_UNIT_PLAN = DOCS_PLANS / "2026-06-09-interstitial-ad-unit-guard.md"
HOSTED_VERIFICATION_PLAN = DOCS_PLANS / "2026-06-10-hosted-static-verification.md"


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
    require('requestURL.scheme != "https"' in source, "URL client must reject non-HTTPS request URLs")
    require(
        source.index('requestURL.scheme != "https"') < source.index("NSMutableURLRequest"),
        "URL client must validate HTTPS before constructing requests",
    )
    require("if let host = requestURL.host" in source, "URL client must guard request URL hosts")
    require("host.isEmpty" in source, "URL client must reject empty request URL hosts")
    require(
        source.index("if let host = requestURL.host") < source.index("NSMutableURLRequest"),
        "URL client must validate host presence before constructing requests",
    )
    require("response as? NSHTTPURLResponse" in source, "URL client must inspect HTTP responses")
    require("httpResponse.statusCode" in source, "URL client must inspect HTTP status codes")
    require("statusCode < 200" in source, "URL client must reject statuses below HTTP 200")
    require("statusCode >= 300" in source, "URL client must reject statuses outside the 2xx range")
    require(
        source.index("httpResponse.statusCode") < source.index("NSString(data: data"),
        "URL client must validate HTTP status before decoding response text",
    )


def check_remote_endpoint_is_https():
    view_controller = read_text("UpDown/ViewController.swift")
    require("https://garethpaul-app.appspot.com/api/updown" in view_controller, "remote prompt endpoint must stay HTTPS")


def check_fabric_build_phase_secrets_are_env_only():
    project = read_text("UpDown.xcodeproj/project.pbxproj")
    require(
        not re.search(r"Fabric\.framework/run [A-Fa-f0-9]{32,} [A-Fa-f0-9]{32,}", project),
        "Fabric build phase must not contain checked-in API keys or build secrets",
    )
    require("FABRIC_API_KEY" in project, "Fabric build phase must read the API key from the environment")
    require("FABRIC_BUILD_SECRET" in project, "Fabric build phase must read the build secret from the environment")
    require(
        "Fabric upload skipped: FABRIC_API_KEY and FABRIC_BUILD_SECRET are not set." in project,
        "Fabric build phase must skip uploads when local credentials are absent",
    )


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


def check_motion_lifecycle_guard():
    view_controller = read_text("UpDown/ViewController.swift")
    require(
        "override func viewWillAppear(animated: Bool)" in view_controller,
        "view controller must restart motion updates when it appears",
    )
    require(
        "super.viewWillAppear(animated)" in view_controller,
        "viewWillAppear must call its superclass implementation",
    )
    require(
        "if manager.deviceMotionActive" in view_controller,
        "motion setup must skip duplicate active device-motion updates",
    )
    require(
        "override func viewWillDisappear(animated: Bool)" in view_controller,
        "view controller must stop motion updates when it disappears",
    )
    require(
        "super.viewWillDisappear(animated)" in view_controller,
        "viewWillDisappear must call its superclass implementation",
    )
    require(
        "manager.stopDeviceMotionUpdates()" in view_controller,
        "view controller must stop device-motion updates off screen",
    )
    require(
        view_controller.index("if manager.deviceMotionActive")
        < view_controller.index("manager.startDeviceMotionUpdatesToQueue"),
        "motion active guard must run before starting device-motion updates",
    )


def check_stale_prompt_completion_guard():
    view_controller = read_text("UpDown/ViewController.swift")
    require(
        "var promptRequestID = 0" in view_controller,
        "prompt fetches must track request generations",
    )
    require(
        "let requestID = self.promptRequestID" in view_controller,
        "prompt fetch completions must capture the active request generation",
    )
    require(
        "if requestID != self.promptRequestID" in view_controller,
        "prompt fetch completions must ignore stale request generations",
    )
    require(
        view_controller.index("if requestID != self.promptRequestID")
        < view_controller.index("self.fetchingPrompt = false"),
        "stale prompt completion guard must run before clearing active fetch state",
    )
    require(
        "override func viewWillDisappear(animated: Bool)" in view_controller
        and "self.promptRequestID += 1" in view_controller,
        "view disappearance must invalidate pending prompt completions",
    )


def check_interstitial_ad_unit_guard():
    view_controller = read_text("UpDown/ViewController.swift")
    require(
        'MPInterstitialAdController(forAdUnitId: "YOUR_AD_UNIT_ID")' not in view_controller,
        "interstitial ads must not load directly from the placeholder ad unit ID",
    )
    require(
        "let InterstitialAdUnitID" in view_controller,
        "interstitial ad unit ID must be centralized for local configuration",
    )
    require(
        "MPInterstitialAdController(forAdUnitId: InterstitialAdUnitID)" in view_controller,
        "interstitial ad controller must use the centralized ad unit ID",
    )
    require(
        "func interstitialAdUnitConfigured() -> Bool" in view_controller,
        "view controller must expose an interstitial ad unit configuration guard",
    )
    require(
        'InterstitialAdUnitID != "YOUR_AD_UNIT_ID"' in view_controller,
        "interstitial ad unit guard must reject the checked-in placeholder",
    )
    require(
        "if self.interstitialAdUnitConfigured()" in view_controller,
        "viewDidLoad must skip interstitial loading when the placeholder ad unit remains",
    )
    require(
        view_controller.index("if self.interstitialAdUnitConfigured()")
        < view_controller.index("self.interstitial.loadAd()"),
        "interstitial ad unit guard must run before loadAd",
    )
    require(
        "self.interstitialAdUnitConfigured() && interstitial.ready" in view_controller,
        "interstitial presentation must verify the ad unit is configured before showing",
    )


def check_docs_plans():
    require(DOCS_PLANS.is_dir(), "docs/plans must exist")
    plans = sorted(DOCS_PLANS.glob("*.md"))
    require(plans, "docs/plans must contain completed maintenance plans")
    require(CANONICAL_PLAN in plans, f"{CANONICAL_PLAN.relative_to(ROOT)} must be present")
    require(STALE_PROMPT_PLAN in plans, f"{STALE_PROMPT_PLAN.relative_to(ROOT)} must be present")
    require(HTTPS_URL_PLAN in plans, f"{HTTPS_URL_PLAN.relative_to(ROOT)} must be present")
    require(URL_HOST_PLAN in plans, f"{URL_HOST_PLAN.relative_to(ROOT)} must be present")
    require(INTERSTITIAL_AD_UNIT_PLAN in plans, f"{INTERSTITIAL_AD_UNIT_PLAN.relative_to(ROOT)} must be present")
    require(HOSTED_VERIFICATION_PLAN in plans, f"{HOSTED_VERIFICATION_PLAN.relative_to(ROOT)} must be present")

    for plan in plans:
        text = plan.read_text(encoding="utf-8")
        require("Status: Completed" in text, f"{plan.name} must be completed")
        require("make check" in text, f"{plan.name} must document make check verification")


def check_hosted_verification():
    workflow = read_text(".github/workflows/check.yml")
    for contract in [
        "pull_request:",
        "branches:\n      - master",
        "permissions:\n  contents: read",
        "timeout-minutes: 5",
        'python-version: ["3.10", "3.12"]',
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
        "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405",
        "run: make check",
    ]:
        require(contract in workflow, f"hosted verification must include {contract!r}")
    require("@v" not in workflow, "hosted verification actions must use immutable commits")


def main():
    checks = [
        check_project_manifest_references,
        check_project_files_parse,
        check_url_client_guard,
        check_remote_endpoint_is_https,
        check_fabric_build_phase_secrets_are_env_only,
        check_prompt_fetch_failure_handling,
        check_motion_callback_guard,
        check_play_state_is_not_implicitly_unwrapped,
        check_prompt_fetch_inflight_guard,
        check_motion_lifecycle_guard,
        check_stale_prompt_completion_guard,
        check_interstitial_ad_unit_guard,
        check_hosted_verification,
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
