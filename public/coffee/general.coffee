window.upload = (event) ->
    $.post "localhost:5000/addDocument"
        documents:
            "title": data.filename
            "FPUrl": url
        postUpload()
        "json"
postUpload = () ->
    null