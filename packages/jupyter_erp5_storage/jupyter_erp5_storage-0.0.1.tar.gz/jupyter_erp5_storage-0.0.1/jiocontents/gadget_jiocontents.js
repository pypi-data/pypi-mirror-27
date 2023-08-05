/*global window, rJS, jIO, FormData */
/*jslint indent: 2, maxerr: 3 */


(function (window, rJS) {
  "use strict";

  /*
    Next two functions deal with a weird issue of unlin-ed strings, ie. list
    of strings instead a single joined string. Adpoted from 
    https://github.com/jupyter/jupyter-drive/blob/master/jupyterdrive/gdrive/notebook_model.js#L45
    with adjustment to match updates in jupyter's data model.
  */
  function unsplit_lines(multiline_string) {
    if (Array.isArray(multiline_string)) {
      return multiline_string.join('');
    } else {
      return multiline_string;
    }
  }
  
  function transform_notebook(notebook, transform_fn) {
    if (!notebook['cells']) {
      return null;
    }
    notebook['cells'].forEach(function (cell) {
      if (cell['source']) {
        cell['source'] = transform_fn(cell['source']);
      }
      if (cell['outputs']) {
        cell['outputs'].forEach(function (output) {
          if (output['data']) {
            for(var key in output['data']) {
              var t = transform_fn(output['data'][key]);
              output['data'][key] = t;
            }
          }
        });
      }
    });
  }

  function toNotebookModel(id, obj, isRootDir) {
    //console.log(obj.value.text_content);
    var cont = null;
    var title = obj.title;
    if(isRootDir) {
      title += " [ref: " + obj.reference + "]";
    } else {
      cont = JSON.parse(obj.text_content);
      transform_notebook(cont, unsplit_lines);
      cont.metadata = cont.metadata || {};     
    }
    var nbobj = { "name": title,
                  "path": id,
                  "type": "notebook",
                  "format": "json",
                  "writable": true,
                  "mimetype": "application/ipynb",
                  "content": cont,
                  // TODO: Fix date representation. Might cause problems!
                  "created": obj.creation_date,
                  "last_modified": obj.modification_date,
                };
    return nbobj;
  }
  
  /*
   *
   * Event handlers API <-> JIO connection points
   *
   */

  function handleGet(e) {
    if(e.detail.path === "") {
      // We a querying for the root directory. Should return a list of contents which themselves have no
      // content
      this.jio_allDocs({
          query: 'portal_type: "Web JSON"',
          select_list : ["text_content", "title", "reference", "creation_date", "modification_date"],
          sort_on: [["modification_date", "descending"]],
          limit: [0, 20]
        })
        .push(function(result) {
          var nbs = [];
          for(var i = 0; i < result.data.rows.length; i++) {
            nbs.push(toNotebookModel(result.data.rows[i].id, result.data.rows[i].value, true));
          }
          var root_dir = {"name": "",
                          "path": "",
                          "content": nbs };
          e.detail.resolve(root_dir);
        }, function(err) {
          console.log(err);
          e.detail.reject(err);
        });
    } else {
      // Get the notebook file
      this.jio_get(e.detail.path)
      .push(function(result) {
        e.detail.resolve(toNotebookModel(e.detail.path, result, false));
      }, function(err) {
        console.log(err);
        e.detail.reject(err);
      });
    }
  }
  
  function handleSave(e) {
    var gadget = this;
    gadget.jio_get(e.detail.path)
    .push(function(result) {
      gadget.jio_put(e.detail.path, {
        title: result.title,
        reference: result.reference,
        text_content: e.detail.model
      })
      .push(function(result_put) {
        console.log("Notebook saved in ERP5", result_put);
        e.detail.resolve(toNotebookModel(e.detail.path, result, false));
      }, function(err) {
        console.log(err);
        e.detail.reject(err);
      });
    }, function (err) {
      console.log(err);
      e.detail.reject(err);
    });
  }
  
  function handleCreate(e) {
    var now = new Date();
    var jioObj = {
      portal_type: "Web JSON",
      parent_relative_url: "web_page_module",
      title: "untitled_notebook",
      reference: "ut_nb_from_" + now.getTime(),
      text_content: JSON.stringify(createBlankNotebook())
    };
    var gadget = this;
    gadget.jio_post(jioObj)
      .push(function(newId) {
        gadget.jio_get(newId)
          .push(function(result) {
            e.detail.resolve(toNotebookModel(newId, result, false));
          }, function(err) {
            console.log(err);
            e.detail.reject(err);
          });
      }, function(err) {
        console.log(err);
        e.detail.reject(err);
      });
  }
  
  function handleRename(e) {
    var gadget = this;
    gadget.jio_put(e.detail.path, {
      title: e.detail.new_title,
    })
    .push(function(id) {
      gadget.jio_get(id)
        .push(function(result) {
          e.detail.resolve(toNotebookModel(id, result, false));
        }, function(err) {
          console.log(err);
          e.detail.reject(err);
        })
    }, function(err) {
      console.log(err);
      e.detail.reject(err);
    });
  }
  
  /*
   *
   * RJS Stuffs
   *
   */

  rJS(window)
    .ready(function (gadget) {
      console.log("Jio Contents Gadget yes yes.");
      return gadget;
    })
    .declareAcquiredMethod("jio_allDocs", "jio_allDocs")
    .declareAcquiredMethod("jio_get", "jio_get")
    .declareAcquiredMethod("jio_put", "jio_put")
    .declareAcquiredMethod("jio_post", "jio_post")
    .onEvent("get_event", handleGet, false, true)
    .onEvent("save_event", handleSave, false, true)
    .onEvent("create_event", handleCreate, false, true)
    .onEvent("rename_event", handleRename, false, true)
    .declareMethod('render', function () {
      console.log("Rendering!");
      document.jiocontentsReady = true;
      return this;
    });
    
    function createBlankNotebook(kernel_type) {
      return {
        "cells": [
          { "cell_type": "code",
            "execution_count": null,
            "metadata": { "collapsed": true },
            "outputs": [],
            "source": []
          }
        ],
        "metadata": {
          "kernelspec": {
            "display_name": "Python 2",
            "language": "python",
            "name": "python2"
          }
        },
        "nbformat": 4,
        "nbformat_minor": 2
      };
    }

}(window, rJS));

