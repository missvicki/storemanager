function allUsers(){    
    formwrapped.style.display = "none"

    const newtoken = localStorage.getItem('token');
    // console.log(newtoken)
    try{
        fetch('http://127.0.0.1:5000/api/v2/users',{
            method:'GET',
            headers: {
                'Content-type': 'application/json',
                'Authorization': `Bearer ${newtoken}`
            },
        }).then((response) => {
            if (response.ok){
                return response.text()
                .then((data) => {
                    const usersData = JSON.parse(data)
                    const users = usersData["users"]
                    // console.log(users)
                         
                    var content = '';

                    //clear table body data
                    const userTableBody = document.querySelector("#userTable > tbody")
                    while (userTableBody.firstChild){
                        userTableBody.removeChild(userTableBody.firstChild)
                    }

                    //get each row in json
                    users.forEach((row) => {
                        // console.log(row)
                        const uname = row["name"]
                        const usname = row["user_name"]
                        const upassword = row["password"]
                        const urole = row["role"]
                        const uid = row["user_id"]
                        
                        content +='<tr>';
                        content += '<td>' + uid + '</td>';
                        content += '<td>' + uname + '</td>';
                        content += '<td>' + usname + '</td>';
                        content += '<td>' + upassword + '</td>';
                        content += '<td>' + urole + '</td>';
                        content += '</tr>';
                        })      
                        //populate table                 
                        $('#userTable').append(content)
                })
            }else if(response.status == 404){
                alert(response.statusText + "-" + "no users found")
            }else if(response.status == 401){
                alert(response.statusText + "-" + "You are unauthorized to perform this action")
            }else{
                alert(response.status + "-" + response.statusText)
            }                 
        })
    }catch (error){
        console.log(error)
    }
    
}
function displayroleUsers(){
    // clear table data
    const userTableBody = document.querySelector("#userTable > tbody")
    while (userTableBody.firstChild){
        userTableBody.removeChild(userTableBody.firstChild)
    }
    // display text field
    const userChecked = document.getElementById("radio-two")
    formwrapped.style.display = userChecked.checked ? "block" : "none"
}
function usersroles(){
    const roleforuser = document.getElementById("roleUser").value

    if (roleforuser == ""){
        alert("Please enter the role for users you want to be displayed")
        document.getElementById("roleUser").focus()
    }else if(roleforuser == 'admin' || roleforuser == 'attendant'){
        const newtoken = localStorage.getItem('token');
        // console.log(newtoken)
        try{
            fetch('http://127.0.0.1:5000/api/v2/users/'+roleforuser,{
                method:'GET',
                headers: {
                    'Content-type': 'application/json',
                    'Authorization': `Bearer ${newtoken}`
                }
            }).then((response) => {
                if (response.ok){
                    return response.text()
                    .then((data) => {
                        const usersData = JSON.parse(data)
                        const users = usersData["users"]
                        // console.log(users)
                            
                        var content = '';

                        //clear table body data
                        const userTableBody = document.querySelector("#userTable > tbody")
                        while (userTableBody.firstChild){
                            userTableBody.removeChild(userTableBody.firstChild)
                        }

                        //get each row in json
                        users.forEach((row) => {
                            // console.log(row)
                            const uname = row["name"]
                            const usname = row["user_name"]
                            const upassword = row["password"]
                            const urole = row["role"]
                            const uid = row["user_id"]
                            
                            content +='<tr>';
                            content += '<td>' + uid + '</td>';
                            content += '<td>' + uname + '</td>';
                            content += '<td>' + usname + '</td>';
                            content += '<td>' + upassword + '</td>';
                            content += '<td>' + urole + '</td>';
                            content += '</tr>';
                            })      
                            //populate table                 
                            $('#userTable').append(content)
                    })
                }else if(response.status == 404){
                    alert(response.statusText + "-" + "no users found")
                    //clear table body data
                    const userTableBody = document.querySelector("#userTable > tbody")
                    while (userTableBody.firstChild){
                        userTableBody.removeChild(userTableBody.firstChild)
                    }
                }else if(response.status == 401){
                    alert(response.statusText + "-" + "You are unauthorized to perform this action")
                    //clear table body data
                    const userTableBody = document.querySelector("#userTable > tbody")
                    while (userTableBody.firstChild){
                        userTableBody.removeChild(userTableBody.firstChild)
                    }
                }else{
                    alert(response.status + "-" + response.statusText)
                    //clear table body data
                    const userTableBody = document.querySelector("#userTable > tbody")
                    while (userTableBody.firstChild){
                        userTableBody.removeChild(userTableBody.firstChild)
                    }
                }                 
            })
        }catch (error){
            console.log(error)
        }
        }else{
        alert("No such user role records")
        document.getElementById("roleUser").focus()
        document.getElementById("roleUser").value = ""
    }

}
