todayTab = function(){

let startFilterButton = document.getElementById("hoje-filter-start-button");
startFilterButton.onclick = filterOrders;

let orderNumInput = document.getElementById("hoje-filter-order-num");
let customerNameInput = document.getElementById("hoje-filter-customer");

let modalSpan = document.getElementById("today-modal-close");
let modal = document.getElementById("hoje-order-modal");
let modalFinish = document.getElementById("hoje-modal-concluir");
let modalTitle = document.getElementById("hoje-order-modal-title");
let modalBody = document.getElementById("hoje-modal-body");
let modalTotal =document.getElementById("hoje-modal-total");

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

        tableOrders += `<tr id=order-page-${pedido.id} data-timestamp="${pedido.timeStamp}" onClick="todayTab.orderInfo(${pedido.id})">    
                            <td>${pedido.id}</td>
                            <td>${pedido.user_name}</td>
                            <td>${formattedDate(pedido.timeStamp)}</td>
                            <td>R$ ${formatMoney(pedido.total)}</td>
                        </tr>`;
  
    }
  
    tableOrders+= '</tbody>';
    document.getElementById("hoje-table").innerHTML=tableOrders;

}

this.orderInfo = function(id){

    let elementInList = orderList.find(function(item){
      return item.id == id;
    });

    setOrderModal(elementInList, modalBody, modalTotal)
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

  document.getElementById("hoje-modal-body").innerHTML=modalTable;
  document.getElementById("hoje-modal-total").innerHTML= "R$ "+formatMoney(totalValue);

}


function filterOrders(){
  let dayInMillis = 86400000;
  let timeFrom=startDatePicker.valueAsNumber
  let timeTo=endDatePicker.valueAsNumber+dayInMillis
  let customerName = customerNameInput.value
  let orderNum = orderNumInput.value

   $.ajax({
      type:"GET",
      url:`/admin_get_orders_today/?time_from=${timeFrom}&time_to=${timeTo}&name=${customerName}&num=${orderNum}`,
      success: function(data){
          parsed_data = JSON.parse(data)
          orderList = parsed_data
          setOrdersTable()

      }
  });

}

function getTodaysOrders(){

    $.ajax({
        type:"GET",
        url:`/admin_get_orders_today`,
        success: function(data){
            parsed_data = JSON.parse(data)
            orderList = parsed_data
            setOrdersTable()
  
        }
    });

}


setOrdersTable();
getTodaysOrders();
}

todayTab = new todayTab();

