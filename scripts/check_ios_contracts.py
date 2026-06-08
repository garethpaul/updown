#!/usr/bin/env python3
"""Static verification for the legacy UpDown iOS project."""

from pathlib import Path
import json
import plistlib
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


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


def main():
    checks = [
        check_project_manifest_references,
        check_project_files_parse,
        check_url_client_guard,
        check_remote_endpoint_is_https,
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
