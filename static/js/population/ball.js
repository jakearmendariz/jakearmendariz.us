function ball() {
    this.r = 30;
    this.x = random(0, window.innerWidth);
    this.y = random(0, window.innerHeight);
    this.vel = createVector(0, 0);
    this.head = createVector(this.x + this.r / 2 - this.r / 6, this.y, );
    this.largeRad = window.innerWidth * 2;
    var deg = random(-10, 10);
    this.dir = random(0, 360);
    this.arr = p5.Vector.fromAngle(radians(this.dir), this.largeRad);

    this.add = random(-2, 2);

    var vision = [];
    //Head of circle is going to be to the right in the beginning

    this.update = function () {
        //Moves them along vector arr
        var xM = this.x - this.arr.x;
        var yM = this.y - this.arr.y;
        var a = dist(this.x, 0, this.arr.x, 0) / 350;
        var b = dist(this.y, 0, this.arr.y, 0) / 350;
        this.vel.x = a;
        this.vel.y = b;
        if (xM > 0) {
            this.x -= a;
        } else {
            this.x += a;
        }
        if (yM > 0) {
            this.y -= b;
        } else {
            this.y += b;
        }

        //Keepsthis.balls on the screen
        if (this.x > width) {
            this.x = 0;
        } else if (this.x < 0) {
            this.x = width;
        }
        if (this.y > height) {
            this.y = 0;
        } else if (this.y < 0) {
            this.y = height;
        }
    };

    this.aim = function () {
        stroke(255);
        this.dir += this.add;
        this.dir = this.dir % 360;
        var deg = random(this.dir, this.dir + 20);
        this.arr = p5.Vector.fromAngle(radians(deg), this.largeRad);
        a = p5.Vector.fromAngle(radians(this.dir), this.largeRad);
        b = p5.Vector.fromAngle(radians(this.dir + 30), this.largeRad);
        //line(this.x, this.y, this.arr.x, this.arr.y);
        let c = p5.Vector.fromAngle(radians(this.dir), 0);
        //line(this.x, this.y, c.x, c.y);
        noStroke();
        fill(255, 255, 255, 0);
        beginShape();
        vertex(this.x, this.y);
        vertex(a.x, a.y);
        vertex(b.x, b.y);
        endShape(CLOSE)
        this.setVision();

    }

    this.drawBall = function () {
        ellipse(this.x, this.y, this.r, this.r);
        // Draw a triangle rotated in the direction of velocity
        /*
        let theta = this.vel.heading() + radians(90);
        fill(127);
        stroke(200);
        push();
        translate(this.x, this.y);
        rotate(theta);
        beginShape();
        vertex(0, -this.r * 2);
        vertex(-this.r, this.r * 2);
        vertex(this.r, this.r * 2);
        endShape(CLOSE);
        pop();
        /*
        noStroke();
        fill(0, 0, 255);
        ellipse(this.x, this.y, this.r, this.r);
        /*
        if (round(this.deg.x - this.x) == 0) {
            triangle(this.x, this.y, this.x + 10, this.y + 40, this.x - 10, this.y + 40);
        } else {
            let slope = (this.deg.y - this.y) / (this.deg.x - this.x);
            if((this.deg.y - this.y) > 0  && (this.deg.x - this.x) > 0){
                
            }
        }
        
        push()
        translate(this.x, this.y);
        //triangle(this.x, this.y, this.x + 10, this.y + 40, this.x - 10, this.y + 40);
        rotate(this.vel.heading());
        //triangle(0, 0, 0 + 10, 0 + 40, 0 - 10, 0 + 40);
        rectMode(CENTER);
        rect(0, 0, 50, 20);
        pop();
        fill(0, 255, 255);
        stroke(255);
        */
    }

    this.setVision = function () {
        let a = -150 + this.dir;
        for (var i = 0; i < 6; i++) {
            let v = p5.Vector.fromAngle(radians(a), 75);
            vision[i] = createVector(this.x + v.x, this.y + v.y);
            a += 50;
            stroke(255);
            //line(this.x, this.y, vision[i].x, vision[i].y);
        }
    }

}

/**
 * Flock
 * 
 * Contains the array of balls. 
 * Will attempt to make them uniform like a flock of birds
 */
function Flock() {
    this.balls = [];
    var size = 30;
    for (var i = 0; i < size; i++) {
        this.balls[i] = new ball();
    }

    /**
     * seperation
     * 
     * This function will loop over every ball checking when it is near another
     * If it is within 70, then it will diverte their course and push them to their right to avoid
     */
    this.seperation = function () {
        for (var i = 0; i < size; i++) {
            for (var j = 0; j < size; j++) {
                /** For some reason this didn't work as the distane function 
                let a = this.balls[i].x - this.balls[j].x;
                let b = this.balls[i].y - this.balls[j].y;
                let distance = sqrt(pow(a, 2), pow(b, 2));
                */
                let a = this.balls[i].x - this.balls[j].x;
                let b = this.balls[i].y - this.balls[j].y;
                let distance = dist(this.balls[i].x, this.balls[i].y, this.balls[j].x, this.balls[j].y);
                if (distance < 50) {
                    line(this.balls[i].x, this.balls[i].y, this.balls[j].x, this.balls[j].y);

                    //Changes the dirretion so they steer away from each other
                    if (abs(this.balls[i].dir - this.balls[j].dir) > 175 && abs(this.balls[i].dir - this.balls[j].dir) < 185) {
                        this.balls[i].dir += 6;
                        this.balls[j].dir += 6;

                    } else if (abs(this.balls[i].dir - this.balls[j].dir) > 60) {
                        this.balls[i].dir += .2;
                    }

                    a = round(a);
                    b = round(b);
                    if (a < 8 && a > 0) {
                        a = 8;
                    }
                    if (a > -8 && a < 0) {
                        a = -8;
                    }
                    if (b < 8 && b > 0) {
                        b = 8;
                    }
                    if (b > -8 && b < 0) {
                        b = -8;
                    }
                    //He is on my left side
                    if (a > 0) {
                        let k = 1 / a;
                        this.balls[i].dir += k + .0;
                    } else if (a < 0) { //He is on my right side
                        let k = 1 / a;
                        this.balls[i].x += k - .0;
                    }

                    if (b > 0) { //He is below me
                        this.balls[i].y += (1 / b + .02);
                    } else if (b < 0) { //He is ontop of me
                        this.balls[i].y += (1 / b) - .02;
                    }


                }
            }
        }
    }

    this.alignment = function () {
        for (var i = 0; i < size; i++) {
            for (var j = 0; j < size; j++) {
                let distance = dist(this.balls[i].x, this.balls[i].y, this.balls[j].x, this.balls[j].y);
                if (distance < 100) {
                    if (abs(this.balls[i].dir - this.balls[j].dir) < 180) {
                        let ave = (this.balls[i].dir + this.balls[j].dir) / 2;
                        this.balls[i].dir = ave + .005;
                        this.balls[j].dir = ave - .005;
                    }
                }
            }
        }
    }

    this.cohesion = function () {
        for (var i = 0; i < size; i++) {
            for (var j = 0; j < size; j++) {
                let distance = dist(this.balls[i].x, this.balls[i].y, this.balls[j].x, this.balls[j].y);
                if (distance < 150) {

                }
            }
        }
    }


    this.update = function () {
        for (var i = 0; i < size; i++) {
            this.balls[i].aim();
            this.balls[i].update();
            this.seperation();
            this.balls[i].drawBall();
            //this.alignment();
        }
    }
}

var flock;

function setup() {
    createCanvas(window.innerWidth, window.innerHeight);
    flock = new Flock();
    frameRate(50);
}


/**
 * draw
 * 
 * Conitnously runs and shows the program
 */
function draw() {
    background(0, 0, 0);
    flock.update();
}