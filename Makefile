.DEFAULT_GOAL := check
.PHONY: __repository-make-authority build check lint root-test static test verify
.SECONDEXPANSION:

PYTHON ?= python3
override PYTHON := $(value PYTHON)
export PYTHON
XCODEBUILD ?= /usr/bin/xcodebuild
override XCODEBUILD := $(value XCODEBUILD)
export XCODEBUILD
override REPOSITORY_MAKE_DOLLAR := $$
override REPOSITORY_MAKE_OPEN := (
ifneq ($(findstring $(REPOSITORY_MAKE_DOLLAR)$(REPOSITORY_MAKE_OPEN),$(value PYTHON)),)
$(error PYTHON must be a literal executable path, not Make syntax)
endif
ifneq ($(findstring $(REPOSITORY_MAKE_DOLLAR)$(REPOSITORY_MAKE_OPEN),$(value XCODEBUILD)),)
$(error XCODEBUILD must be a literal executable path, not Make syntax)
endif
override SHELL := /bin/sh
override .SHELLFLAGS := -c
build check lint root-test static test verify __repository-make-authority: override SHELL := /bin/sh
build check lint root-test static test verify __repository-make-authority: override .SHELLFLAGS := -c

ifneq ($(filter command line,$(origin MAKEFLAGS)),)
$(error MAKEFLAGS must not be overridden for repository verification)
endif
override REPOSITORY_MAKE_FIRST_FLAGS := $(firstword $(MAKEFLAGS))
ifneq ($(filter -%,$(REPOSITORY_MAKE_FIRST_FLAGS)),)
override REPOSITORY_MAKE_FIRST_FLAGS :=
endif
override REPOSITORY_MAKE_SHORT_FLAGS := $(REPOSITORY_MAKE_FIRST_FLAGS) $(filter-out --%,$(filter -%,$(MAKEFLAGS)))
ifneq ($(findstring n,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring t,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring q,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(findstring i,$(REPOSITORY_MAKE_SHORT_FLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(filter --just-print --dry-run --recon --touch --question --ignore-errors,$(MAKEFLAGS)),)
$(error non-executing or error-ignoring MAKEFLAGS are not supported for repository verification)
endif
ifneq ($(strip $(MAKEFILES)),)
$(error MAKEFILES must be empty; repository verification requires this Makefile to be loaded alone)
endif
override MAKEFILES :=
ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override ROOT := $(shell path='$(subst ','"'"',$(value MAKEFILE_LIST))'; path=$$(printf '%s' "$$path" | /usr/bin/sed 's/^ //'); [ -f "$$path" ] || exit 1; directory=$$(/usr/bin/dirname -- "$$path"); CDPATH= cd -- "$$directory" && /bin/pwd -P)
export ROOT
ifeq ($(strip $(ROOT)),)
$(error repository Makefile path could not be resolved)
endif
override REPOSITORY_SHELL_LITERAL = $(subst $$,$$$$,$(subst ','"'"',$1))
override REPOSITORY_ROOT_LITERAL := $(call REPOSITORY_SHELL_LITERAL,$(ROOT))
override REPOSITORY_PYTHON_LITERAL := $(call REPOSITORY_SHELL_LITERAL,$(PYTHON))
override REPOSITORY_XCODEBUILD_LITERAL := $(call REPOSITORY_SHELL_LITERAL,$(XCODEBUILD))

build check lint root-test static test verify:: $$(if $$(filter file,$$(origin MAKEFILE_LIST)),,$$(error MAKEFILE_LIST must not be overridden))
build check lint root-test static test verify:: $$(if $$(shell path=$$$$(/usr/bin/printf '%s' '$$(subst ','"'"',$$(MAKEFILE_LIST))' | /usr/bin/sed 's/^ //') && [ -f "$$$$path" ] && /usr/bin/printf '%s' ok),,$$(error repository Makefile must be loaded alone))
build check lint root-test static test verify:: __repository-make-authority

__repository-make-authority::
	@:

define REPOSITORY_PUBLIC_RECIPES
static::
	'$(REPOSITORY_PYTHON_LITERAL)' '$(REPOSITORY_ROOT_LITERAL)/scripts/check_ios_contracts.py'

lint:: static

test:: static
	@if [ -x '$(REPOSITORY_XCODEBUILD_LITERAL)' ]; then \
		/bin/bash '$(REPOSITORY_ROOT_LITERAL)/scripts/test_ios.sh' '$(REPOSITORY_XCODEBUILD_LITERAL)'; \
	else \
		echo "iOS tests skipped: xcodebuild is not available on this host."; \
	fi

build::
	@if [ -x '$(REPOSITORY_XCODEBUILD_LITERAL)' ]; then \
		cd '$(REPOSITORY_ROOT_LITERAL)' && '$(REPOSITORY_XCODEBUILD_LITERAL)' -project UpDown.xcodeproj -scheme UpDown -destination 'generic/platform=iOS Simulator' CODE_SIGNING_ALLOWED=NO build; \
	else \
		echo "iOS build skipped: xcodebuild is not available on this host."; \
	fi

root-test::
	/bin/sh '$(REPOSITORY_ROOT_LITERAL)/scripts/test-makefile-root.sh'

verify:: root-test static test build

check:: verify
endef
$(eval $(REPOSITORY_PUBLIC_RECIPES))
