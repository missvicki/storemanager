function modProduct(){
    // get field values
    const pdtid = document.getElementById("pdtid").value;
    const pdtcat = document.getElementById("pdtcategory2").value;
    const pdtp = document.getElementById("unitp").value;
    const pdtqt = document.getElementById("q").value;
    const pdtm = document.getElementById("pdtmeasure2").value;

    const newtoken = localStorage.getItem('token');

    //validate
    if(pdtcat == ""){
        alert("Product category required")
        document.getElementById("pdtcategory2").focus()
        document.getElementById("pdtcategory2").value = ""
        document.getElementById("unitp").value = ""
        document.getElementById("q").value = ""
        document.getElementById("pdtmeasure2").value = ""
    }else if(pdtp == ""){
        alert("Product Unit Price required")
        document.getElementById("unitp").focus()
        document.getElementById("pdtcategory2").value = ""
        document.getElementById("unitp").value = ""
        document.getElementById("q").value = ""
        document.getElementById("pdtmeasure2").value = ""      
    }else if(pdtqt == ""){
        alert("Product Quantity required")
        document.getElementById("q").focus()
        document.getElementById("pdtcategory2").value = ""
        document.getElementById("unitp").value = ""
        document.getElementById("q").value = ""
        document.getElementById("pdtmeasure2").value = ""       
    }else if(pdtm == ""){
        alert("Product Measure required")
        document.getElementById("pdtmeasure2").focus()
        document.getElementById("pdtcategory2").value = ""
        document.getElementById("unitp").value = ""
        document.getElementById("q").value = ""
        document.getElementById("pdtmeasure2").value = ""     
    }else if(isNaN(pdtp)){
        alert("Product Price should be a number value")
        document.getElementById("unitp").focus()
        document.getElementById("unitp").value=""
    }else if(isNaN(pdtqt)){
        alert("Product Quantity should be a number value")
        document.getElementById("q").focus()
        document.getElementById("q").value=""
    }else if(!isNaN(pdtcat) || !isNaN(pdtm)){
        alert("Product category, measure should be strings")
        document.getElementById("pdtmeasure2").focus()
        document.getElementById("pdtcategory2").value = ""
        document.getElementById("unitp").value = ""
        document.getElementById("q").value = ""
        document.getElementById("pdtmeasure2").value = "" 
    }else if(pdtp <= 0){
        alert("Product Price should be greater than 0")
        document.getElementById("unitp").focus()
        document.getElementById("unitp").value=""
    }else if(pdtqt <= 0){
        alert("Product Quantity should be greater than 0")
        document.getElementById("q").focus()
        document.getElementById("q").value=""
    }else{
        fetch('https://store-manager-ap1.herokuapp.com/api/v2/products/'+pdtid,{
            method:'PUT',
            headers: {
                'Content-type': 'application/json',
                'Authorization': `Bearer ${newtoken}`
            },
            body: JSON.stringify({"category": pdtcat, "unit_price": parseInt(pdtp), "quantity": parseInt(pdtqt), "measure": pdtm})
        }).then((response) => {
            // console.log(response.text())
            if (response.ok){
                return response.text()
                .then((data) => {
                    alert(data)
                    document.getElementById("pdtid").value = ""
                    document.getElementById("pname").value = ""
                    document.getElementById("pdtcategory2").value = ""
                    document.getElementById("unitp").value = ""
                    document.getElementById("q").value = ""
                    document.getElementById("pdtmeasure2").value = ""
                })
            }else if(response.status == 400){
                alert(response.statusText + "-" + "product already exists")
            }else if(response.status == 401){
                alert(response.statusText + "-" + "You are unauthorized to perform this action")
            }else{
                alert(response.status + "-" + response.statusText)
            }                 
        })
        .catch (console.error) 
    }
}
