//*************************************************************************/
//TO-DO: Create PRODUCT class  (id, desc, price)
//       Create ORDER object (items' references lists, quant, add(), remove())
//       Create AVAILABLE object (items list, gets)
//       Study javascript classes and objects 
//
//Then add methods to access the information more easily
//
//Always update this list
//*************************************************************************/


var list =[]
var listOrder = [
   /* {"id":0,"desc": "Banana", "quant":"10", "price":"2.00"},
    {"id":1, "desc": "Maçã", "quant":"5", "price":"2.00"},
    {"id":2, "desc": "Uva", "quant":"15", "price":"2.00"}*/

  ];

//MODAL ELEMENTS
var finishBtn = document.getElementById("finish_btn"); 
var modal = document.getElementById("myModal");
var submitOrderBtn = document.getElementById("modal_concluir");
var modalSpan = document.getElementsByClassName("close")[0];


submitOrderBtn.onclick = function(){

submitOrder()
}
// When the user clicks the button, open the modal 
finishBtn.onclick = function() {
  modal.style.display = "block";
  postVerifyOrder(listOrder)
  setOrderModal();
}
// When the user clicks on <span> (x), close the modal
modalSpan.onclick = function() {
  modal.style.display = "none";
}
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}




/*
var list = [
    {"id":0,"desc": "Banana", "price":"20.00"},
    {"id":1, "desc": "Maçã", "price":"40.70"},
    {"id":2, "desc": "Manga", "price":"50.60"},
    {"id":3, "desc": "Laranja", "price":"25.00"},
    {"id":4, "desc": "Batata", "price":"60.00"},
    {"id":5, "desc": "Inhame", "price":"70.00"},
    {"id":6, "desc": "Beterraba", "price":"30.00"},
    {"id":7, "desc": "Cenoura", "price":"36.00"},
    {"id":8, "desc": "Alface", "price":"2.00"},
    {"id":9, "desc": "Couve", "price":"2.00"},
    {"id":10, "desc": "Agrião", "price":"2.20"},
];
*/


$.get(
    "/pedido/get-list",
    function(data) {
       //alert('page content: ' + JSON.stringify(data));
       parsed_data = JSON.parse(data)
       list = parsed_data
       /*
       for(key in parsed_data){
           list.push(data[key])
       }*/
       setAvailableList();
    }
);



    var ids = 3;

function Item(id, desc, quant){

  this.id = id;
  this.desc = desc;
  this.quant = quant;

}

function postSaveOrder(order){
    payload = {'order':order,
        'cookies': 0,
        'user': 0}

    $.ajax({
        type:"POST",
        url:'/save-order',
        data: JSON.stringify(payload),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data){
            alert(data)
        }
    });

}

function postVerifyOrder(order){
    payload = {'order':order,
        'cookies': 0,
        'user': 0}

    $.ajax({
        type:"POST",
        url:'/verify-order',
        data: JSON.stringify(payload),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data){
            alert(data)
        }
    });

}

function addItem(){

    var produto = $('#product').val();
    var quantidade = $('#quant').val();
    list.unshift({"id": ids , "desc": produto, "quant": quantidade});
    ids ++;

    $('#product').val("");
    $('#quant').val("");
    setAvailableList();
}


function setAvailableList(){

  var tableAvailable=`<thead class="thead-light">
                        <tr>
                          <th scope="col">Produto</th>
                          <th scope="col">Preço</th>
                          <th scope="col"></th>
                        </tr>
                      </thead>`;

  for(var key in list){

    tableAvailable += `<tr id=avail${list[key].id} data-id=${key} onClick="/*addToOrder(${key})*/">
                        <td>${list[key].desc}</td>
                        <td>${formatMoney(list[key].price)}</td>
                        <td id="input${list[key].id}">
                          <button class="btn btn-light" onClick="addToOrder(${list[key].id}); return false;"> Add </button>
                      </tr>`;

  }
  tableAvailable+= '</tbody>';
  document.getElementById("table-available").innerHTML=tableAvailable;
}

function buttonToTextbox(id){
}
/*function textboxToButton(id){


  $("#" + id).keyup(function(event) {
    if (event.keyCode === 13) {
       
      var buttonHtml =  `<input type="submit" class="btn btn-light" value="Add" onClick="buttonToTextbox(${id})"/>`;
      document.getElementById(id).innerHTML=buttonHtml;

    }
  });


}*/


function setOderList(){

  let totalValue = 0;

  var tableOrder=`<thead class="thead-light">
                    <tr>
                      <th scope="col">Produto</th>
                      <th scope="col">Quantidade</th> 
                      <th scope="col">Preço</th>
                      <th scope="col">Subtotal</th>
                      <th scope="col"></th>
                    </tr>
                  </thead>`;

  for(var key in listOrder){

    //gets the element in the array "list" with the id that's stored in "listOrder"
    let elementInList = list.find(function(item){
      return item.id == listOrder[key].id;
    }); 
    

    tableOrder += `<tr id=order${elementInList.id}>
                      <td>${elementInList.desc}</td>
                      <td>${formatNumber(listOrder[key].quant)}</td>
                      <td>${formatMoney(elementInList.price)}</td>
                      <td>${formatMoney(elementInList.price*listOrder[key].quant)}</td>
                      <td><button class="btn btn-light" onClick="deleteItem(${elementInList.id})">x</button></td>
                    </tr>`;

    totalValue += elementInList.price*listOrder[key].quant;
  }

  tableOrder+= '</tbody>';

  document.getElementById("order_table").innerHTML=tableOrder;
  document.getElementById("total_value").innerHTML= "R$ "+ formatMoney(totalValue);


} 

function setOrderModal(){

  let totalValue = 0;

  var modalTable=`<table class="table table-hover">
                    <thead class="thead-light">
                      <tr>
                        <th scope="col">Produto</th>
                        <th scope="col">Quantidade</th> 
                        <th scope="col">Preço</th>
                        <th scope="col">Subtotal</th>
                      </tr>
                    </thead>`;

  for(var key in listOrder){
    let elementInList = list.find(function(item){
      return item.id == listOrder[key].id;
    });

    modalTable += `<tr id=order${elementInList.id}>
                    <td>${elementInList.desc}</td>
                    <td>${formatNumber(listOrder[key].quant)}</td>
                    <td>${formatMoney(elementInList.price)}</td>
                    <td>${formatMoney(elementInList.price*listOrder[key].quant)}</td>
                  </tr>`;

    totalValue += elementInList.price*listOrder[key].quant;
  }


  modalTable+= `  </tbody>
                </table>`;

  document.getElementById("modal_body").innerHTML=modalTable;

 document.getElementById("modal_total").innerHTML= "R$ "+formatMoney(totalValue);

} 


function editItem(id){

}

function searchList() {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("search-available");
    filter = input.value.toUpperCase(); 
    table = document.getElementById("table-available");
    tr = table.getElementsByTagName("tr");
  
    console.log(tr);

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[0];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }


 /* $(document).ready(function(){

    $('#table-available').find('tr').click( function(){

        listOrder.push(list[$(this).attr("data-id")]);
        alert('You clicked row ' + $(this).attr("data-id"));
        //só funciona a primeira vez quando tem esse comando:
        //acho que é porque ele redefine a lista sem o evento do clique
        setAvailableList();

      
    });
  
  }); */
  
function addToOrder(key){


  var quant = prompt("Quantidade");
  var quant = Number(quant.toString().replace(",", "."));

  if(validNumber(quant)){

    listOrder.push({"id": list[key].id, "quant": quant})
    setOderList();

  }
  else{

    alert("Valor inválido!\nDigite apenas números, usando vírgula para separar as casas decimais.");

  }
 
} 


//deleta item da lista
function deleteItem(id){
   
  var removeIndex = listOrder.map(function(item) { return item.id; })
  .indexOf(id);
  
  console.log(`Apagar item ${removeIndex} id: ${id}`);

  listOrder.splice(removeIndex, 1);
  $('#order'+ id).hide("fast");
}


function submitOrder(){

  localStorage.storedItems = (localStorage.storedItems===undefined) ? "0" : localStorage.storedItems;
  let totalValue = 0;
  let finalList = [];
  let orderInfo;


  for(var key in listOrder){

    let elementInList = list.find(function(item){
      return item.id == listOrder[key].id;
    }); 
    
    finalList.push({"id": elementInList.id, "desc": elementInList.desc, "quant": listOrder[key].quant, "price":elementInList.price })
    totalValue += elementInList.price*listOrder[key].quant;
  }

  orderInfo = {
    timeStamp: new Date().getTime(),
    items: finalList,
    total:totalValue
  }


  localStorage.setItem("ordersList" + localStorage.storedItems, JSON.stringify(orderInfo));
  localStorage.storedItems = Number(localStorage.storedItems) + 1;

  postSaveOrder(orderInfo)

}



setAvailableList();
setOderList();