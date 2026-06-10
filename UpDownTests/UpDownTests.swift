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
