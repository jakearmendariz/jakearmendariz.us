function searchBar() {
    var s = document.getElementById("searchbar").value;
    s = s.toLowerCase();
    clearInfo()
    if (s.includes("everything") || s.includes("intro")) {
        console.log("display intro");
        document.getElementById("info").style.display = "block";
        document.getElementById("matricies").style.display = "block";
        document.getElementById("vectors").style.display = "block";
        document.getElementById("reduce").style.display = "block";
        document.getElementById("identity").style.display = "block";
        document.getElementById("freeVar").style.display = "block";
        document.getElementById("dependence").style.display = "block";
        document.getElementById("reduce").style.display = "block";
    } else if (s.includes("matricies") || s.includes("matrix") || s.includes("multiplication")) {
        console.log("Displaying matricies");
        document.getElementById("matricies").style.display = "block";
        document.getElementById("identity").style.display = "block";
    } else if (s.includes("vector") || s.includes("dot product")) {
        console.log("Displaying vectors");
        document.getElementById("vectors").style.display = "block";
    } else if (s.includes("identity") || s.includes("indenitt")) {
        console.log("Displaying identity");
        document.getElementById("identity").style.display = "block";
    } else if (s.includes("clear")) {
        console.log("clearing information");
        clearInfo()
    } else if (s === "") {

    } else if (s.includes("free") || s.includes("general")) {
        document.getElementById("freeVar").style.display = "block";
    } else if (s == "depen" || s == "rref meaning") {
        document.getElementById("dependence").style.display = "block";
    } else if (s.includes("rref")) {
        document.getElementById("reduce").style.display = "block";
        openR();
    } else if (s.includes("det")) {
        openD();
    } else if (s.includes("inverse")) {
        document.getElementById("inverse").style.display = "block";
    } else if (s.includes("coordinant")) {
        document.getElementById("coordinant").style.display = "block";
    } else if (s.includes("basis")) {
        document.getElementById("basis").style.display = "block";
    } else if (s.includes("row space") || s.includes("column space")) {
        document.getElementById("rowcolspace").style.display = "block";
    } else if (s.includes("range")) {
        document.getElementById("Range").style.display = "block";
    } else if (s.includes("bijective")) {
        document.getElementById("bijective").style.display = "block";
    } else if (s.includes("surjective")) {
        document.getElementById("surjective").style.display = "block";
    } else if (s.includes("injective")) {
        document.getElementById("injective").style.display = "block";
    } else if (s.includes("eigen")) {
        document.getElementById("eigen").style.display = "block";
    } else if (s.includes("diagnol")) {
        document.getElementById("diagnol").style.display = "block";
    } else {
        document.getElementById("help").style.display = "block";
    }


}

function searchE(ele) {
    if (event.key === 'Enter') {
        var s = document.getElementById("searchbar").value;
        s = s.toLowerCase();
        clearInfo()
        if (s.includes("everything") || s.includes("intro")) {
            console.log("display intro");
            document.getElementById("info").style.display = "block";
            document.getElementById("matricies").style.display = "block";
            document.getElementById("vectors").style.display = "block";
            document.getElementById("reduce").style.display = "block";
            document.getElementById("identity").style.display = "block";
            document.getElementById("freeVar").style.display = "block";
            document.getElementById("dependence").style.display = "block";
            document.getElementById("reduce").style.display = "block";
        } else if (s.includes("matricies") || s.includes("matrix") || s.includes("multiplication")) {
            console.log("Displaying matricies");
            document.getElementById("matricies").style.display = "block";
            document.getElementById("identity").style.display = "block";
        } else if (s.includes("vector") || s.includes("dot product")) {
            console.log("Displaying vectors");
            document.getElementById("vectors").style.display = "block";
        } else if (s.includes("identity") || s.includes("indenitt")) {
            console.log("Displaying identity");
            document.getElementById("identity").style.display = "block";
        } else if (s.includes("clear")) {
            console.log("clearing information");
            clearInfo()
        } else if (s === "") {

        } else if (s.includes("free") || s.includes("general")) {
            document.getElementById("freeVar").style.display = "block";
        } else if (s == "depen" || s == "rref meaning") {
            document.getElementById("dependence").style.display = "block";
        } else if (s.includes("rref")) {
            document.getElementById("reduce").style.display = "block";
            openR();
        } else if (s.includes("det")) {
            openD();
        } else if (s.includes("inverse")) {
            document.getElementById("inverse").style.display = "block";
        } else if (s.includes("coordinant")) {
            document.getElementById("coordinant").style.display = "block";
        } else if (s.includes("basis")) {
            document.getElementById("basis").style.display = "block";
        } else if (s.includes("row space") || s.includes("column space")) {
            document.getElementById("rowcolspace").style.display = "block";
        } else if (s.includes("range")) {
            document.getElementById("range").style.display = "block";
        } else if (s.includes("bijective")) {
            document.getElementById("bijective").style.display = "block";
        } else if (s.includes("surjective")) {
            document.getElementById("surjective").style.display = "block";
        } else if (s.includes("injective")) {
            document.getElementById("injective").style.display = "block";
        } else if (s.includes("eigen")) {
            document.getElementById("eigen").style.display = "block";
        } else if (s.includes("diagnol")) {
            document.getElementById("diagnol").style.display = "block";
        } else {
            document.getElementById("help").style.display = "block";

        }
    }
}

function clearInfo() {
    document.getElementById("info").style.display = "none";
    document.getElementById("matricies").style.display = "none";
    document.getElementById("vectors").style.display = "none";
    document.getElementById("identity").style.display = "none";
    document.getElementById("help").style.display = "none";
    document.getElementById("reduce").style.display = "none";
    document.getElementById("dependence").style.display = "none";
    document.getElementById("freeVar").style.display = "none";
    document.getElementById("inverse").style.display = "none";
    document.getElementById("coordinant").style.display = "none";
    document.getElementById("basis").style.display = "none";
    document.getElementById("rowcolspace").style.display = "none";
    document.getElementById("Range").style.display = "none";
    document.getElementById("bijective").style.display = "none";
    document.getElementById("surjective").style.display = "none";
    document.getElementById("injective").style.display = "none";
    document.getElementById("eigen").style.display = "none";
    document.getElementById("diagnol").style.display = "none";
}


function intro() {
    document.getElementById("searchbar").value = 'intro';
    searchBar();
    document.getElementById("searchbar").value = '';
}

function vec() {
    document.getElementById("searchbar").value = 'vector';
    searchBar();
    document.getElementById("searchbar").value = '';
}


function mat() {
    document.getElementById("searchbar").value = 'matricies';
    searchBar();
    document.getElementById("searchbar").value = '';
}


function matMult() {
    document.getElementById("searchbar").value = 'matrix multiplication';
    searchBar();
    document.getElementById("searchbar").value = '';
}


function identity() {
    document.getElementById("searchbar").value = 'identity matrix';
    searchBar();
    document.getElementById("searchbar").value = '';
}


function free() {
    document.getElementById("searchbar").value = 'free variables and general solution';
    searchBar();
    document.getElementById("searchbar").value = '';
}


function basis() {
    document.getElementById("searchbar").value = 'basis';
    searchBar();
    document.getElementById("searchbar").value = '';
}


function row() {
    document.getElementById("searchbar").value = 'row space';
    searchBar();
    document.getElementById("searchbar").value = '';
}


function col() {
    document.getElementById("searchbar").value = 'column space';
    searchBar();
    document.getElementById("searchbar").value = '';
}


function range() {
    document.getElementById("searchbar").value = 'range';
    searchBar();
    document.getElementById("searchbar").value = '';
}

function bij() {
    document.getElementById("searchbar").value = 'bijective';
    searchBar();
    document.getElementById("searchbar").value = '';
}

function inj() {
    document.getElementById("searchbar").value = 'injective';
    searchBar();
    document.getElementById("searchbar").value = '';
}

function sur() {
    document.getElementById("searchbar").value = 'surjective';
    searchBar();
    document.getElementById("searchbar").value = '';
}

function sur() {
    document.getElementById("searchbar").value = 'eigen';
    searchBar();
    document.getElementById("searchbar").value = '';
}

function diag() {
    document.getElementById("searchbar").value = 'diagnolization';
    searchBar();
    document.getElementById("searchbar").value = '';
}