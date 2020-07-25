let startFilterButton = document.getElementById("filter-start-button");
startFilterButton.onclick = filterOrders; // get_orders_by_date_filter; 

let startDatePicker = document.getElementById("filter-start-date");
let endDatePicker = document.getElementById("filter-end-date");
let orderNumInput = document.getElementById("filter-order-num");
let customerNameInput = document.getElementById("filter-customer");



startDatePicker.valueAsNumber = new Date();
endDatePicker.valueAsNumber = new Date();

let modalSpan = document.getElementsByClassName("close")[0];
let modal = document.getElementById("order-modal");
let modalFinish = document.getElementById("modal_concluir");
let modalTitle = document.getElementById("order-modal-title");

let orderList;
let numPedidos = localStorage.storedItems;

// When the user clicks on <span> (x), close the modal
modalSpan.onclick = function() {
  modal.style.display = "none";
}



function setOrdersTable(){

    let tableOrders=`<thead class="thead-light">
                        <tr>
                        <th scope="col">Pedido</th>
                        <th scope="col">Cliente</th>
                        <th scope="col">Data</th>
                        <th scope="col">Valor</th>
                        </tr>
                        </thead><tbody>`;


    for(key in orderList){

        let pedido = orderList[key];

        tableOrders += `<tr id=order-page-${pedido.id} data-timestamp="${pedido.timeStamp}" onClick="orderInfo(${pedido.id})">    
                            <td>${pedido.id}</td>
                            <td>${pedido.user_name}</td>
                            <td>${formattedDate(pedido.timeStamp)}</td>
                            <td>R$ ${formatMoney(pedido.total)}</td>
                        </tr>`;
  
    }
  
    tableOrders+= '</tbody>';
    document.getElementById("hoje-table").innerHTML=tableOrders;

}

function orderInfo(id){

    let elementInList = orderList.find(function(item){
      return item.id == id;
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


function filterOrders(){
  let dayInMillis = 86400000;
  let timeFrom=startDatePicker.valueAsNumber
  let timeTo=endDatePicker.valueAsNumber+dayInMillis
  let customerName = customerNameInput.value
  let orderNum = orderNumInput.value

   $.ajax({
      type:"GET",
      url:`/admin_get_orders/filter/?time_from=${timeFrom}&time_to=${timeTo}&name=${customerName}&num=${orderNum}`,
      success: function(data){
          parsed_data = JSON.parse(data)
          orderList = parsed_data
          setOrdersTable()

      }
  });

}

function get_orders_by_date_filter(){

    let dayInMillis = 86400000;
    let timeFrom=startDatePicker.valueAsNumber
    let timeTo=endDatePicker.valueAsNumber+dayInMillis

     $.ajax({
        type:"GET",
        url:`/admin_get_orders/by_date/${timeFrom}+${timeTo}`,
        success: function(data){
            parsed_data = JSON.parse(data)
            orderList = parsed_data
            setOrdersTable()

        }
    });
}


setOrdersTable();

