#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
XCODEBUILD="${1:-/usr/bin/xcodebuild}"
cd "$ROOT"

device_id="$({ /usr/bin/xcrun simctl list devices available -j 2>/dev/null || printf '{"devices":{}}'; } | /usr/bin/python3 -c '
import json, sys
devices = json.load(sys.stdin).get("devices", {})
for runtime_devices in reversed(list(devices.values())):
    for device in runtime_devices:
        if device.get("isAvailable") and device.get("name", "").startswith("iPhone"):
            print(device["udid"])
            raise SystemExit
')"

if [[ -z "$device_id" ]]; then
    runtime_id="$({ /usr/bin/xcrun simctl list runtimes available -j 2>/dev/null || printf '{"runtimes":[]}'; } | /usr/bin/python3 -c '
import json, sys
runtimes = [runtime for runtime in json.load(sys.stdin).get("runtimes", []) if runtime.get("isAvailable") and runtime.get("platform") == "iOS"]
if runtimes:
    print(runtimes[-1]["identifier"])
')"
    if [[ -n "$runtime_id" ]]; then
        device_type="$(/usr/bin/xcrun simctl list devicetypes -j | /usr/bin/python3 -c '
import json, sys
for device_type in reversed(json.load(sys.stdin).get("devicetypes", [])):
    if device_type.get("name", "").startswith("iPhone"):
        print(device_type["identifier"])
        raise SystemExit
')"
        device_id="$(/usr/bin/xcrun simctl create UpDown-CI "$device_type" "$runtime_id")"
    fi
fi

if [[ -n "$device_id" ]]; then
    destination="platform=iOS Simulator,id=$device_id"
else
    destination="platform=macOS,arch=$(uname -m),variant=Designed for [iPad,iPhone]"
fi

echo "Running UpDown tests on $destination"
"$XCODEBUILD" \
    -project UpDown.xcodeproj \
    -scheme UpDown \
    -destination "$destination" \
    CODE_SIGNING_ALLOWED=NO \
    test
