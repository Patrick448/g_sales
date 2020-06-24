/*$(document).ready(
    function(){
        10,
        $("#btnAdd").click(function(){
        });
    }
);
*/


var list = [
            {"id":0,"desc": "Banana", "quant":"10"},
            {"id":1, "desc": "Maçã", "quant":"5"},
            {"id":2, "desc": "Uva", "quant":"15"}
        ];

var ids = 3;


function Item(id, desc, quant){

    this.id = id;
    this.desc = desc;
    this.quant = quant;

}

 

function addItem(){

    var produto = $('#product').val();
    var quantidade = $('#quant').val();
    list.unshift({"id": ids , "desc": produto, "quant": quantidade});
    ids ++;

    $('#product').val("");
    $('#quant').val("");
  //  alert(produto+quantidade);
    setList(list);
}


function setList(list){
    
     var table='<thead class="thead-light"><tr><th scope="col">Produto</th><th scope="col">Quantidade</th><th scope="col">Ação</th></tr>'

    for(var key in list){
        table += '<tr id="tr'+list[key].id+'"><td>'+ list[key].desc+'</td><td>'+list[key].quant+'</td><td><Input id="edit-button" type="image" title="Editar" class="imgActionBtn" src="/imgs/edit.svg" height="30" width="30" onclick="editItem()"/><Input id="delete-button" type="image" title="Apagar" class="imgActionBtn" src="/imgs/delete.svg" height="30" width="30" onclick="deleteItem('+key+')"/></td></tr>'
    }

    table+= '</tbody>'
    document.getElementById("productsTable").innerHTML=table;

} 

function editItem(id){

    
}


//deleta item da lista
function deleteItem(id){

    //implementar: apagar item da lista json
    list.splice(id, 1);
    $('#tr'+ id).hide("fast");
}

setList(list);