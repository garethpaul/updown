import CoreMotion
import UIKit

struct MotionHysteresisGate {
    private let startRange: ClosedRange<Double>
    private let continuationRange: ClosedRange<Double>

    init(
        startRange: ClosedRange<Double> = 1.0...2.6,
        continuationRange: ClosedRange<Double> = 0.9...2.7
    ) {
        self.startRange = startRange
        self.continuationRange = continuationRange
    }

    func shouldPlay(magnitude: Double, currentlyPlaying: Bool) -> Bool {
        let activeRange = currentlyPlaying ? continuationRange : startRange
        return activeRange.contains(magnitude)
    }

    func shouldResetForUnavailableSample(currentlyPlaying: Bool) -> Bool {
        currentlyPlaying
    }
}

struct MotionUpdateSession {
    private(set) var generation = 0

    mutating func begin() -> Int {
        generation += 1
        return generation
    }

    mutating func invalidate() {
        generation += 1
    }

    func accepts(_ capturedGeneration: Int) -> Bool {
        capturedGeneration == generation
    }
}

struct GameDisplayState {
    static let idleText = "Tilt the phone up for a word"
    static let unavailableText = "No prompts available"

    private(set) var text = GameDisplayState.idleText
    private(set) var playing = false

    mutating func show(prompt: String) {
        text = prompt
        playing = true
    }

    mutating func showUnavailable() {
        text = Self.unavailableText
        playing = false
    }

    mutating func stop() {
        text = Self.idleText
        playing = false
    }
}

final class ViewController: UIViewController {
    private let motionManager = CMMotionManager()
    private let motionGate = MotionHysteresisGate()
    private let promptProvider = PromptProvider()
    private var motionUpdateSession = MotionUpdateSession()
    private var displayState = GameDisplayState()

    @IBOutlet private weak var gameText: UILabel!

    override func viewDidLoad() {
        super.viewDidLoad()
        renderDisplayState()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        beginMotionUpdates()
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        motionUpdateSession.invalidate()
        motionManager.stopDeviceMotionUpdates()
        stop()
    }

    private func beginMotionUpdates() {
        guard motionManager.isDeviceMotionAvailable,
              !motionManager.isDeviceMotionActive else {
            return
        }

        let motionGeneration = motionUpdateSession.begin()
        motionManager.startDeviceMotionUpdates(to: .main) { [weak self] motion, error in
            guard let self else {
                return
            }
            guard motionUpdateSession.accepts(motionGeneration) else {
                return
            }
            guard error == nil, let attitude = motion?.attitude else {
                if motionGate.shouldResetForUnavailableSample(currentlyPlaying: displayState.playing) {
                    stop()
                }
                return
            }

            let magnitude = sqrt(
                attitude.roll * attitude.roll
                    + attitude.yaw * attitude.yaw
                    + attitude.pitch * attitude.pitch
            )

            let shouldPlay = motionGate.shouldPlay(
                magnitude: magnitude,
                currentlyPlaying: displayState.playing
            )

            if shouldPlay {
                if !displayState.playing {
                    play()
                }
            } else if displayState.playing {
                stop()
            }
        }
    }

    private func play() {
        guard let prompt = promptProvider.nextPrompt() else {
            displayState.showUnavailable()
            renderDisplayState()
            return
        }

        displayState.show(prompt: prompt)
        renderDisplayState()
    }

    private func stop() {
        displayState.stop()
        renderDisplayState()
    }

    private func renderDisplayState() {
        gameText.text = displayState.text
    }
}
