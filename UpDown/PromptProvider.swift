struct PromptProvider {
    typealias IndexProvider = (Int) -> Int

    private let prompts: [String]
    private let indexProvider: IndexProvider

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

        let index = indexProvider(prompts.count)
        guard prompts.indices.contains(index) else {
            return nil
        }

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
