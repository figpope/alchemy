String::splice = (idx, rem, s) ->
  @slice(0, idx) + s + @slice(idx + Math.abs(rem))

String::linkForPositions = (positions) ->
  offset = 0
  out = @
  for p in positions
    out = out.splice p.location + offset, 0, '['
    out = out.splice p.location + offset + p.length + 1, 0, ']()'
    offset += 4
  out


window.upload = (event) ->
  addDocument = () ->
    $.post "api/addDocument", 
      'files': JSON.stringify(event.files),
      'sessionID': window.sessionID
      postUpload(),
      "json"
  createSession = (data) ->
    $window.sessionID = data
    addDocument()

  $.post "api/createSession", 
    'gameType': 'document'
    'userID': String(FB.getUserID()),
    createSession(data)

postUpload = () ->
  $('#documents').scope().upload()