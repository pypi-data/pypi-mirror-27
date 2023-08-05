"use strict";

var window = self;
var global = self;

self.IDBTransaction = self.IDBTransaction || self.webkitIDBTransaction ||
    self.msIDBTransaction || {READ_WRITE: "readwrite"};
self.IDBKeyRange = self.IDBKeyRange || self.webkitIDBKeyRange ||
    self.msIDBKeyRange;
self.DOMParser = {};
self.sessionStorage = {};
self.localStorage = {};
self.openDatabase = {};
self.DOMError = {};

// ---------------------------------------------------------------------------

//self.importScripts("standard_erp5/rsvp.js", "standard_erp5/jiodev.js");

//console.log("HEllo WORLD");

onmessage = function(e) {
    if(e.data[0] === "get") {
        /* 
           Return a JSON
           for the directory "" (which is root directory for jupyter)
           containing the directories properties and content which is the
           content of the directory (notebooks only in our case).
           The content of the notebooks themself should be null as per spec.
         */
        postMessage({"name": "",
                     "path": "",
                     "last_modified":
                     "2017-09-06T03:33:29.781159Z",
                     "created": "2017-09-06T03:33:29.781159Z",
                     "content": [{
                         "name": "notebook1.ipynb",
                         // TODO: THIS PATH TO NOTEBOOK FILE
                         "path": "foo/bar/notebook1.ipynb",
                         //"path": "/localhost/Test-Notebook.ipynb",
                         "type": "notebook",
                         "format": "json",
                         "writable": true,
                         "last_modified": "2013-10-02T11:29:27.616675+00:00",
                         "created": "2013-10-01T12:21:20.123456+00:00",
                         "content": null
                     }]
                    });
        
    }
    if(e.data[0] === "create") {
        /*
          Properly: Get all notebook titles and check for the first available
          Untitled#.ipynb
          For now: Use timestamp as title maybe?
        */
        postMessage({
            "name": "Untitled0.ipynb",
            "path": "Untitled0.ipynb",
            "type": "notebook",
            "format": "json", // opt || null by default
            "writable": true, // opt
            "last_modified": "2017-09-07T08:01:40.871584Z",
            "created": "2017-09-07T08:01:40.871584Z",
            "content": null, // opt
        });
    }
};
