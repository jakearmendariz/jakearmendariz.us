/**
 * Snake
 * By Jake Armendariz
 * Written in javascript using the p5 library
 */
var s;
var food, posion;
var posions;
var scale;
var body;
var gameOver = false;
var gameStarted = false;
//1 is easy, 2 is medium, and 3 is hard
var difficulty = -1;
//0:east 1:south 3:north 2: west
var direction = 0;
var ave;
var unit;
var pause = false;
var txt;
var moves = new Array(30);

$(document).ready(function () {

    $.get('file:///Users/jakearmendariz/Desktop/site/views/games/Snakers.txt', function (data) {
        alert(data)
    }, 'text');


});



function preload() {
    //txt = loadStrings("Snakers.txt");
}

//Begis the program, intitalizes the varibles
function setup() {
    console.log(txt);
    if (window.innerWidth < window.innerHeight) {
        var a = window.innerWidth;
    } else {
        var a = window.innerHeight;
    }
    a = a - a % 30;
    createCanvas(a, a);
    unit = a / 30;
    s = new Snake();
    body = [];
    body[0] = s;
    scale = unit;
    ave = height + width / 2;
    frameRate(15);

    for (var i = 0; i < 30; i++) {
        moves[i] = new Array(30);
    }

    food = createVector(
        x = unit * Math.round(Math.random() * 29),
        y = unit * Math.round(Math.random() * 29),
    )

    posion = createVector(
        x = unit * Math.round(Math.random() * 29),
        y = unit * Math.round(Math.random() * 29),
    )
    while ((posion.x == food.x && posion.y == food.y) || (posion.x == body[0].x && posion.y == body[0].y)) {
        posion.x = unit * Math.round(Math.random() * 29);
        posion.y = unit * Math.round(Math.random() * 29);
    }

    posions = [];
    posions[0] = posion;


}

var initGraph = function () {
    for (var i = 0; i < 30; i++) {
        for (var j = 0; j < 30; j++) {
            moves[i][j] = 0;

        }
    }
    for (var i = 0; i < body.length; i++) {
        moves[body[i].x][body[i].y] = -1;
    }
}

function draw() {
    if (!gameStarted) {
        displayTitle()
    } else if (!gameOver) {
        background(0);
        for (var i = 0; i < 30; i++) {
            stroke(255);
            //line(i * unit, 0, i * unit, height);
        }
        for (var i = 0; i < 30; i++) {
            stroke(255);
            //line(0, i * unit, width, i * unit);
        }
        stroke(0);
        if (!pause) {
            s.update();
        }
        fill(255, 100, 100);
        if (s.x === food.x && s.y === food.y) {
            changeFoodLocation();
            eaten();
        }
        //s.show();
        showSnake();
        fill(100, 255, 100);
        rect(food.x, food.y, unit, unit);
        if (difficulty == 3) {
            fill(255, 55, 55);
            for (var i = 0; i < posions.length; i++) {
                rect(posions[i].x, posions[i].y, unit, unit);
            }
        }
        if (death()) {
            gameOver = true;
            var time = millis();
            posions = [];
            posions[0] = posion;
        }
    }
    if (gameOver) {
        background(0);
        textSize(.133 * width);
        fill(255);
        text("Game Over", .5 * width, .466 * height);
        var st = body.length - 1;
        var t = "scored: " + st + "";
        textSize(.06 * width);
        text(t, .5 * width, .58 * height);
        var a = document.getElementById("score").innerHTML;
        if (a < st) {
            a = st;
            document.getElementById("score").innerHTML = st;
        }
        text("High score = " + a + "", .5 * width, .66 * height);
        text("Press any button to restart", .5 * width, .8 * height);
    }
}

//Assigns the new location for the food
changeFoodLocation = function () {
    food.x = unit * Math.round(Math.random() * 29);
    food.y = unit * Math.round(Math.random() * 29);
    for (var i = 0; i < posions.length; i++) {
        if (food.x == posions[i].x && food.y == posions[i].y) {
            food.x = unit * Math.round(Math.random() * 29);
            food.y = unit * Math.round(Math.random() * 29);
        }
    }
    var a = createVector();
    a.x = unit * Math.round(Math.random() * 29);
    a.y = unit * Math.round(Math.random() * 29);
    while (a.x == food.x && a.y == food.y || a.x == body[0].x && a.y == body[0].y) {
        a.x = unit * Math.round(Math.random() * 29);
        a.y = unit * Math.round(Math.random() * 29);
    }
    posions[posions.length] = a;
    console.log("p length: " + posions.length);
};


function displayTitle() {
    textAlign(CENTER);
    background(0);
    textSize(.13 * width);
    fill(100, 255, 100);
    text("Snakers", .5 * width, .45 * height);
    textSize(.02 * width);
    text("By Jake Armendariz", .5 * width, .516 * height);
    textSize(.033 * width);
    fill(300, 300, 300);
    text("Enter a number", .5 * width, .6 * height);
    text("Easy: 1  \t\t\t(Free play)", .5 * width, .65 * height);
    text("Medium: 2 \t(Strict borders)", .5 * width, .7 * height);
    text("Hard: 3  \t\t\t(Bad apples)", .5 * width, .75 * height);
}

/**
 * Handles user controls
 * on easy mode it will keep the snake from turning around and eating itself
 */
function keyPressed() {
    if (!gameStarted) {
        if (keyCode == 49) {
            difficulty = 1;
            frameRate(15);
        } else if (keyCode == 51) {
            difficulty = 3;
            frameRate(17);
        } else {
            difficulty = 2;
            frameRate(20);
        }
        gameStarted = true;
    }

    if (gameOver && gameStarted) {
        gameOver = false;
        gameStarted = false;
        s = new Snake();
        body = [];
        body[0] = s;
        body[0]
    }
    if (keyCode == 81) {
        gameOver = true;
        gameStarted = true;
    }
}

/**
 * Creates the next part of snake, locates it off screen to be moved once the head increase position
 */
eaten = function () {
    var a = new Snake();
    a.x = width;
    a.y = height;
    body[body.length] = a;
};

var up = function () {
    s.dir(0, -1);
    direction = 3;
}

var down = function () {
    s.dir(0, 1);
    direction = 1;
}


var left = function () {
    s.dir(-1, 0);
    direction = 2;
}

var right = function () {
    s.dir(1, 0);
    direction = 0;
}



var turn = function () {


}
/**
Snake is not the actual snake but just one part
The snake is an array of Snake objects
*/
function Snake() {
    this.x = 3 * unit;
    this.y = 3 * unit;
    this.scale = unit;
    this.xSpeed = unit;
    this.ySpeed = 0;
    //a, b represent the initial values of head
    this.update = function () {
        turn();
        var a = this.x;
        var b = this.y;
        this.x += this.xSpeed;
        this.y += this.ySpeed;
        if (difficulty == 1) {
            if (this.x >= width) {
                this.x = 0;
            }
            if (this.x <= -30) {
                this.x = width - this.scale;
            }
            if (this.y >= height) {
                this.y = 0;
            }
            if (this.y <= -30) {
                this.y = height - this.scale;
            }
        } else {
            // On hard mode leaving the bounds kills you
            if (this.x >= width) {
                gameOver = true;
                posions = [];
                posions[0] = posion;
            }
            if (this.x <= -30) {
                gameOver = true;
                posions = [];
                posions[0] = posion;
            }
            if (this.y >= height) {
                gameOver = true;
                posions = [];
                posions[0] = posion;
            }
            if (this.y <= -30) {
                gameOver = true;
                posions = [];
                posions[0] = posion;
            }
        }


        for (var i = body.length - 1; i > 0; i--) {
            if (i == 1) {
                body[i].x = a;
                body[i].y = b;
            } else {
                body[i].x = body[i - 1].x;
                body[i].y = body[i - 1].y;
            }
        }
    }

    this.show = function () {
        fill(255);
        noStroke();
        rect(this.x, this.y, unit, unit);
    };

    this.dir = function (x, y) {
        this.xSpeed = x * this.scale;
        this.ySpeed = y * this.scale;
    };



}

//If the snake eats itself death is invoked
death = function () {
    var a = body[0].x;
    var b = body[0].y;
    if (difficulty == 3) {
        for (var i = 0; i < posions.length; i++) {
            if (body[0].x == posions[i].x && body[0].y == posions[i].y) {
                return true;
            }
        }
    }
    for (var i = 1; i < body.length; i++) {
        var d = dist(a, b, body[i].x, body[i].y);
        if (d == 0) {
            return true;
        }
        if (difficulty == 3) {
            if (body[i].x == posion.x && body[i].y == posion.y) {
                return true;
            }
        }
    }
    return false;
};

//Prints entire snake
showSnake = function () {
    //console.log(body.length);
    for (var i = 0; i < body.length; i++) {
        body[i].show();
    }
};