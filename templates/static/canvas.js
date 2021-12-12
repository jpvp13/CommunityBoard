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

