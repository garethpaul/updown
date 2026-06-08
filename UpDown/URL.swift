//
//  URL.swift
//

import Foundation

class URL{
    func get(url : String, completed : (succeeded: Bool, data: NSString) -> ()) {
        if let requestURL = NSURL(string: url) {
            var request = NSMutableURLRequest(URL: requestURL)
            var session = NSURLSession.sharedSession()
            request.HTTPMethod = "GET"
            var task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
                if error != nil || data == nil {
                    completed(succeeded: false, data: NSString(string: ""))
                    return
                }

                if let strData = NSString(data: data, encoding: NSUTF8StringEncoding) {
                    completed(succeeded: true, data: strData)
                } else {
                    completed(succeeded: false, data: NSString(string: ""))
                }
            })
            task.resume()
        } else {
            completed(succeeded: false, data: NSString(string: ""))
        }
    }
}
