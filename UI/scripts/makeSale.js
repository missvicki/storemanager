function saleProduct(){
    const u_name = document.getElementById("usname").value;
    const p_id = document.getElementById("pdtid").value;
    const pd_qty = document.getElementById("pdtqty").value;
    const p_uprice = localStorage.getItem('p_price')
    const pp_qty = localStorage.getItem('p_qty')
    
    const errorMessage = document.querySelector("span.errors");    
    const newtoken = localStorage.getItem('token');
    const url = 'https://store-manager-ap1.herokuapp.com/api/v2/sales'
    const urlpdt = 'https://store-manager-ap1.herokuapp.com/api/v2/products'

    if(u_name == ""){
        errorMessage.innerText = "Your username is required, select pdt to make purchase"
        document.getElementById("usname").focus()
        document.getElementById("usname").value=""
        document.getElementById("pdtid").value=""
        document.getElementById("pdtqty").value=""
    }else if(p_id == ""){
        errorMessage.innerText = "Product id is required, select pdt to make purchase"
        document.getElementById("pdtid").focus()
        document.getElementById("usname").value=""
        document.getElementById("pdtid").value=""
        document.getElementById("pdtqty").value=""
    }else if(pd_qty == ""){
        errorMessage.innerText = "Product qty is required"
        document.getElementById("pdtqty").focus()
        document.getElementById("pdtqty").value=""
    }else if(p_uprice == ""){
        errorMessage.innerText = "Product price is required, select pdt to make purchase"
        document.getElementById("usname").value=""
        document.getElementById("pdtid").value=""
        document.getElementById("pdtqty").value=""
    }else if(pp_qty == ""){
        errorMessage.innerText ="Product qty is required, select pdt to make purchase"
        document.getElementById("usname").value=""
        document.getElementById("pdtid").value=""
        document.getElementById("pdtqty").value=""
    }else if(isNaN(pd_qty)){
        errorMessage.innerText ="Product qty is number value"
        document.getElementById("pdtqty").focus()
        document.getElementById("pdtqty").value=""
    }else if(pd_qty <= 0){
        errorMessage.innerText ="Product qty should be greater than 0"
        document.getElementById("pdtqty").focus()
        document.getElementById("pdtqty").value=""
    }
    else{
        try{
            fetch(url,{
            method:'POST',
            headers: {
                'Content-type': 'application/json',
                'Authorization': `Bearer ${newtoken}`
            },
            body: JSON.stringify({"user_name": u_name, "product_id": parseInt(p_id), "quantity": parseInt(pd_qty)})
            }).then((response) => {
                // console.log(response.text())
                if (response.ok){
                    return response.text()
                    .then((data) => {
                        try{
                            fetch(urlpdt,{
                            method:'GET',
                            headers: {
                                'Content-type': 'application/json',
                                'Authorization': `Bearer ${newtoken}`
                            },
                            }).then((response) => {
                                if (response.ok){
                                    return response.text()
                                    .then((data) => {
                                        const productsData = JSON.parse(data)
                                        const products = productsData["products"]
                                        // console.log(products)
                                            
                                        var content = '';

                                        //clear table body data
                                        const productTableBody = document.querySelector("#productTable > tbody")
                                        while (productTableBody.firstChild){
                                            productTableBody.removeChild(productTableBody.firstChild)
                                        }

                                        //get each row in json
                                        products.forEach((row) => {
                                            // console.log(row)
                                            const pname = row["product_name"]
                                            const pcategory = row["category"]
                                            const pprice = row["unit_price"]
                                            const pqty = row["quantity"]
                                            const pmeasure = row["measure"]
                                            const pid = row["product_id"]
                                            
                                            content +='<tr>';
                                            content += '<td>' + pid + '</td>';
                                            content += '<td>' + pname + '</td>';
                                            content += '<td>' + pcategory + '</td>';
                                            content += '<td>' + pprice + '</td>';
                                            content += '<td>' + pqty + '</td>';
                                            content += '<td>' + pmeasure + '</td>';
                                            content += '<td><input type="radio" name="radio" onclick="return modifyProduct('+pid+', \'' + pname + '\', \'' + pcategory + '\', '+pprice+', '+pqty+', \'' + pmeasure + '\');"/></td>';
                                            content += '</tr>';
                                            })      
                                            //populate table                 
                                            $('#productTable').append(content)
                                    })
                                }else if(response.status == 404){
                                    errorMessage.innerText = response.statusText + "-" + "no products found"
                                    //clear table body data
                                    const productTableBody = document.querySelector("#productTable > tbody")
                                    while (productTableBody.firstChild){
                                        productTableBody.removeChild(productTableBody.firstChild)
                                    }

                                }else if(response.status == 401){
                                    errorMessage.innerText = response.statusText + "-" + "You are unauthorized to perform this action"
                                }else{
                                    errorMessage.innerText = response.status + "-" + response.statusText
                                }                 
                            })
                        }catch(error){
                            console.log(error)
                        }
                        errorMessage.innerText = data
                        document.getElementById("usname").value=""
                        document.getElementById("pdtid").value=""
                        document.getElementById("pdtqty").value=""
                    })
                }else if(response.status == 404){
                    errorMessage.innerText = response.statusText + "-" + "product does not exist"
                }else if(response.status == 401){
                    errorMessage.innerText = response.statusText + "-" + "You are unauthorized to perform this action"
                }else{
                    errorMessage.innerText = response.status + "-" + response.statusText
                }                 
            })
        }catch(error){
            console.log(error)
        }
    }
}
function cancelSale(){
    const agree = confirm("Are you sure you wish to cancel making this sale?");

    if(agree){
        document.getElementById("usname").value=""
        document.getElementById("pdtid").value=""
        document.getElementById("pdtqty").value=""
    }
}
