function addProducts(){
    // get field values
    const pdt_name = document.getElementById("pdtname").value;
    const pdt_category = document.getElementById("pdtcategory").value;
    const pdt_qty = document.getElementById("pdtqty").value;
    const pdt_price = document.getElementById("unitprice").value;
    const pdt_measure = document.getElementById("pdtmeasure").value;
    const errorMessage = document.querySelector("span.errors");
    const newtoken = localStorage.getItem('token');
    const url = 'https://store-manager-ap1.herokuapp.com/api/v2/products'

    //validate
    if(pdt_name == ""){
        errorMessage.innerText = "Product name required"
        document.getElementById("pdtname").focus()
        document.getElementById("pdtname").value=""
        document.getElementById("pdtcategory").value=""
        document.getElementById("unitprice").value=""
        document.getElementById("pdtqty").value=""
        document.getElementById("pdtmeasure").value=""
    }else if(pdt_category == ""){
        errorMessage.innerText = "Product category required"
        document.getElementById("pdtcategory").focus()
        document.getElementById("pdtname").value=""
        document.getElementById("pdtcategory").value=""
        document.getElementById("unitprice").value=""
        document.getElementById("pdtqty").value=""
        document.getElementById("pdtmeasure").value=""
    }else if(pdt_price == ""){
        errorMessage.innerText = "Product Unit Price required"
        document.getElementById("unitprice").focus()
        document.getElementById("pdtname").value=""
        document.getElementById("pdtcategory").value=""
        document.getElementById("unitprice").value=""
        document.getElementById("pdtqty").value=""
        document.getElementById("pdtmeasure").value=""        
    }else if(pdt_qty == ""){
        errorMessage.innerText = "Product Quantity required"
        document.getElementById("pdtqty").focus()
        document.getElementById("pdtname").value=""
        document.getElementById("pdtcategory").value=""
        document.getElementById("unitprice").value=""
        document.getElementById("pdtqty").value=""
        document.getElementById("pdtmeasure").value=""        
    }else if(pdt_measure == ""){
        errorMessage.innerText = "Product Measure required"
        document.getElementById("pdtmeasure").focus()
        document.getElementById("pdtname").value=""
        document.getElementById("pdtcategory").value=""
        document.getElementById("unitprice").value=""
        document.getElementById("pdtqty").value=""
        document.getElementById("pdtmeasure").value=""        
    }else if(isNaN(pdt_price)){
        errorMessage.innerText = "Product Price should be a number value"
        document.getElementById("unitprice").focus()
        document.getElementById("unitprice").value=""
    }else if(isNaN(pdt_qty)){
        errorMessage.innerText = "Product Quantity should be a number value"
        document.getElementById("pdtqty").focus()
        document.getElementById("pdtqty").value=""
    }else if(!isNaN(pdt_name) || !isNaN(pdt_category) || !isNaN(pdt_measure)){
        errorMessage.innerText = "Product name, category, measure should be strings"
        document.getElementById("pdtname").focus()
        document.getElementById("pdtname").value=""
        document.getElementById("pdtcategory").value=""
        document.getElementById("unitprice").value=""
        document.getElementById("pdtqty").value=""
        document.getElementById("pdtmeasure").value=""
    }else if(pdt_price <= 0){
        errorMessage.innerText = "Product Price should be greater than 0"
        document.getElementById("unitprice").focus()
        document.getElementById("unitprice").value=""
    }else if(pdt_qty <= 0){
        errorMessage.innerText = "Product Quantity should be greater than 0"
        document.getElementById("pdtqty").focus()
        document.getElementById("pdtqty").value=""
    }else{
        try{
            fetch(url,{
            method:'POST',
            headers: {
                'Content-type': 'application/json',
                'Authorization': `Bearer ${newtoken}`
            },
            body: JSON.stringify({"product_name": pdt_name, "category": pdt_category, "unit_price": parseInt(pdt_price), "quantity": parseInt(pdt_qty), "measure": pdt_measure})
        }).then((response) => {
            // console.log(response.text())
            if (response.ok){
                return response.text()
                .then((data) => {
                    errorMessage.innerText = "Product has been added"
                    document.getElementById("pdtname").value=""
                    document.getElementById("pdtcategory").value=""
                    document.getElementById("unitprice").value=""
                    document.getElementById("pdtqty").value=""
                    document.getElementById("pdtmeasure").value=""
                })
            }else if(response.status == 400){
                errorMessage.innerText = response.statusText + "-" + "product already exists"
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
}
