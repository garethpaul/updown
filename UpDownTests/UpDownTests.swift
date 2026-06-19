import XCTest
@testable import UpDown

final class PromptProviderTests: XCTestCase {
    func testReturnsPromptAtInjectedIndex() {
        let provider = PromptProvider(prompts: ["first", "second"]) { count in
            XCTAssertEqual(count, 2)
            return 1
        }

        XCTAssertEqual(provider.nextPrompt(), "second")
    }

    func testEmptyPromptListReturnsNilWithoutSelectingIndex() {
        let provider = PromptProvider(prompts: []) { _ in
            XCTFail("Empty prompt sources must not request an index")
            return 0
        }

        XCTAssertNil(provider.nextPrompt())
    }

    func testWhitespaceOnlyPromptListReturnsNilWithoutSelectingIndex() {
        let provider = PromptProvider(prompts: ["", "   ", "\n\t"]) { _ in
            XCTFail("Blank prompt sources must not request an index")
            return 0
        }

        XCTAssertNil(provider.nextPrompt())
    }

    func testMixedPromptListFiltersBlankValuesWithoutRewritingClues() {
        let provider = PromptProvider(prompts: ["", "   ", "  padded clue  ", "other"]) { count in
            XCTAssertEqual(count, 2)
            return 0
        }

        XCTAssertEqual(provider.nextPrompt(), "  padded clue  ")
    }

    func testInvalidInjectedIndexReturnsNil() {
        let provider = PromptProvider(prompts: ["only"]) { _ in 1 }

        XCTAssertNil(provider.nextPrompt())
    }

    func testConsecutiveSelectionsDoNotRepeatWhenAlternativesExist() {
        var selectionCounts: [Int] = []
        let provider = PromptProvider(prompts: ["first", "second"]) { count in
            selectionCounts.append(count)
            return 0
        }

        XCTAssertEqual(provider.nextPrompt(), "first")
        XCTAssertEqual(provider.nextPrompt(), "second")
        XCTAssertEqual(selectionCounts, [2, 1])
    }

    func testSinglePromptCanBeSelectedRepeatedly() {
        let provider = PromptProvider(prompts: ["only"]) { _ in 0 }

        XCTAssertEqual(provider.nextPrompt(), "only")
        XCTAssertEqual(provider.nextPrompt(), "only")
    }

    func testDuplicatePromptValuesDoNotRepeatWhenAnotherValueExists() {
        var selectionCounts: [Int] = []
        let provider = PromptProvider(prompts: ["same", "same", "other"]) { count in
            selectionCounts.append(count)
            return 0
        }

        XCTAssertEqual(provider.nextPrompt(), "same")
        XCTAssertEqual(provider.nextPrompt(), "other")
        XCTAssertEqual(selectionCounts, [3, 1])
    }

    func testEligibleDuplicateValuesRetainTheirSelectionWeight() {
        var selectionCounts: [Int] = []
        let provider = PromptProvider(prompts: ["first", "weighted", "weighted", "other"]) { count in
            selectionCounts.append(count)
            return selectionCounts.count == 1 ? 0 : 1
        }

        XCTAssertEqual(provider.nextPrompt(), "first")
        XCTAssertEqual(provider.nextPrompt(), "weighted")
        XCTAssertEqual(selectionCounts, [4, 3])
    }

    func testAllIdenticalPromptValuesRemainPlayable() {
        var selectionCounts: [Int] = []
        let provider = PromptProvider(prompts: ["same", "same"]) { count in
            selectionCounts.append(count)
            return 1
        }

        XCTAssertEqual(provider.nextPrompt(), "same")
        XCTAssertEqual(provider.nextPrompt(), "same")
        XCTAssertEqual(selectionCounts, [2, 2])
    }

    func testVisuallyEquivalentPromptValuesDoNotRepeatWhenAlternativeExists() {
        var selectionCounts: [Int] = []
        let provider = PromptProvider(
            prompts: ["Café racer", "  CAFE\u{301}   RACER  ", "Volcano"]
        ) { count in
            selectionCounts.append(count)
            return 0
        }

        XCTAssertEqual(provider.nextPrompt(), "Café racer")
        XCTAssertEqual(provider.nextPrompt(), "Volcano")
        XCTAssertEqual(selectionCounts, [3, 1])
    }

    func testDefaultPromptSourceContainsPlayableValues() {
        XCTAssertGreaterThanOrEqual(PromptProvider.defaultPrompts.count, 20)
        XCTAssertTrue(
            PromptProvider.defaultPrompts.allSatisfy {
                !$0.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
            }
        )
    }
}

final class MotionHysteresisGateTests: XCTestCase {
    func testStartsOnlyInsideStartRange() {
        let gate = MotionHysteresisGate()

        XCTAssertTrue(gate.shouldPlay(magnitude: 1.0, currentlyPlaying: false))
        XCTAssertTrue(gate.shouldPlay(magnitude: 2.6, currentlyPlaying: false))
        XCTAssertFalse(gate.shouldPlay(magnitude: 0.95, currentlyPlaying: false))
        XCTAssertFalse(gate.shouldPlay(magnitude: 2.65, currentlyPlaying: false))
    }

    func testKeepsPlayingAcrossSmallBoundaryFluctuations() {
        let gate = MotionHysteresisGate()

        XCTAssertTrue(gate.shouldPlay(magnitude: 0.95, currentlyPlaying: true))
        XCTAssertTrue(gate.shouldPlay(magnitude: 2.65, currentlyPlaying: true))
    }

    func testStopsOutsideContinuationRange() {
        let gate = MotionHysteresisGate()

        XCTAssertFalse(gate.shouldPlay(magnitude: 0.89, currentlyPlaying: true))
        XCTAssertFalse(gate.shouldPlay(magnitude: 2.71, currentlyPlaying: true))
    }

    func testUnavailableSampleResetsActivePlayState() {
        let gate = MotionHysteresisGate()

        XCTAssertTrue(gate.shouldResetForUnavailableSample(currentlyPlaying: true))
    }

    func testUnavailableSampleLeavesIdleStateUnchanged() {
        let gate = MotionHysteresisGate()

        XCTAssertFalse(gate.shouldResetForUnavailableSample(currentlyPlaying: false))
    }
}

final class MotionUpdateSessionTests: XCTestCase {
    func testCurrentGenerationIsAccepted() {
        var session = MotionUpdateSession()

        let generation = session.begin()

        XCTAssertTrue(session.accepts(generation))
    }

    func testInvalidatedGenerationIsRejected() {
        var session = MotionUpdateSession()
        let generation = session.begin()

        session.invalidate()

        XCTAssertFalse(session.accepts(generation))
    }

    func testReplacementSessionRejectsPreviousGeneration() {
        var session = MotionUpdateSession()
        let previousGeneration = session.begin()

        let currentGeneration = session.begin()

        XCTAssertFalse(session.accepts(previousGeneration))
        XCTAssertTrue(session.accepts(currentGeneration))
    }
}

final class MotionLifecycleStateTests: XCTestCase {
    func testVisibleActiveViewRunsMotionUpdates() {
        var state = MotionLifecycleState()

        state.viewWillAppear(applicationIsActive: true)

        XCTAssertTrue(state.shouldRunMotionUpdates)
    }

    func testBackgroundingVisibleViewSuspendsMotionUpdates() {
        var state = MotionLifecycleState()
        state.viewWillAppear(applicationIsActive: true)

        state.applicationWillResignActive()

        XCTAssertFalse(state.shouldRunMotionUpdates)
    }

    func testForegroundingVisibleViewRestartsMotionUpdates() {
        var state = MotionLifecycleState()
        state.viewWillAppear(applicationIsActive: true)
        state.applicationWillResignActive()

        state.applicationDidBecomeActive()

        XCTAssertTrue(state.shouldRunMotionUpdates)
    }

    func testForegroundingHiddenViewDoesNotStartMotionUpdates() {
        var state = MotionLifecycleState()
        state.viewWillAppear(applicationIsActive: true)
        state.viewWillDisappear()
        state.applicationWillResignActive()

        state.applicationDidBecomeActive()

        XCTAssertFalse(state.shouldRunMotionUpdates)
    }

    func testViewAppearingWhileApplicationIsInactiveDoesNotStartMotionUpdates() {
        var state = MotionLifecycleState()

        state.viewWillAppear(applicationIsActive: false)

        XCTAssertFalse(state.shouldRunMotionUpdates)
    }
}

final class GameDisplayStateTests: XCTestCase {
    func testStoppingActiveGameReturnsVisibleAndLogicalStateToIdle() {
        var state = GameDisplayState()
        state.show(prompt: "Airplane")

        state.stop()

        XCTAssertFalse(state.playing)
        XCTAssertEqual(state.text, GameDisplayState.idleText)
    }

    func testStoppingIdleGameKeepsVisibleAndLogicalStateIdle() {
        var state = GameDisplayState()

        state.stop()

        XCTAssertFalse(state.playing)
        XCTAssertEqual(state.text, GameDisplayState.idleText)
    }
}
