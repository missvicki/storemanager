function signup(){
    const empname = document.getElementById("name_employee").value;
    const empuserName = document.getElementById("name_user").value;
    const empPassword = document.getElementById("password_employee").value;
    const verPassword = document.getElementById("psd_verified").value;
    const empRole = document.getElementById("role").value;
    const errorMessage = document.querySelector("span.errors");

    const newtoken = localStorage.getItem('token');

    const passw=  /^[A-Za-z]\w{6,12}$/;
        
    if(empname == ""){
        errorMessage.innerText = "Employee name required"
        document.getElementById("name_employee").focus()
        document.getElementById("name_employee").value=""
        document.getElementById("name_user").value=""
        document.getElementById("password_employee").value=""
        document.getElementById("psd_verified").value=""
        document.getElementById("role").value=""
    }else if(empuserName == ""){
        errorMessage.innerText = "Employee Username required"
        document.getElementById("name_user").focus()
        document.getElementById("name_employee").value=""
        document.getElementById("name_user").value=""
        document.getElementById("password_employee").value=""
        document.getElementById("psd_verified").value=""
        document.getElementById("role").value=""
    }else if(empPassword == ""){
        errorMessage.innerText = "Employee Password required"
        document.getElementById("password_employee").focus()
        document.getElementById("name_employee").value=""
        document.getElementById("name_user").value=""
        document.getElementById("password_employee").value=""
        document.getElementById("psd_verified").value=""
        document.getElementById("role").value=""
    }else if(verPassword == ""){
        errorMessage.innerText = "Enter password again to verify"
        document.getElementById("psd_verified").focus()
        document.getElementById("name_employee").value=""
        document.getElementById("name_user").value=""
        document.getElementById("password_employee").value=""
        document.getElementById("psd_verified").value=""
        document.getElementById("role").value=""
    }else if(empRole == ""){
        errorMessage.innerText = "Employee Role required"
        document.getElementById("role").focus()
        document.getElementById("name_employee").value=""
        document.getElementById("name_user").value=""
        document.getElementById("password_employee").value=""
        document.getElementById("psd_verified").value=""
        document.getElementById("role").value=""
    }else if(!empPassword.match(passw)){
        errorMessage.innerText = "Password should have at least an upper-case letter, lower-case letter and range from 6-12 characters"
        document.getElementById("password_employee").focus()
        document.getElementById("password_employee").value=""
        document.getElementById("psd_verified").value=""
    }else if(verPassword != empPassword){
        errorMessage.innerText =  "Passwords do not match"
        document.getElementById("password_employee").focus()
        document.getElementById("password_employee").value=""
        document.getElementById("psd_verified").value=""
    }else{
        //fetch url, define method of request and its parameters
        const url = 'https://store-manager-ap1.herokuapp.com/api/v2/auth/signup'
        try{
            fetch(url,{
            method:'POST',
            headers: {
                'Content-type': 'application/json',
                'Authorization': `Bearer ${newtoken}`
            },
            body: JSON.stringify({name: empname, user_name: empuserName, password: empPassword, role: empRole})
        }).then((response) => {
            if (response.ok){
                return response.text()
                .then((data) => {
                    errorMessage.innerText = "Successfuly added a new user"
                    document.getElementById("name_employee").value=""
                    document.getElementById("name_user").value=""
                    document.getElementById("password_employee").value=""
                    document.getElementById("psd_verified").value=""
                    document.getElementById("role").value=""
                })
            }else if(response.status == 400){
                errorMessage.innerText = response.statusText + "-" + "user already exists or bad input data"
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