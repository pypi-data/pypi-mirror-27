/*global window, rJS, RSVP, Handlebars, URI */
/*jslint nomen: true, indent: 2, maxerr: 3 */
(function (window, rJS, RSVP) {
  "use strict";

  var gadget_klass = rJS(window);
  // SNIP
  
  function callJioGadget(gadget, method, param_list) {
    var called = false;
    return new RSVP.Queue()
      .push(function () {
        return gadget.getDeclaredGadget("jio_gadget");
      })
      .push(function (jio_gadget) {
        return jio_gadget[method].apply(jio_gadget, param_list);
      });
  }

  gadget_klass
    .ready(function() {
      console.log("Hello ready!");
      
      var gadget = this,
        setting_gadget,
        setting;
        
      this.props = {
      };
      // Configure setting storage
      return gadget.getDeclaredGadget("setting_gadget")
        .push(function (result) {
          setting_gadget = result;
          return setting_gadget.createJio({
            type: "indexeddb",
            database: "setting"
          });
        })
        .push(function () {

          return setting_gadget.get("setting")
            .push(undefined, function (error) {
              if (error.status_code === 404) {
                return {};
              }
              throw error;
            });
        })
        .push(function (result) {
          setting = result;
          // Extract configuration parameters stored in HTML
          // XXX Will work only if top gadget...
          var gadget_cont = document.querySelector(".gadget-jupyter-page-container");
          var element_list =
            gadget_cont
            .querySelectorAll("script[data-renderjs-configuration]"),
            len = element_list.length,
            key,
            value,
            i;
          for (i = 0; i < len; i += 1) {
            key = element_list[i].getAttribute('data-renderjs-configuration');
            value = element_list[i].textContent;
            gadget.props[key] = value;
            setting[key] = value;
          }

          // Calculate erp5 hateoas url
          //setting.hateoas_url = (new URI(gadget.props.hateoas_url))
          //                    .absoluteTo(location.href)
          //                    .toString();
          
          // TODO HARDCODED - BAD
          setting.hateoas_url = "";

          if (setting.hasOwnProperty('service_worker_url') &&
              (setting.service_worker_url !== '')) {
            if (navigator.serviceWorker !== undefined) {
              // Check if a ServiceWorker already controls the site on load
              if (!navigator.serviceWorker.controller) {
                // Register the ServiceWorker
                navigator.serviceWorker.register(setting.service_worker_url);
              }
            }
          }

          return setting_gadget.put("setting", setting);
        })
        .push(function () {
          // Configure jIO storage
          return gadget.getDeclaredGadget("jio_gadget");
        })

        .push(function (jio_gadget) {
          return jio_gadget.createJio(setting.jio_storage_description);
        })
        .push(function() {
          return gadget.getDeclaredGadget("jiocontents_gadget");
        })
        .push(function(jiocontents_gadget) {
          jiocontents_gadget.render();
        });
    })
    .allowPublicAcquisition("getSetting", function (argument_list) {
      var gadget = this,
        key = argument_list[0],
        default_value = argument_list[1];
      return gadget.getDeclaredGadget("setting_gadget")
        .push(function (jio_gadget) {
          return jio_gadget.get("setting");
        })
        .push(function (doc) {
          return doc[key] || default_value;
        }, function (error) {
          if (error.status_code === 404) {
            return default_value;
          }
          throw error;
        });
    })
    .allowPublicAcquisition("setSetting", function (argument_list) {
      var jio_gadget,
        gadget = this,
        key = argument_list[0],
        value = argument_list[1];
      return gadget.getDeclaredGadget("setting_gadget")
        .push(function (result) {
          jio_gadget = result;
          return jio_gadget.get("setting");
        })
        .push(undefined, function (error) {
          if (error.status_code === 404) {
            return {};
          }
          throw error;
        })
        .push(function (doc) {
          doc[key] = value;
          return jio_gadget.put('setting', doc);
        });
    })
    .allowPublicAcquisition("jio_allDocs", function (param_list) {
      return callJioGadget(this, "allDocs", param_list);
    })
    .allowPublicAcquisition("jio_remove", function (param_list) {
      return callJioGadget(this, "remove", param_list);
    })
    .allowPublicAcquisition("jio_post", function (param_list) {
      return callJioGadget(this, "post", param_list);
    })
    .allowPublicAcquisition("jio_put", function (param_list) {
      return callJioGadget(this, "put", param_list);
    })
    .allowPublicAcquisition("jio_get", function (param_list) {
      return callJioGadget(this, "get", param_list);
    })
    .allowPublicAcquisition("jio_allAttachments", function (param_list) {
      return callJioGadget(this, "allAttachments", param_list);
    })
    .allowPublicAcquisition("jio_getAttachment", function (param_list) {
      return callJioGadget(this, "getAttachment", param_list);
    })
    .allowPublicAcquisition("jio_putAttachment", function (param_list) {
      return callJioGadget(this, "putAttachment", param_list);
    })
    .allowPublicAcquisition("jio_removeAttachment", function (param_list) {
      return callJioGadget(this, "removeAttachment", param_list);
    })
    .allowPublicAcquisition("jio_repair", function (param_list) {
      return callJioGadget(this, "repair", param_list);
    });

}(window, rJS, RSVP));