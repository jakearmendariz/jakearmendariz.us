/**
 * Platform
 * @param {left pos} x
 * @param {top pos} y
 * @param {width} w
 * @param {length} l
 *
 * Platform creastes a Vector
 */
function Platform(x, y, w, l) {
    this.x = x;
    this.y = y;
    this.w = w;
    this.l = l;

    this.displayPlatform = function () {
        fill(120);
        rect(this.x, this.y, this.l, this.w);
        fill(120, 140, 180);
        if (this.y == 0) {
            for (var i = 20; i < this.l; i += 50) {
                for (var j = this.w - 70; j > -100; j -= 80) {
                    rect(this.x + i, j, 30, 50);
                }
            };
        } else {
            fill(120, 140, 180);
            for (var i = 20; i < this.l; i += 50) {
                for (var j = 20; j < window.height + 90; j += 80) {
                    rect(this.x + i, this.y + j, 30, 50);
                }
            };
        }
    }
    this.updatePlatform = function (a) {
        this.x += a;
    };

}

/**
 * Ball
 * @param {Starting pos} this.xPos
 * @param {Starting pos}this.yPos
 * The w and l are the size of the window
 */
function Ball(xPos, yPos, w, h) {
    this.xPos = xPos;
    this.yPos = yPos;
    this.xVel = 0.007 * width;
    this.xVel = 0;
    this.yVel = 0;
    this.g = 0.0003578 * height;
    this.platforms = [];
    this.still = false;
    var ave = w + h / 2;
    this.diameter = 0.075 * ave;
    this.bottom = height - 10;
    this.currentPlatform = 0;
    this.stopp = false;
    this.numBounces = 0;
    this.direction = 0;
    this.numPlat = 0;
    this.side = 0;
    this.time = 0;
    this.tLimit = 500;
    this.score = 0;
    this.img = loadImage('../../public/images/plane.png');
    /**
     * Design of the level
     */


    this.numPlat = 0;


    this.drawBall = function (xloc, yloc, size, num) {
        const grayvalues = 250 / num;
        const steps = size / num;
        for (let i = 20; i < num; i++) {
            fill(i * grayvalues);
            //ellipse(xloc, yloc, size - i * steps, size - i * steps);
        }

        image(this.img, xloc - this.diameter / 2, yloc - this.diameter / 2, this.diameter, this.diameter);
    }

    this.display = function () {


        fill(31, 51, 113);
        for (var i = 0; i < this.platforms.length; i++) {
            this.platforms[i].displayPlatform();
            if (this.platforms[i].x == 0 && this.platforms[i].y == 0) {
                this.score++;
            }
            if (this.platforms[i].y != 0) {
                fill(140);
                beginShape();
                vertex(this.platforms[i].x, this.platforms[i].y);
                vertex(this.platforms[i].x + 20, this.platforms[i].y - 20);
                vertex(this.platforms[i].x + this.platforms[i].l + 20, this.platforms[i].y - 20);
                vertex(this.platforms[i].x + this.platforms[i].l, this.platforms[i].y);
                endShape(CLOSE);
                fill(100);
                beginShape();
                vertex(this.platforms[i].x + this.platforms[i].l + 20, this.platforms[i].y - 20);
                vertex(this.platforms[i].x + this.platforms[i].l, this.platforms[i].y);
                vertex(this.platforms[i].x + this.platforms[i].l, height);
                vertex(this.platforms[i].x + this.platforms[i].l + 20, height);
                endShape(CLOSE);
            } else {
                fill(100);
                beginShape();
                vertex(this.platforms[i].x + this.platforms[i].l + 20, this.platforms[i].y - 20);
                vertex(this.platforms[i].x + this.platforms[i].l, this.platforms[i].y);
                vertex(this.platforms[i].x + this.platforms[i].l, this.platforms[i].w);
                vertex(this.platforms[i].x + this.platforms[i].l + 20, this.platforms[i].w - 20);
                endShape(CLOSE);
            }

        }
        noStroke();
        this.drawBall(this.xPos, this.yPos, this.diameter * 1.75, 50);

    };

    this.addPlatform = function (x, y, l, w) {
        this.numPlat++;
        this.platforms[this.numPlat - 1] = new Platform(
            x,
            y,
            l,
            w,
        );
    };

    /**
     * Helps to move all platforms when ball moves... Like in Mario and shit
     */
    this.movePlat = function (a) {
        for (var i = 0; i < this.platforms.length; i++) {
            this.platforms[i].updatePlatform(a);
        }
    }


    this.maintain = function () {

        if (this.platforms[0].x < -1000) {
            console.log("FUCK ME");
            this.platforms.splice(0, 2);
            this.numPlat -= 2;
            y = random(0, 600);
            var gap = 380;
            if (h > w) {
                gap = 450;
            }
            ball.addPlatform(2750, 0, y, 350);
            ball.addPlatform(2750, y + gap, height - y - gap, 350);
        }
    }


    this.dead = function () {
        if (this.intersection() || this.xIntersection()) {
            return true;
        }
    }

    this.clear = function () {
        this.platforms = [];
        this.numPlat = 0;
    }

    /**
     * Updates the y positon of plane and moves th eblocks
     */
    this.move = function () {
        this.yVel += this.g;
        this.updatePos(this.yVel);

        if (this.direction == 1) {
            if (this.xPos < w - this.diameter / 2) {
                this.movePlat(-5);
            }
        } else if (this.direction == -1) {
            if (this.xPos > this.diameter / 2) {
                ball.movePlat(5);
            }
        }



    };
    /**
     * updatePos
     *
     * It updates the y position based on current velocity
     * It checks for intersection every pixel moved
     */
    this.updatePos = function (vel) {
        var sign;
        if (vel <= 0) {
            sign = -1;
        } else {
            sign = 1;
        }
        for (var i = 0; i < Math.abs(vel); i++) {
            this.yPos += sign;
            var inte = this.intersection();
            if (this.yPos >= h - this.diameter / 2) {
                inte = true;
                this.bottom = h;
            }
            if (inte == true) {
                //   console.log("Intersection baby");

                break;
            }
        }
    };
    /*
          Checks for intersections to the left and right of the ball
      */

    this.xIntersection = function () {
        for (var i = 0; i < this.platforms.length; i++) {
            var x = this.platforms[i].x;
            var y = this.platforms[i].y;
            var w1 = this.platforms[i].w;
            var l1 = this.platforms[i].l;
            var cover = w1 / this.diameter;
            var y1 = y;
            //leftSide of objects

            for (var j = 0; j < cover * 10; j++) {
                var d = dist(x, y, this.xPos, this.yPos);
                if (d < this.diameter / 2) {
                    if (this.yPos > this.platforms[i].y) {
                        this.side = -1;
                        //this.xPos -= 3;
                        //console.log("x intersection");
                        return true;
                    }
                }
                y += this.diameter / 10;
            }
            y = y1;
            //Rightside of objects
            for (var j = 0; j < cover * 10; j++) {
                var d = dist(x + l1, y, this.xPos, this.yPos);
                if (d < this.diameter / 2) {
                    if (this.yPos > this.platforms[i].y) {
                        this.side = 1;
                        // this.xPos += 3;
                        //console.log("x intersection");
                        return true;
                    }
                }
                y += this.diameter / 10;
            }

        }
    };

    /**
intersection

Checks all positions of platforms looking for intersection
if intersecting it will not  move the objects
*/
    this.intersection = function () {
        //console.log("okay");
        for (var i = 0; i < this.platforms.length; i++) {
            //   console.log("In");
            var x = this.platforms[i].x;
            var y = this.platforms[i].y;
            var w1 = this.platforms[i].w;
            var l1 = this.platforms[i].l;

            var x1 = x;
            var cover = l1 / this.diameter;
            //Checks the top of the platform
            for (var j = 0; j < cover * 10; j++) {
                if (this.xPos > x && this.xPos < x + l1) {
                    var d = dist(this.xPos, this.yPos, x, y);
                    if (d <= this.diameter / 2 + 2) {
                        //console.log("ball: " + this.xPos + ", rect: " + x);
                        this.bottom = y;
                        this.currentPlatform = i;
                        return true;
                    }
                    x += this.diameter / 10;
                }

            }
            x = x1;
            //Check the bottom of the platform
            for (var j = 0; j < cover * 10; j++) {
                var d = dist(this.xPos, this.yPos, x, y + w1);

                if (d <= this.diameter / 2 + 2) {
                    this.bottom = y;
                    this.currentPlatform = i;
                    return true;
                }
                x += this.diameter / 10;
            }
        }

        return false;
    };


    /**
     * When the up button is pressed jump will be invoked
     *
     */
    this.jump = function () {
        this.numBounces = 0;
        this.yVel = -29 * this.g;
        this.still = false;
        this.stopp = false;
    };

}