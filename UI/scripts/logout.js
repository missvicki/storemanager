function logout(){
    const agree = confirm("Are you sure you wish to logout?");
    const newtoken = localStorage.getItem('token');
    // console.log(newtoken)
    if(agree){
        try{
            fetch('https://store-manager-ap1.herokuapp.com/api/v2/auth/logout',{
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
                    alert(response.statusText + "-" + "token was revoked")
                }else{
                    alert(response.status + "-" + response.statusText)
                }                       
            })
        }catch (error){
            console.log(error)
        }
                    
    }else{
        return false;
    }
}
            