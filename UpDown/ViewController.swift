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
    var playing = false as Bool!

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


    func begin(){

        // If there is a motion manager available
        if manager.deviceMotionAvailable {

            // Start the device motion updates

            manager.startDeviceMotionUpdatesToQueue(NSOperationQueue.mainQueue()) {
                (motion, error) in

                // Calculate the magnitude of th\e change
                let magnitude = sqrt(pow(motion!.attitude.roll, 2) + pow(motion!.attitude.yaw, 2) + pow(motion!.attitude.pitch, 2))

                // Determine whether the player is playing via boolean
                let playing = self.playing as Bool!

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

    func play(){

        // Play the game
        self.spinner.stopAnimating()
        self.spinner.hidden = true

        // Put a random string into the game
        let url = URL()
        url.get("https://garethpaul-app.appspot.com/api/updown", completed: { (succeeded: Bool, data: NSString) -> () in
            // success
            dispatch_async(dispatch_get_main_queue()) {
                self.gameText.text = data as String
                self.gameText.hidden = false;
            }
            // start playing
            self.playing = true
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

