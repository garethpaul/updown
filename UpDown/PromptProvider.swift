final class PromptProvider {
    typealias IndexProvider = (Int) -> Int

    private let prompts: [String]
    private let indexProvider: IndexProvider
    private var previousPrompt: String?

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

        let alternatives = previousPrompt.map { previous in
            prompts.filter { $0 != previous }
        } ?? prompts
        let candidates = alternatives.isEmpty ? prompts : alternatives
        let candidate = indexProvider(candidates.count)
        guard candidates.indices.contains(candidate) else {
            return nil
        }

        let prompt = candidates[candidate]
        previousPrompt = prompt
        return prompt
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
