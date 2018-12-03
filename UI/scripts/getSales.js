function getSales(){
    const name = localStorage.getItem('username')
    const newtoken = localStorage.getItem('token');
    const errorMessage = document.querySelector("span.errors");
    const urlgetsalebyatttendant = 'https://store-manager-ap1.herokuapp.com/api/v2/sales/'
    try{
        fetch(urlgetsalebyatttendant + name,{
            method:'GET',
            headers: {
                'Content-type': 'application/json',
                'Authorization': `Bearer ${newtoken}`
            },
        }).then((response) => {
            // console.log(response.text())
            if (response.ok){
                return response.text()
                .then((data) => {
                    const salesData = JSON.parse(data)
                    const sale = salesData["sale"]
                    // console.log(sale)
                         
                    var content = '';

                    //clear table body data
                    const saleTableBody = document.querySelector("#saleTable > tbody")
                    while (saleTableBody.firstChild){
                        saleTableBody.removeChild(saleTableBody.firstChild)
                    }

                    //get each row in json
                    sale.forEach((row) => {
                        // console.log(row)
                        const saleid = row["sale_id"]
                        const usname = row["user_name"]
                        const pid = row["product_id"]
                        const total = row["total"]
                        const qtyy = row["quantity"]
                        const dcre = row["date_created"]        
                            
                        content +='<tr>';
                        content += '<td>' + saleid + '</td>';
                        content += '<td>' + usname + '</td>';
                        content += '<td>' + pid + '</td>';
                        content += '<td>' + qtyy + '</td>';
                        content += '<td>' + total + '</td>';
                        content += '<td>' + dcre + '</td>';
                        content += '</tr>';
                    })      
                        //populate table                 
                    $('#saleTable').append(content)
                })      
              
            }else if(response.status == 404){
                errorMessage.innerText= response.statusText + "-" + "no sales found"
            }else if(response.status == 401){
                errorMessage.innerText = response.statusText + "-" + "You are unauthorized to perform this action"
            }else{
                errorMessage.innerText = response.status + "-" + response.statusText
            }                 
        })
    }catch (error){
        console.log(error)
    }
    
}
function getSale(){
    const attname = document.getElementById("saleAtt").value;
    const newtoken = localStorage.getItem('token');
    const errorMessage = document.querySelector("span.errors");
    const url = 'https://store-manager-ap1.herokuapp.com/api/v2/sales/'
    try{
        if(attname == ""){
            errorMessage.innerText = "Please enter attendants name"
            document.getElementById("saleAtt").focus()
            document.getElementById("saleAtt").value = "";
        }else if(!isNaN(attname)){
            errorMessage.innerText = "Attendant name is not number value"
            document.getElementById("saleAtt").focus()
            document.getElementById("saleAtt").value = "";
        }else{
            fetch(url + attname,{
            method:'GET',
            headers: {
                'Content-type': 'application/json',
                'Authorization': `Bearer ${newtoken}`
            },
            }).then((response) => {
                // console.log(response.text())
                if (response.ok){
                    return response.text()
                    .then((data) => {
                        const salesData = JSON.parse(data)
                        const sale = salesData["sale"]
                        // console.log(sale)
                            
                        var content = '';

                        //clear table body data
                        const saleTableBody = document.querySelector("#saleTable > tbody")
                        while (saleTableBody.firstChild){
                            saleTableBody.removeChild(saleTableBody.firstChild)
                        }

                        //get each row in json
                        sale.forEach((row) => {
                            // console.log(row)
                            const saleid = row["sale_id"]
                            const usname = row["user_name"]
                            const pid = row["product_id"]
                            const total = row["total"]
                            const qtyy = row["quantity"]
                            const dcre = row["date_created"]        
                                
                            content +='<tr>';
                            content += '<td>' + saleid + '</td>';
                            content += '<td>' + usname + '</td>';
                            content += '<td>' + pid + '</td>';
                            content += '<td>' + qtyy + '</td>';
                            content += '<td>' + total + '</td>';
                            content += '<td>' + dcre + '</td>';
                            content += '</tr>';
                        })     
                        //populate table                 
                        $('#saleTable').append(content)
                    })      
                
                }else if(response.status == 404){
                    errorMessage.innerText= response.statusText + "-" + "no sales found"
                }else if(response.status == 401){
                    errorMessage.innerText = response.statusText + "-" + "You are unauthorized to perform this action"
                }else{
                    errorMessage.innerText= response.status + "-" + response.statusText
                }                 
            })
        }
        
    }catch (error){
        console.log(error)
    }
    
}
function displaySalesAtt(){
    // clear table data
    const saleTableBody = document.querySelector("#saleTable > tbody")
    while (saleTableBody.firstChild){
        saleTableBody.removeChild(saleTableBody.firstChild)
    }

    // display text field
    const saleTableChecked = document.getElementById("radio-two")
    formwrapped.style.display = saleTableChecked.checked ? "block" : "none"
}
function allSales(){
    formwrapped.style.display = "none"
    const errorMessage = document.querySelector("span.errors");
    const newtoken = localStorage.getItem('token');
    const urlallsales = 'https://store-manager-ap1.herokuapp.com/api/v2/sales'
    // console.log(newtoken)

    try{
        fetch(urlallsales,{
            method:'GET',
            headers: {
                'Content-type': 'application/json',
                'Authorization': `Bearer ${newtoken}`
            },
        }).then((response) => {
            if (response.ok){
                return response.text()
                .then((data) => {
                    const salesData = JSON.parse(data)
                    const sales = salesData["sales"]
                    // console.log(sales)
                         
                    var content = '';

                    //clear table body data
                    const saleTableBody = document.querySelector("#saleTable > tbody")
                    while (saleTableBody.firstChild){
                        saleTableBody.removeChild(saleTableBody.firstChild)
                    }

                    //get each row in json
                    sales.forEach((row) => {
                        // console.log(row)
                        const saleid = row["sale_id"]
                        const usname = row["user_name"]
                        const pid = row["product_id"]
                        const total = row["total"]
                        const qtyy = row["quantity"]
                        const dcre = row["date_created"]        
                            
                        content +='<tr>';
                        content += '<td>' + saleid + '</td>';
                        content += '<td>' + usname + '</td>';
                        content += '<td>' + pid + '</td>';
                        content += '<td>' + qtyy + '</td>';
                        content += '<td>' + total + '</td>';
                        content += '<td>' + dcre + '</td>';
                        content += '</tr>';
                        })      
                        //populate table                 
                        $('#saleTable').append(content)
                })
            }else if(response.status == 404){
                errorMessage.innerText = response.statusText + "-" + "no sales found"
            }else if(response.status == 401){
                errorMessage.innerText = response.statusText + "-" + "You are unauthorized to perform this action"
            }else{
                errorMessage.innerText = response.status + "-" + response.statusText
            }                 
        })
    }catch (error){
        console.log(error)
    }
}
