function logout(){
    const agree = confirm("Are you sure you wish to logout?");
    const newtoken = localStorage.getItem('token');
    const url = 'https://store-manager-ap1.herokuapp.com/api/v2/auth/logout'
    const errorMessage = document.querySelector("span.errors");
    // console.log(newtoken)
    if(agree){
        try{
            fetch(url,{
            method:'DELETE',
            headers: {
                'Content-type': 'application/json',
                'Authorization': `Bearer ${newtoken}`
            }
            }).then((response) => {
                if (response.ok){
                    return response.text()
                        .then((data) => {
                            localStorage.clear()
                            redirect: window.location.replace("index.html") 
                        })
                }else if(response.status == 401){
                    errorMessage.innerText = response.statusText + "-" + "token was revoked"
                }else{
                    errorMessage.innerText = response.status + "-" + response.statusText
                }                       
            })
        }catch (error){
            console.log(error)
        }
                    
    }else{
        return false;
    }
}
            