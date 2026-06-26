# Motion Unavailable State Implementation Plan

Status: Completed

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Replace the impossible idle instruction with an explicit unavailable state when CoreMotion cannot provide device motion.

**Architecture:** Extend the pure `GameDisplayState` with one unavailable transition, then use it only when `CMMotionManager.isDeviceMotionAvailable` is false. Preserve the existing active-session guard, lifecycle resets, prompt failure state, and motion-error behavior.

**Tech Stack:** Swift 5, UIKit, CoreMotion, XCTest, Python static contracts, Xcode hosted tests.

---

### Task 1: Add RED coverage

**Files:**
- Modify: `UpDownTests/UpDownTests.swift`
- Modify: `scripts/check_ios_contracts.py`

Add a state test requiring `showMotionUnavailable()` to set non-playing text to `Motion unavailable`. Add a source contract requiring availability to be checked before the active-session guard and requiring the unavailable state to render before returning.

Run `python3 scripts/check_ios_contracts.py`; expect failure because the source currently silently returns when motion is unavailable.

### Task 2: Implement the minimal state transition

**Files:**
- Modify: `UpDown/ViewController.swift`

Add `motionUnavailableText`, implement `showMotionUnavailable()`, split the combined `beginMotionUpdates` guard, and render the unavailable state when device motion is absent. Leave active motion sessions untouched.

### Task 3: Reconcile public documentation

**Files:**
- Modify: `README.md`
- Modify: `VISION.md`
- Modify: `CHANGES.md`
- Modify: `AGENTS.md`

Document the explicit failure state, validation evidence, simulator/device limitations, and next physical verification step.

### Task 4: Verify completely

Run root and external-directory `make check`, `git diff --check`, and hosted XCTest. Merge only the exact green reviewed head.

## Result

`GameDisplayState` now exposes a dedicated non-playing motion-unavailable
transition. `beginMotionUpdates()` renders that state only when device motion
is unavailable, while an already-active subscription still returns unchanged.
The portable contract recorded the pre-fix failure; final local and hosted
verification evidence is recorded in `CHANGES.md` before merge.
