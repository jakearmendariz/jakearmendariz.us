const DISTANCE = 4
const PACE = 3
const TIME = 5
const ELEVATION = 6

function selectValue(){
    document.getElementById("selectbar").value = document.getElementById("selectValue").value
    let table = document.getElementById("table")
    let rows = table.rows;
    for(let i = 1; i < rows.length; i++){
        console.log("setting value:" + i)
        let value = rows[i].getElementsByTagName("TD")[0]
        value.innerHTML = i
    }
}

function timeToSeconds(arr){
    return arr[0] * 3600 + arr[1] * 60 + arr[2]
}
function sortTable(n) {
  console.log("sort table")
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("table");
  switching = true;
  //Set the sorting direction to ascending:
  dir = "desc"; 

  while (switching) {
    switching = false;
    rows = table.rows;

    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;

      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];

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
    console.log("loop");
  }
  console.log("SelectValue");
  selectValue();
}

function clearIcons(){
    for(let i = 0; i < 12; i++){
        let id = 'a' + i
        // document.getElementById(id).style.display = "none"
    }
    for(let i = 0; i < 7; i++){
        let id = 'b' + i
        document.getElementById(id).style.backgroundColor = "#fff"
    }
}


let dir = 0
function quicksort(n) {
    console.log("quicksort:" + n)
    clearIcons()
    var table, rows, i, x, y;
    table = document.getElementById("table");
    rows = table.rows

    let sortedArr = []
    for (i = 1; i < rows.length; i++) {
        sortedArr.push([i, convert(rows[i], n), rows[i]])
    }
    let id = "a"
    let b = "b" + n
    document.getElementById(b).style.backgroundColor = "#eee"
    if(dir == 0){
        id += 2*n + 1
        console.log(id)
        // document.getElementById(id).style.display = "block"
        quickSort(sortedArr, 0, sortedArr.length-1)
        dir = 1
    }else{
        id += 2*n
        console.log(id)
        // document.getElementById(id).style.display = "block"
        quickSortDesc(sortedArr, 0, sortedArr.length-1)
        dir = 0
    }

    for (i = 1; i < rows.length; i++) {
        rows[i].parentNode.insertBefore(sortedArr[i-1][2], rows[i]);
    }
    console.log("SelectValue");
    selectValue();
    
}

function quickSort(arr, low, high)
{
    if (low < high)
    {
        let pi = partition(arr, low, high);

        quickSort(arr, low, pi - 1);  // Before pi
        quickSort(arr, pi + 1, high); // After pi
    }
}

function partition (arr, low, high)
{
    // pivot (Element to be placed at right position)
    let pivot = arr[high][1];
 
    let i = (low - 1)  // Index of smaller element

    for (let j = low; j <= high- 1; j++)
    {
        // If current element is smaller than the pivot
        if (arr[j][1] < pivot)
        {
            i++;    // increment index of smaller element
            if(i != j)
                swap(arr, i ,j);
        }
    }
    i += 1
    if(i < 0){
        return
    }
    swap(arr, i, high)
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
 
    let i = (low - 1)  // Index of smaller element

    for (let j = low; j <= high- 1; j++)
    {
        // If current element is smaller than the pivot
        if (arr[j][1] > pivot)
        {
            i++;    // increment index of smaller element
            if(i != j)
                swap(arr, i ,j);
        }
    }
    i += 1
    if(i < 0){
        return
    }
    swap(arr, i, high)
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
    }else if(n==ELEVATION){
        console.log(str)
        return parseFloat(str.replace(",", ""))
    }
    return str
}

function swap(array, i, j){
    let temp = array[i]
    array[i] = array[j]
    array[j] = temp
}

//  when is n * n < 2n + nlog(n)