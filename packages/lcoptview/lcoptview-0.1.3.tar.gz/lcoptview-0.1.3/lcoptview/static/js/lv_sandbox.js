// NOTE - the sandbox_functions.js file has to be loaded prior to this one

// This is the function that gets called by the template, set the arguments to cover all of the things that need to be passed

var jsPlumbsetup = function (nodes, links,linklabels, outputlabels) {
	//console.log(nodes)
	//console.log(links)

    // setup some defaults for jsPlumb.
    // instance is the jsPlumb base object
    var instance = jsPlumb.getInstance({
        Endpoint: ["Dot", {radius: 2}],
        Connector:[ "Flowchart", { stub: [0, 0], midpoint: 0.25 } ],//"Straight",
        Container: "#sandbox_container",
    });

    // bind some useful things to the instance for use later
    instance.data = {};
    instance.data.nodes = nodes;
    instance.data.links = links;
    instance.data.linklabels = linklabels;
    instance.data.outputlabels = outputlabels;

    //console.log(instance.data)

    // set up the various types of links

    instance.registerConnectionType("basic", {
      anchor:"Continuous",
      detachable : false,
    });

    instance.registerConnectionType("input", {
      paintStyle: { strokeStyle: "#2e6f9a", lineWidth: 1, outlineColor: "transparent", outlineWidth: 14 },
      overlays: [
          [ "Arrow", {
              location: 1,
              id: "arrow",
              length: 7.5,
              width:7.5,
              foldback: 0.8
          } ],
      ],
    });

    instance.registerConnectionType("biosphere", {
      paintStyle: { strokeStyle: "#484c51", lineWidth: 10, outlineColor: "transparent", outlineWidth: 14 },
      overlays: [
          [ "Arrow", {
              location: 0,
              id: "arrow",
              length: 7.5,
              width:7.5,
              foldback: 0.8,
              direction:-1
          } ],
      ],
    });

    instance.registerConnectionType("intermediate", {
      paintStyle: { strokeStyle: "#aaa", lineWidth: 1, outlineColor: "transparent", outlineWidth: 14 },
      overlays: [
          [ "Arrow", {
              location: 1,
              id: "arrow",
              length: 7.5,
              width:7.5,
              foldback: 0.8
          } ],
          [ "Label", { 
                label: "Connect", 
                id: "label", 
                cssClass: "aLabel",
                }],
      ],
    });

      instance.bind("connection", function (info) {
    //console.log('creating a connection')

    //sort out the label

    data = info.connection.getData()

    //console.log(data)

    var sID = info.sourceId + "_" + info.targetId;

    //console.log("sID = " + sID)

    if(data['connection_type'] == 'intermediate'){
      
      var labelText = linklabels[sID];

      if(typeof labelText == 'undefined'){
          //console.log('doesnt have a label already');
          labelText = 'No Label'
        }

        info.connection.getOverlay("label").setLabel(labelText);

      }
    
    // if it's being generated by the startup process - don't send any info back to the server, otherwise...
    if(!('isExisting' in data)){ 
      // trigger the newConnection Function
      labelText = outputlabels[info.sourceId]
      info.connection.getOverlay("label").setLabel(labelText);
      newConnection(info, instance)

      }

          /*$.post('/sandbox/newConnection/', postData);



        labelText = name + " ("+ amount +" "+ unit +")";
        info.connection.getOverlay("label").setLabel(labelText);
        info.connection.setData({'connection_type':'intermediate', 'connection_amount':amount})
        //console.log( info.connection.getData())*/

      //uncomment when labelShow and lableHide have been rewritten
      //info.connection.getOverlay("label").hide();
      info.connection.bind("mouseover", function(conn){
        labelShow(conn);
      });

      info.connection.bind("mouseout", function(conn){
        labelHide(conn);
      });
  });

    // This function displays the existing nodes in the flowsheet
    // name = name
    // type = transformation/input/output
    // id = uuid
    // initX = integer (initial x value)
    // initY = integer (initial y value)
    
    

    for(i=0;i<nodes.length;i++){
        initNode(newNodeExternal(nodes[i].name, nodes[i].type, nodes[i].id, nodes[i].initX, nodes[i].initY, instance), instance);
    }


    ////console.log(links)
    // This function creates all of the links
    for (i=0;i<links.length;i++){

              var this_source = links[i].sourceID.split(' ').join('_'),
                  this_target = links[i].targetID.split(' ').join('_'),
                  this_type = links[i].type;

              var connection = instance.connect({

                 source: this_source,//links[i]['sourceID'].split(' ').join('_'),
                 target: this_target,//links[i]['targetID'].split(' ').join('_'),
                 type:"basic " + this_type,
                 data:{'connection_type':links[i].type, 'isExisting':true},

               });

              //connection.setType(this_type + " basic")
              //console.log(connection.getType())
              connection.addClass("connection_" + this_type);

               ////console.log(connection);
            }
	
}; // end of jsPlumbSetup