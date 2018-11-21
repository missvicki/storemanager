function allProducts(){
    formwrapped.style.display = "none"

    const newtoken = localStorage.getItem('token');
    // console.log(newtoken)

    fetch('https://store-manager-ap1.herokuapp.com/api/v2/products',{
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
                alert(response.statusText + "-" + "no products found")
            }else if(response.status == 401){
                alert(response.statusText + "-" + "You are unauthorized to perform this action")
            }else{
                alert(response.status + "-" + response.statusText)
            }                 
        })
        .catch (console.error)

}
function displaySingleProduct(){
    // clear table data
    const productTableBody = document.querySelector("#productTable > tbody")
    while (productTableBody.firstChild){
        productTableBody.removeChild(productTableBody.firstChild)
    }

    // display text field
    const productChecked = document.getElementById("radio-two")
    formwrapped.style.display = productChecked.checked ? "block" : "none"
}

function singleproduct(){
    const pdtid = document.getElementById("singleProduct").value

    if (pdtid == ""){
        alert("Please enter the Id for product you want to be displayed")
        document.getElementById("singleProduct").focus()
    }else if(isNaN(pdtid)){
        alert("ID is number value")
        document.getElementById("singleProduct").focus()
        document.getElementById("singleProduct").value=""
    }else{
        const newtoken = localStorage.getItem('token');
        // console.log(newtoken)
        
        fetch('https://store-manager-ap1.herokuapp.com/api/v2/products/'+pdtid,{
                method:'GET',
                headers: {
                    'Content-type': 'application/json',
                    'Authorization': `Bearer ${newtoken}`
                }
            }).then((response) => {
                if (response.ok){
                    return response.text()
                    .then((data) => {
                        // console.log(data)
                        const productData = JSON.parse(data)
                        const products = productData["product"]
                        console.log(products.category)
                            
                        var content = '';

                        //clear table body data
                        const productTableBody = document.querySelector("#productTable > tbody")
                        while (productTableBody.firstChild){
                            productTableBody.removeChild(productTableBody.firstChild)
                        }
                        
                        // get values
                        const pname = products.product_name
                        const pcategory = products.category
                        const pprice = products.unit_price
                        const pqty = products.quantity
                        const pmeasure = products.measure
                        const pid = products.product_id
                            
                        content +='<tr>';
                        content += '<td>' + pid + '</td>';
                        content += '<td>' + pname + '</td>';
                        content += '<td>' + pcategory + '</td>';
                        content += '<td>' + pprice + '</td>';
                        content += '<td>' + pqty + '</td>';
                        content += '<td>' + pmeasure + '</td>';
                        content += '<td><input type="radio" name="radio" onclick="return modifyProduct('+pid+', \'' + pname + '\', \'' + pcategory + '\', '+pprice+', '+pqty+', \'' + pmeasure + '\');"/></td>';
                        content += '</tr>';
                              
                        //populate table                 
                        $('#productTable').append(content)
                    })
                }else if(response.status == 404){
                    alert(response.statusText + "-" + "product with that ID not found")
                     //clear table body data
                     const productTableBody = document.querySelector("#productTable > tbody")
                     while (productTableBody.firstChild){
                         productTableBody.removeChild(productTableBody.firstChild)
                     }
                }else if(response.status == 401){
                    alert(response.statusText + "-" + "You are unauthorized to perform this action")
                     //clear table body data
                     const productTableBody = document.querySelector("#productTable > tbody")
                     while (productTableBody.firstChild){
                         productTableBody.removeChild(productTableBody.firstChild)
                     }
                }else{
                    alert(response.status + "-" + response.statusText)
                     //clear table body data
                     const productTableBody = document.querySelector("#productTable > tbody")
                     while (productTableBody.firstChild){
                         productTableBody.removeChild(productTableBody.firstChild)
                     }
                }                 
            })
            .catch (console.error)
        }
}
// display selected row data into input text
function modifyProduct(id, name, cat, price, qty, meas){
    document.getElementById("pdtid").value = id
    document.getElementById("pname").value = name
    document.getElementById("pdtcategory2").value = cat
    document.getElementById("unitp").value = price
    document.getElementById("q").value = qty
    document.getElementById("pdtmeasure2").value = meas
}

