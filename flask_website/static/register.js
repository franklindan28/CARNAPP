function regSubmit() {
  var message;
  var user_username = document.getElementById("Username").value;
  var user_password = document.getElementById("Password").value;
  var error = document.getElementById("error");

  var data = [{ username: user_username, password: user_password }];

  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8080/createdAcc",
    data: JSON.stringify(data),
    contentType: "application/json",
    dataType: "json",
    success: function (result) {
      message = result.message;
      //console.log(message);
      if (message == "Successfully Registered") {
        window.location.href = "http://127.0.0.1:8080/home";
      } else {
        error.innerHTML = message;
      }
    },
  });
}
