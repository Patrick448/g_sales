function formattedDate(millis){

    let date = new Date(millis)
    let day = date.getDate().toString().padStart(2, '0');
    let month = (date.getMonth()+1).toString().padStart(2, '0');
    let year = date.getFullYear();

    let formatted = day + "/" + month + "/" + year;
    return formatted;
}


function formatMoney(num){

    num = Number(num).toFixed(2);
    let str = num.toString();
    str = str.replace(".", ",")
    var parts = str.split(",");

    if(parts[0].length > 3){
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    }

    return parts.join(",");

}


function formatNumber(num){

    let str = num.toString();

    if(str.match(/,./)){
        num = Number(num).toFixed(1);
    }
  
    str = str.replace(".", ",")
    var parts = str.split(",");

    if(parts[0].length > 3){
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    }

    return parts.join(",");

}


function validNumber(num){

    let resultString = num.toString().match(/[^0-9\.\,]/);
    
    return (resultString===null && num!=null && num!=0) ? true : false;
  
  }


  function filterElements(startFromIndex, container, elementTag, func){

    console.log("START FILTER");

    let elem, i;
    elem = container.getElementsByTagName(elementTag);

    console.log(elem);

    for(i=1; i<elem.length; i++){
         
        if(elem[i]){

            if(func(elem[i])){
                elem[i].style.display = "";
                
            }else{
                elem[i].style.display = "none";
            }
        }
    
    }
}