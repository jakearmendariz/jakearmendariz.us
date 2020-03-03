/**Flappy.js
 * Jake Armendariz
 * This controls the settings for the world
 * Contains none of the actual levels, rather it creates the sceneary
 */


var ball;
var gameStarted = false;
var gameOver = false;
var x;
var longer;
/**
 * setup()
 * it sets all yhe variables intial state
 * Creates the stage
 */

function setup() {
    createCanvas(window.innerWidth, window.innerHeight);
    ave = width + height / 2;
    x = 0;
    ball = new Ball(width * 1 / 4, height / 2, width, height);
    placeplatforms();
    longer = max(width, height);

}


function placeplatforms() {
    var y, x;
    for (var i = 1000; i <= 4000; i += 750) {
        y = random(0, 600);
        var gap = 380;
        if (height > width) {
            gap = 500;
        }
        ball.addPlatform(i, 0, y, 350);
        ball.addPlatform(i, y + gap, height - y - gap, 350);
    }

}
/**
 * keyPressed
 * 
 * Moves the ball to the left, right and up
 */
function keyPressed() {
    ball.jump();
    if (x > 20) {
        gameStarted = true;
        gameOver = false;
    }
}


function mouseClicked() {
    ball.jump();
    if (x > 20) {
        gameStarted = true;
        gameOver = false;
    }
}


/**
 * draw
 * 
 * Conitnously runs and shows the program
 */
function draw() {

    if (!gameStarted && !gameOver) {
        x++;
        background(120, 210, 255);
        textAlign(CENTER);
        fill(255);
        textSize(.13 * width);
        text("Flappy Plane", .5 * width, .45 * height);
        textSize(.013 * longer);
        text("Do anything to play", .5 * width, .7 * height);


    } else if (gameStarted) {
        x = 0;
        background(120, 210, 255);
        ball.direction = 1;
        ball.display();
        ball.move();
        ball.maintain();
        fill(255);
        textSize(.02 * longer);
        text(ball.score, 1600, 50);
        if (ball.dead()) {
            gameStarted = false;
            gameOver = true;
            ball.clear();
            placeplatforms();
            ball.yPos = height / 2;
            //saveStrings(ball.score + "", 'flappy.txt', '');
            ball.score = 0;
        }
    } else if (gameOver) {
        background(120, 210, 255);
        textAlign(CENTER);
        fill(255);
        textSize(.08 * width);
        text("You died", .5 * width, .45 * height);
        textSize(.013 * longer);
        text("Do anything to play again", .5 * width, .7 * height);
        x++;
    }
}