.PHONY: build check lint test verify

PYTHON ?= python3

lint:
	$(PYTHON) scripts/check_ios_contracts.py

test: lint

build:
	@if command -v xcodebuild >/dev/null 2>&1; then \
		xcodebuild -project UpDown.xcodeproj -target UpDown -sdk iphonesimulator -configuration Debug CODE_SIGNING_ALLOWED=NO build; \
	else \
		echo "iOS build skipped: xcodebuild is not available on this host."; \
	fi

verify: lint test build

check: verify
