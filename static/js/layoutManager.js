// bodyTemplate = {'before': data, 'after':data}

class Table{

    constructor(elementId, data, header, rowTemplate){
        this.elementId = elementId;
        this.data = data;
        this.header = header;
        this.rowTemplate = rowTemplate;
        this.rows = []

    }

    showTable(){
        var table='<thead class="thead-light"><tr>';                       
        
        for(var key in header){
            table += `<th scope="col">${header[key]}</th>`
        }

        table += '</tr></thead>';
        table += '<tbody>'

        for(var key in data){

            let row = data[key]
            table += '<tr>'

            for(key in this.rowTemplate){

                col_name = this.rowTemplate[key]
                table += `<td>${row[col_name]}</td>`

            }
            table +='</tr>'
        }
        table+= '</tbody>';
        document.getElementById(self.elementId).innerHTML=table;

    }
}