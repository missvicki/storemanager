function login(){
    var userName = document.getElementById("usernamefield").value;
    var userPassword = document.getElementById("passwordfield").value;
    var userRole = document.getElementById("role").value;

    if(userName == ""){
        alert("Username is required")
        document.getElementById("usernamefield").focus()
        document.getElementById("usernamefield").value=""
        document.getElementById("passwordfield").value=""
        document.getElementById("role").value=""
    }else if(userPassword == ""){
        alert("Password is required")
        document.getElementById("passwordfield").focus()
        document.getElementById("usernamefield").value=""
        document.getElementById("passwordfield").value=""
        document.getElementById("role").value=""
    }else if(userRole == ""){
        alert("Role is required")
        document.getElementById("role").focus()
        document.getElementById("usernamefield").value=""
        document.getElementById("passwordfield").value=""
        document.getElementById("role").value=""
    }else{
        //fetch url, define method of request and its parameters
        fetch('https://store-manager-ap1.herokuapp.com/api/v2/auth/login',{
            method:'POST',
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify({user_name: userName, password: userPassword, role: userRole})
        }).then((response) => {
            if (response.ok){
                return response.text()
                .then((data) => {
                    console.log(data)
                    var accesstoken = JSON.parse(data)
                    var token = accesstoken["access_token"]

                    localStorage.setItem('token', token)
                    if (userRole == 'admin'){
                        alert("Login Successful...Redirecting to admin page")
                        redirect: window.location.replace("indexOwner.html") 
                    }
                    else if (userRole == 'attendant'){
                        alert("Login Successful...Redirecting to attendants page")
                        redirect: window.location.replace("indexAttendants.html") 
                    }
                    else{
                        alert("I don't know you")
                    }
                })
            }else if(response.status == 400){
                alert(response.statusText + "-" + "either wrong username, password, role")
            }else if(response.status == 404){
                alert(response.statusText + "-" + "user does not exist, please signup")
            }else{
                alert(response.status + "-" + response.statusText)
            }                      
        })
        .catch (console.error)
    }
}
