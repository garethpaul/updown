//
//  ViewController.swift
//

import UIKit
import CoreMotion
import MoPub

class ViewController: UIViewController, MPInterstitialAdControllerDelegate {

    // Setup the Motion Manager
    var manager = CMMotionManager()

    // Playing bool to be set when someone is playing the game
    var playing = false
    var fetchingPrompt = false
    var promptRequestID = 0

    // TODO: Replace this test id with your personal ad unit id
    var interstitial: MPInterstitialAdController = MPInterstitialAdController(forAdUnitId: "YOUR_AD_UNIT_ID")

    // IBOutlet
    @IBOutlet var gameText: UILabel!
    @IBOutlet var spinner: UIActivityIndicatorView!

    override func viewDidLoad() {
        super.viewDidLoad()

        // Show the interstitial ad unit
        self.interstitial.delegate = self
        self.interstitial.loadAd()

        // Begin the app
        begin()
    }

    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        begin()
    }

    override func viewWillDisappear(animated: Bool) {
        super.viewWillDisappear(animated)
        manager.stopDeviceMotionUpdates()
        self.promptRequestID += 1
        fetchingPrompt = false
        playing = false
    }

    func begin(){
        if manager.deviceMotionActive {
            return
        }

        // If there is a motion manager available
        if manager.deviceMotionAvailable {

            // Start the device motion updates

            manager.startDeviceMotionUpdatesToQueue(NSOperationQueue.mainQueue()) {
                (motion, error) in

                if let currentMotion = motion {

                    // Calculate the magnitude of the change
                    let magnitude = sqrt(pow(currentMotion.attitude.roll, 2) + pow(currentMotion.attitude.yaw, 2) + pow(currentMotion.attitude.pitch, 2))

                    // Determine whether the player is playing via boolean
                    let playing = self.playing

                    // If the magnitude of change is above 1 or 2.6 (tried via testing changes)
                    if magnitude >= 1 && magnitude <= 2.6 {

                        // If not playing (begin playing)
                        if (playing == false) {
                            self.play()
                        }

                    } else {

                        // If the "magnitude" - shows that the phone is down and user is playing stop playing
                        if playing == true {
                            self.stop()
                        }
                    }
                }
            }
        }
    }

    func play(){
        if self.fetchingPrompt {
            return
        }
        self.fetchingPrompt = true
        self.promptRequestID += 1
        let requestID = self.promptRequestID

        // Play the game
        self.spinner.stopAnimating()
        self.spinner.hidden = true

        // Put a random string into the game
        let url = URL()
        url.get("https://garethpaul-app.appspot.com/api/updown", completed: { (succeeded: Bool, data: NSString) -> () in
            dispatch_async(dispatch_get_main_queue()) {
                if requestID != self.promptRequestID {
                    return
                }
                self.fetchingPrompt = false
                self.spinner.stopAnimating()
                self.spinner.hidden = true
                if succeeded && data.length > 0 {
                    self.gameText.text = data as String
                    self.playing = true
                } else {
                    self.gameText.text = "Prompt unavailable"
                    self.playing = false
                }
                self.gameText.hidden = false;
            }
        })
    }


    func stop(){
        self.playing = false
        self.spinner.hidden = false
        self.gameText.hidden = true
        self.spinner.startAnimating()
    }

    // Present the ad only after it has loaded and is ready
    func interstitialDidLoadAd(interstitial: MPInterstitialAdController) {
        if (interstitial.ready) {
            interstitial.showFromViewController(self)
        }
    }



}
