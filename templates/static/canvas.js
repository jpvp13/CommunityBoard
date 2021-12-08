const canvas = document.querySelector('.canvas');
const ctx = canvas.getContext('2d');
const width = canvas.width = window.innerWidth-50;
const height = canvas.height = window.innerHeight-50;

ctx.fillStyle = 'rgb(242, 242, 242)';
ctx.fillRect(0,0,width,height);

var slider = document.getElementById("pointSize");
var output = document.querySelector(".output");
var pick = document.getElementById("colorPicker");
var downloadCanvas = document.querySelector(".download");

//slider.onchange = size;
output.innerHTML = slider.value;

pick.onchange = function(){
  color = this.value;
  ctx.globalCompositeOperation = 'source-over';
}
slider.oninput = function() {
  output.innerHTML = this.value;
  thickness = this.value;
}

downloadCanvas.onclick = function() {
  var image = canvas.toDataURL("image/png");
  //this.href = image;
  var tmpLink = document.createElement('a');
    tmpLink.download = 'image.png';
    tmpLink.href = image;  

    document.body.appendChild( tmpLink );  
    tmpLink.click();  
    document.body.removeChild( tmpLink ); 
};

/*function eraser(){
    ctx.globalCompositeOperation = 'destination-out';                 
    ctx.fillStyle = 'rgba(242,242,242,1)';                 
    ctx.strokeStyle = 'rgba(242,242,242,1)';
}*/

$(document).ready(function() {
    var flag, dot_flag = false,
      prevX, prevY, currX, currY = 0;
    var $canvas = $('#canvas');
    var ctx = $canvas[0].getContext('2d');
    //var mode;

    /*$("#pencil").click(function(){
      mode = "pencil";
      ctx.globalCompositeOperation = 'source-over';
  });*/
  
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
          ctx.stroke();
          ctx.closePath();
           /*else if (mode == "eraser"){
            ctx.globalCompositeOperation="destination-out";
            ctx.arc(prevX,prevY,8,0,Math.PI*2,false);
            ctx.fill();
            ctx.fillStyle = 'rgb(242, 242, 242)';
            ctx.fillRect(0, 0, width, height);
          }*/
          //currX = prevX;
          //currY = prevY;
        }
      }
    });

    /*$('#eraser').on('click',function(e){
      ctx.strokeStyle = 'rgb(242, 242, 242)';
      });

    $('#pencil').on('click',function(e){
      ctx.globalCompositeOperation = 'source-over';
    });*/

    $('.clear').on('click', function(e) {
        c_width = $canvas.width();
        c_height = $canvas.height();
        ctx.fillStyle = 'rgb(242, 242, 242)';
        ctx.clearRect(0, 0, c_width, c_height);
        ctx.fillRect(0, 0, c_width, c_height);
      });
    
    /*$('.download').on('click', function(e){
      var image = $canvas.toDataURL("image/jpg");
      download.href = image;
    });*/
  });