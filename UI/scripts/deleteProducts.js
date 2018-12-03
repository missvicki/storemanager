function deleteProduct(){
        // get field values
        const pdtid = document.getElementById("pdtid").value;
        const pdtnam = document.getElementById("pname").value;
        const pdtcat = document.getElementById("pdtcategory2").value;
        const pdtp = document.getElementById("unitp").value;
        const pdtqt = document.getElementById("q").value;
        const pdtm = document.getElementById("pdtmeasure2").value;

        const errorMessage = document.querySelector("span.errors");
        const newtoken = localStorage.getItem('token');
    
        //validate
        if(pdtid == ""){
            errorMessage.innerText = "Product id required"
            document.getElementById("pdtid").focus()
            document.getElementById("pdtid").value = ""
            document.getElementById("pname").value =""
            document.getElementById("pdtcategory2").value = ""
            document.getElementById("unitp").value = ""
            document.getElementById("q").value = ""
            document.getElementById("pdtmeasure2").value = ""
        }else if(pdtnam == ""){
            errorMessage.innerText = "Product name required"
            document.getElementById("pname").focus()
            document.getElementById("pdtid").value = ""
            document.getElementById("pname").value =""
            document.getElementById("pdtcategory2").value = ""
            document.getElementById("unitp").value = ""
            document.getElementById("q").value = ""
            document.getElementById("pdtmeasure2").value = ""
        }else if(pdtcat == ""){
            errorMessage.innerText ="Product category required"
            document.getElementById("pdtcategory2").focus()
            document.getElementById("pdtcategory2").value = ""
            document.getElementById("pname").value =""
            document.getElementById("pdtid").value = ""
            document.getElementById("unitp").value = ""
            document.getElementById("q").value = ""
            document.getElementById("pdtmeasure2").value = ""
        }else if(pdtp == ""){
            errorMessage.innerText ="Product Unit Price required"
            document.getElementById("unitp").focus()
            document.getElementById("pdtcategory2").value = ""
            document.getElementById("pname").value =""
            document.getElementById("pdtid").value = ""
            document.getElementById("unitp").value = ""
            document.getElementById("q").value = ""
            document.getElementById("pdtmeasure2").value = ""      
        }else if(pdtqt == ""){
            errorMessage.innerText ="Product Quantity required"
            document.getElementById("q").focus()
            document.getElementById("pdtcategory2").value = ""
            document.getElementById("pname").value =""
            document.getElementById("pdtid").value = ""
            document.getElementById("unitp").value = ""
            document.getElementById("q").value = ""
            document.getElementById("pdtmeasure2").value = ""       
        }else if(pdtm == ""){
            errorMessage.innerText ="Product Measure required"
            document.getElementById("pdtmeasure2").focus()
            document.getElementById("pdtcategory2").value = ""
            document.getElementById("pname").value =""
            document.getElementById("pdtid").value = ""
            document.getElementById("unitp").value = ""
            document.getElementById("q").value = ""
            document.getElementById("pdtmeasure2").value = ""     
        }else if(isNaN(pdtp)){
            errorMessage.innerText ="Product Price should be a number value"
            document.getElementById("unitp").focus()
            document.getElementById("unitp").value=""
        }else if(isNaN(pdtqt)){
            errorMessage.innerText ="Product Quantity should be a number value"
            document.getElementById("q").focus()
            document.getElementById("q").value=""
        }else if(!isNaN(pdtcat) || !isNaN(pdtm)){
            errorMessage.innerText ="Product category, measure should be strings"
            document.getElementById("pdtmeasure2").focus()
            document.getElementById("pdtcategory2").value = ""
            document.getElementById("unitp").value = ""
            document.getElementById("q").value = ""
            document.getElementById("pdtmeasure2").value = "" 
        }else if(pdtp <= 0){
            errorMessage.innerText ="Product Price should be greater than 0"
            document.getElementById("unitp").focus()
            document.getElementById("unitp").value=""
        }else if(pdtqt <= 0){
            errorMessage.innerText ="Product Quantity should be greater than 0"
            document.getElementById("q").focus()
            document.getElementById("q").value=""
        }else{
            try{
                fetch('https://store-manager-ap1.herokuapp.com/api/v2/products/'+pdtid,{
                method:'DELETE',
                headers: {
                    'Content-type': 'application/json',
                    'Authorization': `Bearer ${newtoken}`
                }
            }).then((response) => {
                // console.log(response.text())
                if (response.ok){
                    return response.text()
                    .then((data) => {
                        errorMessage.innerText = data
                        document.getElementById("pdtid").value = ""
                        document.getElementById("pname").value = ""
                        document.getElementById("pdtcategory2").value = ""
                        document.getElementById("unitp").value = ""
                        document.getElementById("q").value = ""
                        document.getElementById("pdtmeasure2").value = ""
                        try{
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
                                    errorMessage.innerText =response.statusText + "-" + "no products found"
                                    //clear table body data
                                    const productTableBody = document.querySelector("#productTable > tbody")
                                    while (productTableBody.firstChild){
                                        productTableBody.removeChild(productTableBody.firstChild)
                                    }

                                }else if(response.status == 401){
                                    errorMessage.innerText =response.statusText + "-" + "You are unauthorized to perform this action"
                                }else{
                                    errorMessage.innerText =response.status + "-" + response.statusText
                                }                 
                            })
                        }catch(error){
                            console.log(error)
                        }
                    })
                }else if(response.status == 404){
                    errorMessage.innerText = response.statusText + "-" + "product does not exists"
                    //clear table body data
                    const productTableBody = document.querySelector("#productTable > tbody")
                    while (productTableBody.firstChild){
                        productTableBody.removeChild(productTableBody.firstChild)
                    }

                }else if(response.status == 401){
                    errorMessage.innerText =response.statusText + "-" + "You are unauthorized to perform this action"
                }else{
                    errorMessage.innerText =response.status + "-" + response.statusText
                }                 
            }).catch(console.error)
            }catch (error) {
                console.log(error)
            }
        }
    }
    