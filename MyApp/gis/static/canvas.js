var hr = 9;
var min = 17;
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
var radius = canvas.height / 2;
ctx.translate(radius, radius); // shift the origin
radius = radius * 0.70
setInterval(drawClock, 1000);

drawNumbers(ctx, radius-radius/40);

function drawClock() {
  drawFace(ctx, radius);
}

function drawFace(ctx, radius) {
  var grad;
  ctx.beginPath();
  ctx.moveTo(0,0);

  var now = new Date();
  var hour = now.getHours();
  var minute = now.getMinutes();
  var second = now.getSeconds();
  ea = -Math.PI/2 + 2*Math.PI*((hour - hr)*60*60 + (minute - min)*60+second)/900;

  ctx.arc(0, 0, radius, -Math.PI/2, ea);
  console.log(ea)
  ctx.fillStyle = "red";
  ctx.fill();

  //following for embedding digital clock inside canvas
  /*string_hour = hour.toString();
  if(minute < 10){
    string_minute = "0" + min.toString();
  }
  else
    string_minute = min.toString();

  if(second < 10){
    string_second = "0" + second.toString();
  }
  else
    string_second = second.toString();
  string_time = string_hour+":"+string_minute+"."+string_second
  ctx.font = "30px Arial";
  //ctx.moveTo(-radius,-radius);
  ctx.fillText(string_time, 0, 0);
  console.log(string_time);
  */
}

function drawNumbers(ctx, radius) {
  var ang;
  var num;
  ctx.font = radius*0.20 + "px arial";
  ctx.textBaseline="middle";
  ctx.textAlign="center";
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