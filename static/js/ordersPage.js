let startFilterButton = document.getElementById("filter-start-button");
startFilterButton.onclick = get_orders_by_date_filter;

let startDatePicker = document.getElementById("filter-start-date");
let endDatePicker = document.getElementById("filter-end-date");

startDatePicker.valueAsNumber = new Date();
endDatePicker.valueAsNumber = new Date();

let modalSpan = document.getElementsByClassName("close")[0];
let modal = document.getElementById("myModal");
let modalFinish = document.getElementById("modal_concluir");
let modalTitle = document.getElementById("order-modal-title");

let orderList;
let numPedidos = localStorage.storedItems;

// When the user clicks on <span> (x), close the modal
modalSpan.onclick = function() {
  modal.style.display = "none";
}



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

        tableOrders += `<tr id=order-page-${pedido.order_id} data-timestamp="${pedido.timeStamp}" onClick="orderInfo(${pedido.order_id})">
                            <td>${pedido.order_id}</td>
                            <td>${formattedDate(pedido.timeStamp)}</td>
                            <td>R$ ${formatMoney(pedido.total)}</td>
                        </tr>`;
  
    }
  
    tableOrders+= '</tbody>';
  
    document.getElementById("table-orders-page").innerHTML=tableOrders;

}


//Old version, keep in case the new one goes wrong
function startFilter(){

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

/*
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

}*/




function orderInfo(id){

    let elementInList = orderList.find(function(item){
      return item.order_id == id;
    });


    setOrderModal(elementInList)
}

function setOrderModal(order){

  let totalValue = 0;
  modal.style.display = "block";


  modalTitle.innerHTML = formattedDate(order.timeStamp)
  var modalTable=`<table class="table table-hover">
                    <thead class="thead-light">
                      <tr>
                        <th scope="col">Produto</th>
                        <th scope="col">Quantidade</th>
                        <th scope="col">Preço</th>
                        <th scope="col">Subtotal</th>
                      </tr>
                    </thead>`;


    for(var key in order.items){
        modalTable += `<tr id=order${order.items[key].id}>
                    <td>${order.items[key].name}</td>
                    <td>${formatNumber(order.items[key].quant)}</td>
                    <td>${formatMoney(order.items[key].price)}</td>
                    <td>${formatMoney(order.items[key].price*order.items[key].quant)}</td>
                  </tr>`;

    totalValue += order.items[key].price*order.items[key].quant;

    }


  modalTable+= `  </tbody>
                </table>`;

  document.getElementById("modal_body").innerHTML=modalTable;

 document.getElementById("modal_total").innerHTML= "R$ "+formatMoney(totalValue);

}


function get_orders_by_date_filter(){

    let dayInMillis = 86400000;
    let timeFrom=startDatePicker.valueAsNumber
    let timeTo=endDatePicker.valueAsNumber+dayInMillis

     $.ajax({
        type:"GET",
        url:`/get_orders/by_date/${timeFrom}+${timeTo}`,
        success: function(data){
            parsed_data = JSON.parse(data)
            orderList = parsed_data
            setOrdersTable()

        }
    });
}


setOrdersTable();

