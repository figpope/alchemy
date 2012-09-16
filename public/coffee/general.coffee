String::splice = (idx, rem, s) ->
  @slice(0, idx) + s + @slice(idx + Math.abs(rem))

String::linkForPositions = (positions) ->
  offset = 0
  out = @
  for p in positions
    console.log p.position + offset
    out = out.splice p.position + offset, 0, '['
    out = out.splice p.position + offset + p.length + 1, 0, ']()'
    offset += 4
  out

postUpload = () ->
  $('#documents').scope().upload()

window.upload = (event) ->
  addDocument = () ->
    $.post "api/addDocument", 
      'files': JSON.stringify(event.files),
      'sessionID': window.sessionID
      postUpload(),
      "json"
  createSession = (data) ->
    window.sessionID = data.sessionID
    addDocument()

  $.post "api/createSession", 
    'gameType': 'document'
    'userID': String(FB.getUserID()),
    (data) ->
      createSession(data)
  null