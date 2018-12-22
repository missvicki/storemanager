function login(){
    const userName = document.getElementById("usernamefield").value;
    const userPassword = document.getElementById("passwordfield").value;
    const userRole = document.getElementById("role").value;
    const errorMessage = document.querySelector("span.errors");
    const url = 'https://store-manager-ap1.herokuapp.com/api/v2/auth/login';

    if(userName == ""){
        errorMessage.innerText ="Username is required"
        document.getElementById("usernamefield").focus()
        document.getElementById("usernamefield").value=""
        document.getElementById("passwordfield").value=""
        document.getElementById("role").value=""
    }else if(userPassword == ""){
        errorMessage.innerText ="Password is required"
        document.getElementById("passwordfield").focus()
        document.getElementById("usernamefield").value=""
        document.getElementById("passwordfield").value=""
        document.getElementById("role").value=""
    }else if(userRole == ""){
        errorMessage.innerText = "Role is required"
        document.getElementById("role").focus()
        document.getElementById("usernamefield").value=""
        document.getElementById("passwordfield").value=""
        document.getElementById("role").value=""
    }else{
        //fetch url, define method of request and its parameters
        try{
            fetch(url,{
            method:'POST',
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify({user_name: userName, password: userPassword, role: userRole})
        }).then((response) => {
            if (response.ok){
                return response.text()
                .then((data) => {
                    // console.log(data)
                    const accesstoken = JSON.parse(data)
                    const token = accesstoken["access_token"]

                    localStorage.setItem('token', token)
                    localStorage.setItem('username', userName)
                    if (userRole == 'admin'){
                        // alert("Login Successful...Redirecting to admin page")
                        errorMessage.innerText = "Login Successful"
                        redirect: window.location.replace("indexOwner.html") 
                    }
                    else if (userRole == 'attendant'){
                        // alert("Login Successful...Redirecting to attendants page")
                        errorMessage.innerText = "Login Successful"
                        redirect: window.location.replace("indexAttendants.html") 
                    }
                    else{
                        errorMessage.innerText ="I don't know you"
                    }
                })
            }else if(response.status == 400){
                errorMessage.innerText = response.statusText + "-" + "either wrong username, password, role"
            }else if(response.status == 404){
                errorMessage.innerText = "User Not Found! Please, Contact Admin"
            }else{
                errorMessage.innerText = response.status + "-" + response.statusText
            }                      
        })
        }catch (error){
            console.log(error)
        }
    }
}
