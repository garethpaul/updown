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

    func testDefaultPromptSourceContainsPlayableValues() {
        XCTAssertGreaterThanOrEqual(PromptProvider.defaultPrompts.count, 20)
        XCTAssertTrue(PromptProvider.defaultPrompts.allSatisfy { !$0.isEmpty })
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
}
