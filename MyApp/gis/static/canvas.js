//var hr = 13;
//var min = 50;
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
var radius = canvas.height / 2;
ctx.save();
ctx.translate(radius, radius); // shift the origin
radius = radius * 0.70
//get context for animation
var animCtx = canvas.getContext("2d");
//15 45 60 120
window.minuteSLA = 15;
window.toBeClearedTimer = 0;

function drawClock() {
  ctx.clearRect(-radius-5, -radius-5, canvas.width, canvas.height);
  var ret = drawFace(ctx, radius);
  //if(ret==1)
    //{animation(animCtx, radius);}
}

function drawFace(ctx, radius) {
  var grad;
  ctx.beginPath();
  ctx.moveTo(0,0);
  var now = new Date();
  var hour = now.getHours();
  var minute = now.getMinutes();
  var second = now.getSeconds();

  var timeMinutes = (hour - hr)*60*60 + (minute - min)*60+second;
  ea = -Math.PI/2 + 2*Math.PI*(timeMinutes)/(window.minuteSLA*60); // since timeMinutes is in seconds and window.minuteSLA is in minute
  if(window.toBeClearedAfterDrawing == 2){
    clearInterval(window.refreshIntervalId);
    ctx.clearRect(-radius-5, -radius-5, canvas.width, canvas.height);
  }
  else if(timeMinutes/60 >= window.minuteSLA ){//| timeMinutes < 0){
    clearInterval(window.refreshIntervalId);
    ctx.clearRect(-radius-5, -radius-5, canvas.width, canvas.height);
        //even if the timer is up, show time elapsed
    ctx.globalCompositeOperation = 'destination-over';
    ctx.font                     = radius/3+"px Arial";
    ctx.textAlign                = 'center';
    ctx.textBaseline             = 'middle';
    ctx.fillStyle                = "black";
    ctx.fillText(Math.floor(timeMinutes/60)+" min",0,0);
    //same as before , below
    ctx.arc(0, 0, radius, -Math.PI/2, 3*Math.PI/2);
    ctx.fillStyle = window.color;
    ctx.fill();
    return 0;
  }
  //below for drawing number in middle
  ctx.globalCompositeOperation = 'destination-over';
  ctx.font                     = radius/3+"px Arial";
  ctx.textAlign                = 'center';
  ctx.textBaseline             = 'middle';
  ctx.fillStyle                = "black";
  ctx.fillText(Math.floor(timeMinutes/60)+" min",0,0);

  //for filling color
  ctx.arc(0, 0, radius, -Math.PI/2, ea);
  ctx.fillStyle = JSON.parse(window.color);
  //console.log(window.color+"\t"+window.minuteSLA);
  ctx.fill();

  //return 1;
}
function animation(animCtx, radius){
	//below for creating arc
var now = new Date();
var millisecond = now.getMilliseconds();
  var unite = millisecond/16.65;
  var diviseur = 30;
  animCtx.strokeStyle = 'green';
  animCtx.beginPath();
  animCtx.lineWidth = 5;
  animCtx.arc(0, 0, radius, (Math.PI)*(unite/diviseur), (Math.PI)*(unite/diviseur)+(Math.PI*1.5), true);
  animCtx.stroke();
}


/*function drawNumbers(ctx, radius) {
  var ang;
  var num;
  ctx.font = radius*0.20 + "px arial";
  ctx.textBaseline="middle";
  ctx.textAlign="center";
  ctx.fillStyle = "black";
  for(num = 1; num < 16; num++){
    ang = num * 2*Math.PI / 15;
    ctx.rotate(ang);
    ctx.translate(0, -radius*1.15);
    ctx.rotate(-ang);
    ctx.fillText(num.toString(), 0, 0);
    ctx.rotate(ang);
    ctx.translate(0, radius*1.15);
    ctx.rotate(-ang);
  }
}
*/