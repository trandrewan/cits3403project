function sendMessage() {
  var messageInput = $("#messageInput");
  var message = messageInput.val();
  messageInput.val("");
  
  var requestData = {
    "message": message
  };
  
  $.ajax({
    url: "http://localhost:5000/get_response",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify(requestData),
    dataType: "json",
    success: function(responseData) {
      displayMessage(responseData.response);
    }
  });
}

function displayMessage(message) {
  var chatlog = $("#chatlog");
  var messageElement = $("<div>").text(message);
  chatlog.append(messageElement);
}
