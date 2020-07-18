const DISTANCE = 4
const PACE = 3
const TIME = 5
function timeToSeconds(arr){
    return arr[0] * 3600 + arr[1] + 60 + arr[2]
}
function sortTable(n) {
  console.log("sort table")
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("table");
  switching = true;
  //Set the sorting direction to ascending:
  dir = "desc"; 
  /*Make a loop that will continue until
  no switching has been done:*/
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /*check if the two rows should switch place,
      based on the direction, asc or desc:*/
      let xValue, yValue;
      let xStr = x.innerHTML.toLowerCase()
      let yStr = y.innerHTML.toLowerCase()
      if(n==DISTANCE){
        xValue = parseFloat(xStr)
        yValue = parseFloat(yStr)
      }else if(n==PACE){
        xValue = parseFloat(xStr.replace(":", "."))
        yValue = parseFloat(yStr.replace(":", "."))
      }
      else if(n==TIME){
        let xArr = xStr.match(/\d+/g).map(Number);
        let yArr = yStr.match(/\d+/g).map(Number);     
        xValue = timeToSeconds(xArr)
        yValue = timeToSeconds(yArr)
      }
      else{
          xValue = xStr
          yValue = yStr
      }
      if (dir == "asc") {
        if (xValue > yValue) {
          //if so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      } else if (dir == "desc") {
        if (xValue < yValue) {
          //if so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /*If a switch has been marked, make the switch
      and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      //Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /*If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again.*/
      if (switchcount == 0 && dir == "desc") {
        dir = "asc";
        switching = true;
      }
    }
  }
}




let dir = 0
function quicksort(n) {
    console.log("quicksort")
    var table, rows, i, x, y;
    table = document.getElementById("table");
    rows = table.rows

    let sortedArr = []
    for (i = 1; i < rows.length; i++) {
        sortedArr.push([i, convert(rows[i], n), rows[i]])
        // console.log(i + ":"+ sortedArr[i-1][1])
    }
    if(dir == 0){
        quickSort(sortedArr, 0, sortedArr.length-1)
        dir = 1
    }else{
        quickSortDesc(sortedArr, 0, sortedArr.length-1)
        dir = 0
    }

    // rows[1].parentNode.insertBefore(sortedArr[4][2], rows[1]);
    for (i = 1; i < rows.length; i++) {
        rows[i].parentNode.insertBefore(sortedArr[i-1][2], rows[i]);
        // console.log(i + ":"+ sortedArr[i-1][1])
    }
}

function quickSort(arr, low, high)
{
    if (low < high)
    {
        /* pi is partitioning index, arr[pi] is now
           at right place */
        let pi = partition(arr, low, high);

        quickSort(arr, low, pi - 1);  // Before pi
        quickSort(arr, pi + 1, high); // After pi
    }
}

function partition (arr, low, high)
{
    // pivot (Element to be placed at right position)
    let pivot = arr[high][1];
    // console.log("low:" + low + " high:" + high)
    // console.log("pivot:" + pivot)
 
    let i = (low - 1)  // Index of smaller element

    for (let j = low; j <= high- 1; j++)
    {
        // If current element is smaller than the pivot
        if (arr[j][1] < pivot)
        {
            i++;    // increment index of smaller element
            // console.log("i:" + i + " j: " + j)
            // console.log("swapping:" + arr[i][1] + " with " + arr[j][1])
            if(i != j)
                swap(arr, i ,j);
            // console.log("complete:" + arr[i][1] + " with " + arr[j][1])
        }
    }
    i += 1
    // console.log("i:" + i + " high: " + high)
    if(i < 0){
        // console.log('i < 0, returning')
        return
    }
    // console.log("swapping:" + arr[i][1] + " with " + arr[high][1])
    swap(arr, i, high)
    // console.log("complete:" + arr[i][1] + " with " + arr[high][1])
    return i
}


function quickSortDesc(arr, low, high)
{
    if (low < high)
    {
        /* pi is partitioning index, arr[pi] is now
           at right place */
        let pi = partitionDesc(arr, low, high);

        quickSortDesc(arr, low, pi - 1);  // Before pi
        quickSortDesc(arr, pi + 1, high); // After pi
    }
}

function partitionDesc (arr, low, high)
{
    // pivot (Element to be placed at right position)
    let pivot = arr[high][1];
    // console.log("low:" + low + " high:" + high)
    // console.log("pivot:" + pivot)
 
    let i = (low - 1)  // Index of smaller element

    for (let j = low; j <= high- 1; j++)
    {
        // If current element is smaller than the pivot
        if (arr[j][1] > pivot)
        {
            i++;    // increment index of smaller element
            // console.log("i:" + i + " j: " + j)
            // console.log("swapping:" + arr[i][1] + " with " + arr[j][1])
            if(i != j)
                swap(arr, i ,j);
            // console.log("complete:" + arr[i][1] + " with " + arr[j][1])
        }
    }
    i += 1
    // console.log("i:" + i + " high: " + high)
    if(i < 0){
        // console.log('i < 0, returning')
        return
    }
    // console.log("swapping:" + arr[i][1] + " with " + arr[high][1])
    swap(arr, i, high)
    // console.log("complete:" + arr[i][1] + " with " + arr[high][1])
    return i
}

  

function convert(element, n){
    let tag = element.getElementsByTagName("TD")[n];
    let str = tag.innerHTML.toLowerCase()
    if(n==DISTANCE){
        return parseFloat(str)
    }else if(n==PACE){
        return parseFloat(str.replace(":", "."))
    }
    else if(n==TIME){
        let arr = str.match(/\d+/g).map(Number);
        return timeToSeconds(arr)
    }
    return str
}

function swap(array, i, j){
    let temp = array[i]
    array[i] = array[j]
    array[j] = temp
}

//  when is n * n < 2n + nlog(n)