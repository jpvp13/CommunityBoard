function input_username() {
    var check = document.querySelector('.username-input').value;
    if (check === "") {
        output = "<p>please enter a name</p>";
        // displayOutput();
        throw "AAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
    }
    return check;

}

function input_password() {
    var check = document.querySelector('.pass-input').value;
    if (check === "") {
        output = "<p>please enter a password</p>";
        // displayOutput();
        throw "AAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
    }
    return check;

}


// function login() {
//     xhttp = new XMLHttpRequest();

//     // username = document.getElementById('username').value
//     // password = document.getElementById('password').value

//     localStorage.setItem("username", input_username());
    
//     xhttp.open("/test", "POST", true);
//     body = { "username": input_username(), "password": input_password() };
//     // xhttp.send(body)
//     xhttp.setRequestHeader('Content-Type', 'application/json');
//     // console.log(JSON.stringify(body))
//     // console.log(body)
//     // xhttp.send(body)
//     xhttp.send(JSON.stringify(body))


//     xhttp.onload = function () {
//         try{
//             const myObj = this.responseText;
//             console.log(myObj)
//         } catch (err){
//             const myObj = this.responseText;

//             const display = document.getElementById('errorDisplay');
//             display.innerHTML = myObj;
//         }
//     }

// }


function testJS() {
    var b = document.getElementById('username').value,
        url = 'http://templates\studentView.html?name=' + encodeURIComponent(b);
        
    document.location.href = url;
}