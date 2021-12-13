const canvas = document.querySelector('.canvas');
const ctx = canvas.getContext('2d');
const width = canvas.width = window.innerWidth-50;
const height = canvas.height = window.innerHeight-50;

//const socketio = io();
var socketio = io.connect('http://localhost:5000');

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
  document.getElementById("totalUsers").innerHTML = count + " drawers active";
  console.log('There are ' + count + ' connected clients.');
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
          //data = JSON.parse(prevX,prevY,currX,currY,color,thickness);
          draw(prevX,prevY,currX,currY,color,thickness);
          /*ctx.beginPath();
          ctx.moveTo(prevX, prevY);
          ctx.lineTo(currX, currY);
          ctx.strokeStyle = color;
          ctx.lineWidth = thickness;
          ctx.lineJoin = ctx.lineCap = 'round';
          ctx.stroke();
          ctx.closePath();*/


          socketio.emit('Canvas Updated', {
            //who: $(this).attr('id'),
            prevX: prevX / width,
            prevY: prevY / height,
            currX: currX / width,
            currY: currY/ height,
            color: color,
            thickness: thickness
          });

        //receiver
        socketio.on('Canvas Updated',draw);

        //update
        socketio.on('update value',function(msg){
        console.log('Canvas Updated',msg);
        (msg.prevX);
        (msg.prevY);
        (msg.currX);
        (msg.currY);
        (msg.color);
        (msg.thickness);
        console.log("I'm working!");
            });
          }
        }
      });
      /*function receive(data){
        var w = $canvas.width();
        var h = $canvas.height();
        
        //draw(data.prevX * w, data.prevY* h, data.currX * w, data.currY * h, data.color, data.thickness);
        draw(data);
      }*/
        
      function draw(prevX,prevY,currX,currY,color,thickness){
        ctx.beginPath();
          ctx.moveTo(prevX, prevY);
          ctx.lineTo(currX, currY);
          ctx.strokeStyle = color;
          ctx.lineWidth = thickness;
          ctx.lineJoin = ctx.lineCap = 'round';
          ctx.stroke();
          ctx.closePath();
      }
<<<<<<< HEAD

      /*//receiver
      socketio.on('Canvas Updated',draw);

      //update
      socketio.on('update value',function(msg){
        console.log('Canvas Updated',msg);
        $(msg.prevX)(msg.prevY)(msg.currX)(msg.currY)(msg.color)(msg.thickness);
      });*/
=======
    }
    
    );
>>>>>>> ae1581765088e3f1559929d1738fa58ece634f11

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

      /*$('input.sync').on('canvas', function(event) {
        socketio.emit('Canvas Updated', {
          //who: $(this).attr('id'),
          prevX: prevX / width,
          prevY: prevY / height,
          currX: currX / width,
          currY: currY/ height,
          color: color,
          thickness: thickness
        });
        return false;
    });*/

      socketio.on('after connect', function(msg) {
        console.log('After connect', msg);
    });

    /*socketio.on('update', function(msg) {
      console.log('Canvas Updated',msg);
      $(msg.prevX)(msg.prevY)(msg.currX)(msg.currY)(msg.color)(msg.thickness);
  });*/
});


