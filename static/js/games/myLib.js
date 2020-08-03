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

    this.r = 31;
    this.g = 51;
    this.b = 113;

    this.displayPlatform = function () {
        fill(this.r, this.g, this.b);
        rect(this.x, this.y, this.l, this.w);
    };

    this.displayPlatform3D = function () {
        fill(this.r, this.g, this.b);
        rect(this.x, this.y, this.l, this.w);
        fill(this.r + 20, this.g + 20, this.b + 30);
        beginShape();
        vertex(this.platforms[i].x, this.platforms[i].y);
        vertex(this.platforms[i].x + 20, this.platforms[i].y - 20);
        vertex(this.platforms[i].x + this.platforms[i].l + 20, this.platforms[i].y - 20);
        vertex(this.platforms[i].x + this.platforms[i].l, this.platforms[i].y);
        endShape(CLOSE);
        fill(this.r - 20, this.g - 20, this.b - 20);
        beginShape();
        vertex(this.platforms[i].x + this.platforms[i].l + 20, this.platforms[i].y - 20);
        vertex(this.platforms[i].x + this.platforms[i].l, this.platforms[i].y);
        vertex(this.platforms[i].x + this.platforms[i].l, height);
        vertex(this.platforms[i].x + this.platforms[i].l + 20, height);
    }

    this.updatePlatform = function (x, y) {
        this.x += x;
        this.y += y;
    };

    this.color = function (r, g, b) {
        this.r = r;
        this.g = g;
        this.b = b;
    }
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
    this.g = 0.0006578 * height;
    this.platforms = [];
    this.still = false;
    var ave = w + h / 2;
    this.diameter = 0.025 * ave;
    this.bottom = height - 10;
    this.currentPlatform = 0;
    this.stopp = false;
    this.numBounces = 0;
    this.direction = 0;
    this.numPlat = 0;
    this.stopp = false;
    this.side = 0;
    this.time = 0;
    this.tLimit = 500;
    this.r = 31;
    this.g = 51;
    this.b = 113;

    /**
     * Design of the level
     */


    this.numPlat = 0;

    this.setGravity = function (gravity) {
        this.g = gravity;
    }

    this.drawBall = function () {
        ellipse(xloc, yloc, size - i * steps, size - i * steps);
    }
    this.drawBall3D = function (xloc, yloc, size, num) {
        const grayvalues = 250 / num;
        const steps = size / num;
        for (let i = 20; i < num; i++) {
            fill(i * grayvalues);
            ellipse(xloc, yloc, size - i * steps, size - i * steps);
        }
    }

    this.display = function () {

        background(235);
        fill(31, 51, 113);
        for (var i = 0; i < this.platforms.length; i++) {
            this.platforms[i].displayPlatform3D();
        }
        noStroke();
        this.drawBall(this.xPos, this.yPos, this.diameter * 1.75, 50);
        //drawAst(this.xPos, this.yPos, this.diameter * 2, 50);
        //ellipse(this.xPos, this.yPos, this.diameter, this.diameter);
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
            this.platforms[i].updatePlatform(a, 0);
        }
    }

    this.mantain = function () {
        for (var i = this.platforms.length - 1; i >= 0; i--) {
            console.log(i + "/ " + this.platforms.length);
            if (this.platforms[i].x < -.5 * width) {
                var y = random(height * 1 / 3, height);
                this.platforms.splice(0, 1);
                this.numPlat--;
                this.addPlatform(width * 2, y, height - y, 600);

            }
        }
    }

    this.trim = function () {
        var a = [];
        for (var i = 1; i < this.platforms.length; i++) {
            a[i - 1] = this.platforms[i];
        }

        this.platforms = a;
    }

    this.move = function () {

        if (this.still) {
            if (!this.intersection()) {
                this.still = false;
            }
        }

        if (!this.still) {
            this.yVel += this.g;
            this.updatePos(this.yVel);
        }

        if (!this.still) {
            //console.log("Not still");
            var a = this.intersection();
            if (this.yPos >= h - this.diameter / 2) {
                //console.log("Floor");
                a = true;
                this.bottom = h;
            }
            if (a) {
                if (this.stopp == true) {
                    //    console.log("Intersection");
                    this.yPos = this.bottom - this.diameter / 2 - 1;
                    this.yVel = 0;
                    this.still = true;
                    this.stopp = false;
                } else {
                    ///    console.log("Intersection");
                    this.yVel *= -40 / 100;
                    this.numBounces++;
                    if (this.numBounces > 3) {
                        this.yPos = this.bottom - this.diameter / 2 - 1;
                        this.yVel = 0;
                        this.still = true;
                    }
                }
            }
        }

        if (this.direction == 1) {
            if (this.xPos < w - this.diameter / 2) {
                //this.xPos += this.xVel;
                //ball.xVel += .3;
                this.movePlat(-10);
            }
        } else if (this.direction == -1) {
            if (this.xPos > this.diameter / 2) {
                // this.xPos -= this.xVel;
                //ball.xVel += .3;
                ball.movePlat(10);
            }
        }

        if (keyIsPressed) {} else {
            this.direction = 0;
            this.xVel = 0;
        }

        if (this.xIntersection()) {

            this.direction = 0;
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
                        console.log("x intersection");
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
                        console.log("x intersection");
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
        for (var i = 0; i < this.platforms.length; i++) {
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
                        console.log("ball: " + this.xPos + ", rect: " + x);
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
     */
    this.jump = function (neg_gravity) {
        this.numBounces = 0;
        this.yVel = neg_gravity * this.g;
        this.still = false;
        this.stopp = false;
    };

    this.drop = function () {
        this.still = false;
        if (this.yPos < this.bottom - this.diameter / 2 - 2) {
            if (this.yVel < 0) {
                this.yVel = 2;
            } else {
                this.yVel += 10;
            }
        }
        this.stopp = true;
    };
}