let startFilterButton = document.getElementById("filter-start-button");
startFilterButton.onclick = startFilter;

let startDatePicker = document.getElementById("filter-start-date");
let endDatePicker = document.getElementById("filter-end-date");

startDatePicker.valueAsNumber = new Date();
endDatePicker.valueAsNumber = new Date();

let orderList;
let numPedidos = localStorage.storedItems;

$.get(
    "/get-all-orders",
    function(data) {
       parsed_data = JSON.parse(data)
       orderList = parsed_data
       setOrdersTable()
    }
);

function setOrdersTable(){


    let tableOrders=`<thead class="thead-light">
                        <tr>
                        <th scope="col">Pedido</th>
                        <th scope="col">Data</th>
                        <th scope="col">Valor</th>
                        </tr>
                        </thead>`;


    for(key in orderList){

        let pedido = orderList[key];

        tableOrders += `<tr id=order-page-${key} data-timestamp="${pedido.timeStamp} onclick="orderInfo(${key})">
                            <td>${key}</td>
                            <td>${formattedDate(pedido.timeStamp)}</td>
                            <td>R$ ${formatMoney(pedido.total)}</td>
                        </tr>`;
  
    }
  
    tableOrders+= '</tbody>';
  
    document.getElementById("table-orders-page").innerHTML=tableOrders;

}


//Old version, keep in case the new one goes wrong
function startFilter2(){

    console.log("START FILTER");

    let startDate, endDate, table, tr, td, i, timeStamp;
    startDate = document.getElementById("filter-start-date").valueAsNumber;
    endDate = document.getElementById("filter-end-date").valueAsNumber;
    table = document.getElementById("table-orders-page");
    tr = table.getElementsByTagName("tr");
    
    let dayInMillis = 86400000;
    console.log(tr);

    for(i=1; i<tr.length; i++){
         
        timeStamp = Number(tr[i].dataset.timestamp);

        if(timeStamp >= startDate && timeStamp < endDate + dayInMillis){
           tr[i].style.display = "";
             
        }else{
            tr[i].style.display = "none";
          
        }
     }
}


function startFilter(){

    let startDate, endDate, table;
    startDate = document.getElementById("filter-start-date").valueAsNumber;
    endDate = document.getElementById("filter-end-date").valueAsNumber;
    table = document.getElementById("table-orders-page");

    let dayInMillis = 86400000;

    filterElements(1, table, "tr", function(element){
        let timeStamp = Number(element.dataset.timestamp);
        return (timeStamp >= startDate && timeStamp < endDate + dayInMillis);
    });

}

function orderInfo(id){





}




setOrdersTable();

