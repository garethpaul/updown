import Foundation

final class PromptProvider {
    typealias IndexProvider = (Int) -> Int

    private struct Prompt {
        let displayValue: String
        let comparisonKey: String
    }

    private let prompts: [Prompt]
    private let indexProvider: IndexProvider
    private var previousPromptKey: String?

    init(
        prompts: [String] = PromptProvider.defaultPrompts,
        indexProvider: @escaping IndexProvider = { Int.random(in: 0..<$0) }
    ) {
        self.prompts = prompts.compactMap { displayValue in
            let comparisonKey = PromptProvider.comparisonKey(for: displayValue)
            guard !comparisonKey.isEmpty else {
                return nil
            }
            return Prompt(displayValue: displayValue, comparisonKey: comparisonKey)
        }
        self.indexProvider = indexProvider
    }

    func nextPrompt() -> String? {
        guard !prompts.isEmpty else {
            return nil
        }

        let alternatives = previousPromptKey.map { previousKey in
            prompts.filter { $0.comparisonKey != previousKey }
        } ?? prompts
        let candidates = alternatives.isEmpty ? prompts : alternatives
        let candidate = indexProvider(candidates.count)
        guard candidates.indices.contains(candidate) else {
            return nil
        }

        let prompt = candidates[candidate]
        previousPromptKey = prompt.comparisonKey
        return prompt.displayValue
    }

    private static func comparisonKey(for prompt: String) -> String {
        prompt
            .components(separatedBy: .whitespacesAndNewlines)
            .filter { !$0.isEmpty }
            .joined(separator: " ")
            .precomposedStringWithCanonicalMapping
            .folding(
                options: [.caseInsensitive, .widthInsensitive],
                locale: Locale(identifier: "en_US_POSIX")
            )
    }

    static let defaultPrompts = [
        "Airplane",
        "Birthday cake",
        "Campfire",
        "Dinosaur",
        "Elevator",
        "Firefighter",
        "Guitar",
        "Hot air balloon",
        "Ice cream",
        "Jellyfish",
        "Kangaroo",
        "Lighthouse",
        "Moon landing",
        "Newspaper",
        "Octopus",
        "Pirate",
        "Roller coaster",
        "Snowman",
        "Telescope",
        "Volcano"
    ]
}
