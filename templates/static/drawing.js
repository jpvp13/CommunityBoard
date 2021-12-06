const canvas = document.querySelector('.canvas');
const ctx = canvas.getContext('2d');;
const width = canvas.width = window.innerWidth-50;
const height = canvas.height = window.innerHeight-50;

ctx.fillStyle = 'rgb(242, 242, 242)';
ctx.fillRect(0,0,width,height);

function openNav() {
    document.getElementById("drawingToolbar").style.width = "200px";
  }
  
  function closeNav() {
    document.getElementById("drawingToolbar").style.width = "0";
  }
