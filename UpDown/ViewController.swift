import CoreMotion
import UIKit

final class ViewController: UIViewController {
    private let motionManager = CMMotionManager()
    private let promptProvider = PromptProvider()
    private var playing = false

    @IBOutlet private weak var gameText: UILabel!

    override func viewDidLoad() {
        super.viewDidLoad()
        gameText.text = "Tilt the phone up for a word"
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        beginMotionUpdates()
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        motionManager.stopDeviceMotionUpdates()
        playing = false
    }

    private func beginMotionUpdates() {
        guard motionManager.isDeviceMotionAvailable,
              !motionManager.isDeviceMotionActive else {
            return
        }

        motionManager.startDeviceMotionUpdates(to: .main) { [weak self] motion, _ in
            guard let self, let attitude = motion?.attitude else {
                return
            }

            let magnitude = sqrt(
                attitude.roll * attitude.roll
                    + attitude.yaw * attitude.yaw
                    + attitude.pitch * attitude.pitch
            )

            if (1...2.6).contains(magnitude) {
                if !playing {
                    play()
                }
            } else if playing {
                stop()
            }
        }
    }

    private func play() {
        guard let prompt = promptProvider.nextPrompt() else {
            gameText.text = "No prompts available"
            playing = false
            return
        }

        gameText.text = prompt
        playing = true
    }

    private func stop() {
        playing = false
        gameText.text = "Tilt the phone up for a word"
    }
}
