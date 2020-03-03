var center;
var bigFlame = true;
var ave;
var rockets = [];
var counter = 0;
setup = function () {
    createCanvas(window.innerWidth, window.innerHeight);
    background(0);
    frameRate(500);
    ave = width + height / 2;

    center = createVector(width / 2, height / 2);
    keyPressed = function () {

        addShot();
        console.log("launch");

    }
}

var radius = window.innerWidth * 2;
draw = function () {
    counter++;
    slideRocket();

}



var drawRocket = function (xPos, yPos) {
    let aHeight = dist(center.x, center.y, xPos, yPos) / 5;
    aWidth = aHeight * (50 / 175);
    noStroke();
    if (counter % 10) {
        bigFlame = !bigFlame;
    }

    fill(220, 220, 220);
    rect(xPos, yPos, aWidth, aHeight);
    fill(200, 200, 200);
    rect(xPos, yPos, aWidth / 6, aHeight);
    fill(180, 180, 180);
    rect(xPos + aWidth / 3, yPos, (aWidth * 2) / 3, aHeight);
    fill(130, 130, 130);
    rect(xPos + (aWidth * 2) / 3, yPos, (aWidth * 1) / 3, aHeight);

    fill(160, 1, 70);
    triangle(
        xPos,
        yPos,
        xPos + aWidth / 2,
        yPos - aHeight * (7 / 16),
        xPos + aWidth,
        yPos
    );
    ellipse(xPos + aWidth / 2, yPos + aHeight * 0.01, aWidth, aHeight * 0.2);
    fill(160 + 20, 1 + 20, 70 + 20);
    triangle(
        xPos,
        yPos + aHeight,
        xPos - aWidth / 2,
        yPos + aHeight,
        xPos,
        yPos + aHeight / 4
    );
    fill(160, 1, 70);
    triangle(
        xPos + (3 / 2) * aWidth,
        yPos + aHeight,
        xPos + aWidth,
        yPos + aHeight,
        xPos + aWidth,
        yPos + aHeight / 4
    );

    triangle(
        xPos + aWidth / 3,
        yPos + aHeight,
        xPos + aWidth * (2 / 3),
        yPos + aHeight,
        xPos + aWidth / 2,
        yPos + aHeight / 4
    );

    if (bigFlame) {
        fill(255, 100, 10);
        triangle(
            xPos,
            yPos + aHeight,
            xPos + aWidth,
            yPos + aHeight,
            xPos + aWidth / 2,
            yPos + aHeight * (9 / 6)
        );
        fill(210, 230, 0);
        triangle(
            xPos + aWidth / 4,
            yPos + aHeight,
            xPos + aWidth - aWidth / 4,
            yPos + aHeight,
            xPos + aWidth / 2,
            yPos + aHeight * (8 / 6)
        );
    } else {
        fill(255, 100, 10);
        triangle(
            xPos,
            yPos + aHeight,
            xPos + aWidth,
            yPos + aHeight,
            xPos + aWidth / 2,
            yPos + aHeight * (11 / 6)
        );
        fill(210, 230, 0);
        triangle(
            xPos + aWidth / 4,
            yPos + aHeight,
            xPos + aWidth - aWidth / 4,
            yPos + aHeight,
            xPos + aWidth / 2,
            yPos + aHeight * (10 / 6)
        );
    }
};

var addShot = function () {
    //var x = createVector(width / 2, height + 200);
    var deg = random(0, 360);
    var x = p5.Vector.fromAngle(radians(deg), radius);
    rockets.push(x);
}

var slideRocket = function () {
    for (let i = 0; i < rockets.length; i++) {
        var xM = rockets[i].x - center.x;
        var yM = rockets[i].y - center.y;
        var a = dist(center.x, 0, rockets[i].x, 0) / 20;
        var b = dist(center.y, 0, rockets[i].y, 0) / 20;
        if (xM > 0) {
            rockets[i].x -= a;
        } else {
            rockets[i].x += a;
        }
        if (yM > 0) {
            rockets[i].y -= b;
        } else {
            rockets[i].y += b;
        }
        drawRocket(rockets[i].x, rockets[i].y);
    }
}