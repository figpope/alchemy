window.updateFb = (response) ->
  userID = response.authResponse.userID
  $.post '/api/login', {
    'userID': userID
  }