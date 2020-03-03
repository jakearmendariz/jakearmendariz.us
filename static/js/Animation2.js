var center;
var colors = [];

setup = function () {
    createCanvas(window.innerWidth, window.innerHeight);
    background(0);
    newBall();
    newBall();
    frameRate(500);
    center = createVector(width / 2, height / 2);

}
var blueballs = [];
var radius = window.innerWidth * 2;

draw = function () {
    background(0);
    newBall();
    newBall();
    newBall();
    newBall();

    drawballs();
    slideBalls();
    shiftCenter();
    console.log(blueballs.length)

}

var newBall = function () {
    if (blueballs.length > 3000) {
        blueballs = subset(blueballs, 1000, 3000);
    }
    var deg = random(0, 360);
    var x = p5.Vector.fromAngle(radians(deg), radius);
    blueballs.push(x);
    colors.push(color(random(0, 10), random(20, 245), random(100, 255)));
}


var drawballs = function () {
    noStroke();
    fill(255);
    //ellipse(center.x, center.y, 15, 15)
    for (let i = 0; i < blueballs.length; i++) {
        fill(colors[i]);
        let r = dist(center.x, center.y, blueballs[i].x, blueballs[i].y) / 5;
        ellipse(blueballs[i].x, blueballs[i].y, r, r)
    }
}

var slideBalls = function () {
    for (let i = 0; i < blueballs.length; i++) {
        var xM = blueballs[i].x - center.x;
        var yM = blueballs[i].y - center.y;
        var a = dist(center.x, 0, blueballs[i].x, 0) / 20;
        var b = dist(center.y, 0, blueballs[i].y, 0) / 20;
        if (xM > 0) {
            blueballs[i].x -= a;
        } else {
            blueballs[i].x += a;
        }
        if (yM > 0) {
            blueballs[i].y -= b;
        } else {
            blueballs[i].y += b;
        }
    }
}

var shiftCenter = function () {
    center.x = mouseX;
    center.y = mouseY;
}