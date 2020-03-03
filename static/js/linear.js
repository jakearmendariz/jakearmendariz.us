var n, m, a, b;
var arr = [
    [],
    [],
    [],
    [],
    [],
    []
];
/**
 * numInput
 * 
 * Determines the size of the matrix inputed and will save it in variables n and m
 */
function numInput() {
    n = document.getElementById("Size").value;
    m = document.getElementById("xSize").value;
    if (n == "2") {
        a = 2;
    } else if (n == "3") {
        a = 3;
    } else if (n == "4") {
        a = 4;
    } else if (n == "5") {
        a = 5;
    } else {
        a = 6;
    }

    if (m == "x2") {
        b = 2;
    } else if (m == "x3") {
        b = 3;
    } else if (m == "x4") {
        b = 4;
    } else if (m == "x5") {
        b = 5;
    } else {
        b = 6;
    }
    //console.log("a: " + a + " b: " + b);
    n = a;
    m = b;
    // console.log("a = " + a + " b = " + b);

    for (var i = 0; i < 6; i++) {
        for (var j = 0; j < 6; j++) {
            var s = "" + i + "" + j;
            // console.log(s + ": hidden");
            document.getElementById(s).style.display = "none";
        }
    }
    //console.log("Adding slots");
    for (var i = 0; i < a; i++) {
        for (var j = 0; j < b; j++) {
            var s = "" + i + "" + j;
            arr[i][j] = parseInt(document.getElementById(s).value);
            // console.log(s + ": displayed");
            document.getElementById(s).style.display = "inLine";
        }
    }
    // mJax();
}

/**
 * Calculates the determinant of a 3x3 matrix
 */
function calcDet() {
    var det = 1;
    for (var j = 0; j < n; j++) {
        if (j >= m) {
            break;
        }
        var c = arr[j][j];
        if (c == 0) {
            c = 1;
        }
        /**
         * Divides pivot column by scalar c to make 1 the leading variable
         */
        for (var i = 0; i < m; i++) {
            arr[j][i] = arr[j][i] / c;
        }
        det *= -c;

        /**
         * Subtracts down the columns making 0's surround the pivot variable
         */
        if (j < m) {
            for (var k = j + 1; k < n; k++) {
                c = -1 * arr[k][j];
                for (var i = 0; i < m; i++) {
                    if (c != 0) {
                        arr[k][i] = arr[k][i] + c * arr[j][i];
                    }
                }
            }
        }

        /**
         * Subtracts up the columns making 0's surround the pivot variable
         */
        if (j > 0) {
            for (var k = j - 1; k >= 0; k--) {
                c = -1 * arr[k][j];
                for (var i = 0; i < m; i++) {
                    if (c != 0) {
                        arr[k][i] = arr[k][i] + c * arr[j][i];
                    }
                }
            }
        }

    }
    consoleArr();
    console.log(linearDependence());
    return (Math.round(linearDependence() * det * 100) / 100);
}

/**
 * Returns whether the matrix is linearly independent
 *  1 if L.I.
 *  0 if L.D.
 */
function linearDependence() {
    for (var i = 0; i < n; i++) {
        for (var j = 0; j < m; j++) {
            if (i == j) {
                if (arr[i][j] != 1) {
                    return 0;
                }
            } else {
                if (arr[i][j] != 0) {
                    return 0;
                }
            }
        }
    }
    return 1;
}



function mJax() {
    document.getElementById("answer").innerHTML = "\begin{bmatrix}0 & 0 & 0\\0 & 0 & 0\\0 & 0 & 0\end{bmatrix}";
    document.getElementById("answer").style.display = "block";
}

/**
 * 
 * @param {The pivot column being checked} i 
 * Return a 1 if swapped, a 0 if no swap
 */
function swap(i) {
    var col = i;
    if (arr[i][i] == 0) {
        while (i < n - 1) {
            i++;
            if (arr[i][col] != 0) {
                console.log("row swapped:" + i + col);
                swapRows(i, col);
                return 1;
            }
        }
    }
    return 0;
}
//Actually swaps the rows
function swapRows(a, b) {
    var temp = [];
    for (var i = 0; i < m; i++) {
        temp[i] = arr[a][i];
    }
    for (var i = 0; i < m; i++) {
        arr[a][i] = arr[b][i];
    }
    for (var i = 0; i < m; i++) {
        arr[b][i] = temp[i];
    }
}

/**
 * Clears the matrix back to starting value
 */
function clearMatrix() {
    for (var i = 0; i < 6; i++) {
        for (var j = 0; j < 6; j++) {
            var s = "" + i + "" + j;
            // console.log(s + ": hidden");
            document.getElementById(s).value = "";
        }
    }
}

/**
 * Reduces the matrix, runs through and tries to put everything into a pivot column
 */
function rref() {
    numInput();
    for (var j = 0; j < n; j++) {
        if (j >= m) {
            break;
        }

        if (swap(j) == 1) {
            consoleArr();
        }
        var c = arr[j][j];
        if (c == 0) {
            c = 1;
        }
        /**
         * Divides pivot column by scalar c to make 1 the leading variable
         */
        var a = j + 1;
        console.log("Dividing row " + a + " by " + c) + " to other rows";
        for (var i = 0; i < m; i++) {
            arr[j][i] = Math.round(arr[j][i] * 100 / c) / 100;
        }

        /**
         * Subtracts down the columns making 0's surround the pivot variable
         */
        if (j < m) {
            for (var k = j + 1; k < n; k++) {
                c = -1 * arr[k][j];
                var a = j + 1;
                console.log("Adding row " + a + " times " + c) + " to other rows";
                for (var i = 0; i < m; i++) {
                    if (c != 0) {
                        arr[k][i] = Math.round(100 * (arr[k][i] + c * arr[j][i])) / 100;
                        consoleArr();
                    }
                }
            }
        }

        /**
         * Subtracts up the columns making 0's surround the pivot variable
         */
        if (j > 0) {
            for (var k = j - 1; k >= 0; k--) {
                c = -1 * arr[k][j];
                var a = j + 1;
                console.log("Adding row " + a + " times " + c) + " to other rows";
                for (var i = 0; i < m; i++) {
                    if (c != 0) {
                        arr[k][i] = Math.round(100 * (arr[k][i] + c * arr[j][i])) / 100;
                        consoleArr();
                    }
                }
            }
        }

    }
    printArr();

}

/*
 * Logs array to console
 */
function consoleArr() {
    var s = "";
    for (var i = 0; i < n; i++) {
        for (var j = 0; j < m; j++) {
            s += "  " + arr[i][j];
        }
        s += "\n";
    }
    console.log(s);
}

/*
 * Printing the array
 */
function printArr() {

    var s = "";
    for (var i = 0; i < n; i++) {
        for (var j = 0; j < m; j++) {
            s += "  " + arr[i][j];
        }
        s += "\n";
    }

    document.getElementById("answer").innerHTML = s;

    // document.getElementById("answer").innerHTML = \begin{bmatrix}1 & 0\\0 & 1\end{bmatrix};
}

function calc() {
    numInput();
    if (a == b) {
        document.getElementById("answer").innerHTML = calcDet();
    } else {
        document.getElementById("answer").innerHTML = "Can only find determinants of square matrices";
    }
    //printArr();
}

function inverse() {
    var s = "";
    numInput();
    if (n == m) {
        for (var i = 0; i < n; i++) {
            for (var j = m; j < 2 * m; j++) {
                if (j - n == i) {
                    arr[i][j] = 1;
                } else {
                    arr[i][j] = 0;
                }
            }
        }

        for (var j = 0; j < n; j++) {
            if (j >= m) {
                break;
            }
            swap(j);
            var c = arr[j][j];
            if (c == 0) {
                c = 1;
            }
            /**
             * Divides pivot column by scalar c to make 1 the leading variable
             */
            for (var i = 0; i < m * 2; i++) {
                arr[j][i] = Math.round(arr[j][i] * 100 / c) / 100;
            }

            /**
             * Subtracts down the columns making 0's surround the pivot variable
             */
            if (j < m) {
                for (var k = j + 1; k < n; k++) {
                    c = -1 * arr[k][j];
                    for (var i = 0; i < m * 2; i++) {
                        if (c != 0) {
                            arr[k][i] = Math.round(100 * (arr[k][i] + c * arr[j][i])) / 100;
                        }
                    }
                }
            }

            /**
             * Subtracts up the columns making 0's surround the pivot variable
             */
            if (j > 0) {
                for (var k = j - 1; k >= 0; k--) {
                    c = -1 * arr[k][j];
                    for (var i = 0; i < m * 2; i++) {
                        if (c != 0) {
                            arr[k][i] = Math.round(100 * (arr[k][i] + c * arr[j][i])) / 100;
                        }
                    }
                }
            }

        }
        if (linearDependence() == 0) {
            document.getElementById("answer").innerHTML = ("Cannot find inverse. It is linearly dependent.");
            return;
        }
    } else {
        document.getElementById("answer").innerHTML = "Can only find the inverse of square matrices"
    }
    s = "";
    for (var i = 0; i < n; i++) {
        for (var j = m; j < 2 * m; j++) {
            s += "  " + arr[i][j];
        }
        s += "\n";
    }
    document.getElementById("answer").innerHTML = s;
}


function openR() {
    document.getElementById("rModal").style.display = " inLine";
    document.getElementById("information").innerHTML = "RREF stand for reduced row echelon form. Guassian elimination allows us to simplify matricies to this form so we can learn more on it's span, basis, dimensions and pretty much every thing else for linear algebra. If you would like a more indepth look at how we are calculating rref, right click anywhere, hit inspect and click on console. Or you can search rref for a better explanation."
    closeD();
    closeI();
    closeM();
    closeG()
}

function closeR() {
    document.getElementById("rModal").style.display = "none";
}

function openD() {
    closeR();
    closeI();
    closeM();
    closeG()
    document.getElementById("dModal").style.display = " inLine";
    document.getElementById("information").innerHTML = "The determinant can only be found in square matricies. One way of understanding it is as a scalar value that tells how much space is being squished or stretched by a given transformation"
}

function closeD() {
    document.getElementById("dModal").style.display = "none";
}

function openI() {
    closeR();
    closeD();
    closeM();
    closeG()
    document.getElementById("iModal").style.display = " inLine";
    document.getElementById("information").innerHTML = "The inverse of the matrix multiplied by the provided matrix will transform it into the identity matrix. This can only work on square matricies."
}

function closeI() {
    document.getElementById("iModal").style.display = "none";
}

function openM() {
    closeR();
    closeD();
    closeI();
    closeG()
    document.getElementById("information").innerHTML = "Matrix multiplication multiplies the first matrix by the second. The length of each row in matrix A must equal the length of each col in matrix B. ex:(3x2)*(2x4) works but (3x3)*(4x3) cannot multiply"
    document.getElementById("mModal").style.display = " inLine";
}

function closeM() {
    document.getElementById("mModal").style.display = "none";
}


function openG() {
    closeR();
    closeD();
    closeI();
    closeM();
    document.getElementById("information").innerHTML = "Coming soon";
    document.getElementById("gModal").style.display = " inLine";
}


function closeG() {
    document.getElementById("gModal").style.display = "none";
}