// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/*
 * For reference see https://github.com/ipython/ipython/wiki/IPEP-27%3A-Contents-Service
 */

define(function(require) {
    "use strict";
    
    var $ = require('jquery');
    var utils = require('base/js/utils');
    

    var baseUrl = "/nbextensions/jiocontents";
    
    var gadget_main_div = document.createElement("div");
    gadget_main_div.setAttribute("data-gadget-url", baseUrl + "/gadget_jupyter_page.html");
    gadget_main_div.setAttribute("class", "gadget-jupyter-page-container");
    document.body.append(gadget_main_div);
    
    document.jiocontentsReady = false;

    var s1 = document.createElement("script"); s1.type = "text/javascript";
      s1.onload = function() {
        console.log("loaded rsvp");
        var s2 = document.createElement("script"); s2.type = "text/javascript";
        s2.onload = function() {
          console.log("loaded renderjs");
          rJS.manualBootstrap();
        };
        s2.src = baseUrl + "/renderjs.js";
        document.head.append(s2);
      };
    s1.src = baseUrl + "/rsvp.js";
    document.head.append(s1);
    
    /*
     .then on this method to be sure the rjs-setup was completed and
     .onEvent are available to receive events
    */
    function waitForReadyPromise() {
      if(document.jiocontentsReady) {
        return Promise.resolve(); // rjs-setup is already complete
      }
      return new Promise(function(resolve, reject) {
        var timerId = window.setInterval(function() {
          if(document.jiocontentsReady) {
            resolve();
            clearInterval(timerId);
          }
        }, 100); // Check every 100ms to see if rjs-setup is complete and eventlistener available
        window.setTimeout(function() {
          if(!document.jiocontentsReady) {
            reject();
          }
        }, 3000) // Reject after 3sec
      });
    }
    
    function getJiocontentsDiv() {
      return document.querySelector(".jiocontents_gadget");
    }
    
    var Contents = function(options) {
        this.base_url = options.base_url;
    };

    /** Error type */
    Contents.DIRECTORY_NOT_EMPTY_ERROR = 'DirectoryNotEmptyError';

    Contents.DirectoryNotEmptyError = function() {
        this.message = 'A directory must be empty before being deleted.';
    };
    
    Contents.DirectoryNotEmptyError.prototype =
        Object.create(Error.prototype);
    Contents.DirectoryNotEmptyError.prototype.name =
        Contents.DIRECTORY_NOT_EMPTY_ERROR;

    Contents.prototype.api_url = function() {
        var url_parts = [
            this.base_url, 'api/contents',
            utils.url_join_encode.apply(null, arguments),
        ];
        return utils.url_path_join.apply(null, url_parts);
    };

    Contents.prototype.create_basic_error_handler = function(callback) {
        if (!callback) {
            return utils.log_ajax_error;
        }
        return function(xhr, status, error) {
            callback(utils.wrap_ajax_error(xhr, status, error));
        };
    };

    /**
     * File Functions (including notebook operations)
     */

    Contents.prototype.get = function (path, options) {
      return waitForReadyPromise()
        .then(function() {
          return new Promise(function(resolve, reject) {
            var ev = new CustomEvent("get_event", {
              detail: {
                path: path,
                resolve: resolve,
                reject: reject
              }
            });
            getJiocontentsDiv().dispatchEvent(ev);
          });
        });
    };

    Contents.prototype.new_untitled = function(path, options) {
      if(options.type !== "notebook") {
        console.log("Creation of non-notebooks is not supported!");
        return Promise.reject("Creation of non-notebooks is not supported!");
      }
      return waitForReadyPromise()
        .then(function() {
          return new Promise(function(resolve, reject) {
            var ev = new CustomEvent("create_event", {
              detail: {
                path: path,
                resolve: resolve,
                reject: reject,
              }
            });
            getJiocontentsDiv().dispatchEvent(ev);
          });
        });
    };

    Contents.prototype.delete = function(path) {
      return Promise.reject("Delete is currently not supported!");
    };

    Contents.prototype.rename = function(path, new_path) {
      return waitForReadyPromise()
        .then(function() {
          return new Promise(function(resolve, reject) {
            var ev = new CustomEvent("rename_event", {
              detail: {
                path: path, 
                // get rid of path-prefix web_page_module. Not used in titles!
                new_title: new_path.split("/")[1],
                resolve: resolve,
                reject: reject
              }
            });
            getJiocontentsDiv().dispatchEvent(ev);
          });
        });
    };

    Contents.prototype.save = function(path, model) {
      return waitForReadyPromise()
        .then(function() {
          return new Promise(function(resolve, reject) {
            var ev = new CustomEvent("save_event", {
              detail: {
                path: path,
                model: JSON.stringify(model.content),
                resolve: resolve,
                reject: reject
              }
            });
            getJiocontentsDiv().dispatchEvent(ev);
          });
        });
    };

    Contents.prototype.copy = function(from_file, to_dir) {
      return Promise.reject("Copy is currently not supported!");
    };

    /**
     * Checkpointing Functions
     */

    Contents.prototype.create_checkpoint = function(path) {
      return Promise.resolve({
        id: "dummy-id",
        last_modified: "2013-10-18T23:54:40+00:00"//dummy
      });
    };

    Contents.prototype.list_checkpoints = function(path) {
      return Promise.resolve([]);
    };

    Contents.prototype.restore_checkpoint = function(path, checkpoint_id) {
      return Promise.resolve();
    };

    Contents.prototype.delete_checkpoint = function(path, checkpoint_id) {
      return Promise.resolve();
    };

    /**
     * File management functions
     */

    Contents.prototype.list_contents = function(path) {
      return this.get(path, {type: 'directory'});
    };
    
    return {'Contents': Contents};
});