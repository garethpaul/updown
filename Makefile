.PHONY: build check lint static test verify

ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PYTHON ?= python3

static:
	$(PYTHON) "$(ROOT)/scripts/check_ios_contracts.py"

lint: static

test:
	@if command -v xcodebuild >/dev/null 2>&1; then \
		"$(ROOT)/scripts/test_ios.sh"; \
	else \
		echo "iOS tests skipped: xcodebuild is not available on this host."; \
	fi

build:
	@if command -v xcodebuild >/dev/null 2>&1; then \
		cd "$(ROOT)" && xcodebuild -project UpDown.xcodeproj -scheme UpDown -destination 'generic/platform=iOS Simulator' CODE_SIGNING_ALLOWED=NO build; \
	else \
		echo "iOS build skipped: xcodebuild is not available on this host."; \
	fi

verify: static test

check: verify
