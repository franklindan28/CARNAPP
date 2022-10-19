function loginSumit() {
  var message;
  var customer_username = document.getElementById("Username").value;
  var customer_password = document.getElementById("Password").value;
  var error = document.getElementById("error");

  var data = [{ username: customer_username, password: customer_password }];

  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8080/submitlogin",
    data: JSON.stringify(data),
    contentType: "application/json",
    dataType: "json",
    success: function (result) {
      //console.log(jQuery().jquery);
      message = result.message;
      //console.log(message);
      if (message == "Welcome") {
        window.location.href = "http://127.0.0.1:8080/home";
      } else {
        error.innerHTML = message;
      }
    },
  });
}
