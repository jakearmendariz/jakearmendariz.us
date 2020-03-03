/**
 * For multiplying matriceis
 */
function numInput2() {
    var n, m;
    var a, b;
    n = document.getElementById("0Size").value;
    m = document.getElementById("0xSize").value;
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
            var s = "0" + i + "" + j;
            // console.log(s + ": hidden");
            document.getElementById(s).style.display = "none";
        }
    }
    //console.log("Adding slots");
    for (var i = 0; i < a; i++) {
        for (var j = 0; j < b; j++) {
            var s = "0" + i + "" + j;
            // console.log(s + ": displayed");
            document.getElementById(s).style.display = "inLine";
        }
    }


}



/**
 * Clears the matrix back to starting value
 */
function clearMatrix2() {
    for (var i = 0; i < 6; i++) {
        for (var j = 0; j < 6; j++) {
            var s = "0" + i + "" + j;
            // console.log(s + ": hidden");
            document.getElementById(s).value = "";
        }
    }
}

function multiply() {
    console.log("Multiplying matricies");
    //n and m are the dimenstions of matrix A and x and y are dimensions of matrix B
    var n, m, x, y;
    n = document.getElementById("Size").value;
    m = document.getElementById("xSize").value;
    if (n == "2") {
        n = 2;
    } else if (n == "3") {
        n = 3;
    } else if (n == "4") {
        n = 4;
    } else if (n == "5") {
        n = 5;
    } else {
        n = 6;
    }

    if (m == "x2") {
        m = 2;
    } else if (m == "x3") {
        m = 3;
    } else if (m == "x4") {
        m = 4;
    } else if (m == "x5") {
        m = 5;
    } else {
        m = 6;
    }

    x = document.getElementById("0Size").value;
    y = document.getElementById("0xSize").value;
    if (x == "2") {
        x = 2;
    } else if (x == "3") {
        x = 3;
    } else if (x == "4") {
        x = 4;
    } else if (x == "5") {
        x = 5;
    } else {
        x = 6;
    }

    if (y == "x2") {
        y = 2;
    } else if (y == "x3") {
        y = 3;
    } else if (y == "x4") {
        y = 4;
    } else if (y == "x5") {
        y = 5;
    } else {
        y = 6;
    }


    var a = [
        [],
        [],
        [],
        [],
        [],
        []
    ];
    var b = [
        [],
        [],
        [],
        [],
        [],
        []
    ];
    //C is the product, its size will be n, y
    var c = [
        [],
        [],
        [],
        [],
        [],
        []
    ];

    if (m != x) {
        document.getElementById("answer").innerHTML = "DNE, the dimensions do not match. The width of A must equal length of B";
        return;
    }
    for (var i = 0; i < n; i++) {
        for (var j = 0; j < m; j++) {
            var s = "" + i + "" + j;
            var t = "0" + i + "" + j;
            a[i][j] = parseInt(document.getElementById(s).value);
        }
    }

    for (var i = 0; i < x; i++) {
        for (var j = 0; j < y; j++) {
            var s = "" + i + "" + j;
            var t = "0" + i + "" + j;
            b[i][j] = parseInt(document.getElementById(t).value);
        }
    }
    //Resulting matrix is size n by y
    //Remmember m and x are the same size
    for (var i = 0; i < n; i++) {
        for (var j = 0; j < y; j++) {
            var sum = 0;
            for (var k = 0; k < m; k++) {
                sum += a[i][k] * b[k][j];
                console.log(a[i][k] + "*" + b[k][j] + "+");
            }
            c[i][j] = sum;
            console.log("\t");
        }
        console.log("\n");
    }
    var s = "";
    for (var i = 0; i < n; i++) {
        for (var j = 0; j < y; j++) {
            s += "  " + c[i][j];
        }
        s += "\n";
    }

    document.getElementById("answer").innerHTML = s;




}