//
//  URL.swift
//

import Foundation

class URL{
    func get(url : String, completed : (succeeded: Bool, data: NSString) -> ()) {
        var request = NSMutableURLRequest(URL: NSURL(string: url)!)
        var session = NSURLSession.sharedSession()
        request.HTTPMethod = "GET"
        var err: NSError?
        var task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
            var strData = NSString(data: data!, encoding: NSUTF8StringEncoding)
            completed(succeeded: true, data: strData!)
            var err: NSError?
            do {
                try json = NSJSONSerialization.JSONObjectWithData(data!, options: .MutableLeaves) as? NSDictionary
            } catch let e: NSError {
                print error
            }
        })
        task.resume()
    }
}