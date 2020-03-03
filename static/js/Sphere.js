function setup() {
    createCanvas(window.innerWidth, window.innerHeight, WEBGL);
    background(0);
    frameRate(60);
}
var x = 2;
var dir = 2;



function draw() {
    background(100);
    if (x < 2) {
        dir = 2;
    }
    if (x > 1200) {
        dir = -2;
    }
    x += dir;
    noFill();
    rotateX(millis() / 2000);
    rotateY(millis() / 2000);
    stroke(255);
    if (x == 600) {
        stroke(255, 0, 0);
    }
    sphere(x, 24, 16);
    sphere(1200 - x, 24, 16);
    if (x == 600) {

    }
    /*
    stroke(0, 255, 0);
    sphere(x, 20, 15);
    stroke(255, 255, 0);
    sphere(x, 21, 13);
    stroke(0, 0, 255);
    sphere(x, 24, 16);
    */

}