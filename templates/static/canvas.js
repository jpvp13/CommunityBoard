const canvas = document.querySelector('.canvas');
const ctx = canvas.getContext('2d');
const width = canvas.width = window.innerWidth-50;
const height = canvas.height = window.innerHeight-50;

const socketio = io();

ctx.fillStyle = 'rgb(242, 242, 242)';
ctx.fillRect(0,0,width,height);

var slider = document.getElementById("pointSize");
var output = document.querySelector(".output");
var pick = document.getElementById("colorPicker");
var downloadCanvas = document.querySelector(".download");
var clear = document.querySelector(".clear");
var pencil = document.getElementById("pencil");

output.innerHTML = slider.value;

// default color and pencil size
var color = 'red';
var thickness = '10';

socketio.on('connect', ()=> {

  console.log('--connected--');
})

socketio.on('disconnect', ()=> {
  console.log('--disconnected--');
})



socketio.on('client_count', (count) => {
  // console.log(count.client_count)

  
  document.getElementById("userColors").innerHTML =  count.user + " has joined the server";
  // document.getElementById("userColors").innerHTML =  count.user + " has joined the server as user " + count.client_count;

  document.getElementById("totalUsers").innerHTML = count.client_count + " drawers active";
  console.log('There are ' + count.client_count + ' connected clients.');
});


pick.onchange = function(){
  color = this.value;
}
slider.oninput = function() {
  output.innerHTML = this.value;
  thickness = this.value;
}

pencil.onclick = function(){
  color = pick.value;
}

downloadCanvas.onclick = function() {
  var image = canvas.toDataURL("image/png");
  
  var tmpLink = document.createElement('a');
    tmpLink.download = 'image.png';
    tmpLink.href = image;  

    document.body.appendChild( tmpLink );  
    tmpLink.click();  
    document.body.removeChild( tmpLink ); 
};


$(document).ready(function() {
    var flag, dot_flag = false,
      prevX, prevY, currX, currY = 0;
    var $canvas = $('#canvas');
    var ctx = $canvas[0].getContext('2d');

  
    $canvas.on('mousemove mousedown mouseup mouseout', function(e) {
      prevX = currX;
      prevY = currY;
      currX = e.clientX - $canvas.offset().left;
      currY = e.clientY - $canvas.offset().top;
      if (e.type == 'mousedown') {
        flag = true;
      }
      if (e.type == 'mouseup' || e.type == 'mouseout') {
        flag = false;
      }
      if (e.type == 'mousemove') {
        if (flag) {
          ctx.beginPath();
          ctx.moveTo(prevX, prevY);
          ctx.lineTo(currX, currY);
          ctx.strokeStyle = color;
          ctx.lineWidth = thickness;
          ctx.lineJoin = ctx.lineCap = 'round';
          ctx.stroke();
          ctx.closePath();
        }
      }
    }
    
    );

    $('#eraser').on('click',function(e){
      color = 'rgb(242, 242, 242)';
      });

    $('.clear').on('click', function(e) {
        c_width = $canvas.width();
        c_height = $canvas.height();
        ctx.fillStyle = 'rgb(242, 242, 242)';
        ctx.clearRect(0, 0, c_width, c_height);
        ctx.fillRect(0, 0, c_width, c_height);
      });
  });

  // ################################################################################

const wsConnection = new WebSocket('ws:127.0.0.1:5000/login', 'json');
wsConnection.onopen = (e) => {
    console.log(`wsConnection open to 127.0.0.1:5000`, e);
};
wsConnection.onerror = (e) => {
    console.error(`wsConnection error `, e);
};
wsConnection.onmessage = (e) => {
    console.log(JSON.parse(e.data));
};



var localId, peerIds;
var peerConnections = {};
var initiator = false;

wsConnection.onmessage = (e) => {
    let data = JSON.parse(e.data);
    switch (data.type) {
        case 'connection':
            localId = data.id;
            break;
        case 'ids':
            peerIds = data.ids;
            connect();
            break;
        case 'signal':
            signal(data.id, data.data);
            break;
    }
};

function onPeerData(id, data) {
    console.log(`data from ${id}`, data);
}

function connect() {
    // cleanup peer connections not in peer ids
    Object.keys(peerConnections).forEach(id => {
        if (!peerIds.includes(id)) {
            peerConnections[id].destroy();
            delete peerConnections[id];
        }
    });
    if (peerIds.length === 1) {
        initiator = true;
    }
    peerIds.forEach(id => {
        if (id === localId || peerConnections[id]) {
            return;
        }

        let peer = new SimplePeer({
            initiator: initiator
        });
        peer.on('error', console.error);
        peer.on('signal', data => {
            wsConnection.send(JSON.stringify({
                type: 'signal',
                id: localId,
                data
            }));
        });
        peer.on('data', (data) => onPeerData(id, data));
        peerConnections[id] = peer;
    });
}

function signal(id, data) {
    if (peerConnections[id]) {
        peerConnections[id].signal(data);
    }
}



function broadcast(data) {
  Object.values(peerConnections).forEach(peer => {
      peer.send(data);
  });
}

function onPeerData(id, data) {
  draw(JSON.parse(data));
}

function draw(data) {
  context.beginPath();
  context.moveTo(data.lastPoint.x, data.lastPoint.y);
  context.lineTo(data.x, data.y);
  context.strokeStyle = data.color;
  context.lineWidth = Math.pow(data.force || 1, 4) * 2;
  context.lineCap = 'round';
  context.stroke();
}

function move(e) {
  if (e.buttons) {
      if (!lastPoint) {
          lastPoint = { x: e.offsetX, y: e.offsetY };
          return;
      }

      draw({
          lastPoint,
          x: e.offsetX,
          y: e.offsetY,
          force: force,
          color: color || 'green'
      });

      broadcast(JSON.stringify({
          lastPoint,
          x: e.offsetX,
          y: e.offsetY,
          color: color || 'green',
          force: force
      }));

      lastPoint = { x: e.offsetX, y: e.offsetY };
  }
}