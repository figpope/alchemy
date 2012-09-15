window.upload = (event) ->
    document = []
    document.append {"title": doc.data.filename, "FPUrl": doc.url} for doc in event.files
    $.post "localhost:5000/addDocument"
        documents: document
        postUpload()
        "json"
postUpload = () ->
    null