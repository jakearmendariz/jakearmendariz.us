var center;
var colors = [];

setup = function () {
    createCanvas(window.innerWidth, window.innerHeight * 2 / 3);
    background(30, 30, 30);
    newBall();
    newBall();
    frameRate(60);
    center = createVector(width / 2, height / 2);

}
var blueballs = [];
var radius = window.innerWidth * 2;

draw = function () {
    background(30);

    newBall();
    newBall();

    //drawballs();
    slideBalls();
    console.log("go");

}

var newBall = function () {
    if (blueballs.length > 6000) {
        blueballs = subset(blueballs, 1000, 6000);
    }
    var deg = random(0, 360);
    var x = p5.Vector.fromAngle(radians(deg), radius);
    x.x += width / 2;
    x.y += height / 2;
    blueballs.push(x);
    colors.push(color(random(160, 180), random(230, 255), random(230, 255)));
}


var drawballs = function () {
    noStroke();
    fill(255);
    //ellipse(center.x, center.y, 15, 15)
    for (let i = 0; i < blueballs.length; i++) {
        fill(colors[i]);
        fill(255);
        let r = dist(center.x, center.y, blueballs[i].x, blueballs[i].y) / 150;
        ellipse(blueballs[i].x, blueballs[i].y, r, r)
    }
}

var slideBalls = function () {
    for (let i = 0; i < blueballs.length; i++) {
        var xM = blueballs[i].x - center.x;
        var yM = blueballs[i].y - center.y;
        var a = dist(center.x, 0, blueballs[i].x, 0) / 280;
        var b = dist(center.y, 0, blueballs[i].y, 0) / 280;
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