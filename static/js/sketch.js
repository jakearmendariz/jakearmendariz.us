/**Skect.js
 * Jake Armendariz
 * This controls the settings for the world
 * Contains none of the actual levels, rather it creates the sceneary
 */


var ball;
/**
 * setup()
 * it sets all yhe variables intial state
 * Creates the stage
 */

function setup() {
  createCanvas(window.innerWidth, window.innerHeight);
  ave = width + height / 2;
  ball = new Ball(width * 1 / 4, height / 8, width, height);
  placeplatforms();

}


function placeplatforms() {
  for (var i = width * 2 / 3; i < width * 3; i += width / 3) {
    var y = random(height / 2, height);
    ball.addPlatform(i, y, height - y, 600);
  }
}
/**
 * keyPressed
 * 
 * Moves the ball to the left, right and up
 */
function keyPressed() {

  if (keyCode == 38) {
    ball.jump();
  } else if (keyCode == 39) {
    ball.direction = 1;
  } else if (keyCode == 37) {
    ball.direction = -1;
  } else if (keyCode == 40) {
    ball.drop();
  } else if (keyCode == 80) {
    ball.addPlatform(ball.xPos - 20, ball.yPos + ball.diameter / 2, height - ball.yPos + ball.diameter / 2, ball.diameter) + 20;
  } else {
    ball.direction = 0;
    ball.xVel = 0;
  }
}

/**
 * draw
 * 
 * Conitnously runs and shows the program
 */
function draw() {
  background(255, 255, 255);
  ball.display();
  ball.move();
  ball.mantain();
}