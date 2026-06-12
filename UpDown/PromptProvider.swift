final class PromptProvider {
    typealias IndexProvider = (Int) -> Int

    private let prompts: [String]
    private let indexProvider: IndexProvider
    private var previousIndex: Int?

    init(
        prompts: [String] = PromptProvider.defaultPrompts,
        indexProvider: @escaping IndexProvider = { Int.random(in: 0..<$0) }
    ) {
        self.prompts = prompts
        self.indexProvider = indexProvider
    }

    func nextPrompt() -> String? {
        guard !prompts.isEmpty else {
            return nil
        }

        let candidateCount = previousIndex == nil || prompts.count == 1
            ? prompts.count
            : prompts.count - 1
        let candidate = indexProvider(candidateCount)
        guard (0..<candidateCount).contains(candidate) else {
            return nil
        }

        let index: Int
        if let previousIndex, prompts.count > 1, candidate >= previousIndex {
            index = candidate + 1
        } else {
            index = candidate
        }

        previousIndex = index
        return prompts[index]
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
